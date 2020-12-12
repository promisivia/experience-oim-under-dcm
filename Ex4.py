from Tool.utilFunc import *
from RunTools.MainForCMAB import MainForCMAB
from RunTools.MainForIC import MainForIC
from RunTools.MainForDCUCB import MainForDCUCB

# data
seed_size = 5
iterations = 10000
dataset = 'Flixster'
save_address = 'SimulationResults/Ex4/'

if __name__ == '__main__':
    G = pickle.load(open('datasets/' + dataset + '/graph.G', 'rb'), encoding='latin1')
    indegree = pickle.load(open('datasets/' + dataset + '/indegree.dic', 'rb'), encoding='latin1')
    parameter = pickle.load(open('datasets/' + dataset + '/nodeFeatures.dic', 'rb'), encoding='latin1')

    MainForCMAB(G, indegree, None, parameter, None, iterations, seed_size, dataset, save_address, real_mode=True)
    MainForIC(G, indegree, None, parameter, None, iterations, seed_size, dataset, save_address, algorithm='CUCB', real_mode=True)
    MainForIC(G, indegree, None, parameter, None, iterations, seed_size, dataset, save_address, algorithm='DILinUCB-IC', real_mode=True)
    MainForDCUCB(G, indegree, None, parameter, None, iterations, seed_size, dataset, save_address, 0.1, times=1, real_mode=True)


