import csv
import sys
import json
import openai

# Input the dataset's file path in the parameter
PATH = sys.argv[1]
# PATH = "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"

features = []

# Read data
with open(PATH) as recvFile:
    recv = csv.reader(recvFile)
    features = next(recv)
    feature_num = len(features)
    values = []
    for row in recv:
        value = []
        for i in range(feature_num):
            value.append(features[i]+": "+row[i])
        values.append(value)

with open(PATH) as recvFile:
    reader = csv.DictReader(recvFile)
    json_data = json.dumps(list(reader),ensure_ascii=False, separators=(',\n', ': '))

# write data into text file
with open('output.txt', 'w') as file:
    for value in values:
        file.write(str(value) + '\n')
# write data into json file
with open('output.json', 'w') as file:
    file.write(json_data)
