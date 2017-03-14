from nltk import PorterStemmer
import string

# Contains some constant variables and term-normalization function.

empty_string = ''

stemmer = PorterStemmer()
punctuations = ["''", '..', '--']

# Normalizes the given term.
def normalize(term):
    term = stemmer.stem(term).casefold()
    if term in string.punctuation or term in punctuations:
        return empty_string
    return term
