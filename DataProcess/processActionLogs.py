import time

movie_set = set()
action_logs = []
fin_rating = open("./raw/Ratings.timed.txt", encoding="utf8", errors='ignore')
# fin_rating = open("./raw/user_taggedartists.dat", encoding="utf8", errors='ignore')
line = fin_rating.readline()  # skip the first line
for line in fin_rating:
    arr = line.replace('\00', '').split()
    # arr = line.replace('\t', ' ').split()
    if len(arr) == 5:  # if len(arr) == 6:
        user = int(arr[0])
        movie = int(arr[1])
        movie_set.add(movie)
        timeArray = time.strptime(arr[3]+' '+arr[4], "%Y-%m-%d %H:%M:%S")
        # timeArray = time.strptime(arr[3]+' '+arr[4]+' '+arr[5], "%d %m %Y")
        # replace with time stamp
        day = timeArray.tm_yday
        if 2007 <= timeArray.tm_year <= 2009:
        # if 2006 <= timeArray.tm_year <= 2011:
            day += 365 * (timeArray.tm_year - 2007)  # day += 365 * (timeArray.tm_year - 2006)
            if timeArray.tm_year > 2008:
                day += 1
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

##############################################
# @output LastFM
# Number of logs:  183991
# Number of action ids:  12523
# Max day:  1955
# Min day:  1

# @output Flixster
# Number of logs:  7296359
# Number of action ids:  48794
# Max day:  1955
# Min day:  1
############################################
