
import serial
import time

# Open serial port
ser = serial.Serial(
    port='/dev/cu.usbserial-0001',      # Change to your Arduino port
    baudrate=9600,
    timeout=1
)

# Wait for Arduino reset
time.sleep(2)

while True:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        print("Line: " + line)