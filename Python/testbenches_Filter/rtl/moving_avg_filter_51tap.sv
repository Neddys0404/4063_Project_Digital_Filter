module moving_avg_filter_51tap (
    input  logic        clk,
    input  logic        rst,
    input  logic        start_flg,
    input  logic [7:0]  inputSig [0:255],
    output logic rdy_flg,
    output logic [7:0]  outputSig [0:255]
);

    // Internal variables
    logic [15:0] sum; // To hold the sum of up to 51 values (max 51*255 = 13005 < 2^14)
    integer i, j;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            for (i = 0; i < 256; i++) begin
                outputSig[i] <= 8'd0;
            end
            rdy_flg <= 0;
        end else if (start_flg) begin
            for (i = 0; i < 256; i++) begin
                sum = 0;
                if (i >= 50) begin
                    for (j = 0; j < 51; j++) begin
                        sum += inputSig[i - j];
                    end
                    outputSig[i] <= sum / 51;
                end else begin
                    // Optional: partial average or just zero padding
                    outputSig[i] <= 8'd0;
                end
            end

            rdy_flg <= 1;
        end
    end

endmodule