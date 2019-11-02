from nsf.keyword import match_keywords


def filter_date(award, start, end):
    return award.effective >= start and award.effective <= end


def filter_directorate(award, directorate):
    return award.directorate == directorate:
    

def filter_abstract(award, keywords):
    return bool(match_keywords(award.abstract, keywords))
