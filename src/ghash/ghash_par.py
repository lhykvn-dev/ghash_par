# Block parallel GHASH
# Block Function            Flattened Function
# 1     Y1 = X1.H           Y1 = X1.H
# 2     Y2 = (Y1.X2).H      Y2 = X1.H^2 + Y1.H
# 3     Y3 = (Y2.X3).H      Y3 = X1.H^3 + X2.H^2 + X3.H
# ...
# n     Yn = (Yn-1.Xn).H    Yn = X1.H^n + X2.H^(n-1) + ... + Xn.H
import struct
import math
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from gf2_mult.gf2_mult import Gf2Mult

def gen_tag(key: bytes, iv: bytes, aad: bytes, ct: bytes) -> bytes:
    cipher_ecb = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor_ecb = cipher_ecb.encryptor()
    H = encryptor_ecb.update(b'\x00' * 16) + encryptor_ecb.finalize()

    # Precompute powers of H
    n = math.ceil(len(ct)/16) + 2 # Including AAD and len block
    H_list = list()
    H_list.append(H)
    gf2mult = Gf2Mult()
    for i in range(1, n):
        # H_list.append(gf_mul(H_list[i-1], H))
        H_list.append(gf2mult.russian_peasant(H_list[i-1], H))
    # for i in range(len(H_list)):
    #     print("GHASH_PAR|H^{}={}".format(i, H_list[i].hex()))

    # GHASH computation over aad||ct
    ct_tag = ghash_par(H_list, aad, ct)
    J0 = iv + b'\x00\x00\x00\x01' # pre-counter block
    j0_tag = (Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).encryptor().update(J0))
    return xor_block(j0_tag, ct_tag)

def xor_block(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def pad16(data: bytes) -> bytes:
    return data + b'\x00' * ((16 - len(data) % 16) % 16)

def ghash_par(H_list: list, aad: bytes, ciphertext: bytes) -> bytes:
    len_block = struct.pack(">QQ", len(aad)*8, len(ciphertext)*8)
    ct_pad16 = pad16(ciphertext)
    gf2mult = Gf2Mult()

    # Parallelizable XOR of GHASH blocks
    for i in range(len(H_list)):
        if i == 0: # 1st Block AAD
            X = gf2mult.russian_peasant(pad16(aad), H_list[-1])
        elif i == len(H_list)-1: # Last Block Len
            X = xor_block(X, gf2mult.russian_peasant(len_block, H_list[0]))
        else: # Payload
            X = xor_block(X, gf2mult.russian_peasant(ct_pad16[(i-1)*16 : i*16], H_list[-i-1]))
    return X


if __name__ == "__main__":
    key = 'd672e2280f5ee1f666e7c6b099dd704ceb2afd898e296de3f8325d2e88c23b71'
    pt = '835dd1afc77b41ae141450025e5ac185b449a34d9d4ccee36c4b294a9289636967372eedf523b0c5792a89ca8660040662ba7835ffced7d02d0192432b63430a'
    aad = '112233445566778899aabbcc'
    iv = '4c47da5fe9a77e101ee7a0f7'
    ct = '835dd1afc77b41ae141450025e5ac185b449a34d9d4ccee36c4b294a9289636967372eedf523b0c5792a89ca8660040662ba7835ffced7d02d0192432b63430a'
    ct_len = 32 # bytes, 2 blocks

    ct_B = bytes.fromhex(pt)[0:ct_len]
    key_B = bytes.fromhex(key)
    aad_B = bytes.fromhex(aad)
    iv_B = bytes.fromhex(iv)

    gen_tag(key_B, iv_B, aad_B, ct_B)