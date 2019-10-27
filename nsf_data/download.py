"""
Download zipped XML files of NSF data by year.
"""
import argparse
import logging
import pathlib
import requests

# TODO: Prevent redownloading the same data?

def main(args):
    logging.basicConfig(
        level=args.log_level or logging.INFO,
        filename='download.log',
        format='%(levelname)s:%(asctime)s:%(message)s'
    )
    
    dir_path = pathlib.Path(args.outfile)
    url = 'https://www.nsf.gov/awardsearch/download'
    
    for year in args.years:
        logging.info(f'Requesting award data for year: {year}')
        params = {'DownloadFileName': year, 'All': 'true'}
        file_path = dir_path / f'{year}.zip' 
        try:  
            r = requests.post(url, params)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.exception(e)
            raise SystemExit
        with file_path.open('wb') as f:
            f.write(r.content)
            logging.info(f'Data for year {year} written to {file_path}')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-v', '--verbose',
        help='Verbose (debug) logging level.',
        const=logging.DEBUG,
        dest='log_level',
        nargs='?',
    )
    group.add_argument(
        '-q', '--quiet',
        help='Silent mode, only log warnings and errors.',
        const=logging.WARN,
        dest='log_level',
        nargs='?',
    )
    parser.add_argument(
        '-o',
        '--outfile',
        action='store',
        default='./',
        help='Write to a particular file rather than the current directory.',
    )
    parser.add_argument(
        'years',
        action='store',
        nargs='*',
        help='Specify the years of NSF data that should be downloaded.',
    )
    args = parser.parse_args()
    main(args)
