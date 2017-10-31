def read_raw_sleep_sleep(file):
    '''str->list of str
    Returns a list of strings representing the periods I am asleep
    '''
    raw_sleep = open(file).read().splitlines()
    for i in range(len(raw_sleep)):
        raw_sleep[i] = raw_sleep[i].strip()
    return raw_sleep

sl = read_raw_sleep_sleep("sleep_tracker.txt")
print(sl)