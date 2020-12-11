import os
import numpy as np

from Model.Real import runReal_IC
from Model.IC import runIC, runIC_DILinUCB
from Tool.utilFunc import *
from Oracle.Greedy_IC import generalGreedy
from BanditAlg.CUCB import UCB1Algorithm as CUCB_Algorithm
from BanditAlg.UCB import UCBAlgorithm
from BanditAlg.DILinUCB import DILinUCBAlgorithm as DILinUCB_Algorithm


class SimulateOnlineData:
    def __init__(self, G, TrueP, oracle, seed_size, iterations, dataset, save_address, algorithm):
        self.tim_ = []
        self.G = G
        self.TrueP = TrueP
        self.seed_size = seed_size
        self.oracle = oracle
        self.iterations = iterations
        self.dataset = dataset
        self.startTime = datetime.datetime.now()
        self.BatchCumlateReward = {}
        self.AlgReward = {}
        self.averageReward = {}
        self.AlgLoss = {}
        self.result_oracle = []
        self.algorithm = algorithm
        self.algorithms = {}
        self.save_address = save_address

    def runAlgorithms(self, algorithms, real_mode=False):
        self.algorithms = algorithms
        for alg_name, algorithm in list(algorithms.items()):
            self.averageReward[alg_name] = []
            self.AlgReward[alg_name] = []

        self.resultRecord()

        for iter_ in range(self.iterations):
            for alg_name, algorithm in list(algorithms.items()):
                S = algorithm.decide()
                # print('choose set:', S)
                if real_mode:
                    reward, live_edges, live_nodes = runReal_IC(self.G, S)
                else:
                    if alg_name[0:2] == 'DI':
                        reward, live_edges, live_nodes = runIC_DILinUCB(self.G, self.TrueP, S)
                    else:
                        reward, live_nodes, live_edges = runIC(self.G, S, self.TrueP)
                algorithm.updateParameters(S, live_nodes, live_edges, iter_)
                # print("rewards: " + str(reward))

                self.AlgReward[alg_name].append(reward)
                # self.averageReward[alg_name].append("%.2f" % np.mean(self.AlgReward[alg_name][0:iter_ + 1]))

            self.resultRecord(iter_)

        # for alg_name in algorithms.keys():
            # print(alg_name, "  average : ", self.averageReward[alg_name][-1])

    def resultRecord(self, iter_=None):
        # if initialize
        if iter_ is None:
            timeRun = self.startTime.strftime('_%m_%d_%H_%M_%S')
            fileSig = '_seedsize' + str(self.seed_size) + '_iter' + str(self.iterations) + '_' + str(
                self.oracle.__name__) + '_' + self.dataset
            self.filenameWriteReward = os.path.join(self.save_address, self.algorithm + timeRun + fileSig + '.csv')
            with open(self.filenameWriteReward, 'w') as f:
                f.write('Time(Iteration)')
                f.write(',' + ','.join([str(alg_name) for alg_name in self.algorithms.keys()]))
                f.write('\n')

        else:
            # if run in the experiment, save the results
            with open(self.filenameWriteReward, 'a+') as f:
                f.write(str(iter_))
                f.write(',' + ','.join([str(self.AlgReward[alg_name][-1]) for alg_name in self.algorithms.keys()]))
                f.write('\n')


def MainForIC(G, indegree, probability, parameter, feature_dic, iterations, seed_size, dataset,
              save_address_prefix, algorithm, real_mode=False, times = 10):
    save_address = save_address_prefix + algorithm
    if not os.path.exists(save_address):
        os.makedirs(save_address)

    for (u, v) in G.edges():
        G[u][v]['weight'] = 1

    x = 1
    while x <= times:
        algorithms = {}
        experiments = SimulateOnlineData(G, probability, generalGreedy, seed_size, iterations, dataset, save_address, algorithm)
        if algorithm == 'UCB':
            algorithms[algorithm] = UCBAlgorithm(G, probability, seed_size)
        elif algorithm == 'CUCB':
            algorithms[algorithm] = CUCB_Algorithm(G, probability, seed_size, generalGreedy)
        elif algorithm[:2] == 'DI':
            DILinUCB_parameter = np.array(list(parameter.values()))[:, 0, :]
            algorithms[algorithm] = DILinUCB_Algorithm(G, DILinUCB_parameter, seed_size, generalGreedy, 0.1)
        experiments.runAlgorithms(algorithms, real_mode)
        x += 1
