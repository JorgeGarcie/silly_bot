
import serial
import time

import analyze_sounds as ana
# Open serial port
ser = serial.Serial(
    port='/dev/cu.usbmodem101',      # Change to your Arduino port
    baudrate=115200,
    timeout=1
)

# Wait for Arduino reset
time.sleep(2)

while True:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        if "F0" not in line:
            print(line, end = " | ")
            try:
                a = float(line)
                print(ana.identify_note(a))
            except Exception as e:
                pass