class DictionaryNode:
    def __init__(self, term, doc_frequency):
        self.term = term
        self.doc_frequency = doc_frequency
    
    def __str__(self):
        return self.term + str(self.doc_frequency)

    def __hash__(self):
        return hash(str(self.term))

    def __eq__ (self, other):
        return self.term == other.term and self.doc_frequency == other.doc_frequency
