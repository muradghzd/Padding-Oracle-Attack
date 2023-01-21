import sys
from oracle_python_v1_2 import pad_oracle

def hex_to_bytearray(hextext):
    return bytearray.fromhex(hextext[2:])

def bytearray_to_hex(arr):
    return "0x" + "".join("{:02x}".format(x) for x in arr)

def detect_padding(C0, C1):
    n = (len(C0)-2)//2
    bytearray_C0 = hex_to_bytearray(C0)
    for i in range(n):
        for j in range(256):
            a = bytearray_C0[i]
            bytearray_C0[i] = j
            if int(pad_oracle(bytearray_to_hex(bytearray_C0), C1)) == 0:
                return i

        
def do_more(n, t, text, arr, C1):
    for i in range(n-1, t-1, -1):
        arr[i] = arr[i] ^ (n-t) ^ ((n-t+1)%256)
    for j in range(256):
        a = arr[t-1]
        arr[t-1] = j
        if int(pad_oracle(bytearray_to_hex(arr), C1)) == 1:
            text[t-1] = ((n-t+1)%256) ^ (j ^ a)
            break
        arr[t-1] = a


def decrypt_text(C0, C1):
    n = (len(C0)-2)//2
    t = detect_padding(C0, C1)
    plaintext = [0]*t
    bytearray_C0 = hex_to_bytearray(C0)
    while t >= 1:
        do_more(n, t, plaintext, bytearray_C0, C1)
        t -= 1
    print("".join(map(chr, plaintext)))

decrypt_text(sys.argv[1], sys.argv[2])
