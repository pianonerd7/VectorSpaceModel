from nltk import PorterStemmer

OPERATORS = { "(" : 3, ")" : 3, "NOT" : 2, "AND" : 1, "OR" : 0 }

def query_file_to_infix(query_file_path):
    query_arr = query_from_file_to_array(query_file_path)

    query_word_arr = []
    for query in query_arr:
        query_word_arr.append(string_to_word_arr(query))

    infix = []
    for query in query_word_arr:
        infix.append(query_to_stack_shunting_yard(query))

    return infix

def query_from_file_to_array(query_file_path):
    queries = []
    with open(query_file_path, mode="r") as qf:
        for line in qf:
            query = line
            if line[-1:] == "\n":
                query = line[:-1]
            queries.append(query)
    return queries

def string_to_word_arr(query):
    word_arr = []

    for word in query.split():
        if word[0] == "(":
            word_arr.append("(")
            if word[1:] not in OPERATORS:
                word_arr.append(PorterStemmer().stem(word[1:]))
            else:
                word_arr.append(word[1:])
        elif word[-1:] == ")":
            if word[:-1] not in OPERATORS:
                word_arr.append(PorterStemmer().stem(word[:-1]))
            else:
                word_arr.append(word[:-1])
            word_arr.append(")")
        else:
            if word not in OPERATORS:
                word_arr.append(PorterStemmer().stem(word))
            else:
                word_arr.append(word)
    return word_arr

def query_to_stack_shunting_yard(query_word_arr):
    word_stack = []
    operator_stack = []

    for item in query_word_arr:
        if item in OPERATORS:
            peek = operator_stack[-1:]
            if len(peek) == 0:
                operator_stack.append(item)
            else:
                if peek[0] == "(":
                    operator_stack.append(item)
                elif item == ")":
                    pop = operator_stack.pop()
                    while pop != "(":
                        word_stack.append(pop)
                        pop = operator_stack.pop()
                elif OPERATORS[peek[0]] < OPERATORS[item]:
                    operator_stack.append(item)
                elif OPERATORS[peek[0]] > OPERATORS[item]:
                    word_stack.append(operator_stack.pop())
                    operator_stack.append(item)
                else:
                    operator_stack.append(item)
        else:
            word_stack.append(item)
    
    while len(operator_stack) != 0:
        word_stack.append(operator_stack.pop())

    return word_stack
