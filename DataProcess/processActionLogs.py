import time

fin_rating = open("./raw/Ratings.timed.txt", encoding="utf8", errors='ignore')
line = fin_rating.readline()  # skip the first line
movie_set = set()
action_logs = []
for line in fin_rating:
    arr = line.replace('\00', '').split()
    if len(arr) == 5:
        user = int(arr[0])
        movie = int(arr[1])
        movie_set.add(movie)
        timeArray = time.strptime(arr[3]+' '+arr[4], "%Y-%m-%d %H:%M:%S")
        # replace with time stamp
        day = timeArray.tm_yday
        if 2007 <= timeArray.tm_year <= 2009:
            if timeArray.tm_year == 2008:
                day += 365
            if timeArray.tm_year == 2009:
                day += (365 + 366)
            action_logs.append([user, movie, day])

fin_rating.close()
print("Number of logs: ", len(action_logs))
print("Number of action ids: ", len(movie_set))

# Sort action logs and output
print("Sorting action_logs...")
action_logs = sorted(action_logs, key=lambda t: (t[1], t[0], t[2]))
print("Writing action_logs...")
with open("processed/action_logs.txt", "w") as fout_action:
    for line in action_logs:
        fout_action.write("%d %d %d\n" % (line[0], line[1], line[2]))
