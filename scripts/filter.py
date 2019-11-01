"""
Retrieves NSF records by Directory name and writes them to a CSV file.
"""
import argparse
import csv
import logging
import pathlib
import zipfile

import bs4

from nsf.award import Award

DIRECTORATES = [
    'Directorate for Geosciences',
    'National Nanotechnology Coordinating Office',
    'Directorate for Engineering',
    'Directorate for Education & Human Resources',
    'Directorate for Social, Behavioral & Economic Sciences',
    'OFFICE OF THE DIRECTOR',
    'Directorate for Mathematical & Physical Sciences',
    'Directorate for Biological Sciences',
    'Office of Polar Programs',
    'National Coordination Office',
    'Office of Information & Resource Management',
    'Directorate for Computer & Information Science & Engineering',
    'Office of Budget, Finance & Award Management'
]


def main(args):
    logging.basicConfig(
        level=args.log_level or logging.INFO,
        filename='filter.log',
        format='%(levelname)s:%(asctime)s:%(message)s'
    )
    logging.info(f'Filtering records by {args.directorate}')
    
    in_path = pathlib.Path(args.infile)
    out_path = pathlib.Path(args.outfile)

    if not in_path.exists():
        logging.error(f'Input file not found: {args.infile}')
        raise SystemExit
    

    zip_files = [f for f in in_path.glob('*.zip')]
    if not zip_files:
        logging.Error(f'No awards found at path: {args.infile}')
        raise SystemExit

    awards = []

    for z in zip_files:
        logging.debug(f'Unzipping directory {z}.')
        with zipfile.ZipFile(z, 'r') as archive:
            for filename in archive.filelist:
                logging.debug(f'Reading file {filename}')
                xml = archive.read(filename)
                soup = bs4.BeautifulSoup(xml, 'xml')
                logging.debug(f'Filtering {filename}')
                directorate = soup.find('Directorate')
                if not directorate:
                    logging.warn(f'Trouble parsing file: {filename}')
                elif directorate.text.upper() == args.directorate.upper():
                    logging.debug(f'Matching award found: {filename}')
                    award = Award(xml_soup)
                    logging.debug(f'Award info extracted: {filename}')
                    awards.append(award.flatten())

    logging.info(f'Filtering complete. Found {len(awards)} awards.')

    with out_path.open('w') as f:
        logging.info(f'Writing results to file: {args.outfile}')
        writer = csv.DictWriter(f, fieldnames=award.Award.fieldnames())
        writer.writeheader()
        writer.writerows(awards)
    
    logging.info(f'Filtering complete. Results are located: {out_path}')
        

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
        '-i', '--infile',
        action='store',
        default='../nsf/data',
        help='The location of the NSF data files.'
    )
    parser.add_argument(
        '-d', '--directorate',
        choices=DIRECTORATES,
        action='store',
        help='Return the award records in a given directorate.'
    )
    parser.add_argument(
        '-o', '--outfile',
        action='store',
        default='results.csv',
        help='The CSV file where award records will be written.'
    )
    args = parser.parse_args()
    main(args)
