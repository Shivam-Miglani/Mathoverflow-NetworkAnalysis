#!/usr/bin/python3

# let's define some constants first

# the number of nodes in ALL 3 layers
NUMBER_OF_NODES = 24818
# do we want to generate lists (in csv format)?
GENERATE_CSV_FLAG = True
# do we want do draw some plots?
DRAW_PLOT_FLAG = False
# should we build directed graph?
# note that this may break some metric calculations
DIRECTED_GRAPH_FLAG = True
# should we allow self loops in the graph?
ALLOW_SELFLOOP_FLAG = False
# which time period of data do we want to process? possible values are 1,2,3
TIMEPERIOD = 3
# sampling ratio?
SAMPLE_RATIO = 0

import networkx as nx

from methods import * 

##### START HERE #####

# let's build the graph from our dataset, they are on data/ directory
G1, G2, G3 = generate_all_aggregated_graphs(timeperiod=TIMEPERIOD, sample_ratio=SAMPLE_RATIO, directed=DIRECTED_GRAPH_FLAG,
                                    allow_selfloop=ALLOW_SELFLOOP_FLAG)

# print some information about the graph
print(nx.info(G1))
print(nx.info(G2))
print(nx.info(G3))

# compute number of appearances
compute_metric(generate_all_node_appearances, "N_Appearances", G1, G2, G3, sample_ratio=SAMPLE_RATIO, timeperiod=TIMEPERIOD,
    n_nodes=NUMBER_OF_NODES, directed=DIRECTED_GRAPH_FLAG, allow_selfloop=ALLOW_SELFLOOP_FLAG,
    generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# compute in degree
compute_metric(nx.in_degree_centrality, "In_Degree", G1, G2, G3, sample_ratio=SAMPLE_RATIO, timeperiod=TIMEPERIOD,
    n_nodes=NUMBER_OF_NODES, directed=DIRECTED_GRAPH_FLAG, allow_selfloop=ALLOW_SELFLOOP_FLAG,
    generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# compute degree
compute_metric(nx.out_degree_centrality, "Out_Degree", G1, G2, G3, sample_ratio=SAMPLE_RATIO, timeperiod=TIMEPERIOD,
    n_nodes=NUMBER_OF_NODES, directed=DIRECTED_GRAPH_FLAG, allow_selfloop=ALLOW_SELFLOOP_FLAG,
    generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# compute pagerank
compute_metric(nx.pagerank, "Pagerank", G1, G2, G3, sample_ratio=SAMPLE_RATIO, timeperiod=TIMEPERIOD,
    n_nodes=NUMBER_OF_NODES, directed=DIRECTED_GRAPH_FLAG, allow_selfloop=ALLOW_SELFLOOP_FLAG,
    generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# compute eigenvector
compute_metric(nx.eigenvector_centrality, "Eigenvector", G1, G2, G3, sample_ratio=SAMPLE_RATIO, timeperiod=TIMEPERIOD,
    n_nodes=NUMBER_OF_NODES, directed=DIRECTED_GRAPH_FLAG, allow_selfloop=ALLOW_SELFLOOP_FLAG,
    generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# compute coreness
compute_metric(nx.core_number, "Coreness", G1, G2, G3, sample_ratio=SAMPLE_RATIO, timeperiod=TIMEPERIOD,
    n_nodes=NUMBER_OF_NODES, directed=DIRECTED_GRAPH_FLAG, allow_selfloop=ALLOW_SELFLOOP_FLAG,
    generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# compute closeness
compute_metric(nx.closeness_centrality, "Closeness", G1, G2, G3, sample_ratio=SAMPLE_RATIO, timeperiod=TIMEPERIOD,
    n_nodes=NUMBER_OF_NODES, directed=DIRECTED_GRAPH_FLAG, allow_selfloop=ALLOW_SELFLOOP_FLAG,
    generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)


# # compute degree
# compute_metric(nx.degree_centrality, "Degree", G1, G2, G3, sample_ratio=SAMPLE_RATIO, timeperiod=TIMEPERIOD,
#     n_nodes=NUMBER_OF_NODES, directed=DIRECTED_GRAPH_FLAG, allow_selfloop=ALLOW_SELFLOOP_FLAG,
#     generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# # compute clustering coefficient
# compute_metric(nx.clustering, "Clustering Coefficient", G1, G2, G3, sample_ratio=SAMPLE_RATIO, timeperiod=TIMEPERIOD,
#     n_nodes=NUMBER_OF_NODES, directed=DIRECTED_GRAPH_FLAG, allow_selfloop=ALLOW_SELFLOOP_FLAG,
#     generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

# # compute betweenness
# # note: it takes a very long time to run
# compute_metric(nx.betweenness_centrality, "Betweenness", G1, G2, G3, sample_ratio=SAMPLE_RATIO, timeperiod=TIMEPERIOD,
#     n_nodes=NUMBER_OF_NODES, directed=DIRECTED_GRAPH_FLAG, allow_selfloop=ALLOW_SELFLOOP_FLAG,
#     generate_csv=GENERATE_CSV_FLAG, draw_plot=DRAW_PLOT_FLAG)

