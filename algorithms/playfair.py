def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = "".join(filter(str.isalpha, text))
    
    prepared = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = ""
        if i + 1 < len(text):
            b = text[i+1]
        if a == b:
            prepared += a + "X"
            i += 1
        else:
            if b:
                prepared += a + b
                i += 2
            else:
                prepared += a + "X"
                i += 1
    return prepared

def generate_matrix(key):
    key = key.upper().replace("J", "I")
    key = "".join(dict.fromkeys(filter(str.isalpha, key)))

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for c in alphabet:
        if c not in key:
            key += c

    matrix = [list(key[i:i+5]) for i in range(0, 25, 5)]
    return matrix

def find_position(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    raise ValueError(f"Ký tự không hợp lệ trong Playfair: {char}")

def encrypt(text, key):
    matrix = generate_matrix(key)
    text = prepare_text(text)

    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]

    return result

def decrypt(text, key):
    matrix = generate_matrix(key)
    text = text.upper().replace("J", "I")
    text = "".join(filter(str.isalpha, text))

    if not text:
        raise ValueError("Ciphertext Playfair không được để trống")
    if len(text) % 2 != 0:
        raise ValueError("Ciphertext Playfair phải có số ký tự chẵn")

    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            result += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:
            result += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]

    return result