#define ztablePin 7      //z table pin
#define magnetPin 8      //magnet pin

void setup()
{
  pinMode(ztablePin, INPUT);
  pinMode(magnetPin, OUTPUT);
  Serial.begin(9600);
  Serial.println("Program Starting");
  delay(10);
}

void loop()
{
  if(digitalRead(ztablePin)==LOW)      //if the z table is not attached, turn the magnet off
{
    Serial.println("Please attach the Z-table");
    digitalWrite(magnetPin, LOW);
}
  delay(1);
}

