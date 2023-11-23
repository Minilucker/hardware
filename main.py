import serial
import db
import time
from Crypto.Cipher import AES

# Configuration du port série
ser = serial.Serial()  # Remplacez 'COMx' par le port série approprié
ser.port = 'COM3'
ser.baudrate = 115200
ser.open()
failedAttempt = 0
# clé AES de 16 bytes
key = b"3WBeW3PuK0SzpCQv"
# création du mode utilisé pour le cipher (ici ECB)
cipher = AES.new(key, AES.MODE_ECB)


try:
    # Boucle infinie pour lire continuellement depuis le port série
    while True:
        # lecture du port série par tranche de 16 bytes, nécessaire pour décrypter la string 
        # chiffrée en AES 128 ECB qui est stocké dans une chaine de 16 bytes (même si le contenu d'origine fait moins)
        encrypteduid = ser.read(size=16)

        uid = cipher.decrypt(encrypteduid)[:8].decode('utf-8')
        # conversion de l'hexadécimal en int
        intuid = int(uid, 16)

        # envoi de la réponse selon le status du badge : VALID ou INVALID
        if (db.check_db(f"{intuid}")):
            ser.write(b'VALID')
            failedAttempt = 0
        else:
            ser.write(b'INVALID')
            failedAttempt += 1
        

 # En cas d'interruption par le clavier (Ctrl+C), fermeture propre du port série
except KeyboardInterrupt:
    ser.close()
