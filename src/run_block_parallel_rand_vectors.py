from py_ref.aesgcm import AESGCM_PYLIB
from ghash import ghash_par
import secrets

N = 1000
MAX_BLOCKS = 10

for i in range(N):
    blocks = secrets.randbelow(MAX_BLOCKS) + 1
    key_B = secrets.token_bytes(32)
    aad_B = secrets.token_bytes(12)
    iv_B = secrets.token_bytes(12)
    pt_B = secrets.token_bytes(16*blocks)

    aesgcm_pylib = AESGCM_PYLIB(key_B)
    ct_tag = aesgcm_pylib.encrypt(iv_B, pt_B, aad_B)
    ct  = ct_tag[:-16]
    tag_ref = ct_tag[-16:]
    tag_ghash_par = ghash_par.gen_tag(key_B, iv_B, aad_B, ct)

    if tag_ref.hex() == tag_ghash_par.hex():
        # print("key      | {}".format(key_B.hex()))
        # print("aad      | {}".format(aad_B.hex()))
        # print("iv       | {}".format(iv_B.hex()))
        # print("pt       | {}".format(pt_B.hex()))
        # print("ct       | {}".format(ct.hex()))
        # print("tag_ref  | {}".format(tag_ref.hex()))
        # print("tag_par  | {}".format(tag_ghash_par.hex()))
        pass
    else:
        print("key      | {}".format(key_B.hex()))
        print("aad      | {}".format(aad_B.hex()))
        print("iv       | {}".format(iv_B.hex()))
        print("pt       | {}".format(pt_B.hex()))
        print("ct       | {}".format(ct.hex()))
        print("tag_ref  | {}".format(tag_ref.hex()))
        print("tag_par  | {}".format(tag_ghash_par.hex()))
        print("Parallel Tag failed")
        break

print("Done!")