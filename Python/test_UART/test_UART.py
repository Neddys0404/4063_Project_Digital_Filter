# import matplotlib.pyplot as plt
# import numpy as np
# import serial
# import threading
# import time

# global n, s, t
# n = 1  # number of periods
# s = 256  # samples per period of signal
# t = np.linspace(0, 0.0001*n, s*n, endpoint=False)

# def map_range(x, in_min, in_max, out_min, out_max):
#     return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# def read_from_port(ser):
#     while True:
#         if ser.in_waiting > 0:
#             try:
#                 data = ser.readline().decode('utf-8', errors='replace').strip()
#                 if data == "!!!":               # receiving protocol invoked
#                     try:

#                         sigRx = []
#                         while (data != "@@@"):      # trap in loop, continue receive until ending command received
#                             print("[WARNING] DO NOT PRESS ANYTHING! RECEIVING PROTOCOL INVOKED!")
#                             if ser.in_waiting > 0:
#                                 data = ser.readline().decode('utf-8', errors='replace').strip()
#                                 sigRx.append(int(data))     # cast to integer (assuming only 3 chars is received)
                                
#                             continue

#                         # Plot the result
#                         sigIn = np.array([])
#                         plt.figure(figsize=(12, 5))
#                         plt.plot(t, sigIn, label='Original Signal', linestyle='--', alpha=0.7)
#                         plt.plot(t, map_range(sigRx, 0, 255, -5, 5), label='Filtered Output', linewidth=2)
#                         plt.title("Digital Low-pass Filter Visualization")
#                         plt.xlabel("time")
#                         plt.ylabel("value")
#                         plt.legend()
#                         plt.grid(True)
#                         plt.tight_layout()
#                         plt.show()

#                     except Exception as e:
#                         print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
#                         print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
#                         print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
#                         print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
#                         print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
#                         print(f"[Error reading] {e}")

#                 else:
#                     print(f"[RX] {data}")
#             except Exception as e:
#                 print(f"[Error reading] {e}")
#         time.sleep(0.1)

# def main():
#     # Set your serial port and baud rate
#     port = input("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nEnter serial port (e.g., COM3 or /dev/ttyUSB0): ")
#     baud = input("\nEnter baud rate (e.g., 9600): ")

#     try:
#         ser = serial.Serial(port, int(baud), timeout=1)
#         print(f"[INFO] Opened {port} at {baud} baud.")
#     except Exception as e:
#         print(f"[ERROR] Could not open port: {e}")
#         return

#     # Start RX thread
#     rx_thread = threading.Thread(target=read_from_port, args=(ser,), daemon=True)
#     rx_thread.start()

#     print("[INFO] Type messages to send. Type 'exit' to quit.")
#     while True:
#         msg = input(">> ")
#         if msg.lower() == "exit":
#             print("[INFO] Closing port...")
#             break
#         try:
#             ser.write((msg + "\n").encode())
#         except Exception as e:
#             print(f"[ERROR writing] {e}")
    
#     ser.close()

# if __name__ == "__main__":
#     main()



# #!/usr/bin/env python3
# import serial
# import threading
# import time
# import csv
# import sys

# #––– Configuration –––#
# DEFAULT_BAUD = 115200
# LINE_DELAY   = 0.001   # seconds between sending lines

# def read_from_port(ser):
#     """Thread: continuously read lines from serial and print them."""
#     while True:
#         try:
#             line = ser.readline().decode('utf-8', errors='replace').rstrip()
#             if line:
#                 print(f"[RX] {line}")
#         except Exception as e:
#             print(f"[Error reading] {e}")
#         time.sleep(0.01)

# def send_csv(ser, path, delay=LINE_DELAY):
#     """Read CSV file at `path` and send each row as ASCII comma‐separated line."""
#     try:
#         with open(path, newline='') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 line = ",".join(row) + "\n"
#                 ser.write(line.encode('ascii'))
#                 ser.flush()
#                 print(f"[Sent CSV] {line.strip()}")
#                 time.sleep(delay)
#     except FileNotFoundError:
#         print(f"[ERROR] CSV file not found: {path}")
#     except Exception as e:
#         print(f"[ERROR] sending CSV: {e}")

# def main():
#     port = input("Serial port (e.g. COM4 or /dev/ttyUSB0): ").strip()
#     baud = input(f"Baud rate [{DEFAULT_BAUD}]: ").strip() or str(DEFAULT_BAUD)
#     try:
#         ser = serial.Serial(port, int(baud), timeout=1)
#     except serial.SerialException as e:
#         print(f"[ERROR] Could not open port {port}: {e}")
#         sys.exit(1)

#     print(f"[INFO] Opened {port} at {baud} baud.")
#     time.sleep(2)  # let the UART settle

#     # start reader thread
#     t = threading.Thread(target=read_from_port, args=(ser,), daemon=True)
#     t.start()

#     print("[INFO] Commands:")
#     print("  sendcsv <file>   Send every row of <file> as CSV lines")
#     print("  exit             Close port and quit")
#     print("  <anything else>  Sent as plain text line")

#     while True:
#         cmd = input(">> ").strip()
#         if not cmd:
#             continue
#         if cmd.lower() == "exit":
#             break
#         if cmd.lower().startswith("sendcsv "):
#             _, path = cmd.split(None, 1)
#             send_csv(ser, path)
#         else:
#             # send it as a simple text line
#             ser.write((cmd + "\n").encode())
#             ser.flush()
#             print(f"[Sent] {cmd}")

#     print("[INFO] Closing port...")
#     ser.close()

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
import serial
import threading
import time
import csv
import sys

#––– Configuration –––#
DEFAULT_BAUD = 115200
DELAY_BETWEEN_ROWS = 1.0   # seconds
#––––––––––––––––––––––#

def read_from_port(ser):
    """Continuously read lines from serial and print them."""
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='replace').rstrip()
            if line:
                print(f"[RX] {line}")
        except Exception as e:
            print(f"[Error reading] {e}")
        time.sleep(0.01)


def send_csv_second_column_as_byte(ser, path, delay=DELAY_BETWEEN_ROWS):
    """
    Read CSV file at `path`, skip header, and for each row:
      - parse the second column as a number (0–255)
      - send it as one raw byte
      - wait `delay` seconds
    """
    try:
        with open("./Python/test_UART/" + path, newline='') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # skip header
            for row in reader:
                if len(row) < 2:
                    print(f"[WARN] skipping malformed row: {row}")
                    continue
                try:
                    # parse B, clamp to 0–255, send as raw byte
                    val = int(float(row[1]))
                    if not 0 <= val <= 255:
                        raise ValueError("out of 0–255 range")
                except Exception as e:
                    print(f"[WARN] skipping row {row}: {e}")
                    continue

                ser.write(bytes([val]))
                print(f"checking : {bytes([val])}")
                ser.flush()
                print(f"[Sent byte] {val}")
                time.sleep(delay)
    except FileNotFoundError:
        print(f"[ERROR] CSV file not found: {path}")
    except Exception as e:
        print(f"[ERROR] sending CSV: {e}")


def main():
    port = input("Serial port (e.g. COM4 or /dev/ttyUSB0): ").strip()
    baud = input(f"Baud rate [{DEFAULT_BAUD}]: ").strip() or str(DEFAULT_BAUD)
    try:
        ser = serial.Serial(port, int(baud), timeout=1)
    except serial.SerialException as e:
        print(f"[ERROR] Could not open port {port}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Opened {port} at {baud} baud.")
    time.sleep(2)  # allow UART to settle

    # start background reader
    threading.Thread(target=read_from_port, args=(ser,), daemon=True).start()

    print("[INFO] Commands:")
    print("  sendcsv <file>   Send only column B as raw byte, 1 s per row")
    print("  exit             Close port and quit")
    print("  <anything else>  Sent as plain text line")

    while True:
        cmd = input(">> ").strip()
        if not cmd:
            continue
        if cmd.lower() == "exit":
            break

        if cmd.lower().startswith("sendcsv "):
            _, path = cmd.split(None, 1)
            send_csv_second_column_as_byte(ser, path)
        else:
            # fallback: send full text line
            ser.write((cmd + "\n").encode())
            ser.flush()
            print(f"[Sent text] {cmd}")

    print("[INFO] Closing port...")
    ser.close()


if __name__ == "__main__":
    main()

