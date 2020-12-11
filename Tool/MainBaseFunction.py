import os
import numpy as np
from conf import *
from Tool.utilFunc import *

from Model.DC import runDC

save_address = "SimulationResults\\Ex2_p=0.2\\" + alg + "-SameP\\"
isExist = os.path.exists(save_address)
if not isExist:
    os.makedirs(save_address)


class SimulateOnlineData:
    def __init__(self, G, TrueP, Prob, oracle, seed_size, iterations, dataset):
        self.tim_ = []
        self.G = G
        self.TrueP = TrueP
        self.Prob = Prob
        self.seed_size = seed_size
        self.oracle = oracle
        self.iterations = iterations
        self.dataset = dataset
        self.startTime = datetime.datetime.now()
        self.BatchCumlateReward = {}
        self.AlgReward = {}
        self.AlgLoss = {}
        self.result_oracle = []

    def runAlgorithms(self, algorithms):
        for alg_name, algorithm in list(algorithms.items()):
            self.AlgReward[alg_name] = []
            self.AlgLoss[alg_name] = []
            self.BatchCumlateReward[alg_name] = []

        self.resultRecord()
        optS = self.oracle(self.G, self.seed_size, self.TrueP)
        optimal_reward, live_edges, live_nodes = runDC(self.G, self.Prob, optS)

        self.result_oracle.append(optimal_reward)
        print('oracle', optimal_reward)
        print(optS)

        for iter_ in range(self.iterations):
            for alg_name, algorithm in list(algorithms.items()):
                S = algorithm.decide()
                print('choose set:', S)
                reward, live_edges, live_nodes = runDC(self.G, self.Prob, S)
                algorithm.updateParameters(S, live_nodes, live_edges, iter_)  # 这里会不会存储参数的更新 没有
                print(alg_name + " : " + str(reward))

                self.AlgReward[alg_name].append(reward)

                if alg_name[:2] != "DI":
                    self.AlgLoss[alg_name].append(algorithm.getLoss()[-1])

            self.resultRecord(iter_)

        # self.showResult()
        for alg_name in algorithms.keys():
            # 这里的 BatchCumlateReward 是单次运行的结果
            print('%s: %.2f' % (alg_name, np.mean(self.BatchCumlateReward[alg_name])))

    def resultRecord(self, iter_=None):
        # if initialize
        if iter_ is None:
            timeRun = self.startTime.strftime('_%m_%d_%H_%M_%S')
            fileSig = '_seedsize' + str(self.seed_size) + '_iter' + str(self.iterations) + '_' + str(
                self.oracle.__name__) + '_' + self.dataset + '_' + str(feedback_level) + "levelfeedback_" + alg
            self.filenameWriteReward = os.path.join(save_address, 'AccReward' + timeRun + fileSig + '.csv')
            with open(self.filenameWriteReward, 'w') as f:
                f.write('Time(Iteration)')
                f.write(',' + ','.join([str(alg_name) for alg_name in algorithms.keys()]))
                f.write('\n')

            # 记录误差的一范数
            if not os.path.exists(os.path.join(save_address, 'ParameterLoss')):
                os.mkdir(os.path.join(save_address, 'ParameterLoss'))
            self.filenameWriteParameterLoss = os.path.join(save_address,
                                                           'ParameterLoss\\Lossweight' + timeRun + fileSig + '.csv')

            with open(self.filenameWriteParameterLoss, 'w') as f:
                f.write('Time(Iteration)')
                f.write(',' + ','.join([str(alg_name) for alg_name in algorithms.keys()]))
                f.write('\n')
        else:
            # if run in the experiment, save the results
            print("Iteration %d" % iter_, " Elapsed time", datetime.datetime.now() - self.startTime)
            self.tim_.append(iter_)
            for alg_name in algorithms.keys():
                self.BatchCumlateReward[alg_name].append(sum(self.AlgReward[alg_name][-1:]))  # 这里只统计了最后一个数
            with open(self.filenameWriteReward, 'a+') as f:
                f.write(str(iter_))
                f.write(',' + ','.join(
                    [str(self.BatchCumlateReward[alg_name][-1]) for alg_name in algorithms.keys()]))  # 只写入了最后一个数
                f.write('\n')

            with open(self.filenameWriteParameterLoss, 'a+') as f:
                f.write(str(iter_))
                f.write(
                    ',' + ','.join([str(self.AlgLoss[alg_name][-1:]) for alg_name in algorithms.keys()]))  # 只写入了最后一个数
                f.write('\n')

    def showResult(self):
        print('average reward for oracle:', np.mean(self.result_oracle))

        f, axa = plt.subplots(1, sharex=True)
        for alg_name in algorithms.keys():
            # 这里的 BatchCumlateReward 是 单次运行的结果
            axa.plot(self.tim_, self.BatchCumlateReward[alg_name], label=alg_name)
            print('%s: %.2f' % (alg_name, np.mean(self.BatchCumlateReward[alg_name])))
        axa.legend(loc='upper left', prop={'size': 9})
        axa.set_xlabel("Iteration")
        axa.set_ylabel("Reward")
        axa.set_title("Average Reward")
        plt.savefig('./SimulationResults/AvgReward' + str(self.startTime.strftime('_%m_%d_%H_%M')) + '.pdf')
        plt.show()
        # plot accumulated reward
        f, axa = plt.subplots(1, sharex=True)
        for alg_name in algorithms.keys():
            result = [sum(self.BatchCumlateReward[alg_name][:i]) for i in range(len(self.tim_))]
            axa.plot(self.tim_, result, label=alg_name)
        axa.legend(loc='upper left', prop={'size': 9})
        axa.set_xlabel("Iteration")
        axa.set_ylabel("Reward")
        axa.set_title("Accumulated Reward")
        plt.savefig('./SimulationResults/AcuReward' + str(self.startTime.strftime('_%m_%d_%H_%M')) + '.pdf')
        plt.show()

        for alg_name in algorithms.keys():
            try:
                loss = algorithms[alg_name].getLoss()
            except:
                continue
            np.save(
                './SimulationResults/Loss-{}'.format(alg_name) + str(self.startTime.strftime('_%m_%d_%H_%M')) + '.npy',
                loss)
