"""
Download zipped XML files of NSF data by year.
"""
import argparse
import logging
import pathlib

from nsf.utils import download


def main(args):
    logging.basicConfig(
        level=args.log_level or logging.INFO,
        filename='download.log',
        format='%(levelname)s:%(asctime)s:%(message)s'
    )

    for year in args.years:
        download(year)


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
        'years',
        action='store',
        nargs='*',
        help='Specify the years of NSF data that should be downloaded.',
    )
    args = parser.parse_args()
    main(args)

