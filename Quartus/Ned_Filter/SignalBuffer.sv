module SignalBuffer (
    input  logic        clk,              // Clock signal
    input  logic        dataRdyFlg,       // Active high: indicates inputQuantSig is ready to be saved
    input  logic [7:0]  inputQuantSig,    // Incoming byte
    input  logic        rst,              // Active High: Rst index n output 
    output logic [7:0]  outputSig [0:255], // Output array to store bytes
    output logic        dataSavedFlg
);

    logic [7:0] writeIndex;           // Index for writing into outputSig
    logic       dataSaved;      // Previous value of dataEndFlg for edge detection

    always_ff @(posedge clk or posedge rst) begin
        // Detect negedge of dataEndFlg
        if (rst == 1) begin
            writeIndex <= 0;
            dataSaved <= 0;
            for (int i = 0; i < 256; i++) begin
                outputSig[i] <= 8'd0;
            end
        end
        else if (dataRdyFlg) begin
            outputSig[writeIndex] <= inputQuantSig;
            writeIndex <= writeIndex + 1;
            dataSaved <= 1;
        end

        assign dataSavedFlg = dataSaved;
    end

endmodule