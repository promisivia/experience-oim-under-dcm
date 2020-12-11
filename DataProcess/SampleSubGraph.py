import pickle
import networkx as nx
import random
import matplotlib.pyplot as plt

file_address = './raw/flickrEdges.txt'
save_dir = '../datasets/Flickr/'

# file_address = './raw/netHEPTEdges.txt'
# save_dir = '../datasets/SameP/NetHEPT/'

# degree = {}
# node_list = []
#
# # count the degree
# with open(file_address) as f:
#     count = 0
#     for line in f:
#         if count > 4:  # skip the first four line
#             # data = line.split(' ')  # Flikr
#             data = line.split('\t')  # NetHEPT
#             u = int(data[0])
#             v = int(data[1])
#             try:
#                 degree[v] += 1
#             except:
#                 degree[v] = 1
#             try:
#                 degree[u] += 1
#             except:
#                 degree[u] = 1
#         count += 1
#
# for key in degree:
#     if 20 <= degree[key] <= 120:
#         node_list.append(key)
#
# print('node list length: ', len(node_list))
#
# small_node_list = [node_list[i] for i in sorted(random.sample(range(len(node_list)), int(len(node_list) / 1000)))]
# print('small node list: ', small_node_list)
# print('small node list length: ', len(small_node_list))
#
# G = nx.Graph()
# with open(file_address) as f:
#     count = 0
#     for line in f:
#         # print(line)
#         if count > 4:
#             # data = line.split(' ')  # Flikr
#             data = line.split('\t')  # NetHEPT
#             u = int(data[0])
#             v = int(data[1])
#
#             if v in small_node_list or u in small_node_list:
#                 G.add_edge(u, v)
#
#         count += 1
#
# print("G size : ", len(G.nodes()), len(G.edges()))
#
# component = max(nx.connected_components(G), key=len)
# Gc = G.subgraph(component).copy()

Gc = pickle.load(open(save_dir + 'graph.G', 'rb'))
nodes = Gc.nodes()
edge = Gc.edges()

G = nx.DiGraph()
indegree = {}
with open(file_address) as f:
    count = 0
    for line in f:
        if count > 4:
            data = line.split(' ')  # Flikr
            # data = line.split('\t')  # NetHEPT
            u = int(data[0])
            v = int(data[1])

            if u in nodes and v in nodes:
                G.add_edge(u, v)
                try:
                    indegree[v] += 1
                except:
                    indegree[v] = 1
        count += 1

nx.draw(G)
plt.show()
print("G size : ", len(G.nodes()), len(G.edges()))

pickle.dump(G, open(save_dir + 'graph.G', "wb"))
pickle.dump(indegree, open(save_dir + 'indegree.dic', "wb"))


####################################################################
# @output
# node list length:  10877
# small node list:  [2083521852, 183494906, 2371006912, 102049534, 2299203803, 91947266, 611263940, 2529257887, 2210235799, 430533428]
# small node list length:  10
# G size :  589 586
# Gc size :  319 5904

# node list length:  10482
# small node list:  [9706155, 9706187, 2250, 4160, 9609094, 203206, 9908192, 202056, 9909186, 205155]
# small node list length:  10
# G size :  374
# G size :  323 3478
#####################################################################
