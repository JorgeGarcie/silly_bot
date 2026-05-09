#include <arduinoFFT.h>

#define AUDIO_PIN A0

const uint8_t SAMPLES = 128;               // better resolution than 64
const double SAMPLING_FREQUENCY = 8000.0;  // Nyquist = 4000 Hz usable range

double vReal[SAMPLES];
double vImag[SAMPLES];

ArduinoFFT<double> FFT =
  ArduinoFFT<double>(vReal, vImag, SAMPLES, SAMPLING_FREQUENCY);

// =========================

void setup() {
  Serial.begin(115200);
}

// =========================

void loop() {

  // ===== SAMPLE AUDIO =====
  for (uint8_t i = 0; i < SAMPLES; i++) {
    vReal[i] = analogRead(AUDIO_PIN) - 512;
    vImag[i] = 0;

    delayMicroseconds(125); // ~8kHz
  }

  // ===== REMOVE DC OFFSET =====
  double mean = 0;
  for (uint8_t i = 0; i < SAMPLES; i++) {
    mean += vReal[i];
  }
  mean /= SAMPLES;

  for (uint8_t i = 0; i < SAMPLES; i++) {
    vReal[i] -= mean;
  }

  // ===== RMS GATE (fix silence fake frequency) =====
  double rms = 0;
  for (uint8_t i = 0; i < SAMPLES; i++) {
    rms += vReal[i] * vReal[i];
  }
  rms = sqrt(rms / SAMPLES);

  if (rms < 15) {   // tune this threshold
    Serial.println("F0: ---");
    delay(50);
    return;
  }

  // ===== FFT =====
  FFT.windowing(FFTWindow::Hamming, FFTDirection::Forward);
  FFT.compute(FFTDirection::Forward);
  FFT.complexToMagnitude();

  // ===== IMPROVED PEAK FINDING =====
  uint8_t peak = 2;
  double bestScore = 0;

  for (uint8_t i = 2; i < SAMPLES / 2; i++) {

    double mag = vReal[i];

    if (mag < 10) continue; // noise filter

    // harmonic suppression + low-frequency preference
    double score = mag / (double)i;

    if (score > bestScore) {
      bestScore = score;
      peak = i;
    }
  }

  // ===== PARABOLIC INTERPOLATION =====
  double a = vReal[peak - 1];
  double b = vReal[peak];
  double c = vReal[peak + 1];

  double denom = (a - 2 * b + c);
  double p = 0;

  if (denom != 0) {
    p = 0.5 * (a - c) / denom;
  }

  double bin = peak + p;

  // ===== BIN → FREQUENCY =====
  double freq =
    bin * SAMPLING_FREQUENCY / SAMPLES;

  Serial.print("F0: ");
  Serial.print(freq, 1);
  Serial.println(" Hz");

  delay(30);
}