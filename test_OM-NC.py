import csv
import sys
import json
import openai
import random
import pandas as pd

openai.api_key = "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"


def getPrompt(path):
    """
    :param path: test dataset file path
    :return: inputs to fine-tuning model and the expected results
    """
    prompts = []
    expected_responses = []

    with open(path, 'r') as file:
        for line in file:
            data = json.loads(line)
            prompt = data.get('prompt')
            expect = data.get('completion')
            if prompt:
                prompts.append(prompt)
                expected_responses.append(expect)
    return prompts, expected_responses


def results(prompts, expected_response):
    """
    This is a function for getting accuracy, precision, recall and f1 score.
    :param prompts: Prompts Input
    :param expected_response: Results of prompts they should be
    """
    # print(expected_response)
    n = len(prompts)
    """number of results which are the same as it should be"""
    true = 0
    # Positive results get from fine-tuning model
    P = 0
    # Negative results get from fine-tuning model
    N = 0
    # Negative results in test data set
    N_real = 0
    # Positive results in test data set
    P_real = 0

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    precision = 0.0
    recall = 0.0
    f1 = 0.0
    for i in range(n):
        # # print(prompts[i])
        response = openai.Completion.create(
            # engine="ada:ft-llm-cybersecurity:newset-k-0-0-5-1-2023-06-15-16-23-23",
            engine="ada:ft-llm-cybersecurity:om-nc-0-2023-08-02-22-23-55",
            prompt=prompts[i],
            max_tokens=1
        )
        result = str(response.choices[0].text.strip())
        print("expected: ", expected_response[i])
        print("result: ", result)
        if expected_response[i] == '0':
            N_real += 1
            if result == expected_response[i]:
                TN += 1
                true += 1
                N += 1
            elif result == '1':
                FN += 1
                P += 1
        elif expected_response[i] == '1':
            P_real += 1
            if result == expected_response[i]:
                TP += 1
                true += 1
                P += 1
            elif result == '0':
                FP += 1
                N += 1

    accuracy = float(true / n)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * (precision * recall) / (precision + recall)

    print("Number of Positive: ", P, " ,and it should be: ", P_real)
    print("Number of Negative: ", N, " ,and it should be: ", N_real)
    print("TP: ", TP, "; FP: ", FP, "; TN: ", TN, "; FN: ", FN)
    print("Accuracy:", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1 Score: ", f1)
    result = ["0", accuracy, precision, recall, f1]
    with open("record_OM-NC.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(result)


if __name__ == '__main__':
    PATH = "test0.jsonl"
    prompts, expect_response = getPrompt(PATH)
    results(prompts, expect_response)
