import re
import datetime
from datetime import timedelta

def parse(s):
    entry = re.split("[._:]", s)

    date = [int(i) for i in entry[0:3]]
    del entry[0:3]

    # convert to 24h time
    for i in range(len(entry)-2):
        if entry[i+2] == "pm":
            if entry[i] != "12":
                entry[i] = str(int(entry[i]) + 12)
        elif entry[i+2] == "am" and entry[i] == "12":
                entry[i] = "0"

    # remove am/pm
    for s in ["am", "pm"]:
        while(s in entry):
            entry.remove(s)

    entry = [int(i) for i in entry]

    combined = []
    for i in range(0, len(entry), 4):
        t0 = datetime.datetime(date[0], date[1], date[2], entry[i], entry[i+1])
        # can compare num entries as string types
        if entry[i] > entry[i+2]:
            nextDay = t0 + timedelta(days=1)
            date = [nextDay.year, nextDay.month, nextDay.day]
        t1 = datetime.datetime(date[0], date[1], date[2], entry[i+2], entry[i+3])
        combined.append([t0, t1])

    return combined

sleep = open("../../data/original/sleep_tracker.txt").read().strip().replace('-', '_').replace(';', '').replace("am", "_am").replace("pm", "_pm").splitlines()
sleep = [i[:i.find("(")]+i[i.find(")")+1:] if i.find("(")>0 else i for i in sleep]

iso8601 = []
for s in sleep:
    if len(s) > 10:
        iso8601 = iso8601 + parse(s)

file = open("../../data/processed/sleep_data.txt",'w')
file = open("../../data/processed/sleep_data.txt",'a')
for i in iso8601:
    file.write(i[0].isoformat()[:-3] + ", " + i[1].isoformat()[:-3] + "\n")
file.close()
