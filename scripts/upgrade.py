"""
The script gets the latest version of Tixati and updates the related files.
"""

import json
import pathlib
import os
import re
import typing as t
import sys

from bs4 import BeautifulSoup

import utils


ROOT_DIR = pathlib.Path(__file__).parents[1]


logger = utils.get_logger(__name__)


def parse_latest_version(download_url: str = '') -> t.Optional[str]:
    """
    Returns the latest Tixati version number from the official website.
    """
    if not download_url:
        download_url = 'https://www.tixati.com/download'
    
    r = utils.make_session().get(download_url, allow_redirects=True)
    
    try:
        r.raise_for_status()
    except requests.HTTPError as err:
        logger.error(str(err))
        return None
    
    soup = BeautifulSoup(r.content, 'html.parser')
    found = soup.select('#main div:first-child big > span')
    
    if not found:
        logger.error('Parse error, version element not found.')
        return None
    
    version = found[0].text
    pattern = r'(\d+\.\d+)$'
    match = re.search(pattern, version, re.I)
    
    if match is None:
        logger.error('Tag version invalid value.')
        return None
    
    return match.group(0)


def update_dockerfile(version: str) -> None:
    """Updates the Tixati version in the Dockerfile."""
    with open(ROOT_DIR / 'docker/Dockerfile', 'r+') as f:
        pattern = r'''(?<=TIXATI_VERSION=)("|'|)([\d+\.]+)\1'''
        repl = f'"{version}"'
        content, found = re.subn(pattern, repl, f.read())
        
        if not found:
            raise RuntimeError('Invalid Dockerfile')
        
        f.seek(0)
        f.truncate()
        f.write(content)


class Matrix:
    def __init__(self, filename: pathlib.Path) -> None:
        self.filename = filename
        with open(filename) as f:
            self.matrix = json.load(f)
    
    def _update_latest_flag(self) -> None:
        for i in self.matrix['include']:
            if i['latest']:
                i['version'] = self.latest_version
                return None
        
        self.matrix['include'].append({
            'latest': true,
            'version': self.latest_version,
        })
        
        return None
    
    @property
    def latest_version(self) -> str:
        """Returns the latest version of Tixati used in the build."""
        self.matrix['version'].sort()
        return self.matrix['version'][-1]
    
    def add_version(self, version: str) -> None:
        """Adds a new build version."""
        if version not in self.matrix['version']:
            self.matrix['version'].append(version)
            self._update_latest_flag()
    
    def remove_version(self, version: str) -> None:
        """Removes the given build version."""
        if version in self.matrix['version']:
            self.matrix['version'].remove(version)
            self._update_latest_flag()
    
    def save(self) -> None:
        with open(self.filename, 'w') as f:
            json.dump(self.matrix, f, indent=2)


def main(argv: t.Sequence[str]) -> int:
    if len(argv) < 2:
        logger.info('The default location will be used for the matrix file.')
        matrix_filename = ROOT_DIR / '.github/matrix.json'
    else:
        matrix_filename = argv[1]
    
    outputs = []
    
    latest_version = parse_latest_version()
    logger.info('The latest version of Tixati on the site: %s' % latest_version)
    outputs.append(('latest_version', latest_version))
    
    matrix = Matrix(matrix_filename)
    
    build_version = matrix.latest_version
    logger.info('Latest version of Tixati to build: %s' % build_version)
    outputs.append(('build_version', build_version))

    if latest_version > build_version:
        matrix.add_version(latest_version)
        matrix.save()
        update_dockerfile(latest_version)
        outputs.append(('updated', 'true'))
        logger.info('All files have been successfully edited')
    else:
        outputs.append(('updated', 'false'))
        logger.info('No update required')
    
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            for name, value in outputs:
                print(f'{name}={value}', file=f)
    
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
