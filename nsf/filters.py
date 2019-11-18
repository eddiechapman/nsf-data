import collections
import datetime
import re

from nsf import KEYWORD_DATA


def filter_date(award, start, end):
    if start is None:
        start = datetime.date(1950, 1, 1)
    if end is None:
        end = datetime.date.today()

    return award.effective >= start and award.effective <= end


def filter_directorate(award, directorate):
    return award.directorate == directorate


def filter_abstract(award):
    if not award.abstract:
        return False
    try:
        hits = match_keywords(award.abstract)
    except SearchTermsNotFound:
        return False

    return True


def match_keywords(text):
    hits = collections.Counter()
    p = KEYWORD_DATA / 'keywords.txt'
    with p.open('r') as f:
        for search_term in f:
            for match in re.finditer(search_term.strip(), text, re.I):
                hits.update({search_term: 1})

    if not hits:
        raise SearchTermsNotFound

    return hits


def filter_unique(award, awards):
    titles = set(award.title.lower().strip() for award in awards)
    titles = sorted(titles)
    return not award.title.lower().strip() in titles


class SearchTermsNotFound(Exception):
    pass
