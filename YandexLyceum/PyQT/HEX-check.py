datainput = open('data.txt', 'rb').read()
count = len(datainput)

print(' ' * 10 + ' '.join(f'{hex(i)[2:]:0>2}' for i in range(16)), '\n')

for i in range(count // 16 + 1):
    onetimepart = datainput[i * 16: i * 16 + 16]
    if onetimepart:
        printable = ''.join((chr(p) if chr(p).isprintable() else '.' for p in onetimepart))
        print(('%0.5x0    ' % i) +
              ''.join(('%0.2x ' % p for p in onetimepart)) +
              ' ' * ((16 - len(onetimepart)) * 3 + 4) + printable)