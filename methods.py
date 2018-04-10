# put your common methods here

import csv
from itertools import islice
import random

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

def split_timeperiods(fname):
    stem = fname.split('.')[0]
    with open(fname) as f,  open('%s-tp1.txt'%stem, 'w') as tp1, \
            open('%s-tp2.txt'%stem, 'w') as tp2, open('%s-tp3.txt'%stem, 'w') as tp3:

        for line in f:
            i, j, t = [int(i) for i in line.strip().split()]

            if t <= 1321883068:
                tp1.write(line)
            elif t <= 1389573148:
                tp2.write(line)
            else:
                tp3.write(line)

def generate_aggregated_graph_from_file(fname, sample_ratio, directed, allow_selfloop, graph_name=None):
    if directed:
        GraphBuilder = nx.DiGraph
    else:
        GraphBuilder = nx.Graph

    if graph_name is not None:
        G = GraphBuilder(name=graph_name)
    else:
        G = GraphBuilder()

    full_lines = []
    with open(fname) as f:
        for line in f:
            full_lines.append(line)

    # sample the data
    if sample_ratio > 0:
        random.seed(1234)
        full_lines = random.sample(full_lines, int(sample_ratio*len(full_lines)))

    for line in full_lines:
        i, j, t = [int(i) for i in line.strip().split()]

        if allow_selfloop:
            G.add_edge(i, j)
        else:
            if i != j:
                G.add_edge(i, j)

    return G

def caculate_node_appearances_from_file(fname, sample_ratio, agg_node_list, delta_t, allow_selfloop):
    time_to_nodes_dict = {}
    result = {}

    for node in agg_node_list:
        result[node] = 0

    # first, we build node list per timeslot dict
    # the key is the timeslot id, value is unique list of nodes
    full_lines = []
    with open(fname) as f:
        for line in f:
            full_lines.append(line)

    # sample the data
    if sample_ratio > 0:
        random.seed(1234)
        full_lines = random.sample(full_lines, int(sample_ratio*len(full_lines)))

    for line in full_lines:
        i, j, t = [int(x) for x in line.strip().split()]
        t = int(t/delta_t)

        if allow_selfloop:
            if time_to_nodes_dict.get(t) is None:
                # we have not yet seen this timeslot
                time_to_nodes_dict[t] = []
                time_to_nodes_dict[t].append(i)
                time_to_nodes_dict[t].append(j)
            else:
                # the timeslot is already there before
                if i not in time_to_nodes_dict[t]:
                    time_to_nodes_dict[t].append(i)
                if j not in time_to_nodes_dict[t]:
                    time_to_nodes_dict[t].append(j)
        else:
            if i != j:
                if time_to_nodes_dict.get(t) is None:
                    # we have not yet seen this timeslot
                    time_to_nodes_dict[t] = []
                    time_to_nodes_dict[t].append(i)
                    time_to_nodes_dict[t].append(j)
                else:
                    # the timeslot is already there before
                    if i not in time_to_nodes_dict[t]:
                        time_to_nodes_dict[t].append(i)
                    if j not in time_to_nodes_dict[t]:
                        time_to_nodes_dict[t].append(j)

    # we then build the resulting dict by counting the number of appearances
    for time, nodes in time_to_nodes_dict.items():
        for node in nodes:
            result[node] += 1

    return result

def generate_all_node_appearances(agg_node_list, sample_ratio, timeperiod, delta_t, allow_selfloop):
    if (timeperiod < 1) or (timeperiod > 3):
        raise ValueError('timeperiod value is outside range')

    n_app1 = caculate_node_appearances_from_file("data/tp%d/sx-mathoverflow-a2q-tp%d.txt"%(timeperiod, timeperiod),
                                                            sample_ratio, agg_node_list, delta_t, allow_selfloop)
    n_app2 = caculate_node_appearances_from_file("data/tp%d/sx-mathoverflow-c2q-tp%d.txt"%(timeperiod, timeperiod),
                                                            sample_ratio, agg_node_list, delta_t, allow_selfloop)
    n_app3 = caculate_node_appearances_from_file("data/tp%d/sx-mathoverflow-c2a-tp%d.txt"%(timeperiod, timeperiod),
                                                            sample_ratio, agg_node_list, delta_t, allow_selfloop)

    return (n_app1, n_app2, n_app3)

def generate_all_aggregated_graphs(timeperiod, sample_ratio, directed, allow_selfloop):
    if (timeperiod < 1) or (timeperiod > 3):
        raise ValueError('timeperiod value is outside range')

    G1 = generate_aggregated_graph_from_file("data/tp%d/sx-mathoverflow-a2q-tp%d.txt"%(timeperiod, timeperiod),
                                                            sample_ratio, directed, allow_selfloop, "a2q graph")
    G2 = generate_aggregated_graph_from_file("data/tp%d/sx-mathoverflow-c2q-tp%d.txt"%(timeperiod, timeperiod),
                                                            sample_ratio, directed, allow_selfloop, "c2q graph")
    G3 = generate_aggregated_graph_from_file("data/tp%d/sx-mathoverflow-c2a-tp%d.txt"%(timeperiod, timeperiod),
                                                            sample_ratio, directed, allow_selfloop, "c2a graph")

    return (G1, G2, G3)

def compute_metric(func_name, result_header, G1, G2, G3, sample_ratio, timeperiod, n_nodes, directed, allow_selfloop, generate_csv=False, draw_plot=False):
    """
        This functions compute the intersection rate and correlation coefficient for a metric.

        Put the metric-calculating-function name to the func_name parameter,
        an identifying human readable string in result_header,
        G1, G2, G3 as three graphs we want to compare based on the metric,
        n_nodes as the maximum number of nodes in the aggregate version,
        directed, allow_selfloop flags to build directed graph and allowing selfloops.

        Optionally we can also make the function to generate CSV files and 
    """

    # initialize the aggregated node list
    agg_node_list = list(set(list(G1) + list(G2) + list(G3)))
    
    # get (unordered) value of the metric for all nodes in dictionary format
    if func_name == generate_all_node_appearances:
        # special case, generate the number of appearance from temporal graph
        m_dict1, m_dict2, m_dict3 = generate_all_node_appearances(agg_node_list, sample_ratio,
                                                timeperiod, 10000, allow_selfloop)
    else:
        m_dict1 = func_name(G1)
        m_dict2 = func_name(G2)
        m_dict3 = func_name(G3)

    # now let's dump the metric values to csv files
    # but first, let's clean our data first by adding nodes with zero value
    # note: the node id is a random number and the range is more than n_nodes

    m_val_dict = {}

    for node in agg_node_list:
        m_val_dict[node] = [0.0, 0.0, 0.0]

    for key, val in m_dict1.items():
        m_val_dict[key][0] = val

    for key, val in m_dict2.items():
        m_val_dict[key][1] = val

    for key, val in m_dict3.items():
        m_val_dict[key][2] = val

    # write them to a CSV file
    if generate_csv:
        stem = '_'.join(result_header.lower().split())
        fname = "metric/%s-tp%d.csv" % (stem, timeperiod)
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
            writer.writerow(['node_id', '%s_tp%d_a2q'%(stem,timeperiod), '%s_tp%d_c2q'%(stem,timeperiod), '%s_tp%d_c2a'%(stem,timeperiod)])
            for key in sorted(m_val_dict):
                writer.writerow([key, m_val_dict[key][0], m_val_dict[key][1], m_val_dict[key][2]])

    # let's print the result
    print("\n##%s Results\n" % result_header)

    # print the correlation coefficient matrix of the given metric
    ml_g1 = [m_val_dict[key][0] for key in sorted(m_val_dict)]
    ml_g2 = [m_val_dict[key][1] for key in sorted(m_val_dict)]
    ml_g3 = [m_val_dict[key][2] for key in sorted(m_val_dict)]

    mf = pd.DataFrame({'a2q': ml_g1, 'c2q' : ml_g2, 'c2a' : ml_g3})
    print(mf.corr())

    # draw the scatter matrix of the given metric
    if draw_plot:
        pd.plotting.scatter_matrix(mf, figsize=(6, 6))
        plt.show()
