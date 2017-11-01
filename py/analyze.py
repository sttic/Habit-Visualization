import datetime

def main():
    data = read_sleep_data("./data/sleep_data.txt")
    data = seperate_entry(data)

    print(data)

def read_sleep_data(file):
    sleep_data = open(file).read().splitlines()
    return sleep_data

def seperate_entry(s):
    for i in range(len(s)):
        s[i] = s[i].split(", ")
    return s

def wait_for_press():
    input("\nPress any key to exit. ")

main()
wait_for_press()