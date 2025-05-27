module uart_block (
    input  logic       clk,
    input  logic       rst,
    input  logic       rx,
    input  logic [7:0] sigOut[0:255],
    output logic       tx,
    output logic [7:0] sigIn[0:255],
    output logic       rdy_flg
);

endmodule