from arduino import *
import time

class ArduinoStepMotor(Arduino):
    def __init__(self, port, baudrate=9600, units = 'mm', limit = 12):
        #115200
        super(ArduinoStepMotor, self).__init__(port, baudrate)
        self.units = units #whether we are using metric or English, important for calculating pitch
        self.position = 0 #the absolute linear position of the motor apparatus
        self.limit = limit #maximum distance motor is allowed to move

        if(self.units == 'in'):
            self.pitch = 50.8
        elif(self.units == 'mm'):
            self.pitch = 2.
        else:
            print('invalid agruement for units, units must be set to "in" or "mm"')
            self.pitch = 50.8
    def step_one(self):
        self.sendData('5')
        print self.getData()

    def relMove(self, distance):
        distance = int(round(distance))
        multiplier = -1 if distance<0 else 1
        for i in range(abs(distance)/100):
            self._send_steps(100*multiplier)
        if abs(distance)%100 != 0:
            self._send_steps((abs(distance)%100)*multiplier)

    def move_mm(self, mm):
        #2mm pitch
        steps_per_rev = 9000
        revs = (mm/self.pitch)
        steps = revs*steps_per_rev
        self.relMove(steps)

    def _send_steps(self, steps):
        self.sendData('6')
        self.sendData(steps)
        print self.getData()

    def absMove(self, newPosition):
        if (newPosition < 0):
            newPosition = 0
        if (newPosition > self.limit):
            newPosition = limit
        self.relMove(newPosition - self.position)
        self.position = newPosition

    def reset(self): # WARNING: THIS CAN INTERFERE WITH PROTCOLS WHICH PREVENT THE MOTOR FROM MOVING OUT OF RANGE
        self.position = 0

sKotty = ArduinoStepMotor('COM5')
sKotty.output([2,3])
for i in range(100):
    sKotty.relMove(-100)
#sKotty.close()
