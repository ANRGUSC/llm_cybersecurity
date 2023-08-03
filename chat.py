import openai
import json
from typing import List, Dict
import random

openai.api_key = "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"


def response(message: List[Dict]):
    # print(json.dumps(message, indent=4))
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=1,
        max_tokens=2
    )
    print(completion)


def select_random(data: List[Dict], n: int, completion: str) -> List[Dict]:
    filtered = [d for d in data if d['completion'] == completion]
    return random.sample(filtered, n)


def few_shot(data: List[Dict]) -> List[Dict]:
    messages = [{
        "role": "system",
        "content": "You are a node attack prediction system. The first number is time, followed by packet volumes in 10 minutes and the average 30-minute, 1-hour, 2-hour, and 4-hour packet volumes for node 0, node 1, node 2, node 3 and node 4. The last number is the node to be predicted."
        }]
    for d in data:
        messages.append({"role": "user", "content": d["prompt"]})
        messages.append({"role": "assistant", "content": d["completion"]})
    return messages


def load_jsonl(filename: str) -> List[Dict]:
    data = []
    with open(filename, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def test_message(data: List[Dict], n: int, messages: List[Dict])-> List[Dict]:
    random_test = random.sample(data, n)
    for line in random_test:
        print(line)
        messages.append({"role" : "user", "content" : line['prompt']})

    return messages

if __name__ == '__main__':
    filename = '30/train_1.4_8h_0.5_5_prepared_2.jsonl'
    data = load_jsonl(filename)

    selected = select_random(data, 5, '0') + select_random(data, 5, '1')

    messages = few_shot(selected)
    messages = test_message(data, 2, messages)
    response(messages)
