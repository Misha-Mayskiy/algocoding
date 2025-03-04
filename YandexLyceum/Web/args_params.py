import sys

args = sys.argv[1:]
sort_flag = False

if '--sort' in args:
    sort_flag = True
    args.remove('--sort')

entries = []
for arg in args:
    key_value = arg.split('=', 1)
    if len(key_value) == 1:
        entries.append((key_value[0], ''))
    else:
        entries.append((key_value[0], key_value[1]))

if sort_flag:
    entries.sort(key=lambda x: x[0])
for key, value in entries:
    print(f"Key: {key} Value: {value}")
