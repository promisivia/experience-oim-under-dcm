from Tool.priorityQueue import PriorityQueue as PQ
from Model.IC import runIC


def Greedy(G, k, p):
    """
    Input: G -- networkx Graph object
    k -- number of initial nodes needed
    p -- propagation probability
    Output: S -- initial set of k nodes to propagate
    """
    R = 1  # number of times to run Random Cascade
    S = []  # set of selected nodes
    # add node to S if achieves maximum propagation for current chosen + this node
    for i in range(k):
        s = PQ()  # priority queue
        for v in G.nodes():
            if v not in S:
                s.add_task(v, 0)  # initialize spread value
                for j in range(R):  # run R times Random Cascade
                    [priority, count, task] = s.entry_finder[v]
                    s.add_task(v, priority - runIC(G, S + [v], p)[0] / R)  # add normalized spread value
        task, priority = s.pop_item()
        S.append(task)
    return S
