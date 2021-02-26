import serial
import re
import time
import string
import io


ser = serial.Serial("/dev/rfcomm0", timeout=None)
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.flushInput()
ser.write(b'2105\r\n')
ser.flush()
seq = []
while True:
    reading = ser.read()
    seq.append(reading)
    joineddata = ' '.join(str(v) for v in seq).replace(' ', '')
    print joineddata
    err = re.search('ERROR', joineddata)
    if err:
        break
    m = re.search('4([^;]*)5:', joineddata) #'/4([^;]*)\n5', joineddata)
    if m:
        ser.close()
        print ('m= ')
        test = str(m.group(0))
        print test
        x = (test[-8:])
        print x
        print x[3:5]
        SoC = (int( x[3:5], 16)/2)
        if SoC > 0 & SoC <= 100:
            print(SoC)
        break
