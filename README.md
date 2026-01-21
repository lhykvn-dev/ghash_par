# Bit-parallel, Block-parallel GHASH for AES-GCM
Authentication is a potential performance bottleneck for AES-GCM due to the sequential structure between GHASH blocks, and the GF2 multiplication in each block. This repository introduces 2 hardware parallelism methods to speed up the generation of the authentication tag.While both methods are independent, implementing both together yields a fully parallelized design of only bitwise XOR-AND operations.

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
GF2 multiplcation can be implemented as a series of parallelizable shift-xors, followed by modulo reduction. The formulation of this bit parallel method takes the iterative long division modulo reduction, and reduces it to a set of bitwise operations. Due to the sparcity and asymetry of the irreducible polynomial, the bitwise parallel method is also resource efficient. More details in `src/gf2_mult/README.md`

## Python
Dependency: uv
```
# Comparison between reference cryptography python library, sequential and block parallel GHASH
uv run python src/run_block_parallel.py

# Comparison between long division, russian peasant and bit parallel GF2 reduction
uv run python src/run_bit_parallel.py

# Bit-parallel table analysis
uv run python src/table_analysis.py

# Random vector tests
uv run python src/run_bit_parallel_rand_vectors.py
uv run python src/run_block_parallel_rand_vectors.py
```

## Use Cases
- NSE replacing the MD5 with AES-GCM authentication tag: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/TP_CUR_Trimmed_NNF_PROTOCOL_6.1.pdf
    - Tag is inserted at the payload header, instead of appending after the payload, resulting in a potential latency bottleneck on the critical path.
    - Further optimizations
        - Consider static blocks as blocks that consist of only static order fields, and dynamic blocks as blocks that contain dynamic order fields.
        - Static Blocks: `Xi.H^k` terms are precomputed and XOR'ed together with AAD and J0 blocks to generate a partial tag
        - Dynamic Blocks: `Xi.H^k` terms are computed in parallel, and XOR'ed with the partial tag to generate the final tag

## Relevant Resources
- AES-CTR spec: https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-38a.pdf
- AES-GCM spec: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf
- GCM validation: https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/cavp-testing-block-cipher-modes#GCMVS
- AES-GCM block diagram: https://upload.wikimedia.org/wikipedia/commons/2/25/GCM-Galois_Counter_Mode_with_IV.svg

## TODOs
- Add hardware implementation