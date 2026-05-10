
import serial
import time

import analyze_sounds as ana

import subprocess

# Open serial port
ser = serial.Serial(
    port='/dev/cu.usbmodem101',      # Change to your Arduino port
    baudrate=115200,
    timeout=1
)

d = {'c2': 1, 'c#2': 2, 'd2': 3, 'd#2': 4, 'e2': 5, 'f2': 6, 'f#2': 7, 'g2': 8, 'g#2': 9, 'a2': 10, 'a#2': 11, 'b2': 12, 'c3': 13, 'c#3': 14, 'd3': 15, 'd#3': 16, 'e3': 17, 'f3': 18, 'f#3': 19, 'g3': 20, 'g#3': 21, 'a3': 22, 'a#3': 23, 'b3': 24, 'c4': 25, 'c#4': 26, 'd4': 27, 'd#4': 28, 'e4': 29, 'f4': 30, 'f#4': 31, 'g4': 32, 'g#4': 33, 'a4': 34, 'a#4': 35, 'b4': 36, 'c5': 37, 'c#5': 38, 'd5': 39, 'd#5': 40, 'e5': 41, 'f5': 42, 'f#5': 43, 'g5': 44, 'g#5': 45, 'a5': 46, 'a#5': 47, 'b5': 48, 'c6': 49, 'c#6': 50, 'd6': 51, 'd#6': 52, 'e6': 53, 'f6': 54, 'f#6': 55, 'g6': 56, 'g#6': 57, 'a6': 58, 'a#6': 59, 'b6': 60, 'c7': 61}
# Wait for Arduino reset
time.sleep(2)
time_count = 0
while True:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        if "F0" not in line:
            print(line, end = " | ")
            try:
                a = float(line)
                note = ana.identify_note(a)
                print(note)
                conv_note = d[note]
                action = 100
                if conv_note in range(0, 12):
                    action = 1
                elif conv_note in range(12, 24):
                    action = 2
                elif conv_note in range(24, 36):
                    action = 3
                elif conv_note in range(36, 48):
                    action = 4
                elif conv_note in range(48, 61):
                    if conv_note ==60:
                        action = 8
                    elif conv_note ==59:
                        action = 7
                    elif conv_note ==58:
                        action = 6
                    else:
                        action = 5
                elif conv_note in range(61, 62):
                    action = 100
                print(f"action: {action}")
                process = subprocess.Popen([
                    "curl",
                    "-X", "POST",
                    "http://192.168.4.1/command",
                    "-H", "Content-Type: application/x-www-form-urlencoded",
                    "-d", str(action)
                ])
            except Exception as e:
                process = subprocess.Popen(["curl", "-X", "POST",  "http://192.168.4.1/command", "-d", str(100)])
    else:
        process = subprocess.Popen(["curl", "-X", "POST",  "http://192.168.4.1/command", "-d", str(100)])