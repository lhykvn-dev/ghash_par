`timescale 1ns/1ps

module tb;
logic clk;
logic [127:0] a, b, c;

initial begin
    clk = 0;
    forever #5 clk = ~clk;
end

and_xor dut(
    .clk (clk),
    .i_a (a),
    .i_b (b),
    .c (c)
);

initial begin
    a = 0; b = 0;
    // Bytes in big endian
    drive_test( 128'h00000000000000000000000000000002,
                128'h00000000000000000000000000000002,
                128'h00000000000000000000000000000004);

    drive_test( 128'h071f09bc9d8836f669055fa9b97d2601,
                128'h4f0c0158cfdaf7afe36acd1420928c14,
                128'h9c5fbf631caa2b89b96585a30aed4fae);

    #50 $display("Tests Completed.");
    $finish;
end

task drive_test(input [127:0] t_a, input [127:0] t_b, input [127:0] t_c);
    @(posedge clk);
    a <= t_a;
    b <= t_b;

    @(posedge clk);
    @(posedge clk);
    #1;
    check_result(t_c);
endtask

function void check_result(input logic [127:0] t_c);
    if (c === t_c) begin
        $display("[PASS]");
        $display("EXP: %h", t_c);
        $display("ACT: %h", c);
    end else begin
        $display("[FAIL]");
        $display("EXP: %h", t_c);
        $display("ACT: %h", c);
    end
endfunction

endmodule