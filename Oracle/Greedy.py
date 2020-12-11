from Model.DC import runDC_getReward


def Greedy(graph, probability, seed_size, iterations):
    S = []
    # 每次选择一个结点
    for i in range(seed_size):
        influence = dict()  # influence for nodes not in S # 影响不在S中的结点

        for v in graph.nodes():
            if v not in S:
                influence[v] = runDC_getReward(graph, probability, S + [v], iterations)
                # print("test node ",v,"influence margin is", influence[v])

        u, val = max(iter(influence.items()), key=lambda k_v: k_v[1])
        # print("select node ",u)
        S.append(u)

    # print("select seed set", S)

    return S
