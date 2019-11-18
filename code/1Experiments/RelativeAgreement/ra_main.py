### Generate a SWN using networkx and derive constructor parameters that 
# result in a graph matching the specs of empirical data for film actor SWN
# Reference - https://www.nature.com/articles/30918
# Empirical data for Film Actors (https://www.nature.com/articles/30918/tables/1):
# Emp data for academics http://networkrepository.com/soc-academia.php
# Clustering Coefficient    C   -> 0.79 | 0.24(For academic avg clustering)
# Avg shortest Path         L   -> 3.65 | 
#### For 100 nodes - k=5/6, p=0.25
#### For 1000 nodes - k=11, p=0.29

import networkx as nx
import numpy as np

num_of_nodes = 100
# k_neighbors_fraction = 0.02 -> 0.10
k_range = np.linspace(0.02,0.1,9)
# p_rewire = 0.05 -> 0.5
p_range = np.linspace(0.05,0.5,10)

G_L_2 = np.zeros([len(k_range)+1,len(p_range)+1])
G_C_2 = np.zeros([len(k_range)+1,len(p_range)+1])

for k in k_range:
    for p in p_range:

        G_temp = nx.generators.random_graphs.watts_strogatz_graph(num_of_nodes, int(k*num_of_nodes), p)
        
        try:
            L_temp = nx.average_shortest_path_length(G_temp)
        except:
            L_temp = 0
        
        C_temp = nx.average_clustering(G_temp)
        G_L_2[list(k_range).index(k)][list(p_range).index(p)] = L_temp
        G_C_2[list(k_range).index(k)][list(p_range).index(p)] = C_temp

print(G_C_2)
print(G_L_2)