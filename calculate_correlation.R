library(ggplot2)
library(corrplot)
library(plyr)

###### METRICS CORRELATION ###### 

setwd("/<path_to>/complex-networks-final-project/metric")

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
C <- cor(d.tp1[,2:NCOL(d.tp1)], use="complete.obs", method="pearson")

### Correlation plot between metrics within layer ###
# create correlation plot between metrics in a2q (G1)
d.tp1.a2q <- subset(d.tp1, select = c("node_id","in_degree_tp1_a2q","out_degree_tp1_a2q",
                                      "n_appearances_tp1_c2a","pagerank_tp1_c2a",
                                      "coreness_tp1_c2a","closeness_tp1_c2a"))
d.tp1.a2q <- rename(d.tp1.a2q, c("in_degree_tp1_a2q"="in_degree", "out_degree_tp1_a2q"="out_degree",
                                 "n_appearances_tp1_c2a"="n_appearances", "pagerank_tp1_c2a"="pagerank",
                                 "coreness_tp1_c2a"="coreness","closeness_tp1_c2a"="closeness"))
C <- cor(d.tp1.a2q[,2:NCOL(d.tp1.a2q)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# create correlation plot between metrics in c2q (G2)
d.tp1.c2q <- subset(d.tp1, select = c("node_id","in_degree_tp1_c2q","out_degree_tp1_c2q",
                                      "n_appearances_tp1_c2a","pagerank_tp1_c2a",
                                      "coreness_tp1_c2a","closeness_tp1_c2a"))
d.tp1.c2q <- rename(d.tp1.c2q, c("in_degree_tp1_c2q"="in_degree", "out_degree_tp1_c2q"="out_degree",
                                 "n_appearances_tp1_c2a"="n_appearances", "pagerank_tp1_c2a"="pagerank",
                                 "coreness_tp1_c2a"="coreness","closeness_tp1_c2a"="closeness"))
C <- cor(d.tp1.c2q[,2:NCOL(d.tp1.c2q)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# create correlation plot between metrics in c2a (G3)
d.tp1.c2a <- subset(d.tp1, select = c("node_id","in_degree_tp1_c2a","out_degree_tp1_c2a",
                                      "n_appearances_tp1_c2a","pagerank_tp1_c2a",
                                      "coreness_tp1_c2a","closeness_tp1_c2a"))
d.tp1.c2a <- rename(d.tp1.c2a, c("in_degree_tp1_c2a"="in_degree", "out_degree_tp1_c2a"="out_degree",
                                 "n_appearances_tp1_c2a"="n_appearances", "pagerank_tp1_c2a"="pagerank",
                                 "coreness_tp1_c2a"="coreness","closeness_tp1_c2a"="closeness"))
C <- cor(d.tp1.c2a[,2:NCOL(d.tp1.c2a)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

### Correlation plot between layers ###
# create correlation plot between layers
# in-degree metric
d.tp1.in_degree <- subset(d.tp1, select = c("node_id","in_degree_tp1_a2q",
                                            "in_degree_tp1_c2q","in_degree_tp1_c2a"))
d.tp1.in_degree <- rename(d.tp1.in_degree, c("in_degree_tp1_a2q"="in_degree_G1",
                                             "in_degree_tp1_c2q"="in_degree_G2",
                                             "in_degree_tp1_c2a"="in_degree_G3"))
C <- cor(d.tp1.in_degree[,2:NCOL(d.tp1.in_degree)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# out-degree metric
d.tp1.out_degree <- subset(d.tp1, select = c("node_id","out_degree_tp1_a2q",
                                             "out_degree_tp1_c2q","out_degree_tp1_c2a"))
d.tp1.out_degree <- rename(d.tp1.out_degree, c("out_degree_tp1_a2q"="out_degree_G1",
                                               "out_degree_tp1_c2q"="out_degree_G2",
                                               "out_degree_tp1_c2a"="out_degree_G3"))
C <- cor(d.tp1.out_degree[,2:NCOL(d.tp1.out_degree)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# closeness metric
d.tp1.closeness <- subset(d.tp1, select = c("node_id","closeness_tp1_a2q",
                                            "closeness_tp1_c2q","closeness_tp1_c2a"))
d.tp1.closeness <- rename(d.tp1.closeness, c("closeness_tp1_a2q"="closeness_G1",
                                             "closeness_tp1_c2q"="closeness_G2",
                                             "closeness_tp1_c2a"="closeness_G3"))
C <- cor(d.tp1.closeness[,2:NCOL(d.tp1.closeness)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

### Histograms ###
# create various histograms in log-log scale
ggplot(data=d.tp1, aes(d.tp1$out_degree_tp1_a2q)) + 
  geom_histogram(aes(y =..density..), 
                 col="red", 
                 binwidth=0.0001,
                 alpha = .2) + 
  scale_x_log10() +
  scale_y_log10() +
  labs(title="P1 Histogram for Out-Degree in a2q") +
  labs(x="Normalized Out-Degree (log-scale)", y="Count (log-scale)")

ggplot(data=d.tp1, aes(d.tp1$in_degree_tp1_a2q)) + 
  geom_histogram(aes(y =..density..), 
                 col="red", 
                 binwidth=0.0001,
                 alpha = .2) + 
  scale_x_log10() +
  scale_y_log10() +
  labs(title="P1 Histogram for In-Degree in a2q") +
  labs(x="Normalized In-Degree (log-scale)", y="Count (log-scale)")

ggplot(data=d.tp1, aes(d.tp1$out_degree_tp1_c2q)) + 
  geom_histogram(aes(y =..density..), 
                 col="red", 
                 binwidth=0.0001,
                 alpha = .2) + 
  scale_x_log10() +
  scale_y_log10() +
  labs(title="P1 Histogram for Out-Degree in c2q") +
  labs(x="Normalized Out-Degree (log-scale)", y="Count (log-scale)")

ggplot(data=d.tp1, aes(d.tp1$in_degree_tp1_c2q)) + 
  geom_histogram(aes(y =..density..), 
                 col="red", 
                 binwidth=0.0001,
                 alpha = .2) + 
  scale_x_log10() +
  scale_y_log10() +
  labs(title="P1 Histogram for In-Degree in c2q") +
  labs(x="Normalized In-Degree (log-scale)", y="Count (log-scale)")

ggplot(data=d.tp1, aes(d.tp1$out_degree_tp1_c2a)) + 
  geom_histogram(aes(y =..density..), 
                 col="red", 
                 binwidth=0.0001,
                 alpha = .2) + 
  scale_x_log10() +
  scale_y_log10() +
  labs(title="P1 Histogram for Out-Degree in c2a") +
  labs(x="Normalized Out-Degree (log-scale)", y="Count (log-scale)")

ggplot(data=d.tp1, aes(d.tp1$in_degree_tp1_c2a)) + 
  geom_histogram(aes(y =..density..), 
                 col="red", 
                 binwidth=0.0001,
                 alpha = .2) + 
  scale_x_log10() +
  scale_y_log10() +
  labs(title="P1 Histogram for In-Degree in c2a") +
  labs(x="Normalized In-Degree (log-scale)", y="Count (log-scale)")

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

### Correlation plot between metrics within layer ###
# create correlation plot between metrics in a2q (G1)
d.tp2.a2q <- subset(d.tp2, select = c("node_id","in_degree_tp2_a2q","out_degree_tp2_a2q",
                                      "n_appearances_tp2_c2a","pagerank_tp2_c2a",
                                      "coreness_tp2_c2a","closeness_tp2_c2a"))
d.tp2.a2q <- rename(d.tp2.a2q, c("in_degree_tp2_a2q"="in_degree", "out_degree_tp2_a2q"="out_degree",
                                 "n_appearances_tp2_c2a"="n_appearances", "pagerank_tp2_c2a"="pagerank",
                                 "coreness_tp2_c2a"="coreness","closeness_tp2_c2a"="closeness"))
C <- cor(d.tp2.a2q[,2:NCOL(d.tp2.a2q)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# create correlation plot between metrics in c2q (G2)
d.tp2.c2q <- subset(d.tp2, select = c("node_id","in_degree_tp2_c2q","out_degree_tp2_c2q",
                                      "n_appearances_tp2_c2a","pagerank_tp2_c2a",
                                      "coreness_tp2_c2a","closeness_tp2_c2a"))
d.tp2.c2q <- rename(d.tp2.c2q, c("in_degree_tp2_c2q"="in_degree", "out_degree_tp2_c2q"="out_degree",
                                 "n_appearances_tp2_c2a"="n_appearances", "pagerank_tp2_c2a"="pagerank",
                                 "coreness_tp2_c2a"="coreness","closeness_tp2_c2a"="closeness"))
C <- cor(d.tp2.c2q[,2:NCOL(d.tp2.c2q)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# create correlation plot between metrics in c2a (G3)
d.tp2.c2a <- subset(d.tp2, select = c("node_id","in_degree_tp2_c2a","out_degree_tp2_c2a",
                                      "n_appearances_tp2_c2a","pagerank_tp2_c2a",
                                      "coreness_tp2_c2a","closeness_tp2_c2a"))
d.tp2.c2a <- rename(d.tp2.c2a, c("in_degree_tp2_c2a"="in_degree", "out_degree_tp2_c2a"="out_degree",
                                 "n_appearances_tp2_c2a"="n_appearances", "pagerank_tp2_c2a"="pagerank",
                                 "coreness_tp2_c2a"="coreness","closeness_tp2_c2a"="closeness"))
C <- cor(d.tp2.c2a[,2:NCOL(d.tp2.c2a)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

### Correlation plot between layers ###
# create correlation plot between layers
# in-degree metric
d.tp2.in_degree <- subset(d.tp2, select = c("node_id","in_degree_tp2_a2q",
                                            "in_degree_tp2_c2q","in_degree_tp2_c2a"))
d.tp2.in_degree <- rename(d.tp2.in_degree, c("in_degree_tp2_a2q"="in_degree_G1",
                                             "in_degree_tp2_c2q"="in_degree_G2",
                                             "in_degree_tp2_c2a"="in_degree_G3"))
C <- cor(d.tp2.in_degree[,2:NCOL(d.tp2.in_degree)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# out-degree metric
d.tp2.out_degree <- subset(d.tp2, select = c("node_id","out_degree_tp2_a2q",
                                             "out_degree_tp2_c2q","out_degree_tp2_c2a"))
d.tp2.out_degree <- rename(d.tp2.out_degree, c("out_degree_tp2_a2q"="out_degree_G1",
                                               "out_degree_tp2_c2q"="out_degree_G2",
                                               "out_degree_tp2_c2a"="out_degree_G3"))
C <- cor(d.tp2.out_degree[,2:NCOL(d.tp2.out_degree)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# closeness metric
d.tp2.closeness <- subset(d.tp2, select = c("node_id","closeness_tp2_a2q",
                                            "closeness_tp2_c2q","closeness_tp2_c2a"))
d.tp2.closeness <- rename(d.tp2.closeness, c("closeness_tp2_a2q"="closeness_G1",
                                             "closeness_tp2_c2q"="closeness_G2",
                                             "closeness_tp2_c2a"="closeness_G3"))
C <- cor(d.tp2.closeness[,2:NCOL(d.tp2.closeness)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# create various histograms in log-log scale
ggplot(data=d.tp2, aes(d.tp2$out_degree_tp2_a2q)) + 
  geom_histogram(aes(y =..density..), 
                 col="red", 
                 binwidth=0.0001,
                 alpha = .2) + 
  scale_x_log10() +
  scale_y_log10() +
  labs(title="P2 Histogram for Out-Degree in a2q") +
  labs(x="Normalized Out-Degree (log-scale)", y="Count (log-scale)")

ggplot(data=d.tp2, aes(d.tp2$in_degree_tp2_a2q)) + 
  geom_histogram(aes(y =..density..), 
                 col="red", 
                 binwidth=0.0001,
                 alpha = .2) + 
  scale_x_log10() +
  scale_y_log10() +
  labs(title="P2 Histogram for In-Degree in a2q") +
  labs(x="Normalized In-Degree (log-scale)", y="Count (log-scale)")

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

### Correlation plot between metrics within layer ###
# create correlation plot between metrics in a2q (G1)
d.tp3.a2q <- subset(d.tp3, select = c("node_id","in_degree_tp3_a2q","out_degree_tp3_a2q",
                                      "n_appearances_tp3_c2a","pagerank_tp3_c2a",
                                      "coreness_tp3_c2a","closeness_tp3_c2a"))
d.tp3.a2q <- rename(d.tp3.a2q, c("in_degree_tp3_a2q"="in_degree", "out_degree_tp3_a2q"="out_degree",
                                 "n_appearances_tp3_c2a"="n_appearances", "pagerank_tp3_c2a"="pagerank",
                                 "coreness_tp3_c2a"="coreness","closeness_tp3_c2a"="closeness"))
C <- cor(d.tp3.a2q[,2:NCOL(d.tp3.a2q)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# create correlation plot between metrics in c2q (G2)
d.tp3.c2q <- subset(d.tp3, select = c("node_id","in_degree_tp3_c2q","out_degree_tp3_c2q",
                                      "n_appearances_tp3_c2a","pagerank_tp3_c2a",
                                      "coreness_tp3_c2a","closeness_tp3_c2a"))
d.tp3.c2q <- rename(d.tp3.c2q, c("in_degree_tp3_c2q"="in_degree", "out_degree_tp3_c2q"="out_degree",
                                 "n_appearances_tp3_c2a"="n_appearances", "pagerank_tp3_c2a"="pagerank",
                                 "coreness_tp3_c2a"="coreness","closeness_tp3_c2a"="closeness"))
C <- cor(d.tp3.c2q[,2:NCOL(d.tp3.c2q)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# create correlation plot between metrics in c2a (G3)
d.tp3.c2a <- subset(d.tp3, select = c("node_id","in_degree_tp3_c2a","out_degree_tp3_c2a",
                                      "n_appearances_tp3_c2a","pagerank_tp3_c2a",
                                      "coreness_tp3_c2a","closeness_tp3_c2a"))
d.tp3.c2a <- rename(d.tp3.c2a, c("in_degree_tp3_c2a"="in_degree", "out_degree_tp3_c2a"="out_degree",
                                 "n_appearances_tp3_c2a"="n_appearances", "pagerank_tp3_c2a"="pagerank",
                                 "coreness_tp3_c2a"="coreness","closeness_tp3_c2a"="closeness"))
C <- cor(d.tp3.c2a[,2:NCOL(d.tp3.c2a)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

### Correlation plot between layers ###
# create correlation plot between layers
# in-degree metric
d.tp3.in_degree <- subset(d.tp3, select = c("node_id","in_degree_tp3_a2q",
                                            "in_degree_tp3_c2q","in_degree_tp3_c2a"))
d.tp3.in_degree <- rename(d.tp3.in_degree, c("in_degree_tp3_a2q"="in_degree_G1",
                                             "in_degree_tp3_c2q"="in_degree_G2",
                                             "in_degree_tp3_c2a"="in_degree_G3"))
C <- cor(d.tp3.in_degree[,2:NCOL(d.tp3.in_degree)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# out-degree metric
d.tp3.out_degree <- subset(d.tp3, select = c("node_id","out_degree_tp3_a2q",
                                             "out_degree_tp3_c2q","out_degree_tp3_c2a"))
d.tp3.out_degree <- rename(d.tp3.out_degree, c("out_degree_tp3_a2q"="out_degree_G1",
                                               "out_degree_tp3_c2q"="out_degree_G2",
                                               "out_degree_tp3_c2a"="out_degree_G3"))
C <- cor(d.tp3.out_degree[,2:NCOL(d.tp3.out_degree)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# closeness metric
d.tp3.closeness <- subset(d.tp3, select = c("node_id","closeness_tp3_a2q",
                                            "closeness_tp3_c2q","closeness_tp3_c2a"))
d.tp3.closeness <- rename(d.tp3.closeness, c("closeness_tp3_a2q"="closeness_G1",
                                             "closeness_tp3_c2q"="closeness_G2",
                                             "closeness_tp3_c2a"="closeness_G3"))
C <- cor(d.tp3.closeness[,2:NCOL(d.tp3.closeness)], use="complete.obs", method="pearson")
corrplot(C, method = "circle")

# create various histograms in log-log scale
ggplot(data=d.tp3, aes(d.tp3$out_degree_tp3_a2q)) + 
  geom_histogram(aes(y =..density..), 
                 col="red", 
                 binwidth=0.0001,
                 alpha = .2) + 
  scale_x_log10() +
  scale_y_log10() +
  labs(title="P3 Histogram for Out-Degree in a2q") +
  labs(x="Normalized Out-Degree (log-scale)", y="Count (log-scale)")

ggplot(data=d.tp3, aes(d.tp3$in_degree_tp3_a2q)) + 
  geom_histogram(aes(y =..density..), 
                 col="red", 
                 binwidth=0.0001,
                 alpha = .2) + 
  scale_x_log10() +
  scale_y_log10() +
  labs(title="P3 Histogram for In-Degree in a2q") +
  labs(x="Normalized In-Degree (log-scale)", y="Count (log-scale)")
