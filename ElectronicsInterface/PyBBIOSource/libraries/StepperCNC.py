"""
 StepperCNC - v1.0
 Copyright 2013 Scott Krulcik

 Stepper motor class to be used with beaglebone in a CNC machine

 Note: "Position" does not refer to angle, it refers to linear distance traveled from a fixed point(0)
"""

from bbio import *

class StepperCNC(object):

  def __init__(self, dir_pin, step_pin, position=0, pitch=20):
    """Creates instance of StepperCNC class
    self.dirPin=dir_pin
    self.stepPin=step_pin
    self.pos=position
    self.threadPitch=20
    self.distancePerStep=1.0/self.threadpitch

  def setPosition(self, position=0):
    self.pos=position

  def getPosition(self):
    return self.pos

  def setPitch(self, pitch):
    self.threadPitch=pitch
    self.distancePerStep=1.0/self.threadpitch

  def step(self, numSteps=1):
    if numSteps!=0:
      self.dir=(HIGH if steps>0 else LOW)
    pause=

 
