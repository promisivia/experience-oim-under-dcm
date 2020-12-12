import pickle

file_address = '../datasets/Flixster/'
graph = pickle.load(open(file_address + 'graph.G', 'rb'), encoding='latin1')

indegree = {}
for (u, v) in graph.edges():
    try:
        indegree[u] += 1
    except:
        indegree[u] = 1
    try:
        indegree[v] += 1
    except:
        indegree[v] = 1

pickle.dump(indegree, open(file_address + 'indegree.dic', "wb"))
