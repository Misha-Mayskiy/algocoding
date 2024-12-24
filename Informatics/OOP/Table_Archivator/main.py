class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def build_tree(text):
    freq = {}
    for char in text:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1

    nodes = [Node(char, freq) for char, freq in freq.items()]

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        connected = Node(None, left.freq + right.freq)
        connected.left = left
        connected.right = right
        nodes.append(connected)

    return nodes[0]

def gen_code(node, current_code, codes):
    if node is None:
        return
    if node.char is not None:
        codes[node.char] = current_code
        return
    gen_code(node.left, current_code + "0", codes)
    gen_code(node.right, current_code + "1", codes)

def encoding_text(text):
    root = build_tree(text)
    codes = {}
    gen_code(root, "", codes)
    encoded_text = "".join([codes[char] for char in text])
    return encoded_text, codes

def decoding_text(encoded_text, codes):
    rev_code = {v: k for k, v in codes.items()}
    cur_code = ""
    decoded_text = ""
    for bit in encoded_text:
        cur_code += bit
        if cur_code in rev_code:
            decoded_text += rev_code[cur_code]
            cur_code = ""
    return decoded_text

if __name__ == "__main__":
    input_text = """Дело было в январе,
    Стояла ёлка на горе,
    А возле этой ёлки
    Бродили злые волки.

    Вот как-то раз ночной порой,
    Когда в лесу так тихо,
    Встречают волка под горой
    Зайчата и зайчиха.

    Кому охота в Новый год
    Попасться в лапы волку?
    Зайчата бросились вперёд
    И прыгнули на ёлку.

    Они прижали ушки,
    Повисли, как игрушки.
    Десять маленьких зайчат
    Висят на ёлке и молчат.

    Обманутые волки
    Под ёлкой пробежали,
    А в это время зайчики
    Спокойно вниз слезали.

    Домой пошли весёлые,
    Песенки запевая,
    Про смелых зайцев маленьких
    И про лесного края."""

    encoded, code_table = encoding_text(input_text)

    original_size = len(input_text) * 8
    compressed_size = len(encoded)

    # print("Сжатый текст:", encoded)
    # print("Таблица кодов:", code_table)

    decoded = decoding_text(encoded, code_table)
    # print("Восстановленный текст:", decoded)

    '''Проверка, что сжатый текст и обратно 
    декодированный, все тот же без потерь'''
    print(str(input_text == decoded).lower())

    # print(f"Исходный размер: {original_size} бит")
    # print(f"Сжатый размер: {compressed_size} бит")
    # print(f"Коэффициент сжатия: {100 - (compressed_size / original_size * 100):.2f}%")
