# https://www.fosshub.com/Tixati-old.html

import hashlib
import itertools
import json
import time
import sys

import requests


FILENAME_PATTERNS = (
    'tixati_{}-1_amd64.deb',
    'tixati-{}-1.x86_64.rpm',
    'tixati-{}-1.x86_64.manualinstall.tar.gz',
    'tixati_{}-1_i686.deb',
    'tixati-{}-1.i686.rpm',
    'tixati-{}-1.i686.manualinstall.tar.gz',
    'tixati-{}-1.win64-install.exe',
    'tixati-{}-1.win32-install.exe',
)


def download(session, url, path, chunk_size=1024):
    """Downloads a file from the specified address."""
    resp = session.get(url, stream=True, allow_redirects=True)

    with open(path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size):
            f.write(chunk)

    return path


def get_download_url(session, filename, release_id):
    resp = session.post(
        'https://api.fosshub.com/download/',
        data={
            'projectId': '5cdd70bc4525770a47e45ed5',
            'releaseId': release_id,
            'projectUri': 'https://fosshub.com/Tixati-old.html',
            'fileName': filename,
            'source': 'CF',
        }
    )
    result = resp.json()
    return result['data']['url']


def make_session():
    sees = requests.Session()
    sees.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    })
    return sees


def md5file(filename: str) -> str:
    obj = hashlib.md5()

    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 8), b''):
            obj.update(chunk)

    return obj.hexdigest()


def main(argv):
    if len(argv) < 2:
        print(f'Usage: python {argv[0]} FILE', file=sys.stderr)
        return 1

    with open(argv[1]) as f:
        pool = {i.pop('n'): i for i in json.load(f)}

    files = itertools.chain((
        p.format(f'2.{i}')
        for i in range(60, 76)
        for p in FILENAME_PATTERNS
    ))
    session = make_session()

    for filename in files:
        info = pool.get(filename)

        if info is not None:
            dest = f'./distr/{filename}'
            release_id = info['r']
            if info['hash']['md5'] != md5file(dest):
                url = get_download_url(session, filename, release_id)
                print(f'{filename} -> {url}')
                time.sleep(1)
                download(session, url, dest)
                time.sleep(5)
            else:
                print(f'{filename} already downloaded.')

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
