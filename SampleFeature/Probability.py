import pickle
import random

edgeDic = {}

# --------------------------- DC Interval P ----------------------------------- #
dataset = 'SameP/NetHEPT'
G = pickle.load(open('../datasets/' + dataset + '/graph.G', 'rb'))
low = 0.1
high = 0.5
for (u, in_degree) in G.in_degree:
    for index in range(in_degree):
        edgeDic[(u, index)] = random.uniform(low, high)
print('prob dic:', edgeDic)
pickle.dump(edgeDic, open('../datasets/' + dataset + '/' + str(low) + '-' + str(high) + '-Probability.dic', "wb"))

# --------------------------- IC/DC Fix P  ----------------------------------- #
prob = 0.8
dataset = 'Small'
G = pickle.load(open('../datasets/' + dataset + '/graph.G', 'rb'))
edgeDic = {}
for (u, v) in G.edges():
    edgeDic[(u, v)] = prob
print('prob dic:', edgeDic)
pickle.dump(edgeDic, open('../datasets/' + dataset + '/' + str(prob) + '-IC-Probability.dic', "wb"))

edgeDic = {}
for (u, in_degree) in G.in_degree:
    for index in range(in_degree):
        edgeDic[(u, index)] = prob
print('prob dic:', edgeDic)
pickle.dump(edgeDic, open('../datasets/' + dataset + '/' + str(prob) + '-Probability.dic', "wb"))
