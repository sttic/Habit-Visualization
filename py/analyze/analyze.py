import datetime
from datetime import timedelta
import dateutil.parser

for file in ["sleep", "campus", "transit"]:
    data = open("../../data/processed/" + file + "_data.txt").read().strip().splitlines()
    data = [[dateutil.parser.parse(j) for j in i.split(", ")] for i in data]

    step = timedelta(minutes=1)
    time, end = data[0][0].replace(hour=0, minute=0), data[-1][1].replace(hour=23, minute=59)

    week = [[[0 for minute in range(60)] for hour in range(24)] for day in range(7)]
    num_weekday = [0 for day in range(7)]
    
    daily_total, counter = [], 0
    
    i, instance = 0, data[0]
    while time != end + step:
        if (time - instance[0]).total_seconds() >= 0 and (time - instance[1]).total_seconds() < 0:
            week[time.weekday()][time.hour][time.minute] += 1
            counter +=1
        elif (time - instance[1]).total_seconds() >= 0 and i < len(data)-1:
            i += 1
            instance = data[i]

        time = time + step

        if time.time() == datetime.time(0,0,0):
            num_weekday[(time-step).weekday()] += 1
            daily_total.append([(time - step).date().isoformat(), counter])
            counter = 0

    avg_hour = [[sum(week[day][hour])/(num_weekday[day]*60) for hour in range(24)] for day in range(7)]
    avg_min = [sum([[week[day][hour][minute]/(num_weekday[day]) for minute in range(60)] for hour in range(24)], []) for day in range(7)]

    active_duration = [i + [i[1]-i[0]] for i in data]
    inactive_duration = [[data[i-1][1], data[i][0]] + [data[i][0]-data[i-1][1]] for i in range(1, len(data))]

    for f in [["_heatmap_minute", avg_min], ["_heatmap_hour", avg_hour], ["_daily_total", daily_total], ["_active_duration", active_duration], ["_inactive_duration", inactive_duration]]:
        newfile = open("../../data/processed/analysis/" + file + f[0] + ".txt",'w')
        for i in f[1]:
            if f[0] == "_daily_total":
                newfile.write(str(i)[1:-1].replace("\'", "") + "\n")
            elif f[0] == "_heatmap_minute" or f[0] == "_heatmap_hour":
                newfile.write(str(i)[1:-1] + "\n")
            elif f[0] == "_active_duration" or f[0] == "_inactive_duration":
                newfile.write(i[0].isoformat()[:-3] + ", " + i[1].isoformat()[:-3] + ", " + str(int(i[2].total_seconds()/60)) + "\n")
        newfile.close()
