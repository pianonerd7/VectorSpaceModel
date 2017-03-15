import getopt
import pickle
from queryParser import *
from node import Node
import math

def read_dictionary_to_memory(dictionary_file_path):
    dictionary = None
    with open(dictionary_file_path, mode="rb") as df:
        dictionary = pickle.load(df)
    return dictionary

def find_posting_in_disk(dictionary, term, postings):
    if term in dictionary:
        offset = dictionary[term].get_pointer() - postings.tell()
        postings.seek(offset, 1)
        return pickle.loads(postings.read(dictionary[term].length))
    else:
        return []

def process_queries(dictionary_file, postings_file, file_of_queries, output_file_of_results):
    print("")

'''
def usage():
    print ("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

dictionary_file = postings_file = file_of_queries = output_file_of_results = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        output_file_of_results = a
    else:
        assert False, "unhandled option"
if dictionary_file == None or postings_file == None or file_of_queries == None or output_file_of_results == None:
    usage()
    sys.exit(2)

process_queries(dictionary_file, postings_file, file_of_queries, output_file_of_results)
'''

read_dictionary_to_memory("dict")