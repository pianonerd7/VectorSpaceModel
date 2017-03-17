This is the README file for A0146123R-A0163945W submission

== Python Version ==

We're using Python Version 3.5.2/3.6.0 for
this assignment.

== General Notes about this assignment ==

Place your comments or requests here for Min to read.  Discuss your
architecture or experiments in general.  A paragraph or two is usually
sufficient.

A lot of the code is recycled from HW2 to prevent reinventing the wheel. 
Indexing is more or less the same, except that the document length is computed
at indexing time to optimize computation time during searching. 

Below is the psuedo code for cosine score calcuation:

cosine_score:
initialize a score_dictionary to store the score of each document
// Calculate score:
for each term t in query frequency table:
    fetch postings list for t
    calculate its weight (tf_idf)
    for each document in the postings:
        calculate its weight (log_tf since df = 1)
        update the score of the document in score_dictionary
        (score_dictionary[document] += weight of t * weight of the document
// Normalization:
for each document that appear in score_dictionary:
    normalized score = score[document] / length_of_document <- get from doc_length_table
    update score
// Rank:
Find the highest 10 scores in the score_dictionary


== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

ESSAY.txt
- answers to the essay question.

index.py 
- reads every file in the reuter folder, indexes, and write to disk.

node.py 
- represents every dictionary object

queryParser.py 
- takes a query file and returns a list of list of words representing a 
list of query

README.txt
- current file. Includes statement of individual work as well as general
notes on the assignment. 

search.py

utility.py
- contain helper methods and constant storing.


== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0146123R-A0163945W, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

We completed all the work and adhere to the policy stated above.


<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

Lecture notes
Introduction to Information Retrieval (Textbook) : reference for essay questions
https://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/ : reference for cosine-similarity
http://www.ics.uci.edu/~djp3/classes/2008_09_26_CS221/Lectures/Lecture26.pdf : reference for cosine-similarity
http://people.eng.unimelb.edu.au/tcohn/comp90042/l3.pdf: phrasal query
