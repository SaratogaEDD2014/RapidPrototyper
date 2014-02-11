#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      krulciks14
#
# Created:     11/02/2014
# Copyright:   (c) krulciks14 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import wx
import os
import time
import GUI.settings as settings

class SlideShow(wx.Panel):
    def __init__(self, parent, directory, pos=wx.DefaultPosition, size=wx.DefaultSize):
        super(SlideShow, self).__init__(parent, id=-1, pos=pos, size=size)
        self.bmp = None
        self.dir = directory

    def show_slides(self, delay=1):
        print os.listdir(self.dir)
        for the_file in os.listdir(self.dir):
            print the_file
            self.bmp = wx.StaticBitmap(self, bitmap=wx.Bitmap(the_file))
            self.bmp.SetSize((400,400))
            time.sleep(delay)

def main():
    app = wx.App()
    frm = wx.Frame(None)
    show = SlideShow(frm,'./generation_buffer/', size= (400,400))
    frm.Show(True)
    show.show_slides()
    app.MainLoop()


if __name__ == '__main__':
    main()
