import os
import numpy as np
from Model.Real import runReal_DC
from Tool.utilFunc import *
from BanditAlg.DILinUCB import DILinUCBAlgorithm as DILinUCB_Algorithm
from BanditAlg.UCB import UCBAlgorithm
from Model.DC import runDC, runDC_DILinUCB
from Oracle.Greedy import Greedy


class SimulateOnlineData:
    def __init__(self, G, Prob, oracle, seed_size, iterations, dataset, save_address, algorithm):
        self.tim_ = []
        self.G = G
        self.Prob = Prob
        self.seed_size = seed_size
        self.oracle = oracle
        self.iterations = iterations
        self.dataset = dataset
        self.startTime = datetime.datetime.now()
        self.averageReward = {}
        self.AlgReward = {}
        self.AlgLoss = {}
        self.result_oracle = []
        self.algorithm = algorithm
        self.algorithms = {}
        self.save_address = save_address

    def runAlgorithms(self, algorithms, real_mode=False):
        self.algorithms = algorithms

        for alg_name, alg in list(algorithms.items()):
            self.AlgReward[alg_name] = []
            self.averageReward[alg_name] = []

        self.resultRecord()

        for iter_ in range(self.iterations):
            for alg_name, algorithm in list(algorithms.items()):
                S = algorithm.decide()
                # print("----------the ", iter_ + 1, "  round---------")
                # print('choose set:', S)
                if real_mode:
                    reward, live_edges, live_nodes = runReal_DC(self.G, S)
                else:
                    if alg_name[:2] == 'DI':
                        reward, live_edges, live_nodes = runDC_DILinUCB(self.G, self.Prob, S)
                    else:
                        reward, live_edges, live_nodes = runDC(self.G, self.Prob, S)
                algorithm.updateParameters(S, live_nodes, live_edges, iter_)
                print("rewards: " + str(reward))

                self.AlgReward[alg_name].append(reward)
                # self.averageReward[alg_name].append("%.2f" % np.mean(self.AlgReward[alg_name][0:iter_ + 1]))

            self.resultRecord(iter_)

            # for alg_name in algorithms.keys():
            #     print("average : ", self.averageReward[alg_name][-1])

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


def MainForDC(G, i, prob, parameter, f, iterations, seed_size, dataset, save_address_prefix, algorithm, times=10, real_mode=False):
    save_address = save_address_prefix + algorithm
    if not os.path.exists(save_address):
        os.makedirs(save_address)

    for (u, v) in G.edges():
        G[u][v]['weight'] = 1

    x = 1
    while x <= times:
        simExperiment = SimulateOnlineData(G, prob, Greedy, seed_size, iterations, dataset, save_address, algorithm)
        algorithms = {}

        if algorithm == 'UCB':
            algorithms[algorithm] = UCBAlgorithm(G, prob, seed_size)
        elif algorithm[:2] == 'DI':
            DILinUCB_parameter = np.array(list(parameter.values()))[:, 0, :]
            algorithms[algorithm] = DILinUCB_Algorithm(G, DILinUCB_parameter, seed_size, Greedy, 0.1)
        simExperiment.runAlgorithms(algorithms, real_mode)

        x += 1
