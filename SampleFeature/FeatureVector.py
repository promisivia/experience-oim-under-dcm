import pickle
import random
import numpy as np
from operator import itemgetter

probDic = {}
featureDic = {}
dimension = 5
p_prob = 0.1
fv_prob = 0.1
scale = 5
dataset = 'Flickr'
kind = 'random'

p = np.array([np.random.normal(0, 0.5, 1)[0] for i in range(dimension - 1)])  # 一个全局的p*
l2_norm = np.linalg.norm(p, ord=2)
# 随机数字然后正则化
p = p / l2_norm
p = [.5 * i for i in p]
p = [*p, .5]

p = [i / scale for i in p]
print('global p* is', p)

# --------------------------- DC probability ----------------------------------- #
G = pickle.load(open('../datasets/' + dataset + '/graph.G', 'rb'))
for (u, in_degree) in G.in_degree:

    prob2fv = {}

    if kind == 'same':
        for k in range(in_degree):
            featureVector = np.array([np.random.normal(0, 0.5, 1)[0] for i in range(dimension - 1)])
            l2_norm = np.linalg.norm(featureVector, ord=2)
            # 随机数字然后正则化
            featureVector = featureVector / l2_norm
            featureVector = [*featureVector, 1]

            prob = min(np.dot(p, np.transpose(featureVector)), 1)
            prob2fv[prob] = featureVector

        # sort in decreasing order
        sorted_prob2fv = sorted(prob2fv.keys(), reverse=True)
        for index, prob in enumerate(sorted_prob2fv):
            probDic[(u, index)] = prob
            featureDic[(list(G.pred[u])[index], u)] = prob2fv[prob]

    # random prob and random feature vector
    elif kind == 'random':
        prob_list = [round(random.uniform(0.1, 0.2), 10) for i in range(in_degree)]
        # sort in decreasing order
        prob_list.sort(reverse=True)
        for index, prob in enumerate(prob_list):
            probDic[(u, index)] = prob

            featureVector = np.array([np.random.normal(-1, 1, 1)[0] for i in range(dimension)])
            featureDic[(list(G.pred[u])[index], u)] = [*featureVector]

    elif kind == 'reduce':
        for index in range(in_degree):
            featureVector = np.array([np.random.normal(0, 0.5, 1)[0] for i in range(dimension - 1)])
            l2_norm = np.linalg.norm(featureVector, ord=2)
            # 随机数字然后正则化
            featureVector = featureVector / l2_norm
            featureVector = [*featureVector, 1]

            prob = min(np.dot([(.9 ** index) * i for i in p], np.transpose(featureVector)), 1)

            probDic[(u, index)] = prob
            featureDic[(list(G.pred[u])[index], u)] = featureVector

print('prob dic:', probDic)
print('fv dic:', featureDic)

pickle.dump(probDic, open('../datasets/' + dataset + '/' + kind + '-Probability.dic', "wb"))
pickle.dump(featureDic, open('../datasets/' + dataset + '/' + kind + '-edgeFeatures.dic', "wb"))


###################################################################################
# same:
# F: global p* is [-0.0429265255531134, 0.061412193399082826, 0.0578032253948285, -0.03232093810219934, 0.1]
# N: global p* is [0.07853479406801706, 0.05923160757662577, -0.017961249800640174, 0.0011385473998759515, 0.1]
# random:
#
#####################################################################################
