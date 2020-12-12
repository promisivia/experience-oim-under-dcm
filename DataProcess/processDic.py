import pickle

file_address = './raw/link.txt'
action_log_address = "./processed/action_logs.txt"

user_to_movie_set = {}  # the movie set the user see
user_to_action_count = {}  # the action count
user_time_set = {}
user_and_time_to_movie = {}

action_logs = open(action_log_address, encoding="utf8", errors='ignore')
for line in action_logs:
    arr = line.split()
    user = int(arr[0])
    movie = int(arr[1])
    time = int(arr[2])
    user_and_time_to_movie[(user, time)] = movie
    try:
        user_to_movie_set[user].add(movie)
    except:
        user_to_movie_set[user] = set()
        user_to_movie_set[user].add(movie)
    try:
        user_time_set[user].add(time)
    except:
        user_time_set[user] = set()
        user_time_set[user].add(movie)
    try:
        user_to_action_count[user] += 1
    except:
        user_to_action_count[user] = 1

action_logs.close()

pickle.dump(user_to_action_count, open('./processed/userActionCount.dic', "wb"))
pickle.dump(user_to_movie_set, open('./processed/userMovieSet.dic', "wb"))
pickle.dump(user_time_set, open('./processed/userTimeSet.dic', "wb"))
pickle.dump(user_and_time_to_movie, open('./processed/userAndTimeToMovie.dic', "wb"))
