import os
import datetime
from BanditAlg.DCUCB import DC_UCB_alg
from BanditAlg.DCLinUCB import DCLinUCBAlgorithm as DCLinUCB
from Oracle.Greedy import Greedy
import numpy as np


class simulation:
    def __init__(self, seed_size, iterations, dataset, save_address):
        self.dataset = dataset
        self.seed_size = seed_size
        self.iterations = iterations
        self.save_address = save_address
        self.startTime = datetime.datetime.now()
        self.algorithms = {}
        self.averageReward = {}
        self.AlgReward = {}
        self.optimal_reward = []

    def runAlgorithms(self, algorithms, real_mode=False):
        self.algorithms = algorithms
        for alg_name, alg in list(algorithms.items()):
            self.AlgReward[alg_name] = []
            self.averageReward[alg_name] = []

        self.resultRecord()

        for i in range(self.iterations):

            for alg_name, alg in list(algorithms.items()):
                # print("----------the ", i + 1, "  round---------")
                S = alg.select_seed()
                # print('choose set:', S)
                if not real_mode:
                    observed_probabilities, reward = alg.simulate(S)
                else:
                    observed_probabilities, reward = alg.runReal(S)
                alg.update(observed_probabilities)
                self.AlgReward[alg_name].append(reward)
                self.averageReward[alg_name].append("%.2f" % np.mean(self.AlgReward[alg_name][0:i + 1]))

                # print("rewards: " + str(reward))
            self.resultRecord(i)

            # for alg_name in algorithms.keys():
                # print("average : ", self.averageReward[alg_name][-1])

    def resultRecord(self, iter_=None):
        # if initialize
        if iter_ is None:
            timeRun = self.startTime.strftime('_%m_%d_%H_%M_%S')
            fileSig = self.dataset + '_iter' + str(self.iterations) + '_seedsize' + str(self.seed_size)
            self.filenameWriteReward = os.path.join(self.save_address,
                                                    'radius0.1' + timeRun + fileSig + '.csv')

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


def MainForDCUCB(G, indegree, probability, parameter, feature_dic, iterations, seed_size, dataset, save_address_prefix,
                 radius, times=10, real_mode=False):
    save_address = save_address_prefix + "DC-UCB-radius" + str(radius)
    if not os.path.exists(save_address):
        os.makedirs(save_address)

    x = 1
    while x <= times:
        algorithms = {}
        experiments = simulation(seed_size, iterations, dataset, save_address)
        algorithms["DC-UCB"] = DC_UCB_alg(G, indegree, probability, seed_size, Greedy, radius)
        experiments.runAlgorithms(algorithms, real_mode)
        x += 1


def MainForDCLinUCB(G, indegree, probability, parameter, feature_dic, iterations, seed_size, dataset, save_address_prefix, times=10, dimension=5, real_mode=False):
    save_address = save_address_prefix + "DCLinUCB"
    if not os.path.exists(save_address):
        os.makedirs(save_address)
    x = 1
    while x <= times:
        algorithms = {}
        experiments = simulation(seed_size, iterations, dataset, save_address)
        algorithms["DC-LinUCB"] = DCLinUCB(G, indegree, probability, seed_size, Greedy, dimension, 0.1, feature_dic)
        experiments.runAlgorithms(algorithms, real_mode)
        x += 1
