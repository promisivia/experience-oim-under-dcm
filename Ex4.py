from Tool.utilFunc import *
from RunTools.MainForCMAB import MainForCMAB
from RunTools.MainForDC import MainForDC
from RunTools.MainForIC import MainForIC
from RunTools.MainForDCUCB import MainForDCUCB

# data
seed_size = 5
iterations = 10000

if __name__ == '__main__':
    dataset = 'Flixster'
    scale = 'DC'
    save_address = 'SimulationResults/Ex4/'

    G = pickle.load(open('datasets/' + dataset + '/graph.G', 'rb'), encoding='latin1')
    indegree = pickle.load(open('datasets/' + dataset + '/indegree.dic', 'rb'), encoding='latin1')
    # P = pickle.load(open('datasets/' + dataset + '/' + scale + '-Probability.dic', 'rb'), encoding='latin1')
    parameter = pickle.load(open('datasets/' + dataset + '/nodeFeatures.dic', 'rb'), encoding='latin1')

    # MainForCMAB(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address, real_mode=True, times=5)
    # MainForIC(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address, algorithm='CUCB', real_mode=True, times=2)
    # MainForIC(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address, algorithm='DILinUCB-IC', real_mode=True, times=2)
    MainForDCUCB(G, indegree, None, parameter, None, iterations, seed_size, dataset, save_address, 0.1, times=1, real_mode=True)


