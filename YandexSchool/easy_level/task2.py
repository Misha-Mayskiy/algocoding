def eval_alternative(input_str):
    needed_answer = 0
    now_sign = 1
    paren_stack = []

    need_operator = True

    i = 0
    len_str = len(input_str)

    while i < len_str:
        symbol = input_str[i]

        if symbol.isdigit():
            num_val = 0
            while i < len_str and input_str[i].isdigit():
                num_val = num_val * 10 + int(input_str[i])
                i += 1
            needed_answer += now_sign * num_val
            need_operator = False
            continue

        elif symbol == '+':
            now_sign = 1
            need_operator = True

        elif symbol == '-':
            if need_operator:
                now_sign *= -1
            else:
                now_sign = -1
            need_operator = True

        elif symbol == '(':
            paren_stack.append(needed_answer)
            paren_stack.append(now_sign)
            needed_answer = 0
            now_sign = 1
            need_operator = True

        elif symbol == ')':
            prev_sign = paren_stack.pop()
            prev_accumulator = paren_stack.pop()
            needed_answer = prev_accumulator + prev_sign * needed_answer
            now_sign = 1
            need_operator = False

        i += 1

    return needed_answer


answer = eval_alternative(input())
print(answer)
