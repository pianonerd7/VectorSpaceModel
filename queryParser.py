
def parse_query(query_file_path):
    query_arr = query_from_file_to_array(query_file_path)
    print (query_arr)

def query_from_file_to_array(query_file_path):
    queries = []
    with open(query_file_path, mode="r") as qf:
        for line in qf:
            query = line
            if line[-1:] == "\n":
                query = line[:-1]
            queries.append(query.split())
    return queries

parse_query("test/query")