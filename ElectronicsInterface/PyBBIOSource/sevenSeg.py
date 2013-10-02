"""sevenSegShift.py - Scott K 11/6/12
   Object for use with a seven segment display connected to a shift register
   for use with beagle bone

   *note this is meant to control 1 digit per register, not multiple digit displays
"""

#-----------------------------------------------------------------------------

from bbio import *
from shiftRegister import *

class sevenSegShift(object):

    #Defines input options to output specific characters
    
    dp=LOW
    
    ONE={LOW, HIGH, HIGH, LOW, LOW, LOW, LOW, dp}
    TWO={HIGH, HIGH, LOW, HIGH, HIGH, LOW, HIGH, dp}
    THREE={HIGH, HIGH, HIGH, HIGH, LOW, LOW, HIGH, dp}
    FOUR={LOW, HIGH, HIGH, LOW, LOW, HIGH, HIGH, dp}
    FIVE={HIGH, LOW, HIGH, HIGH, LOW, HIGH, HIGH, dp}
    SIX={HIGH, LOW, HIGH, HIGH, HIGH, HIGH, HIGH, dp}
    SEVEN={HIGH, HIGH, HIGH, LOW, LOW, LOW, LOW, dp}
    EIGHT={HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, dp}
    NINE={HIGH, HIGH, HIGH, HIGH, LOW, HIGH, HIGH, dp}
    ZERO={HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, LOW, dp}

    NUMS={ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, ZERO}

    def _init_(self, ser=8, rclk=9, srclk=10, anodeCathode=1, numDisp=1, abcdefgp={0,1,2,3,4,5,6,7,8}):
        """Initialized necessary variables for sevenSegShift class"""
      
        #creates new shift register object per display
        
        disp = new ShiftRegister(ser, rclk, srclk, numDisp)

        self.a=abcdefg[0]
        self.b=abcdefg[1]
        self.c=abcdefg[2]
        self.d=abcdefg[3]
        self.e=abcdefg[4]
        self.f=abcdefg[5]
        self.g=abcdefg[6]
        self.dp=abcdefg[7]

        if anodeCathode==0:
            self.ON=HIGH
            self.OFF=LOW
        else:
            self.ON=LOW
            self.OFF=HIGH

    def setDigit(self, char, ndisp):
        if ndisp >= self.disp.NUM_REGISTERS: ndisp=self.disp.NUM_REGISTERS-1
        self.disp.clearRegisters()
        option[char]()
        self.disp.setPins(range(ndisp*8, ndisp*8+8), self.segments)


    def one():
        self.segments[]={0,1,1,0,0,0,0}
    
