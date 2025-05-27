module fir_lowpass_filter (
    input logic clk,
    input logic rst,
    input logic start_flg,
    input logic [7:0] inputSig [0:255], // 8-bit unsigned
    output logic rdy_flg,
    output logic [7:0] outputSig [0:255] // 8-bit unsigned
);

    localparam int TAPS = 51;
    localparam int FRAC_BITS = 14;

    // Fixed-point coefficients (Q2.14), signed 16-bit
    logic signed [15:0] coeffs [0:TAPS-1] = '{
        16'sd40, 16'sd43, 16'sd49, 16'sd60, 16'sd75, 16'sd94, 16'sd117,
        16'sd143, 16'sd173, 16'sd206, 16'sd241, 16'sd278, 16'sd316, 16'sd355,
        16'sd394, 16'sd432, 16'sd469, 16'sd504, 16'sd536, 16'sd565, 16'sd589,
        16'sd609, 16'sd625, 16'sd636, 16'sd642, 16'sd642, 16'sd636, 16'sd625,
        16'sd609, 16'sd589, 16'sd565, 16'sd536, 16'sd504, 16'sd469, 16'sd432,
        16'sd394, 16'sd355, 16'sd316, 16'sd278, 16'sd241, 16'sd206, 16'sd173,
        16'sd143, 16'sd117, 16'sd94, 16'sd75, 16'sd60, 16'sd49, 16'sd43, 16'sd40
    };

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
