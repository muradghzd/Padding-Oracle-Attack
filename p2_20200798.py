import sys
from oracle_python_v1_2 import dec_oracle

def hex_to_bytearray(hextext):
    return bytearray.fromhex(hextext[2:])

def bytearray_to_hex(arr):
    return "0x" + "".join("{:02x}".format(x) for x in arr)

def xor_a_b(a, b):
    return [a[i] ^ b[i] for i in range(len(a))]

def divide_and_pad(text):
    bytearray_text = bytearray.fromhex(str(text.encode('utf-8').hex()))
    n = len(bytearray_text)
    q = int(n/8)
    r = n%8
    pad_list = [8-r]*(8-r)
    ans = []
    if n >= 8:
        for i in range(q):
            ans.append(list(bytearray_text[8*i:8*i+8]))
        if r != 0:
            x = list(bytearray_text[8*q:])
            x.extend(pad_list)
            ans.append(x)
        else:
            ans.append(pad_list)
    else:
        bytearray_text.extend(pad_list)
        ans.append(list(bytearray_text))
    return ans

def encrypt_plaintext(text):
    ans = divide_and_pad(text)
    n = len(ans)
    arr = [0]*(n+1)
    IV = "0xe584debd2abad5b3"
    bytearray_IV = hex_to_bytearray(IV)
    ciphertext = "0xcbd746544cdadf30"
    arr[n] = list(hex_to_bytearray(ciphertext))
    for i in range(n-1, -1, -1):
        y = hex_to_bytearray(dec_oracle(IV, ciphertext).decode('UTF-8'))
        x = xor_a_b(y, bytearray_IV)
        #x = xor_same_length(list(hex_to_bytrearray(dec_oracle(IV, ciphertext).decode('UTF-8'))), IV)
        arr[i] = xor_a_b(ans[i], x)
        ciphertext = bytearray_to_hex(arr[i])
    return arr

a = encrypt_plaintext(sys.argv[1])
b = [bytearray_to_hex(i) for i in a]
print(*b)
