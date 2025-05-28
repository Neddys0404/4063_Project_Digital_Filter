module SignalSender (
    input  logic        clk,           	// Clock signal
    input  logic        rst,           	// Active-high reset
	 input  logic			startFlg,			// Active-high start flag
    input  logic [7:0]  outbytes [0:255], // Input data to transmit
    output logic [7:0]  outputQuantSig,   // Output byte to signal buffer
    output logic        dataRdyFlg,       // High when outputQuantSig is valid
	 output logic 			endFlg
);

    logic [7:0] sendIndex;  // Keeps track of current byte being sent
    logic       sending;    // Indicates sending state

    always_ff @(posedge clk) begin
        if (rst) begin
            sendIndex       <= 0;
            outputQuantSig  <= 8'd0;
            dataRdyFlg      <= 0;
				endFlg			 <= 0;
            sending         <= 1;
        end else if (sending && startFlg) begin
            outputQuantSig <= outbytes[sendIndex];
            dataRdyFlg     <= 1;

            if (sendIndex == 8'd255) begin
                sending    <= 0; // stop sending after last byte
            end else begin
                sendIndex  <= sendIndex + 1;
            end
        end else begin
            // After sending is done, rst
            dataRdyFlg 		 <= 0;
				endFlg 			 <= 1;
				sendIndex       <= 0;
            outputQuantSig  <= 8'd0;
            dataRdyFlg      <= 0;
            sending         <= 1;
        end
    end

endmodule
