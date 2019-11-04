import logging

import requests

from nsf import AWARD_PATH, URL


def download(year):
    logging.info(f'Requesting award data for year: {year}')

    file_path = AWARD_PATH / f'{year}.zip'

    if file_path.exists():
        logging.warn(f'File already exists: {file_path}. Skipping {year}')
    else:
        params = {'DownloadFileName': year, 'All': 'true'}
        try:
            r = requests.post(URL, params)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.exception((f'Encountered error while requesting download. '
                               f'Aborting program. {str(e)}'))
            raise SystemExit

        with file_path.open('wb') as f:
            f.write(r.content)
            logging.info(f'Data for year {year} downloaded.')
