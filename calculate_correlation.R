###### METRICS CORRELATION ###### 

setwd("<path_to>/complex-networks-final-project/metric/")

# TIME PERIOD 1
d.tp1.coreness = read.csv("coreness-tp1.csv", header=T)
d.tp1.eigenvector = read.csv("eigenvector-tp1.csv", header=T)
d.tp1.in_degree = read.csv("in_degree-tp1.csv", header=T)
d.tp1.n_appearances = read.csv("n_appearances-tp1.csv", header=T)
d.tp1.out_degree = read.csv("out_degree-tp1.csv", header=T)
d.tp1.pagerank = read.csv("pagerank-tp1.csv", header=T)

d.tp1 = merge(d.tp1.coreness, d.tp1.eigenvector)
d.tp1 = merge(d.tp1, d.tp1.in_degree)
d.tp1 = merge(d.tp1, d.tp1.n_appearances)
d.tp1 = merge(d.tp1, d.tp1.out_degree)
d.tp1 = merge(d.tp1, d.tp1.pagerank)

d.tp1$node_id <- as.factor(d.tp1$node_id)

str(d.tp1)

attach(d.tp1)
cor(in_degree_tp1_a2q, out_degree_tp1_a2q)
cor(in_degree_tp1_a2q, n_appearances_tp1_a2q)
cor(in_degree_tp1_a2q, pagerank_tp1_a2q)
cor(in_degree_tp1_a2q, coreness_tp1_a2q)
cor(in_degree_tp1_a2q, eigenvector_tp1_a2q)
detach(d.tp1)

# get all pair of columns correlation, overwhelming result
cor(d.tp1[,2:19], use="complete.obs", method="pearson")

# TIME PERIOD 2
d.tp2.coreness = read.csv("coreness-tp2.csv", header=T)
d.tp2.eigenvector = read.csv("eigenvector-tp2.csv", header=T)
d.tp2.in_degree = read.csv("in_degree-tp2.csv", header=T)
d.tp2.n_appearances = read.csv("n_appearances-tp2.csv", header=T)
d.tp2.out_degree = read.csv("out_degree-tp2.csv", header=T)
d.tp2.pagerank = read.csv("pagerank-tp2.csv", header=T)

d.tp2 = merge(d.tp2.coreness, d.tp2.eigenvector)
d.tp2 = merge(d.tp2, d.tp2.in_degree)
d.tp2 = merge(d.tp2, d.tp2.n_appearances)
d.tp2 = merge(d.tp2, d.tp2.out_degree)
d.tp2 = merge(d.tp2, d.tp2.pagerank)

d.tp2$node_id <- as.factor(d.tp2$node_id)

str(d.tp2)

attach(d.tp2)
cor(in_degree_tp2_a2q, out_degree_tp2_a2q)
cor(in_degree_tp2_a2q, n_appearances_tp2_a2q)
cor(in_degree_tp2_a2q, pagerank_tp2_a2q)
cor(in_degree_tp2_a2q, coreness_tp2_a2q)
cor(in_degree_tp2_a2q, eigenvector_tp2_a2q)
detach(d.tp2)

# get all pair of columns correlation, overwhelming result
cor(d.tp2[,2:19], use="complete.obs", method="pearson")

# TIME PERIOD 3
d.tp3.coreness = read.csv("coreness-tp3.csv", header=T)
d.tp3.eigenvector = read.csv("eigenvector-tp3.csv", header=T)
d.tp3.in_degree = read.csv("in_degree-tp3.csv", header=T)
d.tp3.n_appearances = read.csv("n_appearances-tp3.csv", header=T)
d.tp3.out_degree = read.csv("out_degree-tp3.csv", header=T)
d.tp3.pagerank = read.csv("pagerank-tp3.csv", header=T)

d.tp3 = merge(d.tp3.coreness, d.tp3.eigenvector)
d.tp3 = merge(d.tp3, d.tp3.in_degree)
d.tp3 = merge(d.tp3, d.tp3.n_appearances)
d.tp3 = merge(d.tp3, d.tp3.out_degree)
d.tp3 = merge(d.tp3, d.tp3.pagerank)

d.tp3$node_id <- as.factor(d.tp3$node_id)

str(d.tp3)

attach(d.tp3)
cor(in_degree_tp3_a2q, out_degree_tp3_a2q)
cor(in_degree_tp3_a2q, n_appearances_tp3_a2q)
cor(in_degree_tp3_a2q, pagerank_tp3_a2q)
cor(in_degree_tp3_a2q, coreness_tp3_a2q)
cor(in_degree_tp3_a2q, eigenvector_tp3_a2q)
detach(d.tp3)

# get all pair of columns correlation, overwhelming result
cor(d.tp3[,2:19], use="complete.obs", method="pearson")
