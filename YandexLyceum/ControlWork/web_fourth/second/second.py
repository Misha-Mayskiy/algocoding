import json
import csv
import requests


def count_digits(num):
    return len(str(abs(num)))


with open('property.json', 'r') as f:
    props = json.load(f)

host = props['host']
port = props['port']
max_len = props['length']
mod_val = props['mod7']

url = f"http://{host}:{port}/"
response = requests.get(url)
data = response.json()

results = []

for i, numbers in enumerate(data, 1):
    filtered = [n for n in numbers if count_digits(n) <= max_len and n % 7 == mod_val]

    if not filtered:
        continue

    sum_nums = sum(filtered)
    div_sum = sum(n // 7 for n in filtered) // 7

    if len(filtered) == 1:
        prod = filtered[0] ** 2
    else:
        prod = min(filtered) * max(filtered)

    digit_sum = sum(count_digits(n) for n in filtered)

    results.append({
        'no': i,
        'sum': sum_nums,
        'div': div_sum,
        'product': prod,
        'len': digit_sum
    })

with open('chalk.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['no', 'sum', 'div', 'product', 'len'])
    writer.writeheader()
    writer.writerows(results)
