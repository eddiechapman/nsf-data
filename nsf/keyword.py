import pathlib

from nltk import sent_tokenize, word_tokenize
from nltk.util import ngrams

from nsf import KEYWORD_PATH


def open_keywords():
    keywords = KEYWORD_PATH / 'keywords.txt'
    with open(keywords, 'r') as f:
        return [line.strip().lower() for line in f]


def max_phrase_length(keywords):
    """The number of words in the longest search phrase."""
    return max({len(line.split()) for line in keywords})


def match_keywords(keywords, text, n=None):
    if n is None:
        n = max_phrase_length(keywords)

    phrases = set()

    for sentence in sent_tokenize(text):
        words = word_tokenize(sentence.lower())
        for i in range(n + 1):
            phrases.update([' '.join(g) for g in ngrams(words, i)])

    return phrases.intersection(keywords)
