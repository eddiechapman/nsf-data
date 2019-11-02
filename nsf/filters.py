import datetime

from nsf.keyword import match_keywords


def filter_date(award, start, end):
    if start is None:
        start = datetime.date(1950, 1, 1)
    if end is None:
        end = datetime.date.today()

    return award.effective >= start and award.effective <= end


def filter_directorate(award, directorate):
    return award.directorate == directorate


def filter_abstract(award, keywords, n=None):
    return bool(match_keywords(award.abstract, keywords, n))
