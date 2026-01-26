# Standard implementation of GHASH
import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from gf2_mult.gf2_mult import Gf2Mult

def gen_tag(key: bytes, iv: bytes, aad: bytes, ct: bytes) -> bytes:
  cipher_ecb = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
  encryptor_ecb = cipher_ecb.encryptor()
  H = encryptor_ecb.update(b'\x00' * 16) + encryptor_ecb.finalize()
  print("GHASH|H={}".format(H.hex()))

  # GHASH computation over aad||ct
  ct_tag = ghash(H, aad, ct)
  J0 = iv + b'\x00\x00\x00\x01' # pre-counter block
  j0_tag = (Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).encryptor().update(J0))
  return xor_block(j0_tag, ct_tag)

def xor_block(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def pad16(data: bytes) -> bytes:
    return data + b'\x00' * ((16 - len(data) % 16) % 16)

def ghash(H: bytes, aad: bytes, ciphertext: bytes) -> bytes:
    X = b'\x00' * 16
    gf2mult = Gf2Mult()
    for block in [pad16(aad)[i:i+16] for i in range(0, len(pad16(aad)), 16)]:
        X = gf2mult.russian_peasant(xor_block(X, block), H)
    for block in [pad16(ciphertext)[i:i+16] for i in range(0, len(pad16(ciphertext)), 16)]:
        X = gf2mult.russian_peasant(xor_block(X, block), H)
    len_block = struct.pack(">QQ", len(aad)*8, len(ciphertext)*8)
    X = gf2mult.russian_peasant(xor_block(X, len_block), H)
    return X