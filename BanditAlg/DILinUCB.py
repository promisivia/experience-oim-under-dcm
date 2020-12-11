from random import random
import numpy as np
import networkx as nx


class LinUCBUserStruct:
    def __init__(self, featureDimension, userID, RankoneInverse=False):
        self.userID = userID
        self.d = featureDimension
        self.A = np.identity(n=self.d)
        self.b = np.zeros(self.d)
        self.AInv = np.linalg.inv(self.A)
        self.UserTheta = np.zeros(self.d)
        self.RankoneInverse = RankoneInverse
        self.pta_max = 1

    def updateParameters(self, updated_A, updated_b):
        self.A += updated_A
        self.b += updated_b
        self.AInv = np.linalg.inv(self.A)
        self.UserTheta = np.dot(self.AInv, self.b)

    def getTheta(self):
        return self.UserTheta

    def getA(self):
        return self.A

    def getP(self, alpha, article_FeatureVector):
        mean = np.dot(self.UserTheta, article_FeatureVector)
        var = np.sqrt(np.dot(np.dot(article_FeatureVector, self.AInv), article_FeatureVector))
        pta = mean + alpha * var
        if pta > self.pta_max:
            pta = self.pta_max
        return pta


class DILinUCBAlgorithm:
    def __init__(self, G, parameter, seed_size, oracle, alpha, feedback='edge'):
        self.G = G
        self.param = parameter
        self.node_list = list(G.nodes())
        self.oracle = oracle
        self.seed_size = seed_size
        self.dimension = len(G.nodes())
        self.alpha = alpha
        self.feedback = feedback
        self.users = []  # Nodes
        self.P = np.zeros((len(self.node_list), self.dimension))
        self.addA = np.dot(np.array(self.param), np.array(self.param).T)
        for idx, u in enumerate(self.node_list):
            self.users.append(LinUCBUserStruct(self.dimension, u))
            for v_idx in range(len(self.node_list)):
                self.P[idx, v_idx] = self.users[idx].getP(self.alpha, self.param[v_idx])

    def decide(self):
        n = len(self.node_list)
        MG = np.zeros((n, 2))
        MG[:, 0] = np.arange(n)
        influence_UCB = self.P
        np.fill_diagonal(influence_UCB, 1)
        MG[:, 1] = np.sum(influence_UCB, axis=1)

        S = []
        args = []
        temp = np.zeros(n)
        prev_spread = 0

        for k in range(self.seed_size):
            MG = MG[MG[:, 1].argsort()]

            for i in range(0, n - k - 1):
                select_node = int(MG[-1, 0])
                MG[-1, 1] = np.sum(np.maximum(influence_UCB[select_node, :], temp)) - prev_spread
                if MG[-1, 1] >= MG[-2, 1]:
                    prev_spread = prev_spread + MG[-1, 1]
                    break
                else:
                    val = MG[-1, 1]
                    idx = np.searchsorted(MG[:, 1], val)
                    MG_new = np.zeros(MG.shape)
                    MG_new[:idx, :] = MG[:idx, :]
                    MG_new[idx, :] = MG[-1, :]
                    MG_new[idx + 1:, :] = MG[idx:-1, :]
                    MG = MG_new
            args.append(int(MG[-1, 0]))
            S.append(self.node_list[int(MG[-1, 0])])
            temp = np.amax(influence_UCB[np.array(args), :], axis=0)
            MG[-1, 1] = -1

        return S

    def updateParameters(self, S, live_nodes, live_edges, _iter):
        for u in S:
            add_b = np.matmul(self.param, live_edges[u])
            u_idx = self.node_list.index(u)
            self.users[u_idx].updateParameters(self.addA, add_b)

            for v_idx in range(len(self.node_list)):
                self.P[u_idx, v_idx] = self.users[u_idx].getP(self.alpha, self.param[v_idx])
