import random
import numpy as np
from Model.DC import runDC
from Model.Real import runReal_DC
from random import randrange


class node_base:
    def __init__(self, number_of_observations, total_reward, empirical_mean):
        self.observations = number_of_observations
        self.mean = empirical_mean
        self.total_reward = total_reward
        self.p_max = 1

    def updateNode(self, myReward):
        self.total_reward += myReward
        self.observations += 1
        self.mean = self.total_reward / float(self.observations)

    def get_upper_estimation(self, all_rounds):
        if self.observations == 0:
            return 1
        else:
            upper_p = self.mean + 0.1 * np.sqrt(
                3 * np.log(all_rounds) / (2.0 * self.observations))
            if upper_p > self.p_max:
                upper_p = self.p_max
            return upper_p


class CMAB_random_alg:
    def __init__(self, graph, indegree, probabilities, seed_size, oracle):
        self.G = graph
        self.real_P = probabilities
        self.seed_size = seed_size
        self.oracle = oracle
        self.all_rounds = 0
        self.currentP = {}
        self.indegree = indegree
        self.node_bases = {}

        for n in self.G.nodes():
            self.node_bases[n] = node_base(0, 0, 0)
            self.currentP[n] = self.node_bases[n].get_upper_estimation(self.all_rounds)

    def select_seed(self):
        # use oracle to select
        self.all_rounds += 1

        # estimate the upper probability
        for n in self.G.nodes():
            self.currentP[n] = self.node_bases[n].get_upper_estimation(self.all_rounds)

        # S consists of 2 largest nodes
        S = self.oracle(self.currentP, self.seed_size)
        return S

    def simulate(self, S):
        reward, live_edges, live_nodes = runDC(self.G, self.real_P, S)
        return live_edges, reward

    def runReal(self, S):
        reward, live_edges, live_nodes = runReal_DC(self.G, S)
        return live_edges, reward

    def update(self, S, reward):
        random_index = randrange(0, len(S))
        node = S[random_index]
        self.node_bases[node].updateNode(reward / (len(self.G.nodes)))

