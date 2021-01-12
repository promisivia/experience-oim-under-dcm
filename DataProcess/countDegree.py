import networkx as nx
import pickle
import matplotlib.pyplot as plt

# const data
graph_address = './raw/link.txt'
action_log_address = "./processed/action_logs.txt"
save_dir = '../datasets/Flixster/'
degree = {}
fin_rating = open(action_log_address, encoding="utf8", errors='ignore')
line = fin_rating.readline()  # skip the first line
for line in fin_rating:
    data = line.split()
    u = int(data[0])
    v = int(data[1])
    try:
        degree[u] += 1
    except:
        degree[u] = 1
    try:
        degree[v] += 1
    except:
        degree[v] = 1

pickle.dump(degree, open('./processed/degree.dic', "wb"))
