import pickle
import matplotlib.pyplot as plt
import networkx as nx

file_address = './process/'
save_dir = '../datasets/Flixster/'

# newG = nx.DiGraph()
# print('start construct graph with prob between 1 to 300:')
# graph_address = './raw/link.txt'
# with open(graph_address) as f:
#     for line in f:
#         data = line.split()
#         u = int(data[0])
#         v = int(data[1])
#         try:
#             if 1 <= edgeSuccessTimeDic[(u, v)]:
#                 newG.add_edge(u, v)
#         except:
#             print('can not find this edge')
# print("newG size : ", len(newG.nodes()), len(newG.edges()))
# pickle.dump(newG, open(file_address + 'newG.G', "wb"))

start = 5
end = 100
node_list = []

print('start choosing nodes with indegree between ' + str(start) + ' and ' + str(end))
for (node, in_degree) in newG.in_degree:
    if start <= in_degree < end:
        node_list.append(node)

for (node, out_degree) in newG.out_degree:
    if start <= out_degree < end:
        node_list.append(node)

print('nodelist length:', len(node_list))

G = nx.DiGraph()
for (u, v) in newG.edges():
    if (u in node_list or v in node_list) and userActionCountDic[u] > 15 and userActionCountDic[v] > 15:
        G.add_edge(u, v)

nx.draw(G)
plt.show()
print("small G size : ", len(G.nodes()), len(G.edges()))
pickle.dump(G, open(save_dir + 'graph.G', "wb"))