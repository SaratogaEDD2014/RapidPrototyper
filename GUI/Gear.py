#-------------------------------------------------------------------------------
# Name:       Gear
# Purpose:
#
# Author:      krulciks14
#
# Created:     01/11/2013
# Copyright:   (c) krulciks14 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import PartTemplate

class Gear(PartTemplate):
    def __init__(self, numTeeth=25, pitchDistance=.15, pitchDiameter=3.0, bore=1.0):
        super(Gear, self).__init__()
        self.dimensions={"pitchDiameter":self.pitchDiameter, "teeth":self.numTeeth, }

def main():


if __name__ == '__main__':
    main()
