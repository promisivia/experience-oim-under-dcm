from Tool.utilFunc import *
from RunTools.MainForCMAB import MainForCMAB
from RunTools.MainForDC import MainForDC
from RunTools.MainForIC import MainForIC
from RunTools.MainForDCUCB import MainForDCUCB

# data
seed_size = 5
iterations = 10000
dataset_list = ['NetHEPT']  # dataset_list = ['Flickr','NetHEPT' ]
prob_list = [0.8]  # prob_list = [0.2, 0.5, 0.8]

if __name__ == '__main__':
    for i in range(10):
        for dataset in dataset_list:
            for prob in prob_list:
                save_address = "SimulationResults/Ex2/" + dataset + "_p=" + str(prob) + "/"

                G = pickle.load(open('datasets/SameP/' + dataset + '/graph.G', 'rb'), encoding='latin1')
                indegree = pickle.load(open('datasets/SameP/' + dataset + '/indegree.dic', 'rb'), encoding='latin1')
                P = pickle.load(open('datasets/SameP/' + dataset + '/' + str(prob) + 'Probability.dic', 'rb'), encoding='latin1')
                P_DC = pickle.load(open('datasets/SameP/' + dataset + '/' + str(prob) + 'DC_Probability.dic', 'rb'), encoding='latin1')
                parameter = pickle.load(open('datasets/SameP/' + dataset + '/nodeFeatures.dic', 'rb'), encoding='latin1')
                feature_dic = pickle.load(open('datasets/' + dataset + '/' + 'random-edgeFeatures.dic', 'rb'), encoding='latin1')

                MainForCMAB(G, indegree, P_DC, None, None, iterations, seed_size, dataset, save_address, times=1)
                MainForIC(G, indegree, P, parameter, None, iterations, seed_size, dataset, save_address, algorithm='DILinUCB-IC', times=1)
                MainForDC(G, indegree, P_DC, parameter, None, iterations, seed_size, dataset, save_address, algorithm='DILinUCB-DC', times=1)
                MainForIC(G, indegree, P, parameter, None, iterations, seed_size, dataset, save_address, algorithm='CUCB', times=2)
                MainForDCUCB(G, indegree, P_DC, None, None, iterations, seed_size, dataset, save_address, 0.1, times=1)
                MainForIC(G, indegree, P, parameter, None, iterations, seed_size, dataset, save_address, algorithm='IMFB', times=1)
                MainForIC(G, indegree, P, parameter, feature_dic, iterations, seed_size, dataset, save_address, algorithm='IMLinUCB', times=1)
