from RunTools.MainForDC import MainForDC
from Tool.utilFunc import *
from RunTools.MainForCMAB import MainForCMAB
from RunTools.MainForDCUCB import MainForDCUCB, MainForDCLinUCB

# data
dataset = 'Flickr'
kind = 'dense'
scale = 'same-theta-'
seed_size = 10
iterations = 10000

if __name__ == '__main__':
    save_address = 'SimulationResults/Test/' + scale + kind + '/'

    G = pickle.load(open('datasets/' + dataset + '/' + kind + '/graph.G', 'rb'), encoding='latin1')
    indegree = pickle.load(open('datasets/' + dataset + '/' + kind + '/indegree.dic', 'rb'), encoding='latin1')
    P = pickle.load(open('datasets/' + dataset + '/' + kind + '/' + scale + 'Probability.dic', 'rb'), encoding='latin1')
    parameter = pickle.load(open('datasets/' + dataset + '/' + kind + '/nodeFeatures.dic', 'rb'), encoding='latin1')
    feature_dic = pickle.load(open('datasets/' + dataset + '/' + kind + '/' + scale + 'edgeFeatures.dic', 'rb'),
                              encoding='latin1')

    # MainForCMAB(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address)
    MainForDC(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address,
              algorithm='DILinUCB', times=1)
    # MainForDCUCB(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address, 0.1)
    # MainForDCLinUCB(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address)
