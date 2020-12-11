from copy import deepcopy
from random import random
import networkx as nx
import numpy as np


# 跑 SameP 模型，返回根据 seed set生成的 observed set 和 被激活的节点数
def runDC(G, P, S):
    """
    Input: G -- networkx graph object
    S -- initial set of vertices
    p -- propagation probability
    Output: T -- resulted influenced set of vertices (including S)
    """
    # 记录与每个 T 相关的尝试激活它的节点个数
    T_node = {}

    for v in G.nodes():
        T_node[v] = 0

    T = deepcopy(S)  # copy already selected nodes
    E = {}

    i = 0
    while i < len(T):
        for v in G[T[i]]:
            if v not in T:  # if it wasn't selected yet
                # T[i]尝试去激活节点 v
                weight = P[(v, T_node[v])]
                # 激活成功
                if random() <= weight:
                    T.append(v)
                    E[(v, T_node[v])] = 1
                else:
                    E[(v, T_node[v])] = 0
                T_node[v] += 1
        i += 1
    reward = len(T)
    # T 最后被激活的节点
    # len(T) 最后被激活的节点个数
    return reward, E, T


def runDC_DILinUCB(G, P, S):
    """
    Input: G -- networkx graph object
    S -- initial set of vertices
    p -- propagation probability
    Output: T -- resulted influenced set of vertices (including S)
    """
    T_node = {}  # 记录与每个 T 相关的尝试激活它的节点个数
    T = deepcopy(S)  # copy already selected nodes
    E = {}
    Active = nx.Graph()  # 如果一条边被激活了，就存在G中

    for v in G.nodes():
        T_node[v] = 0
        E[v] = [0] * len(G.nodes())

    i = 0
    while i < len(T):
        for v in G[T[i]]:
            if v not in T:  # 对所有不在T中的 T[i]的邻居v
                # T[i]尝试去激活节点 v
                weight = P[(v, T_node[v])]
                # 激活成功
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

    # T 最后被激活的节点
    # len(T) 最后被激活的节点个数
    return reward, E, T


# 返回对应的图和相应 seed set 的 reward
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
