from gf2_mult.gf2_mult import Gf2Mult

# Check product (reversed ordered), no reduction
# x = '40000000000000000000000000000000' # 2
# y = '40000000000000000000000000000000' # 2
# z_exp = '20000000000000000000000000000000' # 4

# x = '80000000000000000000000000000000'
# y = '80000000000000000000000000000000'
# z_exp = '80000000000000000000000000000000'

# Multiply such that there product has only 1 reduction
# Output will reveal the reduction polynomial R
# x = '00000000000000000000000000000004'
# y = '10000000000000000000000000000000'
# z_exp = 'e1000000000000000000000000000000'

# All 1s
# x = 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
# y = 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
# z_exp = 'f402aaaaaaaaaaaaaaaaaaaaaaaaaaaa'

# Check MSB propagation
# x = '00000000000000000000000000000001'
# y = '00000000000000000000000000000001'
# z_exp = 'e6080000000000000000000000000003'

# Test vector
x = '8064be9d95faa0966f6c11b93d90f8e0'
y = '2831490428b356c7f5ef5bf31a8030f2'
z_exp = '75f2b750c5a1a69d91d45538c6fdfa39'

# x = 'edf9f78aa23cc988584e29974c65274e'
# y = '2831490428b356c7f5ef5bf31a8030f2'
# z_exp = '6d6c16647ba7facf1a1201e9881eb082'

x_b = bytes.fromhex(x)
y_b = bytes.fromhex(y)

gf2_mult = Gf2Mult()

z_long_division = gf2_mult.long_division(x_b, y_b)
z_russian_peasant = gf2_mult.russian_peasant(x_b, y_b)
z_bit_parallel = gf2_mult.bit_parallel(x_b, y_b)

print('z_exp={}'.format(z_exp))
print('z_long_division={}'.format(z_long_division.hex()))
print('z_russian_peasant={}'.format(z_russian_peasant.hex()))
print('z_bit_parallel={}'.format(z_bit_parallel.hex()))

if z_long_division == bytes.fromhex(z_exp):
    print("LongDivision|Test passed")
else:
    print("LongDivision|Test failed")

if z_russian_peasant == bytes.fromhex(z_exp):
    print("RussianPeasant|Test passed")
else:
    print("RussianPeasant|Test failed")

if z_bit_parallel == bytes.fromhex(z_exp):
    print("BitParallel|Test passed")
else:
    print("BitParallel|Test failed")