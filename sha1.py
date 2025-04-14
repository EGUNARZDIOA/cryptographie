def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b)) ) & 0xFFFFFFFF


def sha1(message):
    # Step 1: Convert to bytearray (binary-friendly format)
    if isinstance(message, str):
        message = bytearray(message.encode())
    elif isinstance(message, bytes):
        message = bytearray(message)
    
    # Step 2: Pad the message
    original_length = len(message) * 8
    message.append(0x80)  # append '1' bit + seven '0' bits

    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0)

    message += original_length.to_bytes(8, 'big')  # add 64-bit message length

    # Step 3: Initialize 5 hash values (a-e)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Step 4: Process each 512-bit chunk
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        w = [int.from_bytes(chunk[j:j+4], 'big') for j in range(0, 64, 4)]

        # Step 5: Extend to 80 words
        for j in range(16, 80):
            w.append(left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1))

        # Step 6: Initialize temp variables
        a, b, c, d, e = h0, h1, h2, h3, h4

        # Step 7: Main loop
        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (left_rotate(a, 5) + f + e + k + w[j]) & 0xFFFFFFFF
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp

        # Step 8: Add chunk results to the main hash
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Step 9: Produce final 160-bit hash
    return ''.join(f'{x:08x}' for x in [h0, h1, h2, h3, h4])
