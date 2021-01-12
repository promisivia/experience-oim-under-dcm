import numpy as np
from Model.DC import runDC
from Model.Real import runReal_DC


class LinUCBStruct:
    def __init__(self, featureDimension):
        self.n = featureDimension
        self.M = np.identity(n=self.n)
        self.b = np.zeros(self.n).reshape(self.n, 1)

    def updateParameters(self, featureVector, reward):
        self.M += np.dot(featureVector, np.transpose(featureVector))
        self.b += np.dot(reward, featureVector)
        # print('---------M:', self.M, '---------b:', self.b)

    def getMInv(self):
        return np.linalg.inv(self.M)


class edge_base:
    def __init__(self, featureDimension, featureVector, alpha):
        self.n = featureDimension
        self.featureVector = featureVector
        self.rio = alpha
        self.mean = np.zeros(self.n)
        self.pta_max = 1

    # 对应算法的第6行， alpha是rio
    # 返回 U_t(e)
    def getU(self, MInv, p_hat):
        mean = np.dot(np.transpose(self.featureVector), p_hat)
        var = np.sqrt(np.dot(np.dot(np.transpose(self.featureVector), MInv), self.featureVector))
        pta = mean + self.rio * var
        return min(pta, self.pta_max)


class DCLinUCBAlgorithm:
    def __init__(self, graph, indegree, probabilities, seed_size, oracle, dimension, alpha, FeatureDic):
        self.G = graph
        self.indegree = indegree
        self.real_P = probabilities
        self.seed_size = seed_size
        self.oracle = oracle
        self.dimension = dimension
        self.alpha = alpha
        self.FeatureDic = FeatureDic
        self.p_hat = np.zeros(self.dimension)
        self.currentP = {}
        self.edge_bases = {}
        self.STRUCT = LinUCBStruct(dimension)

        for n in self.G.nodes():
            try:
                for i in range(self.indegree[n]):
                    prev = list(self.G.pred[n])[0]
                    featureVector = np.array(self.FeatureDic[(prev, n)]).reshape(dimension, 1)
                    self.edge_bases[(n, i)] = edge_base(dimension, featureVector, alpha)
                    self.currentP[(n, i)] = 1
            except:
                self.indegree[n] = 0

    def select_seed(self):
        S = self.oracle(self.G, self.currentP, self.seed_size, 20)
        # print("---------------the selected seed set is :", S)

        return S

    # 对应14行
    def simulate(self, S):
        # 需要写runDC方法
        reward, live_edges, live_nodes = runDC(self.G, self.real_P, S)
        # observed_probabilities : (node n, index i): reward
        # print("----------------simulation rewards :", reward)
        return live_edges, reward

    def runReal(self, S):
        reward, live_edges, live_nodes = runReal_DC(self.G, S)
        # print("----------------rewards under real situation:", reward)
        return live_edges, reward

    # 对应17-22，加上4-13行
    def update(self, live_edges):

        # 17-22
        # 更新观察到的每个edge_base
        for key, reward in zip(live_edges.keys(), live_edges.values()):
            node = key[0]
            index = key[1]
            self.STRUCT.updateParameters(self.edge_bases[(node, index)].featureVector, reward)

        # 4行
        self.p_hat = np.dot(self.STRUCT.getMInv(), self.STRUCT.b)
        # print("---------------current p_hat ", self.p_hat)

        # 5-13行
        for n in self.G.nodes():
            if self.indegree[n] > 0:
                self.currentP[(n, 0)] = self.edge_bases[(n, 0)].getU(self.STRUCT.getMInv(), self.p_hat)
                for i in range(self.indegree[n] - 1):
                    self.currentP[(n, i + 1)] = min(
                        self.edge_bases[(n, i + 1)].getU(self.STRUCT.getMInv(), self.p_hat),
                        self.currentP[(n, i)])
