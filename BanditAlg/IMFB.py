import numpy as np
import networkx as nx
import random


class MFUserStruct:
    def __init__(self, dimension, userID):
        self.userID = userID
        self.dim = dimension
        self.A = np.identity(n=self.dim)
        self.C = np.identity(n=self.dim)
        self.b = np.array([random.random() for i in range(self.dim)])
        self.d = np.array([random.random() for i in range(self.dim)])
        self.AInv = np.linalg.inv(self.A)
        self.CInv = np.linalg.inv(self.C)
        self.theta_out = np.dot(self.AInv, self.b)
        self.beta_in = np.dot(self.CInv, self.d)

    def updateOut(self, articlePicked_FeatureVector, click):
        self.A += np.outer(articlePicked_FeatureVector, articlePicked_FeatureVector)
        self.b += articlePicked_FeatureVector * click
        self.AInv = np.linalg.inv(self.A)
        self.theta_out = np.dot(self.AInv, self.b)

    def updateIn(self, articlePicked_FeatureVector, click):
        self.C += np.outer(articlePicked_FeatureVector, articlePicked_FeatureVector)
        self.d += articlePicked_FeatureVector * click
        self.CInv = np.linalg.inv(self.C)
        self.beta_in = np.dot(self.CInv, self.d)


class MFAlgorithm:
    def __init__(self, G, P, parameter, seed_size, oracle, dimension, feedback='edge'):
        self.G = G
        self.trueP = P
        self.parameter = parameter
        self.oracle = oracle
        self.seed_size = seed_size
        self.q = 0.25
        self.plus = (1 + self.q) / (1 - self.q)
        self.dimension = dimension
        self.feedback = feedback
        self.list_loss = []
        self.currentP = nx.DiGraph()
        self.users = {}  # Nodes
        for u in self.G.nodes():
            self.users[u] = MFUserStruct(dimension, u)
            for v in self.G[u]:
                self.currentP.add_edge(u, v, weight=random.random())

    def decide(self):
        S = self.oracle(self.G, self.seed_size, self.currentP)
        return S

    def updateParameters(self, S, live_nodes, live_edges, it):
        for node in live_nodes:
            for (u, v) in self.G.edges(node):
                if (u, v) in live_edges:
                    reward = live_edges[(u, v)]
                else:
                    reward = 0
                self.users[u].updateOut(self.users[v].beta_in, reward)
                self.users[v].updateIn(self.users[u].theta_out, reward)
                self.currentP[u][v]['weight'] = self.getP(self.users[u], self.users[v], it)

    def getP(self, u, v, it):
        alpha_1 = 0.1
        alpha_2 = 0.1
        CB = alpha_1 * np.dot(np.dot(v.beta_in, u.AInv), v.beta_in) + alpha_2 * np.dot(np.dot(u.theta_out, v.CInv), u.theta_out)
        prob = np.dot(u.theta_out, v.beta_in) + CB + 2 * np.power(self.q, it)  # 4???
        if prob > 1:
            prob = 1
        if prob < 0:
            prob = 0
        return prob

    def getLoss(self):
        return np.asarray(self.list_loss)
