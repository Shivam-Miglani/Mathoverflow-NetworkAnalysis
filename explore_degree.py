#!/usr/bin/python3

# let's define some constants here

# the number of nodes in ALL 4 layers
NUMBER_OF_NODES = 24818
GENERATE_CSV_FLAG = False
DRAW_PLOT_FLAG = False

import csv
from itertools import islice

import networkx as nx
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')

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
    # returns a dict of node and degree
    # with the node_id as the key
    # and degree of the associated node as the value

    deg = G.degree()

    deg_dict = {}
    for n,d in deg:
        deg_dict[int(n)] = d

    return deg_dict

##### START HERE #####

# let's build the graph from our dataset, they are on data/ directory
G1 = generate_graph_from_file("data/sx-mathoverflow-a2q.txt", "a2q graph")
G2 = generate_graph_from_file("data/sx-mathoverflow-c2q.txt", "c2q graph")
G3 = generate_graph_from_file("data/sx-mathoverflow-c2a.txt", "c2a graph")

# print some information about the graph
print(nx.info(G1))
print(nx.info(G2))
print(nx.info(G3))

# get (unordered) degree metrics for all node in dictionary format
deg_dict1 = get_degree_dictionary(G1)
deg_dict2 = get_degree_dictionary(G2)
deg_dict3 = get_degree_dictionary(G3)

# now, we order the degree descendingly (i.e. high degree first)
ordered_node_deg1 = sorted(deg_dict1, key=deg_dict1.get, reverse=True)
ordered_node_deg2 = sorted(deg_dict2, key=deg_dict2.get, reverse=True)
ordered_node_deg3 = sorted(deg_dict3, key=deg_dict3.get, reverse=True)

# calculate n of top 10%
n_top10 = int(NUMBER_OF_NODES / 10)

# slice our lists to be consisted of only top 10%
ordered_node_deg1 = ordered_node_deg1[:n_top10]
ordered_node_deg2 = ordered_node_deg2[:n_top10]
ordered_node_deg3 = ordered_node_deg3[:n_top10]

# calculate how many degree are in the intersection between all pairs of graph
x12 = len(calculate_intersection(ordered_node_deg1, ordered_node_deg2))
x13 = len(calculate_intersection(ordered_node_deg1, ordered_node_deg3))
x23 = len(calculate_intersection(ordered_node_deg2, ordered_node_deg3))

# finally calculate the intersection rate in top 10% node in term of degree
r1 = float(x12) / float(n_top10)
r2 = float(x13) / float(n_top10)
r3 = float(x23) / float(n_top10)

# let's print the result
print("N(intersection_of_top10p_a2q_and_c2q)/N(top10p) : %f" % r1)
print("N(intersection_of_top10p_a2q_and_c2a)/N(top10p) : %f" % r2)
print("N(intersection_of_top10p_c2q_and_c2a)/N(top10p) : %f" % r3)

# now let's dump the degree data of all layers
# but first, let's clean our data first by adding nodes with zero degree
dl_g1 = [0] * NUMBER_OF_NODES
dl_g2 = [0] * NUMBER_OF_NODES
dl_g3 = [0] * NUMBER_OF_NODES

for i in range(NUMBER_OF_NODES):
    val1 = deg_dict1.get(i+1)
    val2 = deg_dict2.get(i+1)
    val3 = deg_dict3.get(i+1)

    if val1 is not None:
        dl_g1[i] = deg_dict1.get(i+1)

    if val2 is not None:
        dl_g2[i] = deg_dict2.get(i+1)

    if val3 is not None:
        dl_g3[i] = deg_dict3.get(i+1)

if GENERATE_CSV_FLAG:
    # write them to a CSV file
    fname = "degree.csv"
    with open(fname, 'w') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
        writer.writerow(['node_id', 'degree_a2q', 'degree_c2q', 'degree_c2a'])
        for i in range(NUMBER_OF_NODES):
            writer.writerow([(i+1), dl_g1[i], dl_g2[i], dl_g3[i]])

# print the correlation coefficient matrix
df = pd.DataFrame({'a2q': dl_g1, 'c2q' : dl_g2, 'c2a' : dl_g3})
print(df.corr())

# draw the scatter matrix
if DRAW_PLOT_FLAG:
    pd.scatter_matrix(df, figsize=(6, 6))
    plt.show()

