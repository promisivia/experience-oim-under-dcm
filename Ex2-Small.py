from Tool.utilFunc import *
from RunTools.MainForCMAB import MainForCMAB
from RunTools.MainForDC import MainForDC
from RunTools.MainForIC import MainForIC
from RunTools.MainForDCUCB import MainForDCUCB

# data
seed_size = 2
iterations = 10000
dataset_list = ['Small1', 'Small2']  # dataset_list = [, 'NetHEPT']
prob_list = [0.5, 0.8, 0.2]  # prob_list = [0.2, 0.5, 0.8]

if __name__ == '__main__':
    for i in range(10):
        for dataset in dataset_list:
            for prob in prob_list:
                save_address = "SimulationResults/Ex1/" + dataset + "_" + str(prob) + "_10000/"

                G = pickle.load(open('datasets/' + dataset + '/graph.G', 'rb'), encoding='latin1')
                indegree = pickle.load(open('datasets/' + dataset + '/indegree.dic', 'rb'), encoding='latin1')
                P = pickle.load(open('datasets/' + dataset + '/' + str(prob) + '-Probability.dic', 'rb'), encoding='latin1')
                parameter = pickle.load(open('datasets/' + dataset + '/nodeFeatures.dic', 'rb'), encoding='latin1')

                IC_P = {}
                for (node, index) in P:
                    IC_P[(list(G.pred[node])[index], node)] = P[(node, index)]

                # MainForCMAB(G, indegree, P_DC, None, None, iterations, seed_size, dataset, save_address, times=1)
                # MainForIC(G, indegree, P, parameter, None, iterations, seed_size, dataset, save_address, algorithm='DILinUCB-IC', times=1)
                # MainForDC(G, indegree, P_DC, parameter, None, iterations, seed_size, dataset, save_address, algorithm='DILinUCB-DC', times=1)
                MainForIC(G, indegree, IC_P, parameter, None, iterations, seed_size, dataset, save_address, algorithm='CUCB', times=1)
                # MainForDCUCB(G, indegree, P_DC, None, None, iterations, seed_size, dataset, save_address, 0.1, times=1)
                MainForIC(G, indegree, IC_P, parameter, None, iterations, seed_size, dataset, save_address, algorithm='IMFB', times=1)
