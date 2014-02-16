#-------------------------------------------------------------------------------
# Main Menu
# Author:      Scott Krulcik
# Created:     16/10/2013
#-------------------------------------------------------------------------------
from bubble_menu import *
import application.settings as settings
import wx
import templates.gear

class TemplateChooser(DynamicBubbleMenu):
    def __init__(self, parent):
        super(TemplateChooser, self).__init__(parent, "Shape Menu")
        self.parent=parent
        self.Show(False)
        self.imagePath=settings.IMAGE_PATH+"/Templates/T_Chooser/"

        self.extrudeView=wx.Panel(self.parent, pos=(0,40), size=(16,16))
        self.gearView=   templates.gear.GearTemplate(self.parent)
        self.mugView=    wx.Panel(self.parent, pos=(0,40), size=(16,16))
        self.ringView=   wx.Panel(self.parent, pos=(0,40), size=(16,16))
        self.ring2View=  wx.Panel(self.parent, pos=(0,40), size=(16,16))
        self.vaseView=   wx.Panel(self.parent, pos=(0,40), size=(16,16))

        self.extrudeView.Show(False)
        self.gearView.Show(False)
        self.mugView.Show(False)
        self.ringView.Show(False)
        self.ring2View.Show(False)
        self.vaseView.Show(False)

        if settings.icon_view:
            self.extrude=MenuButton(   self, wx.Bitmap(self.imagePath+"Extrusion.png"), wx.Bitmap(self.imagePath+"ExtrusionPress.png"), name='Extrusion', target=self.extrudeView)
            self.gear=   MenuButton(self, wx.Bitmap(self.imagePath+"Gear.png"), wx.Bitmap(self.imagePath+"GearPress.png"), name='Gear', target=self.gearView)
            self.mug=    MenuButton(self, wx.Bitmap(self.imagePath+"Mug.png"), wx.Bitmap(self.imagePath+"MugPress.png"), name='Mug', target=self.mugView)
            self.ring=   MenuButton(self, wx.Bitmap(self.imagePath+"Ring.png"), wx.Bitmap(self.imagePath+"RingPress.png"), name='Ring', target=self.ringView)
            self.ring2=  MenuButton(self, wx.Bitmap(self.imagePath+"Ring.png"), wx.Bitmap(self.imagePath+"VasePress.png"), name='Revolve', target=self.ring2View)
            self.vase=   MenuButton(self, wx.Bitmap(self.imagePath+"Vase.png"), wx.Bitmap(self.imagePath+"VasePress.png"), name='Temp', target=self.vaseView)
        else:
            self.extrude=DynamicButton(self, name='Extrusion', target=self.extrudeView)
            self.gear=   DynamicButton(self, name='Gear', target=self.gearView)
            self.mug=    DynamicButton(self, name='Mug', target=self.mugView)
            self.ring=   DynamicButton(self, name='Ring', target=self.ringView)
            self.ring2=  DynamicButton(self, name='Revolve', target=self.ring2View)
            self.vase=   DynamicButton(self, name='Temp', target=self.vaseView)

        self.buttonList=[self.extrude, self.gear, self.mug, self.ring, self.ring2, self.vase]
        self.setChildren(self.buttonList)
if __name__ == "__main__":
    app = wx.App()
    frm = wx.Frame(None, size=(800,800))
    settings.icon_view = False
    menu = TemplateChooser(frm)
    frm.Show(True)
    menu.Show(True)
    menu.SendSizeEvent()
    menu.CenterOnParent()
    app.MainLoop()
