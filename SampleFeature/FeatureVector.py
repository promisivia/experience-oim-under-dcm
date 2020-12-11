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
dataset = 'dense'
kind = 'same'

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

        # 降序排序
        sorted_prob2fv = sorted(prob2fv.keys(), reverse=True)
        for index, prob in enumerate(sorted_prob2fv):
            probDic[(u, index)] = prob
            featureDic[(list(G.pred[u])[index], u)] = prob2fv[prob]

    if kind == 'reduce':
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

pickle.dump(probDic,
            open('../datasets/' + dataset + '/' + kind + '-theta-Probability.dic', "wb"))
pickle.dump(featureDic,
            open('../datasets/' + dataset + '/' + kind + '-theta-edgeFeatures.dic', "wb"))
