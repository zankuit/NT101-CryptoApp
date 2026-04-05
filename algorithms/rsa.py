import math

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        return None
    return x % phi


def generate_keys(p, q, e):
    if not is_prime(p) or not is_prime(q):
        raise ValueError("p và q phải là số nguyên tố")
    if p == q:
        raise ValueError("p và q phải khác nhau")

    n = p * q
    phi = (p - 1) * (q - 1)

    if not (1 < e < phi):
        raise ValueError("e phải thỏa 1 < e < phi")

    if math.gcd(e, phi) != 1:
        raise ValueError("e không hợp lệ")

    d = mod_inverse(e, phi)
    if d is None:
        raise ValueError("Không tìm được nghịch đảo modular cho e")

    return (e, n), (d, n)


def encrypt(message, pubkey):
    e, n = pubkey
    if not isinstance(message, str):
        raise ValueError("Message phải là chuỗi")

    too_large = [ch for ch in message if ord(ch) >= n]
    if too_large:
        raise ValueError("n quá nhỏ cho dữ liệu đầu vào, hãy chọn p và q lớn hơn")

    return [pow(ord(c), e, n) for c in message]


def decrypt(cipher, privkey):
    d, n = privkey
    if not isinstance(cipher, list) or not all(isinstance(c, int) for c in cipher):
        raise ValueError("Cipher phải là danh sách số nguyên")
    if any(c < 0 or c >= n for c in cipher):
        raise ValueError("Cipher chứa giá trị ngoài phạm vi hợp lệ")

    return "".join(chr(pow(c, d, n)) for c in cipher)