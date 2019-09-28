bool start = false;
int ledPin = 13;
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  pinMode(ledPin,OUTPUT);
}
void loop() {
  String data = Serial.readString();
  if (data == "id") {
    Serial.println("I am the little arduino");
    start = true;
  }
  if (start == true) {
    Serial.println("doing the code this arduino needs to do...");
    digitalWrite(ledPin,HIGH);
    delay(500);
    digitalWrite(ledPin,LOW);
    delay(500);    
  }
}
