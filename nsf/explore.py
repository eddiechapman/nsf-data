import logging
import zipfile

import bs4

from nsf import AWARD_DATA, KEYWORD_DATA
from nsf.award import Award


class AwardExplorer:
    def __init__():
        self.zip_files = [f for f in AWARD_DATA.glob('*.zip')]

        if not self.zip_files:
            logging.Error(
                f'No awards found in {AWARD_DATA}. '
                f'Try downloading by year using the download.py script.'
            )

    def iter_zip(self):
        return (zipfile.Zipfile(f, 'r') for f in self.zip_files)

    def iter_xml(self):
        for zip_file in self.iter_zip():
            logging.info(f'Unzipping {zip_file.filename}')
            for f in zip_file.filelist:
                with zip_file.read(f) as xml:
                    yield bs4.BeautifulSoup(xml, 'xml')

    def iter_award(self):
        return (Award(soup) for soup in self.iter_xml())

    def __iter__(self):
        return (award for award in self.iter_award())
