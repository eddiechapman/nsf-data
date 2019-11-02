import pathlib
import zipfile

import bs4
import requests
from requests.exceptions import RequestException

from nsf import URL, DATA_PATH
from nsf.award import Award


def iter_awards():
    for z in iter_zip():
        logging.info(f'Unzipping {z.filename}')
        for x in iter_xml(z):
            logging.debug(f'Parsing {x}')
            try:
                award = Award(parse_xml(x))
            except Exception e:
                logging.exception(f'Error parsing {x}: {str(e)}')
            else:
                yield award


def iter_zip():
    if not DATA_PATH.exists():
        logging.error(f'Input file not found: {DATA_PATH}')
        raise SystemExit

    zip_files = [f for f in DATA_PATH.glob('*.zip')]

    if not zip_files:
        logging.Error(f'No awards found at path: {DATA_PATH}')
        raise SystemExit

    return (zipfile.ZipFile(f, 'r') for f in zip_files)


def iter_xml(archive):
    return (f for f in archive.filelist)


def parse_xml(archive, filename):
    with archive.read(filename) as f:
        yield bs4.BeautifulSoup(f, 'xml')


def download(year):
    logging.info(f'Requesting award data for year: {year}')

    params = {'DownloadFileName': year, 'All': 'true'}
    file_path = DATA_PATH / f'{year}.zip'

    if file_path.exists():
        logging.warn(f'File already exists: {file_path}. Skipping {year}')
    else:
        try:
            r = requests.post(URL, params)
            r.raise_for_status()
        except RequestException as e:
            logging.exception((f'Encountered error while requesting download. '
                               f'Aborting program. {str(e)}'))
            raise SystemExit

        with file_path.open('wb') as f:
            f.write(r.content)
            logging.info(f'Data for year {year} written to {DATA}')


def to_csv():
    pass
