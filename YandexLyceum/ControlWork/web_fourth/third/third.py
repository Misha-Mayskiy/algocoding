import sys
import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('port')
parser.add_argument('file')
parser.add_argument('--word')
parser.add_argument('--n', type=int)
args = parser.parse_args()

url = f"http://{args.host}:{args.port}/"
response = requests.get(url)
witches = response.json()

requests_list = []
with open(args.file, 'r') as f:
    for line in f:
        if line.strip():
            requests_list.append(json.loads(line))

for req_idx, req in enumerate(requests_list, 1):
    happened = req['happened'].lower()
    urgency = req['urgency']

    matching_witches = []

    for witch_idx, witch_data in enumerate(witches, 1):
        name = witch_data[0]
        services = witch_data[1].lower()

        if args.word:
            services += f", {args.word.lower()}"

        words = happened.split()
        has_word_match = any(word in services for word in words)

        number = witch_idx
        if args.n:
            number += args.n

        is_urgent_match = number % urgency == 0

        if has_word_match and is_urgent_match:
            matching_witches.append(name)

    if matching_witches:
        print(f"{req_idx}: {', '.join(matching_witches)}")
