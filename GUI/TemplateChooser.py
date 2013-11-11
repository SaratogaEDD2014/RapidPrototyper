#-------------------------------------------------------------------------------
# Main Menu
# Author:      Scott Krulcik
# Created:     16/10/2013
#-------------------------------------------------------------------------------
import BubbleMenu
import AppSettings
import wx
import Templates.GearTemplate

class TemplateChooser(BubbleMenu.BubbleMenu):
    def __init__(self, parent):
        BubbleMenu.BubbleMenu.__init__(self, parent, wx.Bitmap(AppSettings.IMAGE_PATH+"Main/"+"BubbleTitle.png"), "Shape Menu", size=wx.Size(440,440))
        self.parent=parent
        self.Show(False)
        self.imagePath=AppSettings.IMAGE_PATH+"/Templates/T_Chooser/"

        self.extrudeView=wx.Panel(self.parent)
        self.gearView=   Templates.GearTemplate.GearTemplate(self.parent)
        self.mugView=    wx.Panel(self.parent)
        self.ringView=   wx.Panel(self.parent)
        self.ring2View=  wx.Panel(self.parent)
        self.vaseView=   wx.Panel(self.parent)


        self.extrude=BubbleMenu.BubbleButton(   self, wx.Bitmap(self.imagePath+"Extrusion.png"), wx.Bitmap(self.imagePath+"ExtrusionPress.png"), target=self.extrudeView)
        self.gear=   BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"Gear.png"), wx.Bitmap(self.imagePath+"GearPress.png"), target=self.gearView)
        self.mug=    BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"Mug.png"), wx.Bitmap(self.imagePath+"MugPress.png"), target=self.mugView)
        self.ring=   BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"Ring.png"), wx.Bitmap(self.imagePath+"RingPress.png"), target=self.ringView)
        self.ring2=  BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"Ring.png"), wx.Bitmap(self.imagePath+"VasePress.png"), target=self.ring2View)
        self.vase=   BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"Vase.png"), wx.Bitmap(self.imagePath+"VasePress.png"), target=self.vaseView)

        self.buttonList=[self.extrude, self.gear, self.mug, self.ring, self.ring2, self.vase]
        self.setChildren(self.buttonList)
