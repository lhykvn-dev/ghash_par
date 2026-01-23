from gf2_mult.tables import Tables

def gen_codeblock():
    table = Tables().gf2mult_table
    code_block = ''

    for i in range(len(table)):
        code_block += 'assign c_i[{}]='.format(i)
        for j in range(len(table[i])):
            code_block += '(a[{}]&b[{}])'.format(table[i][j][0], table[i][j][1])
            if j != len(table[i])-1:
                code_block += '^'
        code_block += ';\n'

    code_block += '''
always @(posedge clk) begin
    c_r <= c_i;
end
assign c = c_r;
'''
    return code_block