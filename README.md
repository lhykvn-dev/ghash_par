# Bit-parallel, Block-parallel GHASH for AES-GCM
Authentication is a potential performance bottleneck for AES-GCM due to the sequential structure between GHASH blocks, and the GF2 multiplication in each block. A block parallel method is proposed to break the sequential dependency between GHASH blocks, and a bit parallel method is proposed to speed up the GF2 multiplication. While both methods are independent, implementing both together yields a fully parallelized design of scalable XOR-AND operations.

The bit parallel method is implemented in RTL and synthesized at 450 MHz for `xcku5p-ffvb676-2-e` Kintex Ultrascale+ FPGA, achieving 57.6 Gbps throughput, 2.22 ns latency and with a CLB LUT utilization of 7362 (3.39%). With block parallelism, throughput and utilization scale linearly, with minimal latency cost.

## Block Parallelism
Block parallelism breaks the GHASH sequential dependency by distributing the GF2 multiplcation across GHASH blocks, giving rise to the equation:
```
Yn = X1.H^n + X2.H(n-1) + ... + Xn.H, where
Xi in the input of the i-th sequential GHASH block,
Yj is the output of the j-th sequential GHASH block,
and H^k is the k-th power of the hashkey H.
```
Each `Xi.H^k` term can be computed in parallel, and the final result is the XOR of all X.H terms.
Furthermore, powers of the hashkey H can be precomputed.

## Bit Parallelism
GF2 multiplcation can be implemented as a series of parallelizable shift-xors, followed by modulo reduction. The formulation of the proposed bit parallel reduction method takes the iterative long division modulo reduction, and reduces it to a set of bitwise operations. Due to the sparcity and asymetry of the irreducible polynomial, the bitwise parallel method is also resource efficient. More details in `src/gf2_mult/README.md`

## Python Code
Dependency: Python, uv

Comparison between reference cryptography python library, sequential and block parallel GHASH
```
uv run python src/run_block_parallel.py
```
Comparison between long division, russian peasant and bit parallel GF2 reduction
```
uv run python src/run_bit_parallel.py
```
Bit-parallel GF2 Multiplication hardware analysis
```
uv run python src/table_analysis.py
```
Random vector tests
```
uv run python src/run_bit_parallel_rand_vectors.py
uv run python src/run_block_parallel_rand_vectors.py
```
### RTL
Dependency: Vivado 2025.2

Bit-parallel GF2 Multiplication Systemverilog code generation.
```
uv run python src/gen_sv.py
```
Run Vivado Synthesis
```
vivado -mode batch -source run_synth.tcl
```
Synthesis reports generated design in `synth_out`

## Use Cases
- NSE replacing the MD5 with AES-GCM authentication tag: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/TP_CUR_Trimmed_NNF_PROTOCOL_6.1.pdf
    - Tag is inserted at the payload header, instead of appending after the payload, resulting in a potential latency bottleneck as the tag is calculated over the entire payload first.
    - Further optimizations
        - Consider static blocks as blocks that consist of only static order fields, and dynamic blocks as blocks that contain dynamic order fields.
        - Static Blocks: `Xi.H^k` terms are precomputed and XOR'ed together with AAD and J0 blocks to generate a partial tag
        - Dynamic Blocks: `Xi.H^k` terms are computed in parallel, and XOR'ed with the partial tag to generate the final tag

## Relevant Resources
- AES-CTR spec: https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-38a.pdf
- AES-GCM spec: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf
- GCM validation: https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/cavp-testing-block-cipher-modes#GCMVS
- AES-GCM block diagram: https://upload.wikimedia.org/wikipedia/commons/2/25/GCM-Galois_Counter_Mode_with_IV.svg
