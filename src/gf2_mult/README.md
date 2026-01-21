# Bit-Parallel GF2 reduction AES-GCM example

## Notation
```
Irreducible polynomial, R = x^128 + x^7 + x^2 + x + 1
256-bit product input, I
128-bit reduced output, O
```

## Formulation
Following the long division method, consider that the significant bits of `I` will effect subsequent bits by the polynomial `R`.
```
I[255]: O[134], O[129], O[128], O[127]
```
Of note, the first output bit toggled is `O[255-(128-7)] = O[134]`, by applying the `x^7` polynomial to `I[255]`.

Also, outputs in the range `O[134]` to `O[128]` would be further reduced, toggling output bits in the range `O[134-(128-7)]=O[13]` to `O[0]`.
```
O[134]: O[13], O[8], O[7], O[6]
```
Conversely, we can find the set of input bits for each output bit.
```
O[134]: xor(I[255], I[134])
...
O[127]: xor(I[255], I[254], I[253], I[248], I[127])
...
O[14]: xor(I[142], I[141], I[140], I[135], I[14])
```
For O[13] to O[0], also consider the calculated outputs from `O[134] to O[128]` as noted earlier.

If the set contains `I[134]` to `I[14]`, unfold them from the corresponding `O[134]` to `O[14]`
```
O[13]: xor(I[141], I[140], I[139], I[134], I[13])
Folding I[134],
O[13]: xor(I[141], I[140], I[139], (I[255], I[134]), I[13])
```
Finally take output bits `O[0]` to `O[127]` as the final reduced output.

A generic algorithm is implemented in the `gen_reduction_table` method in`tables.py`, for any given irreducible polynomial R, and input bit length

## Analysis
From `table_analysis.py` script,
```
Product Table: each entry is a list of tuples representing the bitwise AND terms,
followed by a bitwise XOR of all tuples in the list.
max output_fan_in= 256
max input_fan_out= 128
max terms= 128
total_terms= 16384
--------------------------------------------------
Reduction Table: each entry is a list of integers representing the bitwise XORs of input bits
total_xors (w/o combining)= 532
max output_fan_in= 8
max input_fan_out= 8
--------------------------------------------------
GF2Mult Table: combines product and reduction tables to a single table
total_terms (w/o combining)= 40832
max output_fan_in= 1008
max LUT chain= 4
max input_fan_out= 528
--------------------------------------------------
```
Following the formulation, for a irreducible polynomial R, the distance between the 2 largest monomials, and the number of monomials both contribute to the overall number of XOR terms. The number of XOR terms increase directly as the weight increases. A large distance results in less folding of intermediate output terms. Since R is sparse and asymetric with monomials concentrated close to 0, the overall number of XOR terms for the reduction table is small.

While the reduction table alone is relatively efficient, a fully parallelizable GF2Mult table is large due to the resource heavy product table.

If implemented using LUT6 primitives, the max levels of logic is `log6(1008) = 4`, making it feasible for Ultrascale+ devices.