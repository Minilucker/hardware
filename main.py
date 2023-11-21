import serial
import db

ser = serial.Serial()  # Remplacez 'COMx' par le port série approprié
ser.port = 'COM3'
ser.baudrate = 9600
ser.open()

try:
    
    while True:
        uid = ser.read(size=8).decode("utf-8")
        print(uid)
        if (uid == '53ae5299'):
            ser.write(bytes('VALID', 'utf-8'))
        if (uid == '23b0d50b'):
            ser.write(bytes('INVALID', 'utf-8'))
        


except KeyboardInterrupt:
    ser.close()
