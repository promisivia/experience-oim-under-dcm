import networkx as nx
import pickle
import matplotlib.pyplot as plt

# const data
graph_address = './raw/link.txt'
action_log_address = "./processed/action_logs.txt"
save_dir = '../datasets/Flixster-v4/'

ID_COUNT = 20
INTERVAL = 365
TOTAL_DAY = 1052  # 1052@Flixster 1955@LastFM


def movieToSetId(movie):
    return movie % ID_COUNT


def have_activation(set1, set2):
    count = 0
    for t1 in set1:
        for t2 in set2:
            t1 = int(t1)
            t2 = int(t2)
            if t1 - t2 <= INTERVAL or t2 - t1 <= INTERVAL:
                count += 1
            if t1 < INTERVAL and t1 + TOTAL_DAY - t2 <= INTERVAL:
                count += 1
            if t2 < INTERVAL and t2 + TOTAL_DAY - t1 <= INTERVAL:
                count += 1
    return count


# prepare movie set and user to time:
user_movie_id_set = {}
user_movie_time = {}

fin_rating = open(action_log_address, encoding="utf8", errors='ignore')
line = fin_rating.readline()  # skip the first line
for line in fin_rating:
    arr = line.split()
    user = int(arr[0])
    movie_set_id = movieToSetId(int(arr[1]))
    time = int(arr[2])

    try:
        user_movie_id_set[user].add(movie_set_id)
    except:
        user_movie_id_set[user] = set()
        user_movie_id_set[user].add(movie_set_id)

    try:
        user_movie_time[(user, movie_set_id)].add(time)
    except:
        user_movie_time[(user, movie_set_id)] = set()
        user_movie_time[(user, movie_set_id)].add(time)

fin_rating.close()
print("Finish finding the movie set and user to time")

# find graph with edge active
# degree = pickle.load(open('./processed/degree.dic', 'rb'))
G = nx.Graph()
degree = {}
with open(graph_address) as f:
    for line in f:
        data = line.split()
        u = int(data[0])
        v = int(data[1])

        try:
            u_set = user_movie_id_set[u]
            v_set = user_movie_id_set[v]
        except:
            continue

        try:
            degree[u] += 1
        except:
            degree[u] = 1
        try:
            degree[v] += 1
        except:
            degree[v] = 1

        set = u_set & v_set
        for movie_id in set:
            u_time_set = user_movie_time[(u, movie_id)]
            v_time_set = user_movie_time[(v, movie_id)]

            if have_activation(u_time_set, v_time_set) > 20:
                G.add_edge(u, v)
                continue

f.close()
print("G size : ", len(G.nodes()), len(G.edges()))

newG = nx.Graph()
for (u, v) in G.edges():
    if degree[u] > 20 and degree[v] > 20:
        newG.add_edge(u, v)
print("newG size : ", len(newG.nodes()), len(newG.edges()))


# find max component
component = max(nx.connected_components(newG), key=len)
Gc = newG.subgraph(component).copy()
print("max component size : ", len(Gc.nodes()), len(Gc.edges()))

nodes = Gc.nodes()

finalG = nx.DiGraph()
with open(graph_address) as f:
    for line in f:
        data = line.split()
        u = int(data[0])
        v = int(data[1])
        if u in nodes and v in nodes:
            finalG.add_edge(u, v)
            finalG.add_edge(v, u)

f.close()

print("Finish finding the max component")
print("final size : ", len(finalG.nodes()), len(finalG.edges()))
nx.draw(finalG)
plt.show()
pickle.dump(finalG, open(save_dir + 'graph.G', "wb"))

#######################################
# G size :  4194 3605
# newG size :  404 370
# max component size :  204 210
# Finish finding the max component
# final size :  204 938
########################################
