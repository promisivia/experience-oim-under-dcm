import pickle
import matplotlib.pyplot as plt
import networkx as nx

# file_address = '../datasets/Small2/'
# graph = pickle.load(open(file_address + 'graph.G', 'rb'), encoding='latin1')
# for index in range(0, 100):
#     plt.cla()
#     plt.title('(b) 20 nodes, 51 edges', fontsize=16)
#     nx.draw(graph, with_labels=True)
#     plt.savefig(file_address + 'graph'+str(index)+'.png', dpi=400)
#
# file_address = '../datasets/Small1/'
# graph = pickle.load(open(file_address + 'graph.G', 'rb'), encoding='latin1')
# for index in range(0, 100):
#     plt.cla()
#     plt.title('(a) 10 nodes, 13 edges', fontsize=16)
#     nx.draw(graph, with_labels=True)
#     plt.savefig(file_address + 'graph'+str(index)+'.pdf', dpi=400)

file_address = '../datasets/Flixster/'
graph = pickle.load(open(file_address + 'graph.G', 'rb'), encoding='latin1')
nx.draw(graph)
plt.show()
