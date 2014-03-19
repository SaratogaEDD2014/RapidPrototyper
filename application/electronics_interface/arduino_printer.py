from arduino.ardunio_stepper import *


#These constants are based on our Arduino code, stepper motor, and threaded rod
STEP_PIN = 3
DIR_PIN = 2
STEPS_PER_REV = 400
PITCH = 20

class PrinterInterface(object):
    def __init__(self, serial_port='COM5', layer_depth=.01):#.012):
        self.ardu = ArduinoStepMotor(serial_port)
        self.ardu.output([STEP_PIN, DIR_PIN])
        self.set_layer_depth(layer_depth)

    def set_layer_depth(self, depth):
        self.layer_depth = depth
        steps_per_in = STEPS_PER_REV*PITCH
        steps_per_layer = int(steps_per_in*depth)
        self.ardu.set_steps_per_layer(steps_per_layer)

    def next_layer(self):
        self.ardu.move_layer()

    def zero(self):
        """Should zero motor"""
        pass

    def destroy(self):
        self.ardu.close()


def main():
##    sKotty = ArduinoStepMotor('COM5')
##    sKotty.output([2,3])
##
##
##    sKotty.set_steps_per_layer(10)
##    for i in range(40):
##        sKotty.move_layer()
##
##
##    time.sleep(.1)
##    sKotty.close()
    p = PrinterInterface()
    p.set_layer_depth(.01)
    for i in range(50):
        p.next_layer()
    p.destroy()

if __name__ == '__main__':
    main()