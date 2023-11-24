import serial
import db
import time
import datetime
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

# 1 seconde de plus pour match le délai de 1s entre l'envoi du signal LOCKED et l'allumage de la led
default_lockout_duration = 61
current_lockout_duration = default_lockout_duration

try:

    # Boucle infinie pour lire continuellement depuis le port série
    while True:
        lastMin = int(datetime.datetime.now().strftime('%M'))
        
        # lecture du port série par tranche de 16 bytes, nécessaire pour décrypter la string
        # chiffrée en AES 128 ECB qui est stocké dans une chaine de 16 bytes (même si le contenu d'origine fait moins)
        encrypteduid = ser.read(size=16)
        currentMin = int(datetime.datetime.now().strftime('%M'))
        if (currentMin < lastMin) :
            lockout_duration = current_lockout_duration
        uid = cipher.decrypt(encrypteduid)[:8].decode('utf-8')
       
        # conversion de l'hexadécimal en int
        intuid = int(uid, 16)
        print(f"Received uid n°{intuid} ... is ", end="")

        # envoi de la réponse selon le status du badge : VALID ou INVALID
        if (db.check_db(f"{intuid}")):
            print("Valid")
            ser.write(b'VALID')
            failedAttempt = 0
        else:
            failedAttempt += 1
            print("Invalid")
            
            # système de lockout dans le cas de tentative bruteforce, l'intention était d'augmenter la durée
            # plus le lockout était atteint (la durée se reset a chaque heure), mais j'ai été contraint
            # de reset l'esp en essayant d'implémenter le tout, donc on se contentera de 60 secondes. 
            if (failedAttempt > 3):
                failedAttempt = 0
                total_seconds = current_lockout_duration
                print("Too many failure, beginning lockout") 
                ser.write(b'LOCKED')

                while total_seconds > 0:
                    timer = datetime.timedelta(seconds = total_seconds)
                    print(f"Time remaining : {total_seconds}")
                    time.sleep(1)
                    total_seconds -= 1

                print("End of lockout")
            else:
               
                ser.write(b'INVALID')
                
        

 # En cas d'interruption par le clavier (Ctrl+C), fermeture propre du port série
except KeyboardInterrupt:
    ser.close()
