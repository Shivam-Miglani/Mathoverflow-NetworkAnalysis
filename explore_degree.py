#!/usr/bin/python3

import networkx as nx
from itertools import islice

def calculate_intersection(lst1, lst2):
    # taken from
    # https://www.geeksforgeeks.org/python-intersection-two-lists/
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]

    return lst3

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

def get_degree_dictionary(G):
    deg = G.degree()

    deg_dict = {}
    for n,d in deg:
        deg_dict[int(n)] = d

    return deg_dict

G1 = generate_graph_from_file("data/sx-mathoverflow-a2q.txt", "a2q graph")
G2 = generate_graph_from_file("data/sx-mathoverflow-c2q.txt", "c2q graph")
G3 = generate_graph_from_file("data/sx-mathoverflow-c2a.txt", "c2a graph")

print(nx.info(G1))
print(nx.info(G2))
print(nx.info(G3))

deg_dict1 = get_degree_dictionary(G1)
deg_dict2 = get_degree_dictionary(G2)
deg_dict3 = get_degree_dictionary(G3)

ordered_node_deg1 = sorted(deg_dict1, key=deg_dict1.get, reverse=True)
ordered_node_deg2 = sorted(deg_dict2, key=deg_dict2.get, reverse=True)
ordered_node_deg3 = sorted(deg_dict3, key=deg_dict3.get, reverse=True)

# calculate n of top 10%
n_10p_g1 = int(len(ordered_node_deg1))
n_10p_g2 = int(len(ordered_node_deg2))
n_10p_g3 = int(len(ordered_node_deg3))

x12 = len(calculate_intersection(ordered_node_deg1[:n_10p_g1], ordered_node_deg2[:n_10p_g2]))
x13 = len(calculate_intersection(ordered_node_deg1[:n_10p_g1], ordered_node_deg3[:n_10p_g3]))
x23 = len(calculate_intersection(ordered_node_deg2[:n_10p_g2], ordered_node_deg3[:n_10p_g3]))

r1 = float(x12) / float(len(ordered_node_deg1[:n_10p_g1]))
r2 = float(x12) / float(len(ordered_node_deg2[:n_10p_g2]))

r3 = float(x13) / float(len(ordered_node_deg1[:n_10p_g1]))
r4 = float(x13) / float(len(ordered_node_deg3[:n_10p_g3]))

r5 = float(x23) / float(len(ordered_node_deg2[:n_10p_g2]))
r6 = float(x23) / float(len(ordered_node_deg3[:n_10p_g3]))

# print("%f %f %f %f %f %f" % (r1, r2, r3, r4, r5, r6))
print("N(intersection_of_top10p_a2q_and_c2q)/N(top10p_a2q) : %f" % r1)
print("N(intersection_of_top10p_a2q_and_c2q)/N(top10p_c2q) : %f" % r2)

print("N(intersection_of_top10p_a2q_and_c2a)/N(top10p_a2q) : %f" % r3)
print("N(intersection_of_top10p_a2q_and_c2a)/N(top10p_c2a) : %f" % r4)

print("N(intersection_of_top10p_c2q_and_c2a)/N(top10p_c2q) : %f" % r5)
print("N(intersection_of_top10p_c2q_and_c2a)/N(top10p_c2a) : %f" % r6)

