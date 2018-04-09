#!/usr/bin/python3

# let's define some constants first

# the number of nodes in ALL 3 layers
NUMBER_OF_NODES = 24818
# do we want to generate lists (in csv format)?
GENERATE_CSV_FLAG = False
# do we want do draw some plots?
DRAW_PLOT_FLAG = False

import csv
from itertools import islice

import networkx as nx
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from methods import * 

matplotlib.style.use('ggplot')

##### START HERE #####

# let's build the graph from our dataset, they are on data/ directory
G1, G2, G3 = generate_all_graphs()

# print some information about the graph
print(nx.info(G1))
print(nx.info(G2))
print(nx.info(G3))

###########################################
## Degree Computations
###########################################

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

# calculate how many nodes are in the intersection between all pairs of graph
d12 = len(calculate_intersection(ordered_node_deg1, ordered_node_deg2))
d13 = len(calculate_intersection(ordered_node_deg1, ordered_node_deg3))
d23 = len(calculate_intersection(ordered_node_deg2, ordered_node_deg3))

# calculate how many clustering coefficients are in the intersection among all graphs
d_all = len(calculate_intersection3(ordered_node_deg1, ordered_node_deg2, ordered_node_deg3))

# finally calculate the intersection rate in top 10% node in term of degree
r1 = float(d12) / float(n_top10)
r2 = float(d13) / float(n_top10)
r3 = float(d23) / float(n_top10)
r_all = float(d_all) / float(n_top10)

# let's print the result
print("\n##Degree Results\n")
print("N(intersection_of_top10p_a2q_and_c2q)/N(top10p) : %f" % r1)
print("N(intersection_of_top10p_a2q_and_c2a)/N(top10p) : %f" % r2)
print("N(intersection_of_top10p_c2q_and_c2a)/N(top10p) : %f" % r3)
print("N(intersection_of_top10p_all)/N(top10p) : %f" % r_all)

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

# write them to a CSV file
if GENERATE_CSV_FLAG:
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

###########################################
## Clustering Coefficient Computations
###########################################

# get (unordered) clustering metrics for all node in dictionary format
clust_dict1 = nx.clustering(G1)
clust_dict2 = nx.clustering(G2)
clust_dict3 = nx.clustering(G3)

# now, we order the clustering coefficients descendingly (i.e. high clustering coeff first)
ordered_node_clust1 = sorted(clust_dict1, key=clust_dict1.get, reverse=True)
ordered_node_clust2 = sorted(clust_dict2, key=clust_dict2.get, reverse=True)
ordered_node_clust3 = sorted(clust_dict3, key=clust_dict3.get, reverse=True)

# calculate n of top 10%
n_top10 = int(NUMBER_OF_NODES / 10)

# slice our lists to be consisted of only top 10%
ordered_node_clust1 = ordered_node_clust1[:n_top10]
ordered_node_clust2 = ordered_node_clust2[:n_top10]
ordered_node_clust3 = ordered_node_clust3[:n_top10]

# calculate how many clustering coefficients are in the intersection between all pairs of graph
c12 = len(calculate_intersection(ordered_node_clust1, ordered_node_clust2))
c13 = len(calculate_intersection(ordered_node_clust1, ordered_node_clust3))
c23 = len(calculate_intersection(ordered_node_clust2, ordered_node_clust3))

# calculate how many clustering coefficients are in the intersection among all graphs
c_all = len(calculate_intersection3(ordered_node_clust1, ordered_node_clust2, ordered_node_clust3))

# finally calculate the intersection rate in top 10% node in term of Clustering Coefficient
r_c1 = float(c12) / float(n_top10)
r_c2 = float(c13) / float(n_top10)
r_c3 = float(c23) / float(n_top10)
r_c_all = float(c_all) / float(n_top10)

# let's print the result
print("\n##Clustering Coefficients Results\n")
print("N(intersection_of_top10p_a2q_and_c2q)/N(top10p) : %f" % r_c1)
print("N(intersection_of_top10p_a2q_and_c2a)/N(top10p) : %f" % r_c2)
print("N(intersection_of_top10p_c2q_and_c2a)/N(top10p) : %f" % r_c3)
print("N(intersection_of_top10p_all)/N(top10p) : %f" % r_c_all)

# now let's dump the Clustering Coefficient data of all layers
# but first, let's clean our data first by adding nodes with zero Clustering Coefficient
cl_g1 = [0] * NUMBER_OF_NODES
cl_g2 = [0] * NUMBER_OF_NODES
cl_g3 = [0] * NUMBER_OF_NODES

for i in range(NUMBER_OF_NODES):
    val1 = clust_dict1.get(i+1)
    val2 = clust_dict2.get(i+1)
    val3 = clust_dict3.get(i+1)

    if val1 is not None:
        cl_g1[i] = clust_dict1.get(i+1)

    if val2 is not None:
        cl_g2[i] = clust_dict2.get(i+1)

    if val3 is not None:
        cl_g3[i] = clust_dict3.get(i+1)

# write them to a CSV file
if GENERATE_CSV_FLAG:
    fname = "clustering.csv"
    with open(fname, 'w') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
        writer.writerow(['node_id', 'clust_a2q', 'clust_c2q', 'clust_c2a'])
        for i in range(NUMBER_OF_NODES):
            writer.writerow([(i+1), cl_g1[i], cl_g2[i], cl_g3[i]])

# print the correlation coefficient matrix
c_df = pd.DataFrame({'a2q': cl_g1, 'c2q' : cl_g2, 'c2a' : cl_g3})
print(c_df.corr())

# draw the scatter matrix
if DRAW_PLOT_FLAG:
    pd.scatter_matrix(c_df, figsize=(6, 6))
    plt.show()
