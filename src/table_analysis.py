# Product Table
# total_terms= 16384
# --------------------------------------------------
# Reduction Table
# total_xors (w/o combining)= 532
# max output_fan_in= 8
# max input_fan_out= 8
# --------------------------------------------------
# GF2Mult Table
# total_terms (w/o combining)= 40832
# max output_fan_in= 1008
# max input_fan_out= 528
# --------------------------------------------------
from gf2_mult.tables import Tables
from math import log, ceil

x_bytes = 16
y_bytes = 16
R_B = 0xe1000000000000000000000000000000.to_bytes(16, 'big')

tables = Tables(x_bytes, y_bytes, R_B)
reduce_table = tables.reduce_table
prod_table = tables.prod_table
gf2mult_table = tables.gf2mult_table

# for i in range(len(reduce_table)):
#     print('reduce_table|i={}|vec={}'.format(i, reduce_table[i]))
# for i in range(len(prod_table)):
#     print('prod_table|i={}|vec={}'.format(i, prod_table[i]))
# for i in range(len(gf2mult_table)):
#     print('gf2mult_table|i={}|vec={}'.format(i, gf2mult_table[i]))

# Stats
print('Product Table')
# note that each bitwise AND term is unique
total_terms = 0

for p in prod_table:
    terms = len(p)
    total_terms = total_terms + terms

# max fan in, max fanout, max terms can be easily derived
print('max output_fan_in= {}'.format(2*128))
print('max input_fan_out= {}'.format(128))
print('max terms= {}'.format(128))
print('total_terms= {}'.format(total_terms))
print('-'*50)

print('Reduction Table')
max_fan_in = 0
total_xors = 0
input_fan_out = [0]*256

for r in reduce_table:
    total_xors = total_xors + len(r) - 1

    for val in r:
        input_fan_out[val] = input_fan_out[val] + 1

    if len(r) > max_fan_in:
        max_fan_in = len(r)

print('total_xors (w/o combining)= {}'.format(total_xors))
print('max output_fan_in= {}'.format(max_fan_in))
print('max input_fan_out= {}'.format(max(input_fan_out)))
print('-'*50)

print('GF2Mult Table')
# note that each bitwise AND term is unique
total_terms = 0
max_terms = 0
max_fan_in = 0
input_fan_out = [0]*128

for g in gf2mult_table:
    terms = len(g)

    for tup in g:
        input_fan_out[tup[0]] = input_fan_out[tup[0]] + 1

    if terms > max_terms:
        max_terms = terms
    total_terms = total_terms + terms

# For each output bit, the same input bit can be used in multiple terms
print('total_terms (w/o combining)= {}'.format(total_terms))
print('LUTs= {}'.format(ceil(2*total_terms/6)))
print('max output_fan_in= {}'.format(2*max_terms))
print('max LUT chain= {}'.format(ceil(log(2*max_terms, 6))))
print('max input_fan_out= {}'.format(max(input_fan_out)))
print('-'*50)