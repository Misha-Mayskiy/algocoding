# string = " ".join(input().lower().replace(" ", "")).split()
# dictans = {}
# ansstring = ""
# for i in string:
#     if i in dictans.keys():
#         dictans[i] += 1
#     else:
#         dictans[i] = 1
# for k, i in dictans.items():
#     print(f"{k}-{i}", end=" ")
# У МЕНЯ РАБОТАЛООООО ПРОВЕРКА НЕ СРАБОТАЛА АОАОАОАО FATAL ERROR 404

# dictold = eval(input())
# dictnew = eval(input())
# kept = sorted({i for i in dictold.keys() if i in dictnew.keys()})
# added = sorted({i for i in dictnew.keys() if i not in dictold.keys()})
# removed = sorted({i for i in dictold.keys() if i not in dictnew.keys()})
# print({'kept': set(kept), 'added': f"{*added}", 'removed': set(removed)})
# # У МЕНЯ РАБОТАЛООООО ПРОВЕРКА НЕ СРАБОТАЛА АОАОАОАО FATAL ERROR 404

# def extract_keys(d):
#     keys = []
#
#     def recursive_helper(current_dict):
#         for key in current_dict:
#             keys.append(key)
#             if isinstance(current_dict[key], dict):
#                 recursive_helper(current_dict[key])
#
#     recursive_helper(d)
#     return keys
#
#
# print(extract_keys(eval(input())))

# def parse_to_dict(input_string):
#     # Убираем пробелы вокруг строки и лишние символы
#     input_string = input_string.strip()
#
#     # Обработка формата с фигурными скобками
#     if input_string.startswith('{') and input_string.endswith('}'):
#         input_string = input_string[1:-1]
#
#     # Обработка формата без фигурных скобок
#     if input_string:
#         items = input_string.split(',')
#     else:
#         items = []
#
#     result = {}
#     for item in items:
#         # Разделяем по двоеточию
#         key_value = item.split(':')
#         if len(key_value) == 2:
#             key = key_value[0].strip().strip("'").strip('"')
#             value = key_value[1].strip().strip("'").strip('"')
#             result[key] = value
#
#     return result
#
#
# print(parse_to_dict(input()))

dict_multi = {}

def put(keys, value):
    key_tuple = tuple(keys)
    if key_tuple not in dict_multi:
        dict_multi[key_tuple] = []
    dict_multi[key_tuple].append(value)

def get(keys):
    results = []
    for key in keys:
        for k in dict_multi.keys():
            if key in k:
                results.extend(dict_multi[k])
    return results

a = eval(input())
b = input()
put(a, b)

print(get(a)[0])