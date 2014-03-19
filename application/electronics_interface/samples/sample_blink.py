from arduino import Arduino
import time
import serial

#b = Arduino('/dev/ttyUSB0')
b = Arduino('COM5')
pin = 3
#ser=serial.Serial('COM5', 9600)

#declare output pins as a list/tuple
#b.output([pin])
#b.output([2,3])


for x in range(200):
    #b.setHigh(pin)
    #print b.getState(pin)
    #b.setLow(pin)
    #print b.getState(pin)
    #b.step()
    time.sleep(.005)
#ser.write('6')
    b.sendData('6')
    b.sendData('400')
#b.sendData('9')
#time.sleep(1)

b.close()
