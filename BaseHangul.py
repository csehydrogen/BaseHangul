import io

"""
U+AC00..U+D7AF  Hangul Syllables  11,184  11,172  Hangul

ABCDE : (BYTE_CHARS ** 5) states
ABCD- : (BYTE_CHARS ** 4) states
ABC-- : (BYTE_CHARS ** 3) states
AB--- : (BYTE_CHARS ** 2) states
A---- : (BYTE_CHARS ** 1) states

XYZ : (BYTE_CHARS ** 5) + (BYTE_CHARS ** 4) states (< HAN_CHARS ** 3)
XY- : (BYTE_CHARS ** 3) + (BYTE_CHARS ** 2) states (< HAN_CHARS ** 2)
X-- : (BYTE_CHARS ** 1)                     states (< HAN_CHARS ** 1)
"""

BYTE_CHUNK = 5
BYTE_CHARS = 256

HAN_CHUNK = 3
HAN_CHARS = 11172
HAN_BASE = 0xAC00

assert (BYTE_CHARS ** 5) + (BYTE_CHARS ** 4) < (HAN_CHARS ** 3)
assert (BYTE_CHARS ** 3) + (BYTE_CHARS ** 2) < (HAN_CHARS ** 2)
assert (BYTE_CHARS ** 1)                     < (HAN_CHARS ** 1)

def encode(b):
    if type(b) != bytes:
        raise

    buf = io.StringIO()

    # number of chunks except the last
    n = max(len(b) - 1, 0) // BYTE_CHUNK
    for i in range(n):
        s = 0
        for j in range(BYTE_CHUNK - 1, -1, -1):
            s *= BYTE_CHARS
            s += b[i * BYTE_CHUNK + j]
        for j in range(HAN_CHUNK):
            buf.write(chr(HAN_BASE + s % HAN_CHARS))
            s //= HAN_CHARS

    # the last chunk
    byte_rem = len(b) - n * BYTE_CHUNK
    s = 0
    for j in range(byte_rem - 1, -1, -1):
        s *= BYTE_CHARS
        s += b[n * BYTE_CHUNK + j]

    han_rem = 0
    if byte_rem == 1:
        han_rem = 1
    elif byte_rem == 2:
        han_rem = 2
        s += BYTE_CHARS ** 3
    elif byte_rem == 3:
        han_rem = 2
    elif byte_rem == 4:
        han_rem = 3
        s += BYTE_CHARS ** 5
    elif byte_rem == 5:
        han_rem = 3

    for j in range(han_rem):
        buf.write(chr(HAN_BASE + s % HAN_CHARS))
        s //= HAN_CHARS

    ret = buf.getvalue()
    buf.close()
    return ret

def decode(b):
    if type(b) != str:
        raise

    buf = io.BytesIO()

    # number of chunks except the last
    n = max(len(b) - 1, 0) // HAN_CHUNK
    for i in range(n):
        s = 0
        for j in range(HAN_CHUNK - 1, -1, -1):
            o = ord(b[i * HAN_CHUNK + j])
            if o < HAN_BASE or o >= HAN_BASE + HAN_CHARS:
                raise
            s *= HAN_CHARS
            s += o - HAN_BASE
        for j in range(BYTE_CHUNK):
            buf.write(bytes([s % BYTE_CHARS]))
            s //= BYTE_CHARS
        if s != 0:
            raise

    # the last chunk
    han_rem = len(b) - n * HAN_CHUNK
    s = 0
    for j in range(han_rem - 1, -1, -1):
        o = ord(b[n * HAN_CHUNK + j])
        if o < HAN_BASE or o >= HAN_BASE + HAN_CHARS:
            raise
        s *= HAN_CHARS
        s += o - HAN_BASE

    byte_rem = 0
    if han_rem == 1:
        if s < BYTE_CHARS ** 1:
            byte_rem = 1
        else:
            raise
    elif han_rem == 2:
        if s < BYTE_CHARS ** 3:
            byte_rem = 3
        elif s < BYTE_CHARS ** 3 + BYTE_CHARS ** 2:
            byte_rem = 2
            s -= BYTE_CHARS ** 3
        else:
            raise
    elif han_rem == 3:
        if s < BYTE_CHARS ** 5:
            byte_rem = 5
        elif s < BYTE_CHARS ** 5 + BYTE_CHARS ** 4:
            byte_rem = 4
            s -= BYTE_CHARS ** 5
        else:
            raise

    for j in range(byte_rem):
        buf.write(bytes([s % BYTE_CHARS]))
        s //= BYTE_CHARS

    ret = buf.getvalue()
    buf.close()
    return ret
