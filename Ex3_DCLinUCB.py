from Tool.utilFunc import *
from RunTools.MainForDCUCB import MainForDCUCB, MainForDCLinUCB

# data
dataset = 'Flickr'
kind = 'dense'
scale = 'same-theta-'
seed_size = 10
iterations = 10000

if __name__ == '__main__':
    save_address = 'SimulationResults/Ex3-15/' + scale + kind + '/'

    G = pickle.load(open('datasets/' + dataset + '/' + kind + '/graph.G', 'rb'), encoding='latin1')
    indegree = pickle.load(open('datasets/' + dataset + '/' + kind + '/indegree.dic', 'rb'), encoding='latin1')
    P = pickle.load(open('datasets/' + dataset + '/' + kind + '/' + scale + 'Probability.dic', 'rb'), encoding='latin1')
    parameter = pickle.load(open('datasets/' + dataset + '/' + kind + '/nodeFeatures.dic', 'rb'), encoding='latin1')
    feature_dic = pickle.load(open('datasets/' + dataset + '/' + kind + '/' + scale + 'edgeFeatures.dic', 'rb'),
                              encoding='latin1')

    # MainForDC(G, indegree, P, P, feature_dic, iterations, seed_size, dataset, save_address,
    #           algorithm='DILinUCB-DC-new-old-DC', times=10)
    # MainForDCUCB(G, indegree, P, 'parameter', feature_dic, iterations, seed_size, dataset, save_address, 0.1, 1)
    MainForDCLinUCB(G, indegree, P, 'parameter', feature_dic, iterations, seed_size, dataset, save_address, times=1, dimension=5)
