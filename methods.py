# put your common methods here
import networkx as nx

def calculate_intersection(lst1, lst2):
    # taken from
    # https://www.geeksforgeeks.org/python-intersection-two-lists/
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]

    return lst3

def calculate_intersection3(lst1, lst2, lst3):
    # taken from
    # https://www.geeksforgeeks.org/python-intersection-two-lists/
    temp = set(lst2)
    lst4 = [value for value in lst1 if value in temp]
    temp = set(lst3)
    lst5 = [value for value in lst4 if value in temp]

    return lst5

def generate_graph_from_file(fname, graph_name=None):
    if graph_name is not None:
        G = nx.Graph(name=graph_name)
    else:
        G = nx.Graph()

    with open(fname) as f:
        for line in f:
            i, j, t = [int(i) for i in line.strip().split()]
            G.add_edge(i, j)

    return G

def generate_all_graphs():
    G1 = generate_graph_from_file("data/sx-mathoverflow-a2q.txt", "a2q graph")
    G2 = generate_graph_from_file("data/sx-mathoverflow-c2q.txt", "c2q graph")
    G3 = generate_graph_from_file("data/sx-mathoverflow-c2a.txt", "c2a graph")

    return (G1, G2, G3)

def get_degree_dictionary(G):
    # returns a dict of node and degree
    # with the node_id as the key
    # and degree of the associated node as the value

    deg = G.degree()

    deg_dict = {}
    for n,d in deg:
        deg_dict[int(n)] = d

    return deg_dict
