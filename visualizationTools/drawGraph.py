import pickle
import matplotlib.pyplot as plt
import networkx as nx

file_address = '../datasets/Small/'
graph = pickle.load(open(file_address + 'graph.G', 'rb'), encoding='latin1')
plt.cla()
plt.title('(a) 20 nodes, 70 edges', fontsize=16)
nx.draw(graph, with_labels=True)
plt.savefig(file_address + 'graph.pdf', dpi=400)
