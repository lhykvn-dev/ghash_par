from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AESGCM_PYLIB:
    def __init__(self, key: bytes):
        if len(key) != 32:
            raise ValueError("Key must be 256 bits (32 bytes)")
        self.aes256gcm = AESGCM(key)

    def encrypt(self, iv: bytes, pt: bytes, aad: bytes):
        return self.aes256gcm.encrypt(iv, pt, aad)

    def decrypt(self, iv: bytes, ct_tag: bytes, aad: bytes):
        return self.aes256gcm.decrypt(iv, ct_tag, aad)

if __name__ == "__main__":
    pt = '835dd1afc77b41ae141450025e5ac185b449a34d9d4ccee36c4b294a9289636967372eedf523b0c5792a89ca8660040662ba7835ffced7d02d0192432b63430a'
    key = 'd672e2280f5ee1f666e7c6b099dd704ceb2afd898e296de3f8325d2e88c23b71'
    aad = '112233445566778899aabbcc'
    iv = '4c47da5fe9a77e101ee7a0f7'

    key256b = bytes.fromhex(key)
    ptB = bytes.fromhex(pt)
    aad12B = bytes.fromhex(aad)
    iv12B = bytes.fromhex(iv)

    aes256gcm = AESGCM(key256b)
    aes256gcm_ct_tag = aes256gcm.encrypt(iv12B, ptB, aad12B)
    aes256gcm_ct = aes256gcm_ct_tag[:-16]
    aes256gcm_tag = aes256gcm_ct_tag[-16:]
    aes256gcm_decrypt_pt = aes256gcm.decrypt(iv12B, aes256gcm_ct_tag, aad12B)
    print("GCM|ct={}".format(aes256gcm_ct.hex()))
    print("GCM|tag={}".format(aes256gcm_tag.hex()))
    print("GCM|decrypt_pt={}".format(aes256gcm_decrypt_pt.hex()))
    if ptB == aes256gcm_decrypt_pt:
        print("PASS")
    else:
        print("FAIL")