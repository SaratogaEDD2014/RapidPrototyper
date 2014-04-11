#define photosensorPin 9    //photosensor pin

void setup()
{
  pinMode(photosensorPin, INPUT);
  Serial.begin(9600);
  delay(10);
}

void loop()
{ 
  if(digitalRead(photosensorPin)==HIGH)   //if the photosensor is recieving data
{
  Serial.println("Resin level is low, please replace");
}
  delay(1);
} 
//more will be added at some point