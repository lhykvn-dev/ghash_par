from hw.gen_codeblock import gen_codeblock
import os

fn = os.path.join(os.path.dirname(__file__), 'hw', 'and_xor.sv')

start_block = '''
`timescale 1ns / 1ps

module and_xor(
    input clk,
    input [127:0] i_a,
    input [127:0] i_b,
    output [127:0] c
);
logic[127:0] c_i;
logic[127:0] c_r;
logic[127:0] a;
logic[127:0] b;

always @(posedge clk) begin
    a <= i_a;
    b <= i_b;
end
'''
end_block = '''
endmodule
'''

code_block = gen_codeblock()

with open(fn, "w") as f:
    f.write(start_block)
    f.write(code_block)
    f.write(end_block)