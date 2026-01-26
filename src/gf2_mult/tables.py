# Generates the XOR-AND tables for GF2 multiplication
class Tables():
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
        self.reduce_table = self.gen_reduction_table(self.R_B, 8*(x_bytes + y_bytes))
        self.prod_table = self.gen_prod_table()
        self.gf2mult_table = self.gen_gf2mult_table()

    def gen_prod_table(self):
        """
        Bits ordered from left to right
        Outputs a 255-entry product table
        Each entry is the logical function of a output bit,
        represented by a list of tuples.
        Each tuple is a bitwise AND of 2 input bits,
        followed by a bitwise XOR of all tuples in the list.
        """
        prod_table = []
        for i in range(8*(self.x_bytes + self.y_bytes)-1):
            vec = []
            for j in range(i+1):
                if j < self.x_bytes*8 and i-j < self.y_bytes*8:
                    vec.append((j, i-j))
            prod_table.append(vec)

        # for i in range(255):
        #     print('{}: {}'.format(i, prod_table[i]))
        # print(len(prod_table))
        return prod_table

    def gen_gf2mult_table(self) -> list:
        '''
        Combines product and reduction tables to a single gf2mult table
        '''
        table = []
        for vec in self.reduce_table:
            a = []
            for val in vec:
                if val < 255: # last bit padded
                    a.extend(self.prod_table[val])
            table.append(a)
        return table

    def gen_reduction_table(self, R: bytes, in_bits: int) -> list:
        '''
        Generates a reduction table for a given reduction polynomial R and input bit length in_bits.
        Each entry is a list representing by the bitwise XORs of input bits.
        '''
        degree = 8*len(R)
        r_b = ''.join(f'{byte:08b}' for byte in R)
        L, r_vec = self._find_distance_vector(r_b)
        table_len = in_bits - L
        fold_len = table_len - L
        table = [0]*table_len

        for i in range(table_len):
            vec = list()
            for poly in r_vec:
                val = i + degree - poly
                if val <= in_bits-1 and val >= degree:
                    vec.append(val)
            vec.append(i)
            table[i] = vec

        # Decrement for multiple folds
        for i in range(fold_len, -1, -1):
            for val in table[i]:
                if val < table_len and val >= degree and val is not i:
                    for fold_val in table[val]:
                        if fold_val is not val:
                            # xor(a,a) = 0
                            if fold_val not in table[i]:
                                table[i].append(fold_val)
                            else:
                                table[i].remove(fold_val)
        return table[0:degree]

    def apply_product_table(self, x_B: bytes, y_B: bytes, table: list) -> bytes:
        '''
        Bits ordered from left to right
        Output length is 255 bits, left-shift to make it byte ordered
        '''
        x_b = self._bytes2binstr(x_B)
        y_b = self._bytes2binstr(y_B)
        z_b = ''
        for vec in table:
            bit = False
            for j in vec:
                bit ^= (x_b[j[0]] == '1') and (y_b[j[1]] == '1')

            if bit:
                z_b += '1'
            else:
                z_b += '0'

        z_b += '0'
        z = int(z_b, 2)
        return z

    def apply_reduce_table(self, x_B: bytes, table: list) -> bytes:
        '''
        Bits ordered from left to right
        '''
        x_b = self._bytes2binstr(x_B)
        z_b = ''
        for v in table:
            bit = False
            for val in v:
                bit ^= (x_b[val] == '1')
            if bit:
                z_b += '1'
            else:
                z_b += '0'
        z = int(z_b, 2)
        z_B = z.to_bytes(16, 'big')
        return z_B

    def apply_gf2mult_table(self, x_B: bytes, y_B: bytes, table: list) -> bytes:
        '''
        Bits ordered from left to right
        '''
        x_b = self._bytes2binstr(x_B)
        y_b = self._bytes2binstr(y_B)
        z_b = ''
        for vec in table:
            bit = False
            for j in vec:
                bit ^= (x_b[j[0]] == '1') and (y_b[j[1]] == '1')

            if bit:
                z_b += '1'
            else:
                z_b += '0'
        z = int(z_b, 2)
        return z

    def _find_distance_vector(self, r_b: str) -> tuple[int, list]:
        '''
        Returns list of polynomials, and
        distance between the first 2 polynomials
        '''
        x = 0
        vec = list()
        for i in range(len(r_b)):
            if r_b[i]=='1':
                x=i
                vec.append(i)
        return len(r_b)-x, vec

    def _bytes2binstr(self, bytes_data):
        return ''.join(f'{byte:08b}' for byte in bytes_data)
