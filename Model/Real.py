from copy import deepcopy
from random import choice
import pickle
import networkx as nx

TOTAL_DAY = 1000
INTERVAL = 90
file_address = "DataProcess/processed/"
user_time_set = pickle.load(open(file_address + "userTimeSet.dic", 'rb'))
user_time_to_movie = pickle.load(open(file_address + "userAndTimeToMovie.dic", 'rb'))
user_first_day = {}


def movieToSetId(movie):
    return movie % 20


def get_movie_id(user, day):
    movie = user_time_to_movie.get((user, day))
    if movie is None:
        return None
    else:
        return movieToSetId(movie)  # the movie ID user see today


def runReal_IC(G, S):
    T = deepcopy(S)  # copy already selected nodes
    E = {}

    # randomly choose a day that user v has see a movie
    for v in S:
        time = int(choice(list(user_time_set[v])))
        user_first_day[v] = time

    # for every seed in seed set
    i = 0
    while i < len(T):
        user = T[i]
        first_day = user_first_day[user]  # the day it is added to the seed set
        user_movie_id = get_movie_id(user, first_day)  # the movie ID user see today

        # for its neighbours
        for nei in G[user]:
            if nei not in T:
                # see what v influence in 100 days from the day it is added to the set
                for day in range(first_day, first_day + INTERVAL + 1):
                    day = day % TOTAL_DAY
                    nei_movie_id = get_movie_id(nei, day)
                    if nei_movie_id is not None:
                        if nei_movie_id == user_movie_id:
                            E[(user, nei)] = 1
                            T.append(nei)
                            user_first_day[nei] = day
                        else:
                            E[(user, nei)] = 0
            else:  # for ic full, should also influence but there is not effect
                E[(user, nei)] = 0

        i += 1

    reward = len(T)
    return reward, E, T


def runReal_DILinUCB(G, S):
    T = deepcopy(S)  # copy already selected nodes
    E = {}
    Active = nx.Graph()  # store all the active edge, find path then
    for v in G.nodes():
        E[v] = [0] * len(G.nodes())

    # randomly choose a day that user v has see a movie
    for v in S:
        time = int(choice(list(user_time_set[v])))
        user_first_day[v] = time

    # for every seed in seed set
    i = 0
    while i < len(T):
        user = T[i]
        first_day = user_first_day[user]  # the day it is added to the seed set
        user_movie_id = get_movie_id(user, first_day)  # the movie ID user see today

        # for its neighbours
        for nei in G[user]:
            if nei not in T:
                # see what v influence in 100 days from the day it is added to the set
                for day in range(first_day, first_day + INTERVAL + 1):
                    day = day % TOTAL_DAY
                    nei_movie_id = get_movie_id(nei, day)
                    if nei_movie_id is not None:
                        if nei_movie_id == user_movie_id:
                            Active.add_edge(user, nei)
                            T.append(nei)
                            user_first_day[nei] = day
        i += 1

    for u in S:
        for (idx, v) in enumerate(G.nodes()):
            try:
                if nx.has_path(Active, u, v):
                    E[u][idx] = 1
            except:
                E[u][idx] = 0

    reward = len(T)
    return reward, E, T


def runReal_DC(G, S):
    T_node = {}  # record the count of nodes trying to active v
    T = deepcopy(S)  # copy already selected nodes
    E = {}

    for v in G.nodes():
        T_node[v] = 0

    for v in S:
        time = int(choice(list(user_time_set[v])))
        user_first_day[v] = time

    # for every seed in seed set
    i = 0
    while i < len(T):
        user = T[i]
        first_day = user_first_day[user]  # the day it is added to the seed set
        user_movie_id = get_movie_id(user, first_day)  # the movie ID user see today

        # for its neighbours
        for nei in G[user]:
            if nei not in T:
                # see what v influence in 100 days from the day it is added to the set
                for day in range(first_day, first_day + INTERVAL + 1):
                    day = day % INTERVAL
                    nei_movie_id = get_movie_id(nei, day)
                    if nei_movie_id is not None:
                        if nei_movie_id == user_movie_id:
                            E[(nei, T_node[nei])] = 1
                            T.append(nei)
                            user_first_day[nei] = day
                        else:
                            E[(nei, T_node[nei])] = 0
        i += 1

    reward = len(T)
    return reward, E, T
