// Librairie utilisée pour le chiffrement AES 128 (ECB malheureusement), source de Cipher.h : https://github.com/josephpal/esp32-Encrypt,
// c'est une librairie qui implémente mbedtls en aes 128 ECB, je l'ai utilisé car n'ayant pas réussi à implémenter mbedtls (que ce soit en aes 128 ECB ou en 256 CBC)
#include <Cipher.h>
#include "SPI.h"
#include "MFRC522.h"

// Définition des broches
#define red_pin D0 // Pin led 
#define green_pin D1 // Pin led 
#define rst_pin D3 // RES pin
#define ss_pin D4  // SDA (SS) pin

// Initialisation du lecteur RFID MFRC522
MFRC522 mfrc522(ss_pin, rst_pin);

// Initialisation de la classe Cipher de Cipher.h
Cipher * cipher = new Cipher();

// Variable pour stocker la réponse de la communication série
String response = "";

// Fonction pour valider le badge en fonction de la réponse
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

  // Configuration des broches en sortie
  pinMode(rst_pin, OUTPUT);
  pinMode(red_pin,OUTPUT);


  cipher->setKey("3WBeW3PuK0SzpCQv");
  pinMode(green_pin, OUTPUT);

}
void loop() {
    // Vérifie si une nouvelle carte RFID est présente, sinon relance la boucle

   if (!mfrc522.PICC_IsNewCardPresent()) { return; }

   // Lit les informations de la carte RFID, si il n'y en a pas, relance la boucle

   if (!mfrc522.PICC_ReadCardSerial()) { return; }

    //déclaration de la string destinée à contenir la chaine à chiffrer
    char encryptable[9]; 

    //compteur de l'espace déjà occupé dans le buffer de encryptable
    int cx = 0;

    // convertit mfrc522.uid.uidByte (byteArray) en char*, pour ça plusieurs option était possible j'aurais pu directement convertir
    // en classe String, cependant j'aurais été obligé de vérifier chaque paire hexadécimale pour vérifier qu'aucun 0 non significatif 
    // n'a sauté, par exemple : 23b0d50b, dans cet uid, 0b serait devenu b, faussant l'uid original
    for (byte bChar: mfrc522.uid.uidByte) {
      cx += snprintf(encryptable+cx, 9-cx, "%02x", bChar);
    }

    // convertit encryptable en classe String
    String sEncryptable = String(encryptable);

    // chiffre l'uid
    String encryptedString = cipher->encryptString(sEncryptable);

    // envoi l'uid chiffré
    Serial.print(encryptedString);

    // Lit la réponse de la communication série
    response = Serial.readString();

    // Appelle la fonction pour valider le badge en fonction de la réponse
    validateBadge(response);
}