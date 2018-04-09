#!/usr/bin/python3

# let's define some constants first

# the number of nodes in ALL 3 layers
NUMBER_OF_NODES = 24818
# do we want to generate lists (in csv format)?
GENERATE_CSV_FLAG = False
# do we want do draw some plots?
DRAW_PLOT_FLAG = False

import networkx as nx

from methods import * 

##### START HERE #####

# let's build the graph from our dataset, they are on data/ directory
G1, G2, G3 = generate_all_graphs()

# print some information about the graph
print(nx.info(G1))
print(nx.info(G2))
print(nx.info(G3))

# compute degree
compute_metric(get_degree_dictionary, "Degree", G1, G2, G3, NUMBER_OF_NODES,
    generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# compute clustering coefficient
compute_metric(nx.clustering, "Clustering Coefficient", G1, G2, G3,
    NUMBER_OF_NODES, generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# compute pagerank
compute_metric(nx.pagerank, "Pagerank", G1, G2, G3,
    NUMBER_OF_NODES, generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# compute betweenness
compute_metric(nx.betweenness_centrality, "Betweenness", G1, G2, G3,
    NUMBER_OF_NODES, generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# compute eigenvector
compute_metric(nx.eigenvector_centrality, "Eigenvector", G1, G2, G3,
    NUMBER_OF_NODES, generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)
