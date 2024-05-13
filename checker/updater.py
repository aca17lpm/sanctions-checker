import requests
import time
import datetime
import json
import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('scheduler')

from packages.sanctions.adapter import get_custom_un_session
from packages.sanctions.constants import (
    SANCTIONS_FOLDER, UK_LIST, EU_LIST, AU_LIST, UN_LIST, TIMESTAMP,
    UK_ADDRESS, EU_ADDRESS, AU_ADDRESS, UN_ADDRESS, USA_ADDRESSES, USA_FILENAMES,
    USA_FOLDER
)


normal_session = requests.Session()

def download_file(url, filename, session=normal_session) -> bool:
    """Download a file from an URL

    Parameters
    ----------
    url : str
        The URL to download
    filename : str
        The name of the file to save
    
    Returns
    -------
    bool
        Whether the download was successful
    """
    response = session.get(url)
    if response.status_code == 200:
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'wb') as f:
            f.write(response.content)
        logger.info(f"Download successful for {filename}")
        return True
    else:
        logger.info(f"Failed to download at {url}. Status code: {response.status_code}")
        return False

def update_usa():
    """Only return true if all of the downloads are correct
    """

    folder = SANCTIONS_FOLDER + USA_FOLDER
    successes = []
    for index, address in enumerate(USA_ADDRESSES):
        successes.append(download_file(address, folder + '/' + USA_FILENAMES[index]))

    return all(successes)

def update_uk():
    filename = SANCTIONS_FOLDER + UK_LIST
    return download_file(UK_ADDRESS, filename)

def update_eu():
    filename = SANCTIONS_FOLDER + EU_LIST
    return download_file(EU_ADDRESS, filename)

def update_au():
    filename = SANCTIONS_FOLDER + AU_LIST
    return download_file(AU_ADDRESS, filename)

def update_un():
    filename = SANCTIONS_FOLDER + UN_LIST
    return download_file(UN_ADDRESS, filename, session=get_custom_un_session())

def write_download_timestamps(download_timestamps):
    """Write back to timestamp.json"""
    with open(SANCTIONS_FOLDER + TIMESTAMP, 'w') as f:
        json.dump(download_timestamps, f)

def read_download_timestamps():
    """Read timestamp.json as python datetimes"""
    try:
        with open(SANCTIONS_FOLDER + TIMESTAMP, 'r') as f:
            timestamps = json.load(f)
            return {key: datetime.datetime.fromtimestamp(int(value)) for key, value in timestamps.items()}
    except FileNotFoundError:
        return {}

def update_all():
    """Updates all of the sanctions lists and records when they were updated
    in timestamp.json
    """

    logger.info("Updating all CSV Sanctions...")

    download_timestamps = read_download_timestamps()

    def timestamp():
        return str(int(time.time()))

    if update_usa():
        download_timestamps['us'] = timestamp()

    if update_uk():
        download_timestamps['uk'] = timestamp()

    if update_eu():
        download_timestamps['eu'] = timestamp()

    if update_au():
        download_timestamps['au'] = timestamp()

    if update_un():
        download_timestamps['un'] = timestamp()

    print(download_timestamps)

    write_download_timestamps(download_timestamps)
    logger.info(f"CSV Sanctions updated... {download_timestamps}")

if __name__ == '__main__':
    update_all()