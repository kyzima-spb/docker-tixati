import logging
import logging.handlers
import os
import re
import typing as t

from bs4 import BeautifulSoup
import docker
import docker.errors
import requests
import yaml


LOG_FILE = 'log.txt'
DOWNLOAD_PAGE_URL = 'https://www.tixati.com/download'
WORKFLOW_DIR = os.path.abspath(
    f'{os.path.dirname(__file__)}/../.github/workflows'
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILE,
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding='utf8',
)

formatter = logging.Formatter(
    '[{levelname:^7}] {name}:{lineno} - {asctime}\n{message}',
    datefmt='%Y-%m-%d %H:%M:%S',
    style='{',
)
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


def load_workflow(filename: str) -> t.Any:
    with open(os.path.join(WORKFLOW_DIR, filename)) as f:
        return yaml.safe_load(f)


def parse_last_version(soup: BeautifulSoup) -> t.Optional[str]:
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


def save_workflow(filename: str, data: t.Any) -> None:
    with open(os.path.join(WORKFLOW_DIR, filename), 'w') as f:
        yaml.safe_dump(data, f)


def image_exists(name: str) -> bool:
    try:
        client = docker.from_env()
        client.images.get_registry_data(name)
        return True
    except docker.errors.NotFound:
        return False


if __name__ == '__main__':
    logger.info('Start check')
    
    r = requests.get(DOWNLOAD_PAGE_URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    last_version = parse_last_version(soup)

    if not image_exists('kyzimaspb/tixati:%s' % last_version):
        print(last_version)

    # data = load_workflow('dockerhub-description.yml')
    # data['name'] = 'Update Docker Hub Description'
    # save_workflow('dockerhub-description.yml', data)
