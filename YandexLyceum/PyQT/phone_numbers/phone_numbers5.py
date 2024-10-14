class WrongFormat(Exception):
    pass


class WrongLen(Exception):
    pass


class WrongOperator(Exception):
    pass


class WrongCountry(Exception):
    pass


def check_phone_status(num):
    try:
        num = ''.join(num.split())
        check5 = False
        check6 = num.startswith('+')
        for m in countries:
            if num.startswith(m):
                check5 = True
                code = m
                break
        check1 = check5 or num.startswith('8')
        check2 = all(num.split('-'))
        check3 = num.count('(') == 1 and num.count(')') == 1 and num.find('(') < num.find(')')
        check4 = num.count('(') == 0 and num.count(')') == 0
        if check1 and check2 and (check3 or check4):
            if num.startswith('8'):
                num = num[1:]
                ans = '+7'
            else:
                num = num[num.find(code) + len(code):]
                ans = code
            for m in num:
                if m in '0123456789':
                    ans += m
                elif m.isalpha():
                    raise WrongFormat
            if len(ans) >= 12:
                if ans[2:5] not in operators and ans.startswith('+7'):
                    raise WrongOperator
                return ans
            else:
                raise WrongLen
        elif not check5 and check6:
            raise WrongCountry
        else:
            raise WrongFormat
    except WrongFormat:
        return 'неверный формат'
    except WrongLen:
        return 'неверное количество цифр'
    except WrongOperator:
        return 'не определяется оператор сотовой связи'
    except WrongCountry:
        return 'не определяется код страны'


operators = ['910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '980', '981', '982', '983', '984',
             '985', '986', '987', '988', '989',
             '920', '921', '922', '923', '924', '925', '926', '927', '928', '929', '930', '931', '932', '933', '934',
             '935', '936', '937', '938', '939',
             '902', '903', '904', '905', '906', '960', '961', '962', '963', '964', '965',
             '966', '967', '968', '969']
countries = ['+7', '+359', '+55', '+1']
print(check_phone_status(input()))
