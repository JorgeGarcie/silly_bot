#include <arduinoFFT.h>

#define AUDIO_PIN A0

const uint8_t SAMPLES = 64;
const double SAMPLING_FREQUENCY = 8000.0;

double vReal[SAMPLES];
double vImag[SAMPLES];

// MUST be double (library limitation)
ArduinoFFT<double> FFT =
  ArduinoFFT<double>(
    vReal,
    vImag,
    SAMPLES,
    SAMPLING_FREQUENCY
  );

void setup() {
  Serial.begin(115200);
}

void loop() {

  // ===== SAMPLE =====
  for (uint8_t i = 0; i < SAMPLES; i++) {
    vReal[i] = analogRead(AUDIO_PIN) - 512;
    vImag[i] = 0;

    delayMicroseconds(125);
  }

  // ===== DC REMOVE =====
  double mean = 0;
  for (uint8_t i = 0; i < SAMPLES; i++) mean += vReal[i];
  mean /= SAMPLES;

  for (uint8_t i = 0; i < SAMPLES; i++) vReal[i] -= mean;

  // ===== FFT =====
  FFT.windowing(FFTWindow::Hamming, FFTDirection::Forward);
  FFT.compute(FFTDirection::Forward);
  FFT.complexToMagnitude();

  // ===== PEAK FIND =====
  uint8_t peak = 2;
  double maxVal = 0;

  for (uint8_t i = 2; i < SAMPLES / 2; i++) {
    if (vReal[i] > maxVal) {
      maxVal = vReal[i];
      peak = i;
    }
  }

  // ===== PARABOLA FIT =====
  double a = vReal[peak - 1];
  double b = vReal[peak];
  double c = vReal[peak + 1];

  double denom = (a - 2 * b + c);
  double p = 0;

  if (denom != 0) {
    p = 0.5 * (a - c) / denom;
  }

  double bin = peak + p;

  double freq = bin * SAMPLING_FREQUENCY / SAMPLES;

  Serial.print("F0: ");
  Serial.print(freq, 1);
  Serial.println(" Hz");

  delay(30);
}