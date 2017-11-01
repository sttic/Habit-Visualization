# TODO add terminal interaction

import re

def main():
    sleep = read_raw_sleep("sleep_tracker.txt")
    iso8601 = ""

    for s in sleep:
        if len(s) > 10:
            iso8601 = iso8601 + parse(s)
    #print(iso8601, end="")
    write_sleep_data(iso8601)

def read_raw_sleep(file):
    '''str->list of str
    Returns a list of strings representing the periods I am asleep
    '''
    raw_sleep = open(file).read().replace('-', '_').replace(';', '').replace("am", "_am").replace("pm", "_pm").splitlines()
    for i in range(len(raw_sleep)):
        raw_sleep[i] = raw_sleep[i].strip()
    return raw_sleep

def parse(s):
    entry = re.split("[._:]", s)

    date = [entry[0], entry[1], entry[2]]
    del entry[0:3]

    # convert to 24h time and with placeholder zero for single digits
    for i in range(len(entry)-2):
        if entry[i+2] == "pm":
            if entry[i] != "12":
                entry[i] = str(int(entry[i]) + 12)
        elif entry[i+2] == "am":
            if len(entry[i]) == 1:
                entry[i] = "0" + entry[i]
            elif entry[i] == "12":
                entry[i] = "00"

    # remove am/pm
    for s in ["am", "pm"]:
        while(s in entry):
            entry.remove(s)

    combined = ""
    for i in range(0, len(entry), 4):
        t0 = date[0] + "-" + date[1] + "-" + date[2] + "T" + entry[i] + ":" + entry[i+1]
        # can compare num entries as string types
        if entry[i] > entry[i+2]:
            date = incr_date(date)
        t1 = date[0] + "-" + date[1] + "-" + date[2] + "T" + entry[i+2] + ":" + entry[i+3]
        combined = combined + t0 + ", " + t1 + "\n"

    return combined

def incr_date(date):
    year, month, day = int(date[0]), int(date[1]), int(date[2])

    if is_leap_year(year):
        DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if day < DAYS_IN_MONTH[int(month) - 1]:
        day = day + 1
    elif month < 12:
        month = month + 1
    else:
        year = year + 1

    return [format_single(year), format_single(month), format_single(day)]

def is_leap_year(year):
    return year % 4 == 0 and not(year % 100 == 0 and year % 400 != 0)

def format_single(i):
    s = str(i)
    if len(s) == 1:
        return "0" + s
    return s

def write_sleep_data(s):
    file = open("./data/sleep_data.txt",'w')
    file.write(s)
    file.close()

main()
