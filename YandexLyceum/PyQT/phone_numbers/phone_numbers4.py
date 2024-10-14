s = ''.join(input().split())
try:
    assert s[0] == '+'
    assert s[1] == '7'

except AssertionError:
    if not s.startswith('8'):
        print('неверный формат')
        exit(0)
try:
    assert s.count('--') == 0
    assert not s.startswith('-')
    assert s[-1] != '-'
    assert s.count('(') == s.count(')') == 1 or s.count('(') == s.count(')') == 0
except AssertionError:
    print('неверный формат')
    exit(0)
s = s.replace('(', '')
s = s.replace(')', '')
s = s.replace('-', '')
if s.startswith('8'):
    s = '+7' + s[1:]
operator = s[2:5]
mts = ['910', '911', '912', '913', '914', '915', '916', '917', '918', '919',
       '980', '981', '982', '983', '984', '985', '986', '987', '988', '989']
megafon = ['920', '921', '922', '923', '924', '925', '926', '927', '928',
           '929', '930', '931', '932', '933', '934', '935', '936', '937',
           '938', '939']
beeline = ['902', '903', '904', '905', '906', '960', '961', '962', '963',
           '964', '965', '966', '967', '968', '969']
allop = mts + megafon + beeline
try:
    assert len(s) == 12
except AssertionError:
    print('неверное количество цифр')
    exit(0)
try:
    assert operator in allop
except AssertionError:
    print('не определяется оператор сотовой связи')
    exit(0)
print(s)