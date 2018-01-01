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

        if time.date() !=  (time - step).date():
            num_weekday[(time-step).weekday()] += 1
            daily_total.append([(time - step).date().isoformat(), counter])
            counter = 0

    avg_hour = [[sum(week[day][hour])/(num_weekday[day]*60) for hour in range(24)] for day in range(7)]
    avg_min = [sum([[week[day][hour][minute]/(num_weekday[day]) for minute in range(60)] for hour in range(24)], []) for day in range(7)]

    for f in [["_heatmap_minute", avg_min], ["_heatmap_hour", avg_hour], ["_daily_total", daily_total]]:
        newfile = open("../../data/processed/analysis/" + file + f[0] + ".txt",'w')
        newfile = open("../../data/processed/analysis/" + file + f[0] + ".txt",'w')
        if f[0] == "_daily_total":
            for i in f[1]:
                newfile.write(str(i)[1:-1].replace("\'", "") + "\n")
        else:
            for i in f[1]:
                newfile.write(str(i)[1:-1] + "\n")
        newfile.close()
