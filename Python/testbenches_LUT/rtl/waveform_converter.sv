module waveform_converter (
    input logic clk,
    input logic rst,
    input logic start_flg,
    input logic [3:0] sw, // One-hot: 0001=sine, 0010=triangle, 0100=square, 1000=FM
    input logic [7:0] inputQuantSig [0:255],
    output logic rdy_flg,
    output logic [7:0] outputQuantSig [0:255]
);

    integer val;
    integer i;
    integer step_size;
    integer pos;
    logic fm_bit;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            for (i = 0; i < 256; i++)
                outputQuantSig[i] <= 8'd0;
            rdy_flg <= 0;
        end else if (start_flg) begin
            case (sw)
                4'b0001: begin // Sine (just copy)
                    for (i = 0; i < 256; i++)
                        outputQuantSig[i] <= inputQuantSig[i];
                end
                4'b0010: begin // Triangle wave
                    val <= inputQuantSig[0];
                    for (i = 0; i < 255; i++) begin
                        if (outputQuantSig[i] >= outputQuantSig[i + 1]) begin
                            if (val >= 0)
                                val <= val - 2;
                    
                        end else begin
                            if (val < 255)
                                val <= val + 2;
                        end
                        outputQuantSig[i] <= val;
                    end
                    outputQuantSig[255] <= outputQuantSig[254];
                end
                4'b0100: begin // Square wave
                    for (i = 0; i < 256; i++)
                        outputQuantSig[i] <= (inputQuantSig[i] >= 128) ? 8'd255 : 8'd0;
                end
                4'b1000: begin // Frequency Modulated wave (simulated)
                    pos = 0;
                    fm_bit = 0;
                    for (i = 0; i < 256; i++) begin
                        // Higher sine value = faster change
                        // Map [0, 255] to [1, 51] steps (low freq = slow change, high freq = fast toggle)
                        step_size = 51 - (inputQuantSig[i] * 50) / 255;
                        pos += 1;
                        if (pos >= step_size) begin
                            fm_bit = ~fm_bit;
                            pos = 0;
                        end
                        outputQuantSig[i] <= fm_bit ? 8'd255 : 8'd0;
                    end
                end
                default: begin
                    for (i = 0; i < 256; i++)
                        outputQuantSig[i] <= 8'd0;
                end
            endcase

            rdy_flg <= 1;
        end
    end
endmodule
