# Tags are generated from reference cryptograph python library,
# and checked against standard and parallel implementations of GHASH.
#
from py_ref.aesgcm import AESGCM_PYLIB
from ghash import ghash
from ghash import ghash_par

key = 'd672e2280f5ee1f666e7c6b099dd704ceb2afd898e296de3f8325d2e88c23b71'
pt = '835dd1afc77b41ae141450025e5ac185b449a34d9d4ccee36c4b294a9289636967372eedf523b0c5792a89ca8660040662ba7835ffced7d02d0192432b63430a'

aad = '112233445566778899aabbcc'
iv = '4c47da5fe9a77e101ee7a0f7'
exp_tag = 'ecfb1479ede65b59fc47ec272a188dae'

key_B = bytes.fromhex(key)
aad_B = bytes.fromhex(aad)
iv_B = bytes.fromhex(iv)

pt_len = 32 # 2 blocks
pt_B = bytes.fromhex(pt)[0:pt_len]

aesgcm_pylib = AESGCM_PYLIB(key_B)
ct_tag = aesgcm_pylib.encrypt(iv_B, pt_B, aad_B)
ct  = ct_tag[:-16]
tag_ref = ct_tag[-16:]
decrypt_pt = aesgcm_pylib.decrypt(iv_B, ct_tag, aad_B)

# Manually generate the tag to check the intermediate values
tag_ghash = ghash.gen_tag(key_B, iv_B, aad_B, ct)
tag_ghash_par = ghash_par.gen_tag(key_B, iv_B, aad_B, ct)

print("GCM|tag_ghash={}".format(tag_ghash.hex()))
print("GCM|tag_ghash_par={}".format(tag_ghash_par.hex()))
print("GCM|ct={}".format(ct.hex()))
print("GCM|tag_ref={}".format(tag_ref.hex()))
print("GCM|decrypt_pt={}".format(decrypt_pt.hex()))

# Checks
if tag_ref.hex() == tag_ghash.hex():
    print("Tag pass")
else:
    print("Tag failed")

if tag_ref.hex() == tag_ghash_par.hex():
    print("Parallel Tag pass")
else:
    print("Parallel Tag failed")

if decrypt_pt == pt_B:
    print("Decryption pass")
else:
    print("Decryption fail")