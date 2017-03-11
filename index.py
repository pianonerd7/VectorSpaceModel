#!/usr/bin/python
from nltk import sent_tokenize, word_tokenize, PorterStemmer
import string
import os
import getopt
import sys
import re
from node import Node
import json
import pickle
#from nltk.corpus import stopwords 

# Find list of unique tokens in all file path with respect to its document ID
def process_documents(file_path, dictionary_file, postings_file):
    tables = []
    files = []
    for filename in os.listdir(file_path):
        if filename == ".DS_Store":
            continue
        new_file_path = file_path + filename
        tables.append(process_document(new_file_path, int(filename)))
        files.append(int(filename))
    dictionary = merge_tables(tables)
    write_to_disk(dictionary, dictionary_file, postings_file, files)

def process_document(file, doc_ID):
    content = open(file, "r").read()

    terms = []
    with open(file, mode="r") as f:
        for line in f:
            for sent in sent_tokenize(line):
                for word in word_tokenize(sent):
                    #if word not in stopwords.words("english"):
                    #if word.isdigit() == False:
                    terms.append(PorterStemmer().stem(word.lower()))
    
    table = dict()

    for word in terms:
        if word not in table:
            table[word] = doc_ID

    return table

def merge_tables(table_array):
    dictionary = dict()
    for table in table_array:
        for key in table:
            if key not in dictionary:
                dictionary[key] = []
            dictionary[key].append(table[key])
    return sort_dictionary(dictionary)

def sort_dictionary(dictionary):
    new_dictionary = dict()
    for key in dictionary:
        posting = dictionary[key]
        new_dictionary[key] = sorted(posting)
    return new_dictionary

def write_to_disk(dictionary, dictionary_file, postings_file, files):
    dict_to_disk = write_post_to_disk(dictionary, postings_file)
    dict_to_disk["ALL_FILES"] = files
    write_dict_to_disk(dict_to_disk, dictionary_file)

def write_dict_to_disk(dict_to_disk, dictionary_file):
    with open(dictionary_file, mode="wb") as df:
        pickle.dump(dict_to_disk, df)
        
def write_post_to_disk(dictionary, postings_file):
    dict_to_disk = dict()
    with open(postings_file, mode="wb") as pf:
        for key in dictionary:
            dict_to_disk[key] = Node(key, len(dictionary[key]), pf.tell(), pf.write(pickle.dumps(dictionary[key])))
    return dict_to_disk 

def disk_to_memory(dictionary_file):
    training_data = pickle.load(open(file(dictionary_file), 'rb'))

def printDict(dictionary):
    for key in dictionary:
        k = key.term + ", " + str(key.frequency)
        print (k, dictionary[key])

def usage():
    print ("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

directory_of_documents = dictionary_file = postings_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        directory_of_documents = a
    elif o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    else:
        assert False, "unhandled option"
if directory_of_documents == None or dictionary_file == None or postings_file == None:
    usage()
    sys.exit(2)

process_documents(directory_of_documents, dictionary_file, postings_file)
