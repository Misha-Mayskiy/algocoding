from microschemes import *

not_top = TNot()
and_top = TAnd()
not_bottom = TNot()
and_bottom = TAnd()
or_final = TOr()

not_top.link(and_top, 2) # not(Y) -> and(X, not(Y))

and_top.link(or_final, 1)

not_bottom.link(and_bottom, 1) # not(X) -> and(not(X), Y)

and_bottom.link(or_final, 2)

print("X\tY\tРезультат")

test_inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]

for X_val, Y_val in test_inputs:
    not_top.In1 = Y_val
    and_top.In1 = X_val
    not_bottom.In1 = X_val
    and_bottom.In2 = Y_val
    result = or_final.Res
    print(f"{int(X_val)}\t{int(Y_val)}\t{int(result)}")
