import serial
import db

ser = serial.Serial()  # Remplacez 'COMx' par le port série approprié
ser.port = 'COM3'
ser.baudrate = 115200
ser.open()

try:
    
    while True:
        uid = ser.read(size=8).decode("utf-8")
        intuid = int(uid, 16)
        if (db.check_db(f"{intuid}")):
            ser.write(b'VALID')
        else:
            ser.write(b'INVALID')
        


except KeyboardInterrupt:
    ser.close()
