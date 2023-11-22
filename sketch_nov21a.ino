#include "SPI.h"
#include "MFRC522.h"


#define red_pin D0 // Pin led 
#define green_pin D1 // Pin led 
#define rst_pin D3 // RES pin
#define ss_pin D4  // SDA (SS) pin


MFRC522 mfrc522(ss_pin, rst_pin);

String response = "";

void validateBadge(String response){
  if (response == "VALID") {
      digitalWrite(green_pin, HIGH);
      delay(1000);
      digitalWrite(green_pin, LOW);
      
    }
    if (response == "INVALID") {
      digitalWrite(red_pin, HIGH);
      delay(1000);
      digitalWrite(red_pin, LOW);
    }
}

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
  delay(5);
  mfrc522.PCD_DumpVersionToSerial();

  pinMode(rst_pin, OUTPUT);
  // Set pin 0 and 1 as output
  pinMode(red_pin,OUTPUT);
  pinMode(green_pin, OUTPUT);

}
void loop() {
  
   if (!mfrc522.PICC_IsNewCardPresent()) { return; }
   if (!mfrc522.PICC_ReadCardSerial()) { return; }

    Serial.printf("%02x", mfrc522.uid.uidByte[0]);
    Serial.printf("%02x", mfrc522.uid.uidByte[1]);
    Serial.printf("%02x", mfrc522.uid.uidByte[2]);
    Serial.printf("%02x", mfrc522.uid.uidByte[3]);

    response = Serial.readString();
    validateBadge(response);
}