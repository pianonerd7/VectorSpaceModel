# Node class represent every key in the dictionary. It contains a String 
# representing the token, a number representing the frequency, and a pointer
# to the posting in disk

class Node:
    def __init__(self, term, frequency, pointer, size):
        self.term = term
        self.frequency = frequency
        self.pointer = pointer
        self.length = size

    def get_term(self):
        return self.term
    
    def get_frequency(self):
        return self.frequency

    def get_pointer(self):
        return self.pointer

    def set_pointer(self, pointer):
        self.pointer = pointer

    def set_length(self, length):
        self.length = length
    
    def print_node(self):
        print (self.term, self.frequency, self.pointer, self.length)
