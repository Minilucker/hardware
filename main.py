import serial
import db

ser = serial.Serial()  # Remplacez 'COMx' par le port série approprié
ser.port = 'COM3'
ser.baudrate = 9600
ser.open()

try:
    
    while True:
        uid = ser.read(size=8).decode("utf-8")
        if (db.check_db(uid)):
            ser.write('VALID')
        else:
            ser.write('INVALID')
        


except KeyboardInterrupt:
    ser.close()
