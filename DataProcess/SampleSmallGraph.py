import time
import pickle
import networkx as nx
import random

start = time.time()
G = nx.DiGraph()
in_degree = {}

nodelist = [i for i in range(20)]

for u in nodelist:
    for v in nodelist:
        if u == v:
            continue
        if random.random() < 0.15:
            G.add_edge(u, v, weight=1)

print(len(G.nodes()), len(G.edges()))
print(G)
pickle.dump(G, open('../datasets/Small2/graph.G', "wb"))
print('Built Small2 graph G', time.time() - start, 's')
