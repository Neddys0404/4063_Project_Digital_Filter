module fir_lowpass_filter (
    input logic clk,
    input logic rst,
    input logic [7:0] inputSig [0:255],
    output logic [7:0] outputSig [0:255]
);

    // Define FIR filter length
    localparam int TAPS = 51;

    // Coefficients as real constants
    real coeffs[TAPS] = '{
        0.00242698, 0.00259684, 0.00300694, 0.00366492, 0.00457305, 0.00572802, 0.00712089,
        0.00873714, 0.01055687, 0.01255514, 0.01470241, 0.01696509, 0.01930626, 0.02168639,
        0.02406419, 0.02639746, 0.02864405, 0.03076275, 0.0327142,  0.03446178, 0.0359724,
        0.03721727, 0.03817254, 0.03881982, 0.03914661, 0.03914661, 0.03881982, 0.03817254,
        0.03721727, 0.0359724,  0.03446178, 0.0327142,  0.03076275, 0.02864405, 0.02639746,
        0.02406419, 0.02168639, 0.01930626, 0.01696509, 0.01470241, 0.01255514, 0.01055687,
        0.00873714, 0.00712089, 0.00572802, 0.00457305, 0.00366492, 0.00300694, 0.00259684,
        0.00242698
    };

    // Internal real array for temporary convolution result
    real conv_result;
    int i, j;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            for (i = 0; i < 256; i++) begin
                outputSig[i] <= 8'd0;
            end
        end else begin
            for (i = 0; i < 256; i++) begin
                conv_result = 0.0;
                for (j = 0; j < TAPS; j++) begin
                    if ((i - j) >= 0)
                        conv_result += coeffs[j] * real'(inputSig[i - j]);
                end
                // Clamp and assign result to output
                if (conv_result < 0.0)
                    outputSig[i] <= 8'd0;
                else if (conv_result > 255.0)
                    outputSig[i] <= 8'd255;
                else
                    outputSig[i] <= $rtoi(conv_result);
            end
        end
    end

endmodule
