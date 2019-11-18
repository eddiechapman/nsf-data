"""
Retrieves awards based on the following criteria:

    - award effective between 1/1/2011 and 11/3/2019
    - award directorate is CISE
    - award abstract matches text from the keyword list

11/4/19
"""
import argparse
import collections
import csv
import datetime
import logging
import pathlib

from nsf.explore import AwardExplorer
from nsf.filters import (
    filter_date, filter_directorate, filter_abstract, filter_unique
)


def main(args):
    logging.basicConfig(
        level=args.log_level or logging.INFO,
        filename='filter.log',
        format='%(levelname)s:%(asctime)s:%(message)s'
    )

    start = datetime.date(2011, 1, 1)
    end = datetime.date.today()
    directorate = 'Direct For Computer & Info Scie & Enginr'
    out_path = pathlib.Path('results_CISE_2019-11-04.csv')

    logging.info(f'Filtering records by {directorate}')

    c = collections.Counter()
    awards = []
    explorer = AwardExplorer()

    for award in explorer:
        logging.debug(f'Filtering award {award.id}')
        c.update({'awards': 1})

        logging.debug(f'Filtering dates: {start}-{end}')
        if filter_date(award, start, end):
            logging.debug(f'...True: {award.effective}')
            c.update({'date': 1})
        else:
            logging.debug(f'...False: {award.effective}')
            continue

        logging.debug(f'Filtering directorate: {directorate}')
        if filter_directorate(award, directorate):
            logging.debug(f'...True: {award.directorate}')
            c.update({'directorate': 1})
        else:
            logging.debug(f'...False: {award.directorate}')
            continue

        logging.debug('Filtering keywords')
        if filter_abstract(award):
            logging.debug('...True')
            c.update({'keyword': 1})
        else:
            logging.debug('...False')
            continue

        logging.debug('Filtering unique')
        if filter_unique(award, awards):
            logging.debug('...True')
            c.update({'unique': 1})
        else:
            logging.debug('...False')
            continue

        awards.append(award)
        logging.debug(f'Passed all filters: award # {award.id}')

    logging.info('Filtering complete.')
    logging.info(f'Inspected:      {c["awards"]}')
    logging.info(f'By date:        {c["date"]}')
    logging.info(f'By directorate: {c["directorate"]}')
    logging.info(f'By keyword:     {c["keyword"]}')
    logging.info(f'By uniqueness:  {c["unique"]}')
    logging.info(f'Retrieved:      {len(awards)}')

    if awards:
        with out_path.open('w') as f:
            logging.info(f'Writing results to file: {out_path}')
            writer = csv.DictWriter(f, fieldnames=awards[0].flatten().keys())
            writer.writeheader()
            writer.writerows([a.flatten() for a in awards])

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
    args = parser.parse_args()
    main(args)
