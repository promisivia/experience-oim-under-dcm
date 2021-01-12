from Tool.utilFunc import *
from RunTools.MainForCMAB import MainForCMAB
from RunTools.MainForDC import MainForDC
from RunTools.MainForDCUCB import MainForDCUCB

seed_size = 2
iterations = 10000
dataset_list = ['Small1']
scale_list = ['0.2']

if __name__ == '__main__':
    for i in range(20):
        for dataset in dataset_list:
            for scale in scale_list:
                save_address = 'SimulationResults/Ex1/' + dataset + '_' + scale + '_' + str(iterations) + '/'

                G = pickle.load(open('datasets/' + dataset + '/graph.G', 'rb'), encoding='latin1')
                indegree = pickle.load(open('datasets/' + dataset + '/indegree.dic', 'rb'), encoding='latin1')
                P = pickle.load(open('datasets/' + dataset + '/' + scale + '-Probability.dic', 'rb'), encoding='latin1')
                parameter = pickle.load(open('datasets/' + dataset + '/nodeFeatures.dic', 'rb'), encoding='latin1')
                feature_dic = pickle.load(open('datasets/' + dataset + '/edgeFeatures.dic', 'rb'), encoding='latin1')

                MainForDC(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address, algorithm='UCB', times=1)
                MainForCMAB(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address, times=1)
                MainForDC(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address, algorithm='DILinUCB-DC', times=1)
                MainForDCUCB(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address, 0.1, times=1)
