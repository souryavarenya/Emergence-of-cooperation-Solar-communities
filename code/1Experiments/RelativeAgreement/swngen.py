import numpy as np 
import networkx as nx 

def swntest(k_frac,p):
    C = []
    L = []
    n = 10
    nodes = 1000
    for i in range(n):
        Gt = nx.generators.random_graphs.watts_strogatz_graph(nodes, int(k_frac*nodes), p)
        try:
            L.append(nx.average_shortest_path_length(Gt))
        except:
            L.append(0)
        C.append(nx.average_clustering(Gt))

    C_avg = sum(C)/n
    L_avg = sum(L)/n

    print("Clustering Coefficient - " + str(C_avg))
    print("Avg shortest distacne - " + str(L_avg))