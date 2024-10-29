layouts = ['йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю',
           'qwertyuiop', 'asdfghjkl', 'zxcvbnm']
lower = set(''.join(layouts))
upper = set(''.join(layouts).upper())
digits = set('1234567890')


def is_password_valid(password):
    chars = set(password)
    if not (chars & lower and chars & upper and chars & digits and len(password) > 8):
        return 'error'
    for i in range(len(password) - 2):
        if password[i:i + 3].lower() in ''.join(layouts):
            return 'error'
    return 'ok'


print(is_password_valid(input()))
