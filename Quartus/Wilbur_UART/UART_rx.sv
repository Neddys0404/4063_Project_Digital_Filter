module uart_rx (
    input  logic       clk,
    input  logic       rst,
    input  logic       rx,
    output logic [7:0] data,
    output logic       data_valid
);
    parameter CLK_FREQ = 50000000;
    parameter BAUD_RATE = 115200;
    localparam CLKS_PER_BIT = CLK_FREQ / BAUD_RATE;

    typedef enum logic [1:0] {
        IDLE, START, DATA, STOP
    } state_t;

    state_t state;
    logic [15:0] clk_count;
    logic [2:0]  bit_index;
    logic [7:0]  rx_data;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            state <= IDLE;
            data_valid <= 0;
            clk_count <= 0;
            bit_index <= 0;
        end else begin
            case (state)
                IDLE: begin
                    data_valid <= 0;
                    if (!rx) begin
                        state <= START;
                        clk_count <= 0;
                    end
                end

                START: begin
                    if (clk_count == CLKS_PER_BIT / 2) begin
                        if (!rx) begin
                            clk_count <= 0;
                            state <= DATA;
                            bit_index <= 0;
                        end else begin
                            state <= IDLE;  // false start
                        end
                    end else begin
                        clk_count <= clk_count + 1;
                    end
                end

                DATA: begin
                    if (clk_count == CLKS_PER_BIT - 1) begin
                        clk_count <= 0;
                        rx_data[bit_index] <= rx;
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
                    if (clk_count == CLKS_PER_BIT - 1) begin
                        state <= IDLE;
                        data <= rx_data;
                        data_valid <= 1;
                        clk_count <= 0;
                    end else begin
                        clk_count <= clk_count + 1;
                    end
                end
            endcase
        end
    end
endmodule
