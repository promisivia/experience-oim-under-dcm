import pickle
import random

edgeDic = {}

# --------------------------- Ex1 Model ----------------------------------- #
# G = pickle.load(open('../datasets/Small1/graph.G', 'rb'))
# low = 0.5
# high = 0.9
# for (u, in_degree) in G.in_degree:
#     for index in range(in_degree):
#         edgeDic[(u, index)] = random.uniform(low, high)
# print('prob dic:', edgeDic)
# pickle.dump(edgeDic, open('../datasets/Small1/' + str(low) + '-' + str(high) + '-Probability.dic', "wb"))

# --------------------------- DC probability ----------------------------------- #
G = pickle.load(open('../datasets/Flickr/dense/graph.G', 'rb'))
for (u, in_degree) in G.in_degree:
    prob_list = [round(random.uniform(0, 0.1), 5) for i in range(in_degree)]
    # 降序排序
    prob_list.sort(reverse=True)
    for index, prob in enumerate(prob_list):
        edgeDic[(u, index)] = prob
print('prob dic:', edgeDic)
pickle.dump(edgeDic, open('../datasets/Flickr/0-0.1-DC-Probability.dic', "wb"))

# --------------------------- Ex2_p=0.2 Model ----------------------------------- #
# prob = 0.8
# dataset = 'NetHEPT'
# G = pickle.load(open('../datasets/SameP/' + dataset + '/graph.G', 'rb'))
# edgeDic = {}
# for (u, v) in G.edges():
#     edgeDic[(u, v)] = prob
# print('prob dic:', edgeDic)
# pickle.dump(edgeDic, open('../datasets/SameP/' + dataset + '/' + str(prob) + 'Probability.dic', "wb"))

# --------------------------- Ex2_p=0.2 SameP ----------------------------------- #
# G = pickle.load(open('../datasets/SameP/graph.G', 'rb'))
# edgeDic = {}
# for (u, in_degree) in G.in_degree:
#     for index in range(in_degree):
#         edgeDic[(u, index)] = prob
# print('prob dic:', edgeDic)
# pickle.dump(edgeDic, open('../datasets/SameP/' + dataset + '/' + str(prob) + 'DC_Probability.dic', "wb"))
