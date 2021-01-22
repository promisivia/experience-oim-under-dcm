from math import inf

min_day = inf
max_day = 0
with open("processed/action_logs.txt", "rb") as fout_action:
    count = 0
    for line in fout_action:
        arr = line.split()
        day = int(arr[2])
        min_day = min(day, min_day)
        max_day = max(day, max_day)
        count += 1

# print("count", count)
print("Max day: ", max_day)
print("Min day: ", min_day)

##############################################
# @output LastFM
# Max day:  1955
# Min day:  1

# @output Flixster
# Max day:  1052
# Min day:  1
############################################
