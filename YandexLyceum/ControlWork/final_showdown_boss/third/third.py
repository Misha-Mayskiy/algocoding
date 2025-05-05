import sys
import json
import urllib.request

port = sys.stdin.readline().strip()
fuu_bad_fish = sys.stdin.readline().strip()
min_fatness = int(sys.stdin.readline().strip())

url = f'http://127.0.0.1:{port}'
data = json.loads(urllib.request.urlopen(url).read().decode())

my_home_aquariums = {}
for rec in data:
    if rec['fat'] > min_fatness and rec['fish'] != fuu_bad_fish:
        my_home_aquariums.setdefault(rec['aqua'], set()).add(rec['fish'])

for aqua in sorted(my_home_aquariums, reverse=True):
    print(f"{aqua}: {' + '.join(sorted(my_home_aquariums[aqua]))}")
