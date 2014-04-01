// encoder pin on interrupt 0 (pin 2)
attachInterrupt(0, encoderPinChangeA, CHANGE);
// encoder pin on interrupt 1 (pin 3)
attachInterrupt(1, encoderPinChangeB, CHANGE);
encoder = 0;

void encoderPinChangeA() {
 if (digitalRead(encoder_a)==digitalRead(encoder_b)) {
  encoder--;
 }
 else{
  encoder++;
 }
}

void encoderPinChangeB() {
 if (digitalRead(encoder_a) != digitalRead(encoder_b)) {
  encoder--;
 }
 else {
  encoder++;
 }
}
