import networkx as nx
import pickle
import matplotlib.pyplot as plt

action_logs = []
user_set = set()
user_action_count = pickle.load(open("./processed/userActionCount.dic", 'rb'))

# part1: read the action log
fin_rating = open("./processed/action_logs.txt", encoding="utf8", errors='ignore')
line = fin_rating.readline()  # skip the first line
for line in fin_rating:
    arr = line.split()
    user = int(arr[0])
    movie = int(arr[1])

    if movie == 54053:
        user_set.add(user)

fin_rating.close()
print("Number of users: ", len(user_set))

# part2: read the graph
#
# degree = {}
# node_list = []
#
# f_graph = open('./raw/link.txt', encoding="utf8", errors='ignore')
# for line in f_graph:
#     data = line.split()
#     u = int(data[0])
#     v = int(data[1])
#     try:
#         degree[v] += 1
#     except:
#         degree[v] = 1
#     try:
#         degree[u] += 1
#     except:
#         degree[u] = 1
# f_graph.close()
#
# for key in user_set:
#     if 20 <= degree[key]:
#         node_list.append(key)
#
# print('node list length: ', len(node_list))

G = nx.Graph()
f_graph = open('./raw/link.txt', encoding="utf8", errors='ignore')
for line in f_graph:
    data = line.split()
    u = int(data[0])
    v = int(data[1])
    if u in user_set and v in user_set:
        G.add_edge(u, v)

f_graph.close()

print("G size : ", len(G.nodes()), len(G.edges()))

# nx.draw(G)
# plt.show()
# pickle.dump(G, open(save_dir + 'graph_max_component.G', "wb"))


# part3: find the max connected component
print("start finding max component...")
save_dir = "./processed/"

component = max(nx.connected_components(G), key=len)
Gc = G.subgraph(component).copy()
print("the max component Gc size : ", len(Gc.nodes()), len(Gc.edges()))

# nx.draw(Gc)
# plt.show()

pickle.dump(Gc, open(save_dir + 'graph_max_component.G', "wb"))

#######################################
# @output:
# Number of users: 2252
# G size: 23917 24870
# the max component Gc size: 21433 23162
########################################
