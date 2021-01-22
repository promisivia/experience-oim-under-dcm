import time
import pickle
import networkx as nx
import random
import matplotlib.pyplot as plt

start = time.time()
G = nx.DiGraph()
in_degree = {}

nodelist = [i for i in range(20)]

for u in nodelist:
    for v in nodelist:
        if u == v:
            continue
        if random.random() < 0.2:
            G.add_edge(u, v, weight=1)

print(len(G.nodes()), len(G.edges()))
nx.draw(G)
plt.show()
pickle.dump(G, open('../datasets/Small/graph.G', "wb"))
print('Built Small graph G', time.time() - start, 's')
