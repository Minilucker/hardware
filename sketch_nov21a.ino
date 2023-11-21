#include "SPI.h"
#include "MFRC522.h"
#include <cstring>


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
  Serial.begin(9600);
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
  
   if ( !mfrc522.PICC_IsNewCardPresent()) { return; }
   if ( !mfrc522.PICC_ReadCardSerial()) { return; }

    String uidArr[4] = {String(mfrc522.uid.uidByte[0], HEX), String(mfrc522.uid.uidByte[1], HEX), String(mfrc522.uid.uidByte[2], HEX), String(mfrc522.uid.uidByte[3], HEX)};
    for (int i=0; i<4; i++) {
      if(uidArr[i].length() == 1) {
        uidArr[i] = "0" + uidArr[i];
      }
    }
    Serial.print(uidArr[0] + uidArr[1] + uidArr[2] + uidArr[3]);
    response = Serial.readString();
    validateBadge(response);
  
    
    return;  
}
