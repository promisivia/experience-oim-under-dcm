import pickle

save_dir = '../datasets/NetHEPT/'

nodeDic = {}
edgeDic = {}
degree = []
G = pickle.load(open(save_dir + 'graph.G', 'rb'))
n = len(G.nodes())
for index, u in enumerate(G.nodes()):
    fv = [0 for i in range(n)]
    fv[index] = 1
    nodeDic[u] = [fv, fv]

pickle.dump(nodeDic, open(save_dir + 'nodeFeatures.dic', "wb"))
