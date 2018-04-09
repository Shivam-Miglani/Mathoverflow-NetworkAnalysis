# put your common methods here

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

def compute_metric(func_name, result_header, G1, G2, G3, n_nodes, generate_csv=False, draw_plot=False):
    # get (unordered) pagerank metrics for all node in dictionary format
    m_dict1 = func_name(G1)
    m_dict2 = func_name(G2)
    m_dict3 = func_name(G3)

    # now, we order the pagerank descendingly (i.e. high pagerank first)
    ordered_node_m1 = sorted(m_dict1, key=m_dict1.get, reverse=True)
    ordered_node_m2 = sorted(m_dict2, key=m_dict2.get, reverse=True)
    ordered_node_m3 = sorted(m_dict3, key=m_dict3.get, reverse=True)

    # calculate n of top 10%
    n_top10 = int(n_nodes / 10)

    # slice our lists to be consisted of only top 10%
    ordered_node_m1 = ordered_node_m1[:n_top10]
    ordered_node_m2 = ordered_node_m2[:n_top10]
    ordered_node_m3 = ordered_node_m3[:n_top10]

    # calculate how many nodes are in the intersection between all pairs of graph
    m12 = len(calculate_intersection(ordered_node_m1, ordered_node_m2))
    m13 = len(calculate_intersection(ordered_node_m1, ordered_node_m3))
    m23 = len(calculate_intersection(ordered_node_m2, ordered_node_m3))

    # calculate how many clustering coefficients are in the intersection among all graphs
    m_all = len(calculate_intersection3(ordered_node_m1, ordered_node_m2, ordered_node_m3))

    # finally calculate the intersection rate in top 10% node in term of pagerank
    rm1 = float(m12) / float(n_top10)
    rm2 = float(m13) / float(n_top10)
    rm3 = float(m23) / float(n_top10)
    rm_all = float(m_all) / float(n_top10)

    # let's print the result
    print("\n##%s Results\n" % result_header)
    print("N(intersection_of_top10p_a2q_and_c2q)/N(top10p) : %f" % rm1)
    print("N(intersection_of_top10p_a2q_and_c2a)/N(top10p) : %f" % rm2)
    print("N(intersection_of_top10p_c2q_and_c2a)/N(top10p) : %f" % rm3)
    print("N(intersection_of_top10p_all)/N(top10p) : %f" % rm_all)

    # now let's dump the pagerank data of all layers
    # but first, let's clean our data first by adding nodes with zero pagerank
    ml_g1 = [0] * n_nodes
    ml_g2 = [0] * n_nodes
    ml_g3 = [0] * n_nodes

    for i in range(n_nodes):
        val1 = m_dict1.get(i+1)
        val2 = m_dict2.get(i+1)
        val3 = m_dict3.get(i+1)

        if val1 is not None:
            ml_g1[i] = m_dict1.get(i+1)

        if val2 is not None:
            ml_g2[i] = m_dict2.get(i+1)

        if val3 is not None:
            ml_g3[i] = m_dict3.get(i+1)

    # write them to a CSV file
    if generate_csv:
        fname = "pagerank.csv"
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
            writer.writerow(['node_id', 'degree_a2q', 'degree_c2q', 'degree_c2a'])
            for i in range(n_nodes):
                writer.writerow([(i+1), ml_g1[i], ml_g2[i], ml_g3[i]])

    # print the correlation coefficient matrix
    mf = pd.DataFrame({'a2q': ml_g1, 'c2q' : ml_g2, 'c2a' : ml_g3})
    print(mf.corr())

    # draw the scatter matrix
    if draw_plot:
        pd.scatter_matrix(mf, figsize=(6, 6))
        plt.show()

