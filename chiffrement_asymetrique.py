import random

def is_prime(n, k=5):
    if n in (2, 3):
        return True
    if n <= 1 or n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True

def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1  # assurer un nombre impair et de bonne taille
        if is_prime(p):
            return p

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, y, x = extended_gcd(b, a % b)
        return g, x, y - (a // b) * x

def modinv(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise Exception("Pas d'inverse modulaire")
    return x % phi

def generate_keys(bits=512):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # standard
    d = modinv(e, phi)

    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key

def encrypt(message, public_key):
    e, n = public_key
    block_size = (n.bit_length() - 1) // 8  # taille max en octets

    blocks = []
    for i in range(0, len(message), block_size):
        block = message[i:i + block_size].encode()
        m = int.from_bytes(block, 'big')
        c = pow(m, e, n)
        blocks.append(c)
    return blocks

def decrypt(cipher_blocks, private_key):
    d, n = private_key
    message = b""

    for c in cipher_blocks:
        m = pow(c, d, n)
        block = m.to_bytes((m.bit_length() + 7) // 8, 'big')
        message += block

    return message.decode(errors="ignore")  # ignore les artefacts éventuels


def main():
    print("🔐 Génération des clés RSA...")
    pub, priv = generate_keys(bits=128)  # attention, 128 bits = peu sécurisé, mais rapide pour test

    message = input("Quel est votre message ? \n")
    print("Message original :", message)

    encrypted = encrypt(message, pub)
    message_encrypté = 0
    for i in encrypted:
        message_encrypté += i
    print("🔒 Chiffré :", message_encrypté)

    decrypted = decrypt(encrypted, priv)
    print("🔓 Déchiffré :", decrypted)

if __name__ == "__main__":
    main()