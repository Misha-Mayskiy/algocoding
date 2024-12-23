def max_symmetry_find(m, tolerance):
    len_arr = len(m)
    max_seq_len = 0
    st_pos = 0

    def symmetry_check(li, ri):
        nonlocal max_seq_len, st_pos
        while li >= 0 and ri < len_arr and abs(
                m[li] - m[ri]) <= tolerance * 2 - tolerance / 2:
            li -= 1
            ri += 1
        cur_seq_len = ri - li - 1
        if cur_seq_len > max_seq_len:
            max_seq_len = cur_seq_len
            st_pos = li + 1

    for i in range(len_arr):
        symmetry_check(i, i)
        symmetry_check(i, i + 1)

    return [int(x) if x == 0.0 else x for x in m[st_pos:st_pos + max_seq_len]]


m = list(map(float, input().split()))
sigmaboychik = 0.2
print(" ".join(map(str, max_symmetry_find(m, sigmaboychik))))
