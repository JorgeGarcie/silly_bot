import sys
import serial


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else "COM3"
    baud = int(sys.argv[2]) if len(sys.argv) > 2 else 115200
    ser = serial.Serial(port, baud, timeout=1)
    print(f"reading {port} @ {baud}")
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            print(line)


if __name__ == "__main__":
    main()
