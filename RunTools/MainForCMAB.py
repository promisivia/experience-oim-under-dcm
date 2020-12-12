import os
import datetime
import numpy as np
from BanditAlg.CMAB_average import CMAB_average_alg
from BanditAlg.CMAB_random import CMAB_random_alg
from Oracle.CMAB import CMAB_max


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
                print("--------------the ", i + 1, " round---------------")
                S = alg.select_seed()
                if not real_mode:
                    observed_probabilities, reward = alg.simulate(S)
                else:
                    observed_probabilities, reward = alg.runReal(S)
                alg.update(S, reward)
                self.AlgReward[alg_name].append(reward)
                self.averageReward[alg_name].append("%.2f" % np.mean(self.AlgReward[alg_name][0:i + 1]))

            self.resultRecord(i)

            for alg_name in algorithms.keys():
                print("average : ", self.averageReward[alg_name][-1])

    def resultRecord(self, iter_=None):
        # if initialize
        if iter_ is None:
            timeRun = self.startTime.strftime('_%m_%d_%H_%M_%S')
            fileSig = '_seedsize' + str(self.seed_size) + '_iter' + str(self.iterations) + '_' + self.dataset
            self.filenameWriteReward = os.path.join(self.save_address, str(list(self.algorithms.keys())[0]) + timeRun + fileSig + '.csv')
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


def MainForCMAB(G, indegree, prob, parameter, feature_dic, T, seed_size, dataset, save_address_prefix, times=10, real_mode=False):
    if not os.path.exists(save_address_prefix + "CMAB-average"):
        os.makedirs(save_address_prefix + "CMAB-average")

    if not os.path.exists(save_address_prefix + "CMAB-random"):
        os.makedirs(save_address_prefix + "CMAB-random")

    x = 1
    while x <= times:
        algorithms = {}
        experiments = simulation(seed_size, T, dataset, save_address_prefix + "CMAB-average")
        algorithms["CMAB_average"] = CMAB_average_alg(G, indegree, prob, seed_size, CMAB_max, 0.1)
        experiments.runAlgorithms(algorithms, real_mode)

        algorithms = {}
        experiments = simulation(seed_size, T, dataset, save_address_prefix + "CMAB-random")
        algorithms["CMAB_random"] = CMAB_random_alg(G, indegree, prob, seed_size, CMAB_max)
        experiments.runAlgorithms(algorithms, real_mode)

        x += 1
