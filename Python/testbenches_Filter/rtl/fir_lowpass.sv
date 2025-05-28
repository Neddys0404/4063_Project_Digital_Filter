module fir_lowpass (
    input logic clk,
    input logic rst,
    input logic start_flg,
    input logic [7:0] inputSig [0:255], // 8-bit unsigned
    output logic rdy_flg,
    output logic [7:0] outputSig [0:255] // 8-bit unsigned
);

    localparam int TAPS = 50;
    localparam int FRAC_BITS = 14;
    logic signed [15:0] coeffs [0:TAPS-1];

    // Fixed-point coefficients (Q2.14), signed 16-bit
    initial begin
        coeffs[0] = 16'sd40;
        coeffs[1] = 16'sd43;
        coeffs[2] = 16'sd49;
        coeffs[3] = 16'sd60;
        coeffs[4] = 16'sd75;
        coeffs[5] = 16'sd94;
        coeffs[6] = 16'sd117;
        coeffs[7] = 16'sd143;
        coeffs[8] = 16'sd173;
        coeffs[9] = 16'sd206;
        coeffs[10] = 16'sd241;
        coeffs[11] = 16'sd278;
        coeffs[12] = 16'sd316;
        coeffs[13] = 16'sd355;
        coeffs[14] = 16'sd394;
        coeffs[15] = 16'sd432;
        coeffs[16] = 16'sd469;
        coeffs[17] = 16'sd504;
        coeffs[18] = 16'sd536;
        coeffs[19] = 16'sd565;
        coeffs[20] = 16'sd589;
        coeffs[21] = 16'sd609;
        coeffs[22] = 16'sd625;
        coeffs[23] = 16'sd636;
        coeffs[24] = 16'sd642;
        coeffs[25] = 16'sd642;
        coeffs[26] = 16'sd636;
        coeffs[27] = 16'sd625;
        coeffs[28] = 16'sd609;
        coeffs[29] = 16'sd589;
        coeffs[30] = 16'sd565;
        coeffs[31] = 16'sd536;
        coeffs[32] = 16'sd504;
        coeffs[33] = 16'sd469;
        coeffs[34] = 16'sd432;
        coeffs[35] = 16'sd394;
        coeffs[36] = 16'sd355;
        coeffs[37] = 16'sd316;
        coeffs[38] = 16'sd278;
        coeffs[39] = 16'sd241;
        coeffs[40] = 16'sd206;
        coeffs[41] = 16'sd173;
        coeffs[42] = 16'sd143;
        coeffs[43] = 16'sd117;
        coeffs[44] = 16'sd94;
        coeffs[45] = 16'sd75;
        coeffs[46] = 16'sd60;
        coeffs[47] = 16'sd49;
        coeffs[48] = 16'sd43;
        coeffs[49] = 16'sd40;
    end

    // Internal signed accumulator (wide enough to hold 51 * 255 * 2^14)
    logic signed [31:0] acc;
    integer i, j;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            for (i = 0; i < 256; i++) begin
                outputSig[i] <= 8'd0;
            end
            rdy_flg <= 0;
        end else if (start_flg) begin
            for (i = 0; i < 256; i++) begin
                acc = 0;
                for (j = 0; j < TAPS; j++) begin
                    if ((i - j) >= 0) begin
                        acc += $signed({8'd0, inputSig[i - j]}) * coeffs[j];
                    end
                end
                // Fixed-point adjustment: >> FRAC_BITS (Q2.14)
                acc = acc >>> FRAC_BITS;

                // Clamp to 8-bit unsigned output
                if (acc < 0)
                    outputSig[i] <= 8'd0;
                else if (acc > 255)
                    outputSig[i] <= 8'd255;
                else
                    outputSig[i] <= acc[7:0];

                rdy_flg <= 1;
            end
        end
    end

endmodule
