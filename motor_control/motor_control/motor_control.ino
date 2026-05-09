const int EN1 = 5;   // PWM, to L293D pin 1
  const int IN1 = 4;   //      to L293D pin 2
  const int IN2 = 7;   //      to L293D pin 7

  void setup() {
    pinMode(EN1, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
  }

  void loop() {
    // Forward, half speed
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(EN1, 255);
    delay(5000);

    // Stop
    analogWrite(EN1, 0);
    delay(1000);

    // Reverse, half speed
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(EN1, 150);
    delay(2000);

    // Stop
    analogWrite(EN1, 0);
    delay(1000);
  }