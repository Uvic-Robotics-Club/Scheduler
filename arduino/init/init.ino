
bool connected_to_serial = false;


const char PACKET_START_MARKER = '>';
const char PACKET_END_MARKER = '<';

String incoming;

int ledPin = 13;

void blink(){
    digitalWrite(ledPin,HIGH);
    delay(500);
    digitalWrite(ledPin,LOW);
    delay(500);
}
void setup() {
  
  // put your setup code here, to run once:
  static bool receive_in_progress = false;
  char received_char;
  pinMode(ledPin,OUTPUT);
  
//  pinMode(pin, OUTPUT);
  Serial.begin (9600);
  Serial.setTimeout(99);



  while(!connected_to_serial){
    String x = Serial.readString();
    if(x == 'id'){
      Serial.write(">Motor driver<");
      blink();
      connected_to_serial = true;
    }
  }

}

void loop() {
  // put your main code here, to run repeatedly:

  //blink an LED to signal task is successful
  blink();
}
