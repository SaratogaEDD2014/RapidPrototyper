#-------------------------------------------------------------------------------
# Main Menu
# Author:      Scott Krulcik
# Created:     16/10/2013
#-------------------------------------------------------------------------------
import BubbleMenu
import AppSettings
import wx

class MainMenu(BubbleMenu.BubbleMenu):
    def __init__(self, parent):
        BubbleMenu.BubbleMenu.__init__(self, parent, wx.Bitmap(AppSettings.IMAGE_PATH+"Main/"+"BubbleTitle.png"), "Shape Menu", size=wx.DefaultSize)
        self.imagePath=AppSettings.IMAGE_PATH+"Main/"
        self.buttonList=[BubbleMenu.BubbleButton(   self, wx.Bitmap(self.imagePath+"buttonTemplate1.png"), wx.Bitmap(self.imagePath+"buttonPressed1.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate2.png"), wx.Bitmap(self.imagePath+"buttonPressed2.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate3.png"), wx.Bitmap(self.imagePath+"buttonPressed3.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate4.png"), wx.Bitmap(self.imagePath+"buttonPressed4.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate5.png"), wx.Bitmap(self.imagePath+"buttonPressed5.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate6.png"), wx.Bitmap(self.imagePath+"buttonPressed6.png"))]
        self.AddMany(self.buttonList)
