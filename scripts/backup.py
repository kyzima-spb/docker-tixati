import ftplib
import hashlib
from io import BytesIO
import os
import re
import sys
import tempfile
import typing as t
from urllib.request import urlopen


class FTP_TLS(ftplib.FTP_TLS):
    def exists(self, path: str) -> bool:
        try:
            self.sendcmd('MLST %s' % path)
            return True
        except ftplib.error_perm:
            return False
    
    def read_text(self, path: str) -> str:
        buffer = BytesIO()
        self.retrbinary('RETR %s' % path, buffer.write)
        buffer.seek(0)
        return buffer.read().decode()
    
    def write(self, path: str, fp) -> None:
        fp.seek(0)
        self.storbinary('STOR %s' % path, fp)
    
    def write_text(self, path: str, text: str) -> None:
        self.write(path, BytesIO(text.encode()))



def get_filenames(version: str) -> t.Sequence[str]:
    return tuple(
        ('tixati_%s-1_%s' if name.endswith('.deb') else 'tixati-%s-1.%s') % (version, name)
        for name in (
            'amd64.deb', 'i686.deb',
            'x86_64.rpm', 'i686.rpm',
            'x86_64.manualinstall.tar.gz', 'i686.manualinstall.tar.gz',
            'win64-install.exe', 'win32-install.exe',
        )
    )


def get_latest_release():
    with urlopen('https://www.tixati.com/download', timeout=60) as f:
        match = re.search(r'Version (\d+(?:\.\d+)?) Now Available!', f.read().decode())

        if match is None:
            raise RuntimeError('The website layout has changed.')

        return match[1]


def main() -> int:
    latest_release = get_latest_release()

    try:
        host = os.environ['FTP_HOST']
        user = os.environ['FTP_USER']
        password = os.environ['FTP_PASSWORD']
    except KeyError as err:
        print(f'Secret {err} must be set!', file=sys.stderr)
        return 1
    
    with FTP_TLS(host, user=user, passwd=password, timeout=60) as ftp:
        for name in get_filenames(latest_release):
            url = 'https://download.tixati.com/%s' % name

            with tempfile.TemporaryFile() as tf, urlopen(url, timeout=60) as rf:
                tf.write(rf.read())
                tf.seek(0)

                hashsum = hashlib.file_digest(tf, hashlib.md5).hexdigest()

                if ftp.exists(name):
                    if hashsum == ftp.read_text('%s.hashsum' % name):
                        print('The latest release file %s has not changed.' % name)
                        continue
                    else:
                        print('Backup updated release: %s to path: %s' % (latest_release, name))
                else:
                    print('Backup new release: %s to path: %s' % (latest_release, name))    

                ftp.write(name, tf)
                ftp.write_text('%s.hashsum' % name, hashsum)

    return 0


if __name__ == '__main__':
    sys.exit(main())
