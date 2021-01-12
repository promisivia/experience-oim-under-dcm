import pickle
import random

edgeDic = {}

# --------------------------- Range Prob ----------------------------------- #
# G = pickle.load(open('../datasets/NetHEPT/graph.G', 'rb'))
# low = 0.5
# high = 0.9
# for (u, in_degree) in G.in_degree:
#     for index in range(in_degree):
#         edgeDic[(u, index)] = random.uniform(low, high)
# print('prob dic:', edgeDic)
# pickle.dump(edgeDic, open('../datasets/NetHEPT/' + str(low) + '-' + str(high) + '-Probability.dic', "wb"))

# ---------------------------- Same Prob  ----------------------------------- #
prob = 0.2
dataset = 'SameP/NetHEPT'
G = pickle.load(open('../datasets/' + dataset + '/graph.G', 'rb'))
edgeDic = {}
for (u, v) in G.edges():
    edgeDic[(u, v)] = prob
print('prob dic:', edgeDic)
pickle.dump(edgeDic, open('../datasets/' + dataset + '/' + str(prob) + 'Probability.dic', "wb"))

# --------------------------- Ex2 DC Model ----------------------------------- #
G = pickle.load(open('../datasets/' + dataset + '/graph.G', 'rb'))
edgeDic = {}
for (u, in_degree) in G.in_degree:
    for index in range(in_degree):
        edgeDic[(u, index)] = prob
print('prob dic:', edgeDic)
pickle.dump(edgeDic, open('../datasets/' + dataset + '/' + str(prob) + '-Probability.dic', "wb"))
