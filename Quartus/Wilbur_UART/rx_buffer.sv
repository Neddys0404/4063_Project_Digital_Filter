module rx_buffer (
    input  logic        clk,
    input  logic        rst,
    input  logic [7:0]  data_in,      // char from uart_rx
    input  logic        data_valid,   // valid flag from uart_rx
    output logic [7:0]  outputSig [0:255],
    output logic        done          // goes high when all 256 values are loaded
);
    typedef enum logic [1:0] {
        IDLE, LOAD1, LOAD2, LOAD3
    } state_t;

    state_t state;

    logic [7:0] char_buffer[2:0];  // Store the 3 chars for one value
    logic [1:0] char_count;        // 0 to 2
    logic [7:0] value_count;       // 0 to 255
    logic       all_done;

    // Digit values (ASCII '0'-'9' to 0-9)
    logic [3:0] digit0, digit1, digit2;
    logic [7:0] int_value;

    // FSM and logic
    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            char_count <= 0;
            value_count <= 0;
            state <= IDLE;
            all_done <= 0;
        end else if (!all_done) begin
            case (state)
                IDLE: begin
                    if (data_valid) begin
                        char_buffer[0] <= data_in;
                        char_count <= 1;
                        state <= LOAD2;
                    end
                end

                LOAD2: begin
                    if (data_valid) begin
                        char_buffer[1] <= data_in;
                        char_count <= 2;
                        state <= LOAD3;
                    end
                end

                LOAD3: begin
                    if (data_valid) begin
                        char_buffer[2] <= data_in;

                        // Convert and store into outputSig
                        digit2 <= char_buffer[0] - "0";
                        digit1 <= char_buffer[1] - "0";
                        digit0 <= data_in          - "0";

                        int_value <= (digit2 * 100) + (digit1 * 10) + digit0;
                        outputSig[value_count] <= (digit2 * 100) + (digit1 * 10) + digit0;

                        // Increment pointer or finish
                        if (value_count == 8'd255) begin
                            all_done <= 1;
                        end else begin
                            value_count <= value_count + 1;
                        end

                        state <= IDLE;
                    end
                end

                default: state <= IDLE;
            endcase
        end
    end

    assign done = all_done;

endmodule
