import pickle
import random
import numpy as np

featureDic = {}
dimension = 5
dataset = 'NetHEPT'

# --------------------------- DC probability ----------------------------------- #
G = pickle.load(open('../datasets/' + dataset + '/graph.G', 'rb'))
for (u, v) in G.edges():
    featureVector = np.array([np.random.normal(-1, 1, 1)[0] for i in range(dimension)])
    l2_norm = np.linalg.norm(featureVector, ord=2)
    featureVector = featureVector / l2_norm
    featureDic[u, v] = [*featureVector]

print('fv dic:', featureDic)

pickle.dump(featureDic, open('../datasets/' + dataset + '/random-edgeFeatures.dic', "wb"))
