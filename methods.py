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

def generate_aggregated_graph_from_file(fname, graph_name=None):
    if graph_name is not None:
        G = nx.Graph(name=graph_name)
    else:
        G = nx.Graph()

    with open(fname) as f:
        for line in f:
            i, j, t = [int(i) for i in line.strip().split()]
            G.add_edge(i, j)

    return G

def caculate_node_appearances_from_file(fname, n_nodes):
    nodes_in_timeslot = {}
    result = {}

    # first, we build node list per timeslot dict
    # the key is the timeslot id, value is unique list of nodes
    with open(fname) as f:
        for line in f:
            i, j, t = [int(i) for i in line.strip().split()]

            if nodes_in_timeslot.get(t) is None:
                # we have not yet seen this timeslot
                nodes_in_timeslot[t] = []
                nodes_in_timeslot[t].append(i)
                nodes_in_timeslot[t].append(j)
            else:
                # the timeslot is already there before
                if i not in nodes_in_timeslot[t]:
                    nodes_in_timeslot[t].append(i)
                if j not in nodes_in_timeslot[t]:
                    nodes_in_timeslot[t].append(j)

    # we then build the resulting dict by counting the number of appearances
    for time, node_list in nodes_in_timeslot.items():
        for n in node_list:
            if result.get(n) is None:
                result[n] = 1
            else:
                result[n] += 1

    return result

def generate_all_node_appearances(n_nodes):
    n_app1 = caculate_node_appearances_from_file("data/a2q-t-redacted.txt", n_nodes)
    n_app2 = caculate_node_appearances_from_file("data/c2q-t-redacted.txt", n_nodes)
    n_app3 = caculate_node_appearances_from_file("data/c2a-t-redacted.txt", n_nodes)

    return (n_app1, n_app2, n_app3)

def generate_all_aggregated_graphs():
    G1 = generate_aggregated_graph_from_file("data/sx-mathoverflow-a2q.txt", "a2q graph")
    G2 = generate_aggregated_graph_from_file("data/sx-mathoverflow-c2q.txt", "c2q graph")
    G3 = generate_aggregated_graph_from_file("data/sx-mathoverflow-c2a.txt", "c2a graph")

    return (G1, G2, G3)

def compute_metric(func_name, result_header, G1, G2, G3, n_nodes, generate_csv=False, draw_plot=False):
    """
        This functions compute the intersection rate and correlation coefficient for a metric.

        Put the metric-calculating-function name to the func_name parameter,
        an identifying human readable string in result_header,
        G1, G2, G3 as three graphs we want to compare based on the metric,
        n_nodes as the maximum number of nodes in the aggregate version,

        Optionally we can also make the function to generate CSV files and 
    """
    
    # get (unordered) value of the metric for all nodes in dictionary format
    if func_name == generate_all_node_appearances:
        # special case, generate the number of appearance from temporal graph
        m_dict1, m_dict2, m_dict3 = generate_all_node_appearances(n_nodes)
    else:
        m_dict1 = func_name(G1)
        m_dict2 = func_name(G2)
        m_dict3 = func_name(G3)

    # now, we order the metric value descendingly (i.e. high value first)
    ordered_node_m1 = sorted(m_dict1, key=m_dict1.get, reverse=True)
    ordered_node_m2 = sorted(m_dict2, key=m_dict2.get, reverse=True)
    ordered_node_m3 = sorted(m_dict3, key=m_dict3.get, reverse=True)

    # calculate n of top 10%
    n_top10 = int(n_nodes / 10)

    # get top 10% subset of our ordered node id list
    ordered_node_top10_m1 = ordered_node_m1[:n_top10]
    ordered_node_top10_m2 = ordered_node_m2[:n_top10]
    ordered_node_top10_m3 = ordered_node_m3[:n_top10]

    # calculate how many nodes are in the intersection between all pairs of graph
    m12 = len(calculate_intersection(ordered_node_top10_m1, ordered_node_top10_m2))
    m13 = len(calculate_intersection(ordered_node_top10_m1, ordered_node_top10_m3))
    m23 = len(calculate_intersection(ordered_node_top10_m2, ordered_node_top10_m3))

    # calculate how many nodes are in the intersection among all graphs
    m_all = len(calculate_intersection3(ordered_node_top10_m1, ordered_node_top10_m2, ordered_node_top10_m3))

    # finally calculate the intersection rate in top 10% node in term of the given metric
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

    # now let's dump the metric values data of all layers
    # but first, let's clean our data first by adding nodes with zero value
    # note: the node id is a random number and the range is more than n_nodes

    # initialize the aggregated node list
    agg_node_list = list(set(list(G1.nodes()) + list(G2.nodes()) + list(G3.nodes())))
    m_val_dict = {}

    for node in agg_node_list:
        m_val_dict[node] = [0, 0, 0]

    for key, val in m_dict1.items():
        m_val_dict[key][0] = val

    for key, val in m_dict2.items():
        m_val_dict[key][1] = val

    for key, val in m_dict3.items():
        m_val_dict[key][2] = val

    # write them to a CSV file
    if generate_csv:
        fname = "%s.csv" % '_'.join(result_header.lower().split())
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
            writer.writerow(['node_id', 'val_a2q', 'val_c2q', 'val_c2a'])
            for key in sorted(m_val_dict):
                writer.writerow([key, m_val_dict[key][0], m_val_dict[key][1], m_val_dict[key][2]])

    # print the correlation coefficient matrix of the given metric
    ml_g1 = [m_val_dict[key][0] for key in sorted(m_val_dict)]
    ml_g2 = [m_val_dict[key][1] for key in sorted(m_val_dict)]
    ml_g3 = [m_val_dict[key][2] for key in sorted(m_val_dict)]

    mf = pd.DataFrame({'a2q': ml_g1, 'c2q' : ml_g2, 'c2a' : ml_g3})
    print(mf.corr())

    # draw the scatter matrix of the given metric
    if draw_plot:
        pd.scatter_matrix(mf, figsize=(6, 6))
        plt.show()
