# shift_test.py - Scott K 11/6/2012
# 
# Interfaces with shift registers to create displays.
# 
# This example is in the public domain
from bbio import *

SER = 8	    				   	  #pin 14 on the 75HC595
RCLK = 9     				 	  #pin 12 on the 75HC595
SRCLK = 10   				 	  #pin 11 on the 75HC595

NUM_REGISTERS=2   				  #number of shift registers
NUM_REG_PINS=NUM_REGISTERS*8                      #number of total pins

registers[NUM_REG_PINS]

#-----------------------------------------------------------------------------
