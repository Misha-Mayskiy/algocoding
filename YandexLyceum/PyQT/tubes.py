with open('pipes.txt', mode='r', encoding='utf-8') as file:
    textinput = file.readlines()

tubelist = [1 / float(i) if float(i) != 0.0 else 0 for i in textinput[:-2]]
support = 0
for i in list(map(int, textinput[-1].split())):
    support += tubelist[i - 1]
fileanswer = open('time.txt', mode='w', encoding='utf-8')
fileanswer.write(str(1 / support * 60))