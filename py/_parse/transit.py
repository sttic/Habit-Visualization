data = open("../../data/original/transit.txt").read().strip().splitlines()
data = [i[:-i[::-1].find(",")-1] for i in data]
data = [i[:i.find("(")]+i[i.find(")")+1:] if i.find("(")>0 else i for i in data]

file = open("../../data/processed/transit_data.txt",'w')
for i in data:
    file.write(i + "\n")
file.close()
