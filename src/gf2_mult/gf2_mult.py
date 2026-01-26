# Notes
# - bit order is reversed from left to right
# - product output is 255-bits, zero-padding on the right to 256-bits (32 bytes)
from .tables import Tables

class Gf2Mult():
    def __init__(self,
        x_bytes = 16,
        y_bytes = 16,
        R_B = 0xe1000000000000000000000000000000.to_bytes(16, 'big')):

        self.x_bytes = x_bytes
        self.y_bytes = y_bytes
        self.R_B = R_B
        self.r_bytes = len(self.R_B)
        self.r_bits = 8*self.r_bytes
        self.z_bytes = x_bytes + y_bytes - self.r_bytes

        self.tables = Tables(x_bytes, y_bytes, R_B)
        self.reduce_table = self.tables.reduce_table
        self.prod_table = self.tables.prod_table
        self.gf2mult_table = self.tables.gf2mult_table

    def russian_peasant(self, x_B: bytes, y_B: bytes) -> bytes:
        x = int.from_bytes(x_B, 'big')
        y = int.from_bytes(y_B, 'big')
        r = int.from_bytes(self.R_B, 'big')
        z = 0
        for i in range(self.r_bits):
            if (x >> (self.r_bits - 1 - i)) & 1:
                z ^= y
            if y & 1:
                y = (y >> 1) ^ r
            else:
                y >>= 1
        return z.to_bytes(self.z_bytes, 'big')

    def long_division(self, x_B: bytes, y_B: bytes) -> bytes:
        r = int.from_bytes(self.R_B, 'big')
        z = self._product(x_B, y_B) # using shift-xor iterations
        # z = self.tables.apply_product_table(x_B, y_B, self.prod_table)

        for i in range(self.r_bits): # Reduce
            if (z >> i) & 1:
                z ^= r << i+1

        return z.to_bytes(32, 'big')[0:self.z_bytes]

    def bit_parallel(self, x_B: bytes, y_B: bytes) -> bytes:
        # # Applying Product and Reduce Tables seperately
        # # z = self._product(x_B, y_B) # using shift-xor iterations
        # z = self.tables.apply_product_table(x_B, y_B, self.prod_table)
        # prod_bytes = self.x_bytes + self.y_bytes
        # z = self.tables.apply_reduce_table(z.to_bytes(prod_bytes, 'big'), self.reduce_table)

        # Applying combined GF2 multiplication table
        z = self.tables.apply_gf2mult_table(x_B, y_B, self.gf2mult_table).to_bytes(self.r_bytes, 'big')
        return z

    def _product(self, x_B: int, y_B: int):
        """
        Bits ordered from left to right
        """
        x = int.from_bytes(x_B, 'big')
        y = int.from_bytes(y_B, 'big')
        z = 0
        for i in range(self.r_bits):
            if (y >> i) & 1:
                z ^= x << (i+1)
        return z

    def _binstr2vec(self, binstr: str) -> list:
        vec = []
        for i in range(len(binstr)):
            if binstr[i] == '1':
                vec.append(i)
        return vec

