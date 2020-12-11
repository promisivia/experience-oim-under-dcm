from copy import deepcopy
from random import choice
import pickle

file_address = "DataProcess/processed/"
user_time_set = pickle.load(open(file_address + "userTimeSet.dic", 'rb'))
user_time_to_movie = pickle.load(open(file_address + "userAndTimeToMovie.dic", 'rb'))
user_real_first_day = {}
user_virtual_first_day = {}


def movieToSetId(movie):
    return movie % 10


def virtual2real(user, virtual_day):
    real_first = user_real_first_day[user]
    virtual_first = user_virtual_first_day[user]
    return (virtual_day + real_first - virtual_first) % (365 + 365 + 366)


def check_user_valid(user, virtual_day):
    # 100 days round
    if user_virtual_first_day[user] <= virtual_day < user_virtual_first_day[user] + 100:
        return True
    else:
        return False


def get_movie_id(user, day):
    movie = user_time_to_movie.get((user, str(day)))
    if movie is None:
        return None
    else:
        return movieToSetId(movie)  # the movie ID user see today


def runReal_IC(G, S):
    T = deepcopy(S)  # copy already selected nodes
    E = {}

    for v in S:
        # randomly choose a day that user v has see a movie
        time = int(choice(list(user_time_set[str(v)])))
        user_real_first_day[v] = time
        user_virtual_first_day[v] = 0  # seed set virtual day is all 0

    virtual_day = 0
    while True:
        i = 0
        no_valid_seed = True
        # for every seed in seed set
        while i < len(T):
            user = T[i]
            # if in a range of valid day
            if not check_user_valid(user, virtual_day):
                i += 1
                continue

            no_valid_seed = False

            # if see a movie
            real_day = virtual2real(user, virtual_day)
            user_movie_id = get_movie_id(user, real_day)
            if user_movie_id is None:
                i += 1
                continue

            # for its neighbours
            for neighbour in G[user]:
                if neighbour not in T:
                    neighbour_movie_id = get_movie_id(neighbour, real_day)
                    if neighbour_movie_id is not None:
                        if neighbour_movie_id == user_movie_id:
                            E[(user, neighbour)] = 1
                            T.append(neighbour)
                            user_real_first_day[neighbour] = real_day
                            user_virtual_first_day[neighbour] = virtual_day
                        else:
                            E[(user, neighbour)] = 0
            i += 1

        virtual_day += 1
        if no_valid_seed:
            break

    reward = len(T)
    return reward, E, T


def runReal_DC(G, S):
    T = deepcopy(S)  # copy already selected nodes
    E = {}
    T_node = {}   # record the count of nodes trying to active v

    for v in G.nodes():
        T_node[v] = 0

    for v in S:
        # randomly choose a day that user v has see a movie
        time = int(choice(list(user_time_set[str(v)])))
        user_real_first_day[v] = time
        user_virtual_first_day[v] = 0  # seed set virtual day is all 0

    virtual_day = 0
    while True:
        print("simulating the "+str(virtual_day)+" day")
        i = 0
        no_valid_seed = True
        # for every seed in seed set
        while i < len(T):
            user = T[i]
            # if in a range of valid day
            if not check_user_valid(user, virtual_day):
                i += 1
                continue

            no_valid_seed = False

            # if see a movie
            real_day = virtual2real(user, virtual_day)
            user_movie_id = get_movie_id(user, real_day)

            if user_movie_id is None:
                i += 1
                continue

            # for its neighbours
            for neighbour in G[user]:
                if neighbour not in T:
                    neighbour_movie_id = get_movie_id(neighbour, real_day)
                    if neighbour_movie_id is not None:
                        if neighbour_movie_id == user_movie_id:
                            E[(neighbour, T_node[neighbour])] = 1
                            T.append(neighbour)
                            user_real_first_day[neighbour] = real_day
                            user_virtual_first_day[neighbour] = virtual_day
                        else:
                            E[(neighbour, T_node[neighbour])] = 0
                        T_node[neighbour] += 1
            i += 1

        virtual_day += 1
        if no_valid_seed:
            break

    reward = len(T)
    return reward, E, T
