from gf2_mult.gf2_mult import Gf2Mult
import secrets

gf2_mult = Gf2Mult()
N = 10000

for i in range(N):
    x_b = secrets.token_bytes(16)
    y_b = secrets.token_bytes(16)
    z_long_division = gf2_mult.long_division(x_b, y_b)
    z_bit_parallel = gf2_mult.bit_parallel(x_b, y_b)

    if z_long_division == z_bit_parallel:
        # print('x      | {}'.format(x_b.hex()))
        # print('y      | {}'.format(y_b.hex()))
        # print('longdiv| {}'.format(z_long_division.hex()))
        # print('bitPar | {}'.format(z_bit_parallel.hex()))
        pass
    else:
        print("Test failed")
        print('x      | {}'.format(x_b.hex()))
        print('y      | {}'.format(y_b.hex()))
        print('longdiv| {}'.format(z_long_division.hex()))
        print('bitPar | {}'.format(z_bit_parallel.hex()))
        break

print('Done!')
