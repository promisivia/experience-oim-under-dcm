from Tool.utilFunc import *
from RunTools.MainForIC import MainForIC

seed_size = 2
iterations = 10000
dataset_list = ['Small1', 'Small2']
scale_list = ['0.2', '0.5', '0.8']

if __name__ == '__main__':
    for i in range(10):
        for dataset in dataset_list:
            for scale in scale_list:
                save_address = 'SimulationResults/Ex1/' + dataset + '_' + scale + '/'

                G = pickle.load(open('datasets/' + dataset + '/graph.G', 'rb'), encoding='latin1')
                indegree = pickle.load(open('datasets/' + dataset + '/indegree.dic', 'rb'), encoding='latin1')
                P_DC = pickle.load(open('datasets/' + dataset + '/' + scale + '-Probability.dic', 'rb'), encoding='latin1')
                P_IC = pickle.load(open('datasets/' + dataset + '/' + scale + '-IC-Probability.dic', 'rb'), encoding='latin1')
                parameter = pickle.load(open('datasets/' + dataset + '/nodeFeatures.dic', 'rb'), encoding='latin1')
                feature_dic = pickle.load(open('datasets/' + dataset + '/random-edgeFeatures.dic', 'rb'), encoding='latin1')

                MainForIC(G, indegree, P_IC, parameter, None, iterations, seed_size, dataset, save_address, algorithm='IMFB', times=1)
                MainForIC(G, indegree, P_IC, parameter, None, iterations, seed_size, dataset, save_address, algorithm='CUCB', times=1)