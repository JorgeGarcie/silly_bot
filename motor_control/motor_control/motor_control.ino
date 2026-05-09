// Two continuous-rotation servos (e.g. FS90R) on D8 (right) and D9 (left).
// Wiring:
//   Right red    -> 5V       Left red    -> 5V
//   Right brown  -> GND      Left brown  -> GND
//   Right orange -> D8       Left orange -> D9
//
// On continuous-rotation servos: 0 = full one way, 90 = stop, 180 = full other way.
// "Stop" may need tweaking per servo (e.g. 88-92).
//
// Serial protocol: laptop sends a single integer per line.
//   0 = STOP, 1 = FORWARD, 2 = BACK, 3 = LEFT, 4 = RIGHT
// Codes 5-100 reserved for future primitives.

#include <Servo.h>

Servo wheelRight;
Servo wheelLeft;

const int STOP_RIGHT = 92;
const int STOP_LEFT  = 90;

void moveForward() {
  wheelRight.write(180);
  wheelLeft.write(0);
}

void moveBack() {
  wheelRight.write(0);
  wheelLeft.write(180);
}

// Tank turns: both wheels spin the same physical direction in place.
void turnLeft() {
  wheelRight.write(150);
  wheelLeft.write(150);
}

void turnRight() {
  wheelRight.write(30);
  wheelLeft.write(30);
}

void stopAll() {
  wheelRight.write(STOP_RIGHT);
  wheelLeft.write(STOP_LEFT);
}

void dispatch(int code) {
  switch (code) {
    case 1: moveForward(); break;
    case 2: moveBack();    break;
    case 3: turnLeft();    break;
    case 4: turnRight();   break;
    case 100: stopAll();    break;
    default: /* unknown — ignore */ break;
  }
}

void setup() {
  Serial.begin(115200);
  wheelRight.attach(8);
  wheelLeft.attach(9);
  stopAll();
  delay(500);
}

void loop() {
  if (Serial.available()) {
    int code = Serial.parseInt();
    if (Serial.read() == '\n' || code != 0 || Serial.peek() == -1) {
      dispatch(code);
    }
  }
}
