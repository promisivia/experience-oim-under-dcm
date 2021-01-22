from copy import deepcopy
from random import random
import networkx as nx
import numpy as np


def runDC(G, P, S):
    """
    Input: G -- networkx graph object
    S -- initial set of vertices
    p -- propagation probability
    Output: T -- resulted influenced set of vertices (including S)
    """
    T_node = {}

    for v in G.nodes():
        T_node[v] = 0

    T = deepcopy(S)  # copy already selected nodes
    E = {}

    i = 0
    while i < len(T):
        for v in G[T[i]]:
            if v not in T:  # if it wasn't selected yet
                # T[i] attempts to activate node v
                weight = P[(v, T_node[v])]
                if random() <= weight:
                    T.append(v)
                    E[(v, T_node[v])] = 1
                else:
                    E[(v, T_node[v])] = 0
                T_node[v] += 1
        i += 1
    reward = len(T)
    return reward, E, T


def runDC_DILinUCB(G, P, S):
    """
    Input: G -- networkx graph object
    S -- initial set of vertices
    p -- propagation probability
    Output: T -- resulted influenced set of vertices (including S)
    """
    T_node = {}  # record count of node try to active node v
    T = deepcopy(S)  # copy already selected nodes
    E = {}
    Active = nx.Graph()

    for v in G.nodes():
        T_node[v] = 0
        E[v] = [0] * len(G.nodes())

    i = 0
    while i < len(T):
        for v in G[T[i]]:
            if v not in T:
                # T[i] attempts to activate node v
                weight = P[(v, T_node[v])]
                if random() <= weight:
                    Active.add_edge(T[i], v)
                    T.append(v)
                T_node[v] += 1
        i += 1
    reward = len(T)

    for u in S:
        for (idx, v) in enumerate(G.nodes()):
            try:
                if nx.has_path(Active, u, v):
                    E[u][idx] = 1
            except:
                E[u][idx] = 0

    return reward, E, T


def runDC_getReward(graph, real_P, seed_set, iterations):
    rewards = []
    for j in range(iterations):
        rewards.append(0)

        # Each node is associated with a number of attempts to activate
        T_node = {}

        for v in graph.nodes():
            T_node[v] = 0

        T = deepcopy(seed_set)

        i = 0
        while i < len(T):
            # T[i] attempts to activate node v
            for v in graph[T[i]]:
                if v not in T:
                    # active success
                    if random() <= real_P[(v, T_node[v])]:
                        T.append(v)
                    T_node[v] += 1
            i += 1
        rewards[j] = len(T)

    return np.mean(rewards)
