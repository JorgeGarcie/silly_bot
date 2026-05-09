// Two continuous-rotation servos (e.g. FS90R) on D8 (right) and D9 (left).
// Wiring:
//   Right red    -> 5V       Left red    -> 5V
//   Right brown  -> GND      Left brown  -> GND
//   Right orange -> D8       Left orange -> D9
//
// NeoPixel (Adafruit) on D6:
//   NeoPixel +5V (or VCC)  -> 5V
//   NeoPixel GND           -> GND
//   NeoPixel DIN           -> D6
//   (For long strips: 1000uF cap across +/- and a 470 ohm resistor on DIN.)
//
// On continuous-rotation servos: 0 = full one way, 90 = stop, 180 = full other way.
// "Stop" may need tweaking per servo (e.g. 88-92).
//
// Serial protocol: laptop sends a single integer per line.
//   1 = FORWARD, 2 = BACK, 3 = LEFT, 4 = RIGHT, 5 = POOP, 6 = WOW, 100 = STOP

#include <Servo.h>
#include <Adafruit_NeoPixel.h>

#define NEOPIXEL_PIN  6
#define NUM_PIXELS    12   // 12-pixel ring
#define RING_OFFSET   0    // rotate the ring: increase if pixel 0 isn't at 12 o'clock

Servo wheelRight;
Servo wheelLeft;
Adafruit_NeoPixel pixels(NUM_PIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

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

void pixelsOff() {
  pixels.clear();
  pixels.show();
}

// WOW: light every pixel bright white.
void wow() {
  for (int i = 0; i < NUM_PIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(255, 255, 255));
  }
  pixels.show();
}

// Light a contiguous arc of `count` pixels centered at `centerIdx`.
void arc(int centerIdx, int count, uint32_t color) {
  pixels.clear();
  int start = centerIdx - count / 2;
  for (int i = 0; i < count; i++) {
    int idx = ((start + i) % NUM_PIXELS + NUM_PIXELS) % NUM_PIXELS;
    pixels.setPixelColor(idx, color);
  }
  pixels.show();
}

// SMILE: bottom third of the ring (centered at 6 o'clock).
void smile() {
  arc((NUM_PIXELS / 2 + RING_OFFSET) % NUM_PIXELS, NUM_PIXELS / 3, pixels.Color(255, 200, 0));
}

// FROWN: top third of the ring (centered at 12 o'clock).
void frown() {
  arc(RING_OFFSET % NUM_PIXELS, NUM_PIXELS / 3, pixels.Color(0, 100, 255));
}

void dispatch(int code) {
  switch (code) {
    case 1: moveForward(); break;
    case 2: moveBack();    break;
    case 3: turnLeft();    break;
    case 4: turnRight();   break;
    case 6: wow();         break;
    case 7: smile();       break;
    case 8: frown();       break;
    case 100: stopAll();   break;
    default: /* unknown — ignore */ break;
  }
}

void setup() {
  Serial.begin(115200);
  wheelRight.attach(8);
  wheelLeft.attach(9);
  stopAll();
  pixels.begin();
  pixels.setBrightness(80);  // 0-255; keep modest to avoid USB brown-out
  pixelsOff();
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
