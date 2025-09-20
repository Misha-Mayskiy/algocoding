from microschemes import TLogElement as logelement

elNot = logelement.TNot()
elAnd = logelement.TAnd()
elAnd.link(elNot, 1)

for A in range(2):
    elAnd.In1 = bool(A)
    for B in range(2):
        elAnd.In2 = bool(B)
