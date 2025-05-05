import csv
import json

sum_of_infuzoria = {}
with open('curious.csv', newline='') as csv_file:
    for roow in csv.DictReader(csv_file):
        name = roow['name']
        sum_of_infuzoria.setdefault(name, {'things': [], 'places': [], 'degrees': []})
        sum_of_infuzoria[name]['things'].append(roow['surprised'])
        sum_of_infuzoria[name]['places'].append(roow['where'])
        sum_of_infuzoria[name]['degrees'].append(int(roow['degree']))

with open('invisible.jsonl', 'w') as out_file:
    for name, info in sum_of_infuzoria.items():
        one_of_answers = {
            'name': name,
            'things': sorted(info['things']),
            'places': sorted(info['places']),
            'ave_degree': sum(info['degrees']) // len(info['degrees']),
            'max_degree': max(info['degrees'])
        }
        out_file.write(json.dumps(one_of_answers, ensure_ascii=False) + '\n')
