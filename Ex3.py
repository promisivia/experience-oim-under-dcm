from RunTools.MainForDC import MainForDC
from Tool.utilFunc import *
from RunTools.MainForCMAB import MainForCMAB
from RunTools.MainForDCUCB import MainForDCUCB, MainForDCLinUCB

# data
dataset_list = ['Flickr']  # dataset_list = ['Flickr', 'NetHEPT']
kind_list = ['same']  # kind_list = ['same', 'random']  # same or random
seed_size = 5
iterations = 10000

if __name__ == '__main__':
    for dataset in dataset_list:
        for kind in kind_list:
            save_address = 'SimulationResults/Ex3/' + dataset + '-' + kind + '/'

            G = pickle.load(open('datasets/' + dataset + '/graph.G', 'rb'), encoding='latin1')
            indegree = pickle.load(open('datasets/' + dataset + '/indegree.dic', 'rb'), encoding='latin1')
            P = pickle.load(open('datasets/' + dataset + '/' + kind + '-Probability.dic', 'rb'), encoding='latin1')
            parameter = pickle.load(open('datasets/' + dataset + '/nodeFeatures.dic', 'rb'), encoding='latin1')
            feature_dic = pickle.load(open('datasets/' + dataset + '/' + kind + '-edgeFeatures.dic', 'rb'), encoding='latin1')

            MainForCMAB(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address)
            MainForDC(G, indegree, P, parameter, None, iterations, seed_size, dataset, save_address, algorithm='DILinUCB-DC')
            MainForDCUCB(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address, 0.1)
            MainForDCLinUCB(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address)
