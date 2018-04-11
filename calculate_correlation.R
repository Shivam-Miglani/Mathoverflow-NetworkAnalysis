###### METRICS CORRELATION ###### 

setwd("E:/CODE/MDCN/complex-networks-final-project/metric")

# TIME PERIOD 1
files.tp1 <- list.files(path = getwd(),pattern = "-tp1.csv")
data.tp1 <- lapply(files.tp1, read.csv, sep=",")
d.tp1 <- Reduce(function(x,y) merge(x,y, all=TRUE), data.tp1)
d.tp1$node_id <- as.factor(d.tp1$node_id)
str(d.tp1)

attach(d.tp1)
cor(in_degree_tp1_a2q, out_degree_tp1_a2q)
cor(in_degree_tp1_a2q, n_appearances_tp1_a2q)
cor(in_degree_tp1_a2q, pagerank_tp1_a2q)
cor(in_degree_tp1_a2q, coreness_tp1_a2q)
cor(in_degree_tp1_a2q, eigenvector_tp1_a2q)
cor(in_degree_tp1_a2q, closeness_tp1_a2q)
detach(d.tp1)

# get all pair of columns correlation, overwhelming result
cor(d.tp1[,2:NCOL(d.tp1)], use="complete.obs", method="pearson")

###############
# TIME PERIOD 2
###############
files.tp2 <- list.files(path = getwd(),pattern = "-tp2.csv")
data.tp2 <- lapply(files.tp2, read.csv, sep=",")
d.tp2 <- Reduce(function(x,y) merge(x,y, all=TRUE), data.tp2)
d.tp2$node_id <- as.factor(d.tp2$node_id)
str(d.tp2)

attach(d.tp2)
cor(in_degree_tp2_a2q, out_degree_tp2_a2q)
cor(in_degree_tp2_a2q, n_appearances_tp2_a2q)
cor(in_degree_tp2_a2q, pagerank_tp2_a2q)
cor(in_degree_tp2_a2q, coreness_tp2_a2q)
cor(in_degree_tp2_a2q, eigenvector_tp2_a2q)
cor(in_degree_tp2_a2q, closeness_tp2_a2q)
detach(d.tp2)

# get all pair of columns correlation, overwhelming result
cor(d.tp2[,2:NCOL(d.tp2)], use="complete.obs", method="pearson")

###############
# TIME PERIOD 3
###############
files.tp3 <- list.files(path = getwd(),pattern = "-tp3.csv")
data.tp3 <- lapply(files.tp3, read.csv, sep=",")
d.tp3 <- Reduce(function(x,y) merge(x,y, all=TRUE), data.tp3)
d.tp3$node_id <- as.factor(d.tp3$node_id)
str(d.tp3)

attach(d.tp3)
cor(in_degree_tp3_a2q, out_degree_tp3_a2q)
cor(in_degree_tp3_a2q, n_appearances_tp3_a2q)
cor(in_degree_tp3_a2q, pagerank_tp3_a2q)
cor(in_degree_tp3_a2q, coreness_tp3_a2q)
cor(in_degree_tp3_a2q, eigenvector_tp3_a2q)
cor(in_degree_tp3_a2q, closeness_tp3_a2q)
detach(d.tp3)

# get all pair of columns correlation, overwhelming result
cor(d.tp3[,2:NCOL(d.tp3)], use="complete.obs", method="pearson")
