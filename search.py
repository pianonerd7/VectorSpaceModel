import getopt
import sys
import pickle
from queryParser import *
from node import Node
from utility import *
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

def process_queries(dictionary_file, postings_file, query_file_path, output_file_of_results):
    dictionary = read_dictionary_to_memory(dictionary_file)
    infix_arr = query_file_to_infix(query_file_path)

    results = []
    with open(postings_file, 'rb') as postings:
        for infix in infix_arr:
            results.append(process_query(infix, dictionary, postings))
    write_to_output(results, output_file_of_results)

def write_to_output(results, output_file_of_results):
    with open(output_file_of_results, mode="w") as of:
        for result in results:
            of.write(format_result(result) + "\n")

def format_result(result_list):
    result_str = ""
    for item in result_list:
        result_str = result_str + str(item) + " "
    return result_str

def process_query(infix_arr, dictionary, postings):
    result_cache = infix_arr
    final_result = []

    if len(infix_arr) == 1:
        return find_posting_in_disk(dictionary, infix_arr[0], postings)

    while len(result_cache) > 1:
        result_cache, final_result = process_query_rec(result_cache, dictionary, postings)
    return final_result

def process_query_rec(infix_arr, dictionary, postings):
    if len(infix_arr) == 1:
        return find_posting_in_disk(dictionary, infix_arr[0], postings)

    result_cache = infix_arr
    final_result = []

    for i in range(0, len(result_cache)):
        item = result_cache[i]
        if type(item) != list and item in OPERATORS:
            first = second = term = None
            if item == "AND":
                if type(result_cache[i-2]) == str:
                    first = find_posting_in_disk(dictionary, result_cache[i-2], postings)
                else:
                    first = result_cache[i-2]
                if type(result_cache[i-1]) == str:
                    second = find_posting_in_disk(dictionary, result_cache[i-1], postings)
                else:
                    second = result_cache[i-1]
                temp_result = and_operator(first, second)

                new_cache = []
                if i-2 > 0 or i+1 < len(result_cache):
                    wrap_list = [temp_result]
                    new_cache = wrap_list
                    if i-2 > 0:
                        new_cache= result_cache[:i-2] + new_cache
                    if i+1 < len(result_cache):
                        new_cache = new_cache + result_cache[i+1:]
                    result_cache = new_cache
                    break
                else:
                    final_result = temp_result
                    result_cache = []
                    break
                #result_cache = new_cache
            elif item == "OR":
                if type(result_cache[i-2]) == str:
                    first = find_posting_in_disk(dictionary, result_cache[i-2], postings)
                else:
                    first = result_cache[i-2]
                if type(result_cache[i-1]) == str:
                    second = find_posting_in_disk(dictionary, result_cache[i-1], postings)
                else:
                    second = result_cache[i-1]
                temp_result = or_operator(first, second)

                new_cache = []
                if (i-2 > 0) or (i+1 < len(result_cache)):
                    wrap_list = [temp_result]
                    new_cache = wrap_list
                    if i-2 > 0:
                        new_cache=result_cache[:i-2] + new_cache
                    if i+1 < len(result_cache):
                        new_cache = new_cache + result_cache[i+1:]
                    result_cache = new_cache
                    break
                else:
                    final_result = temp_result
                    result_cache=[]
                    break
    return result_cache, final_result

def and_operator(list1, list2):
    skip_interval1 = int(math.sqrt(len(list1)))
    skip_interval2 = int(math.sqrt(len(list2)))

    ptr1 = 0
    ptr2 = 0

    result = []
    while ptr1 < len(list1) and ptr2 < len(list2):
        if list1[ptr1] == list2[ptr2]:
            result.append(list1[ptr1])
            ptr1 += 1
            ptr2 += 1
        elif list1[ptr1] < list2[ptr2]:
            if has_skip_node(skip_interval1, ptr1, len(list1)):
                if list1[ptr1 + skip_interval1] <= list2[ptr2]:
                    ptr1 = ptr1 + skip_interval1
                else:
                    ptr1 += 1
            else:
                ptr1 += 1
        elif list1[ptr1] > list2[ptr2]:
            if has_skip_node(skip_interval2, ptr2, len(list2)):
                if list2[ptr2 + skip_interval2] <= list1[ptr1]:
                    ptr2 = ptr2 + skip_interval2
                else:
                    ptr2 += 1
            else:
                ptr2 += 1
    return result

def or_operator(list1, list2):
    skip_interval1 = int(math.sqrt(len(list1)))
    skip_interval2 = int(math.sqrt(len(list2)))

    ptr1 = 0
    ptr2 = 0

    result = []
    while ptr1 < len(list1) and ptr2 < len(list2):
        if list1[ptr1] == list2[ptr2]:
            if list1[ptr1] not in result:
                result.append(list1[ptr1])
            ptr1 += 1
            ptr2 += 1
        elif list1[ptr1] < list2[ptr2]:
            result.append(list1[ptr1])
            ptr1 += 1
        elif list1[ptr1] > list2[ptr2]:
            result.append(list2[ptr2])
            ptr2 += 1

    if ptr1 < len(list1):
        result = result + list1[ptr1:]
    elif ptr2 < len(list2):
        result = result + list2[ptr2:]
    return result

def has_skip_node(skip_interval, ptr, max):
    return ptr != 0 and ptr%skip_interval == 0 and ptr + skip_interval < max

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
