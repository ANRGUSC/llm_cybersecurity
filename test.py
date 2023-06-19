import csv
import sys
import json
import openai
import string

openai.api_key = "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"

prompts = []
# prompts_1_2_3 = []
types = []
with open("./test_data/test.csv", "r+") as testFile:
    recv = csv.reader(testFile)

    for row in recv:
        prompts.append(row[0])
        types.append(row[-1])

n = len(prompts)
true = 0
P = 0
N = 0
N_real = 0
P_real = 0
TP = 0
TN = 0
FP = 0
FN = 0
precision = 0.0
recall = 0.0
f1 = 0.0
for i in range(n):
    # print(prompts[i])
    response = openai.Completion.create(
        engine="ada:ft-llm-cybersecurity:newset-k-0-0-5-1-2023-06-15-16-23-23",
        prompt=prompts[i],
        max_tokens=1
    )
    result = str(response.choices[0].text.strip())
    # first = remove_punctuation(first)
    print(types[i], result)
    if types[i] == '0':
        N_real += 1
        if result == types[i]:
            TN += 1
            true += 1
            N += 1
        elif result == '1':
            FN += 1
            P += 1
    elif types[i] == '1':
        P_real += 1
        if result == types[i]:
            TP += 1
            true += 1
            P += 1
        elif result == '0':
            FP += 1
            N += 1

precision = TP / (TP + FP)
recall = TP / (TP + FN)
f1 = 2*(precision*recall)/(precision+recall)
print("Number of Positive: ", P, " ,and it should be: ", P_real)
print("Number of Negative: ", N," ,and it should be: ", N_real)
print("Accuracy:", float(true / n))
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)
