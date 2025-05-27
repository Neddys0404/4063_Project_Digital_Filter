module SignalSender (
    input  logic        clk,           // Clock signal
    input  logic        rst,           // Active-high reset
    input  logic [7:0]  outbytes [0:255], // Input data to transmit
    output logic [7:0]  outputQuantSig,   // Output byte to signal buffer
    output logic        dataRdyFlg,       // High when outputQuantSig is valid
    output logic        dataEndFlg        // High when last byte is being sent
);

    logic [7:0] sendIndex;  // Keeps track of current byte being sent
    logic       sending;    // Indicates sending state

    always_ff @(posedge clk) begin
        if (rst) begin
            sendIndex       <= 0;
            outputQuantSig  <= 8'd0;
            dataRdyFlg      <= 0;
            dataEndFlg      <= 0;
            sending         <= 1;
        end else if (sending) begin
            outputQuantSig <= outbytes[sendIndex];
            dataRdyFlg     <= 1;

            // Assert dataEndFlg only for the last byte
            if (sendIndex == 8'd255) begin
                dataEndFlg <= 1;
                sending    <= 0; // stop sending after last byte
            end else begin
                dataEndFlg <= 0;
                sendIndex  <= sendIndex + 1;
            end
        end else begin
            // After sending is done, hold flgs low
            dataRdyFlg <= 0;
            dataEndFlg <= 0;
        end
    end

endmodule
