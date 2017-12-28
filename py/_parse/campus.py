data = open("../../data/original/on_campus_tracker.txt").read().strip().splitlines()
data = [i[:i.find("(")]+i[i.find(")")+1:] if i.find("(")>0 else i for i in data]

file = open("../../data/processed/campus_data.txt",'w')
file = open("../../data/processed/campus_data.txt",'a')
for i in data:
    file.write(i + "\n")
file.close()
