"""
Retrieves NSF records by Directory name and writes them to a CSV file.
"""
import argparse
import collections
import csv
import datetime
import logging
import pathlib

from nsf.award import Award
from nsf.io import iter_awards
from nsf.explore import AwardExplorer
from nsf.filters import filter_date, filter_directorate, filter_abstract
from nsf.keyword import open_keywords, max_phrase_length


def main(args):
    logging.basicConfig(
        level=args.log_level or logging.INFO,
        filename='filter.log',
        format='%(levelname)s:%(asctime)s:%(message)s'
    )

    y, m, d = [int(t) for t in args.start.split('-')]
    start = datetime.date(y, m, d)
    y, m, d = [int(t) for t in args.end.split('-')]
    end = datetime.date(y, m, d)

    out_path = pathlib.Path(args.outfile)

    logging.info(f'Filtering records by {args.directorate}')

    c = collections.Counter()
    keywords = open_keywords()
    n = max_phrase_length(keywords)
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

        logging.debug(f'Filtering directorate: {args.directorate}')
        if filter_directorate(award, args.directorate):
            logging.debug(f'...True: {award.directorate}')
            c.update({'directorate': 1})
        else:
            logging.debug(f'...False: {award.directorate}')
            continue

        logging.debug('Filtering keywords')
        if filter_abstract(award, keywords, n):
            logging.debug('...True')
            c.update({'keyword': 1})
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
    logging.info(f'Retrieved:      {len(awards)}')

    with out_path.open('w') as f:
        logging.info(f'Writing results to file: {args.outfile}')
        writer = csv.DictWriter(f, fieldnames=Award.fieldnames())
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
    parser.add_argument(
        '-s', '--start',
        action='store',
        help='The earliest date to retrieve awards [YYYY-MM-DD]',
        default='1950-01-01'
    )
    parser.add_argument(
        '-e', '--end',
        action='store',
        help='The latest date to retrieve awards [YYYY-MM-DD]',
        default=str(datetime.date.today())
    )
    parser.add_argument(
        '-d', '--directorate',
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
