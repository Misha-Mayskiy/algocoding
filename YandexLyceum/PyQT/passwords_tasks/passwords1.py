def bad_pass(m):
    bsubjects = ['qwertyuiop', 'asdfghjkl',
                 'zxcvbnm', 'йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю']
    num = list('1234567890')
    if len(m) <= 8 or m.islower() or m.isupper() or m.isdigit() or m.isalpha():
        return 'error'

    list_lower = m.lower()
    for i in bsubjects:
        for j in range(len(i) - 2):
            if i[j: j + 3] in list_lower:
                return 'error'

    for i in num:
        if i in m:
            return 'ok'

    return 'error'


print(bad_pass(input()))
