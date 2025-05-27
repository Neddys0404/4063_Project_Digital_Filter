import matplotlib.pyplot as plt
import numpy as np
import serial
import threading
import time

global n, s, t
n = 1  # number of periods
s = 256  # samples per period of signal
t = np.linspace(0, 0.0001*n, s*n, endpoint=False)

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def read_from_port(ser):
    while True:
        if ser.in_waiting > 0:
            try:
                data = ser.readline().decode('utf-8', errors='replace').strip()
                if data == "!!!":               # receiving protocol invoked
                    try:

                        sigRx = []
                        while (data != "@@@"):      # trap in loop, continue receive until ending command received
                            print("[WARNING] DO NOT PRESS ANYTHING! RECEIVING PROTOCOL INVOKED!")
                            if ser.in_waiting > 0:
                                data = ser.readline().decode('utf-8', errors='replace').strip()
                                sigRx.append(int(data))     # cast to integer (assuming only 3 chars is received)
                                
                            continue

                        # Plot the result
                        sigIn = np.array([])
                        plt.figure(figsize=(12, 5))
                        plt.plot(t, sigIn, label='Original Signal', linestyle='--', alpha=0.7)
                        plt.plot(t, map_range(sigRx, 0, 255, -5, 5), label='Filtered Output', linewidth=2)
                        plt.title("Digital Low-pass Filter Visualization")
                        plt.xlabel("time")
                        plt.ylabel("value")
                        plt.legend()
                        plt.grid(True)
                        plt.tight_layout()
                        plt.show()

                    except Exception as e:
                        print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
                        print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
                        print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
                        print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
                        print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
                        print(f"[Error reading] {e}")

                else:
                    print(f"[RX] {data}")
            except Exception as e:
                print(f"[Error reading] {e}")
        time.sleep(0.1)

def main():
    # Set your serial port and baud rate
    port = input("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nEnter serial port (e.g., COM3 or /dev/ttyUSB0): ")
    baud = input("\nEnter baud rate (e.g., 9600): ")

    try:
        ser = serial.Serial(port, int(baud), timeout=1)
        print(f"[INFO] Opened {port} at {baud} baud.")
    except Exception as e:
        print(f"[ERROR] Could not open port: {e}")
        return

    # Start RX thread
    rx_thread = threading.Thread(target=read_from_port, args=(ser,), daemon=True)
    rx_thread.start()

    print("[INFO] Type messages to send. Type 'exit' to quit.")
    while True:
        msg = input(">> ")
        if msg.lower() == "exit":
            print("[INFO] Closing port...")
            break
        try:
            ser.write((msg + "\n").encode())
        except Exception as e:
            print(f"[ERROR writing] {e}")
    
    ser.close()

if __name__ == "__main__":
    main()

