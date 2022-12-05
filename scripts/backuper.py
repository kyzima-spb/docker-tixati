import ftplib
import logging
import os
import sys
import time
import typing as t

from dotenv import load_dotenv
import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_handler = logging.StreamHandler()

formatter = logging.Formatter(
    '[{levelname:^7}] {lineno} - {asctime}\n{message}',
    # '::{levelname} file={pathname},line={lineno},title={asctime}::{message}',
    datefmt='%Y-%m-%d %H:%M:%S',
    style='{',
)
logger_handler.setFormatter(formatter)
logger.addHandler(logger_handler)


def backup_version(host: str, user: str, password: str, version: str):
    logger.info('Backup started.')

    download_urls = [i.format(version) for i in (
        'https://download3.tixati.com/download/tixati_{}-1_amd64.deb',
        'https://download3.tixati.com/download/tixati-{}-1.x86_64.rpm',
        'https://download3.tixati.com/download/tixati-{}-1.x86_64.manualinstall.tar.gz',
        'https://download2.tixati.com/download/tixati_{}-1_i686.deb',
        'https://download2.tixati.com/download/tixati-{}-1.i686.rpm',
        'https://download2.tixati.com/download/tixati-{}-1.i686.manualinstall.tar.gz',
        'https://download1.tixati.com/download/tixati-{}-1.win64-install.exe',
        'https://download1.tixati.com/download/tixati-{}-1.win32-install.exe',
    )]

    with ftplib.FTP_TLS(host, user=user, passwd=password, timeout=60) as ftp:
        ftp.cwd('domains/supernatural.myjino.ru')

        if not ftp_file_exists(ftp, 'tixati'):
            ftp.mkd('tixati')

        ftp.cwd('tixati')

        for url in download_urls:
            filename = os.path.basename(url)

            if not ftp_file_exists(ftp, filename):
                if not requests.head(url, allow_redirects=True).ok:
                    logger.warning(f'File {filename!r} not found.')
                else:
                    resp = requests.get(url, stream=True, allow_redirects=True)
                    ftp.storbinary('STOR %s' % filename, resp.raw, 4096)
                    logger.info('Backup %s' % filename)
                    time.sleep(1)

    logger.info('Backup finished.')


def ftp_file_exists(ftp: ftplib.FTP_TLS, path: str) -> bool:
    try:
        ftp.sendcmd('MLST %s' % path)
        return True
    except ftplib.error_perm:
        return False


def main(argv: t.Sequence[str]) -> int:
    if len(argv) < 1:
        logger.error('Version not found.')
        return 1

    try:
        host = os.environ['FTP_HOST']
        user = os.environ['FTP_USER']
        password = os.environ['FTP_PASSWORD']
    except KeyError as err:
        logger.error(f'Secret {err} must be set!')
        return 1

    backup_version(host, user, password, version=argv[0])

    return 0


if __name__ == '__main__':
    load_dotenv()
    sys.exit(main(sys.argv[1:]))
