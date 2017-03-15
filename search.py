import getopt
import pickle
from queryParser import *
from node import Node
import math
from utility import *

def read_dictionary_to_memory(dictionary_file_path):
    dictionary = None
    doc_length_table = None
    with open(dictionary_file_path, mode="rb") as df:
        data = pickle.load(df)
        dictionary = data[0]
        doc_length_table = data[1]
    return (dictionary, doc_length_table)

def find_posting_in_disk(dictionary, term, posting_file_path):
    with open(posting_file_path, mode="rb") as pf:
        if term in dictionary:
            pf.seek(dictionary[term].get_pointer())
            return pickle.loads(pf.read(dictionary[term].length))
        else:
            return []

def process_queries(dictionary_file, postings_file, file_of_queries, output_file_of_results):
    (dictionary, doc_length_table) = read_dictionary_to_memory(dictionary_file)
    queries = parse_query(file_of_queries)
    for query in queries:
        process_query_ltc(dictionary, postings_file, query)

def extract_docID(postings):
    unique_docs = set()
    for posting in postings:
        unique_docs.add([pair[0] for pair in posting])
    return unique_docs

# process_query_ltc takes in a list of words that represents a query, and outputs the
# ltc matrix
def process_query_ltc(dictionary, postings, query):
    ltc_matrix = []
    posting = []
    for word in query:
        posting.append(find_posting_in_disk(dictionary, word, postings))
    print (posting)
    docs = extract_docID(posting)

def get_freq_table_for_query(query):
    query_freq_table = dict()
    for word in query:
        if word not in query_freq_table:
            query_freq_table[word] = 0
        query_freq_table[word] += 1
    return query_freq_table

# since the terms in the query_freq_table would never have a value of
# 0, we can safely assume that math.log(0, 10) would never be an issue for us
def calculate_log_tf(query_freq_table):
    log_tf = dict()
    for word in query_freq_table:
        log_tf[word] = 1 + math.log(query_freq_table[word], 10)
    return log_tf

def calculate_idf_df(dictionary, postings, query):
    idf_df = dict()

    collection_size = dictionary[COLLECTION_SIZE]
    for word in query:
        idf_df[word] = math.log((collection_size/dictionary[word].get_doc_frequency()), 10)

    return idf_df

def calculate_tfidf_query(log_tf, idf_df, query):
    tfidf = dict()

    for word in query:
        tfidf[word] = 0
        if word in log_tf and word in idf_df:
            tfidf[word] = log_tf[word] * idf_df[word]

def calculate_tfidf_document(log_tf, idf_df, query):
    tfidf = dict()

    for word in query:
        cur_word = dict()
        # if word in log_tf and word in idf_df:

'''
Document

log_tf
get postings for every term in the query. list<postings>
get all docs --> list<docs>
            doc1            doc2            doc3            ...
query term  1 + log(tf)     1 + log(tf)     1 + log(tf)
query term  1 + log(tf)     1 + log(tf)     1 + log(tf)
dict<query term, dict<doc, log_tf>>

df
1

tf*idf = log_tf (since it's just tf*idf * 1)

cos_normalization


Query

log_tf
tf table for every word in the query, 1 + log(tf)
dict<term, 1+log(tf)>

idf_df
get the term object from dictionary and get df
            idf
query term  log(n/df)
query term  log(n/df)

dict<query term, idf>

cos_normalization

'''


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

process_queries("dict", "post", "query", "out")