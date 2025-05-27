module uart_tx (
    input  logic        clk,
    input  logic        rst,
    input  logic [7:0]  data,
    input  logic        data_valid,
    output logic        tx,
    output logic        ready
);
    parameter CLK_FREQ = 50000000;
    parameter BAUD_RATE = 115200;
    localparam CLKS_PER_BIT = CLK_FREQ / BAUD_RATE;

    typedef enum logic [2:0] {
        IDLE, START, DATA, STOP, CLEANUP
    } state_t;

    state_t state;
    logic [15:0] clk_count;
    logic [2:0]  bit_index;
    logic [7:0]  tx_data;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            state <= IDLE;
            tx <= 1;
            clk_count <= 0;
            bit_index <= 0;
            ready <= 1;
        end else begin
            case (state)
                IDLE: begin
                    tx <= 1;
                    clk_count <= 0;
                    bit_index <= 0;
                    ready <= 1;
                    if (data_valid) begin
                        tx_data <= data;
                        state <= START;
                        ready <= 0;
                    end
                end

                START: begin
                    tx <= 0;
                    if (clk_count == CLKS_PER_BIT - 1) begin
                        clk_count <= 0;
                        state <= DATA;
                    end else begin
                        clk_count <= clk_count + 1;
                    end
                end

                DATA: begin
                    tx <= tx_data[bit_index];
                    if (clk_count == CLKS_PER_BIT - 1) begin
                        clk_count <= 0;
                        if (bit_index == 7) begin
                            state <= STOP;
                        end else begin
                            bit_index <= bit_index + 1;
                        end
                    end else begin
                        clk_count <= clk_count + 1;
                    end
                end

                STOP: begin
                    tx <= 1;
                    if (clk_count == CLKS_PER_BIT - 1) begin
                        clk_count <= 0;
                        state <= CLEANUP;
                    end else begin
                        clk_count <= clk_count + 1;
                    end
                end

                CLEANUP: begin
                    state <= IDLE;
                end
            endcase
        end
    end
endmodule
