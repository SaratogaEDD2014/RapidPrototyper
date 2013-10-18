#-------------------------------------------------------------------------------
# Main Menu
# Author:      Scott Krulcik
# Created:     16/10/2013
#-------------------------------------------------------------------------------
import BubbleMenu
import AppSettings
import wx

class TemplateChooser(BubbleMenu.BubbleMenu):
    def __init__(self, parent):
        BubbleMenu.BubbleMenu.__init__(self, parent, wx.Bitmap(AppSettings.IMAGE_PATH+"Main/"+"BubbleTitle.png"), "Shape Menu", size=wx.DefaultSize)
        self.imagePath=AppSettings.IMAGE_PATH+"/Templates/T_Chooser/"
        self.buttonList=[BubbleMenu.BubbleButton(   self, wx.Bitmap(self.imagePath+"Extrusion.png"), wx.Bitmap(self.imagePath+"ExtrusionPress.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"Gear.png"), wx.Bitmap(self.imagePath+"GearPress.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"Mug.png"), wx.Bitmap(self.imagePath+"MugPress.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"Ring.png"), wx.Bitmap(self.imagePath+"RingPress.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"Vase.png"), wx.Bitmap(self.imagePath+"VasePress.png"))]
        self.AddMany(self.buttonList)
