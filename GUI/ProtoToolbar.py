import wx
import copy
from ToolbarButton import *
import GUI.settings as settings
import GUI.util.app_util as blank_graphics
import BubbleEvent

class ProtoToolbar(wx.Panel):
    def __init__(self, parent, id=-1, position=wx.DefaultPosition, size=wx.Size(settings.app_w, settings.toolbar_h)):
        super(ProtoToolbar, self).__init__(parent, id, position, size)
        #self.Show(False)
        self.imagePath=settings.IMAGE_PATH

        self.backButton =  ToolbarButton(self, wx.Bitmap(self.imagePath+'back.png'), wx.Bitmap(self.imagePath+'back_select.png'), wx.Bitmap(self.imagePath+'back_disable.png'), name="back")
        self.quitButton =  ToolbarButton(self, wx.Bitmap(self.imagePath+'quit.png'), wx.Bitmap(self.imagePath+'quit_select.png'), name="quit")
        self.blank_space = blank_graphics.BlankGradient(self, size=(settings.app_w-self.backButton.GetSize()[0]-self.quitButton.GetSize()[0], self.backButton.GetSize()[1]), col1=settings.toolbar_bottom, col2=settings.toolbar_top)
        #, pos=(self.backButton.GetSize()[0], 0)

        self.Bind(wx.EVT_BUTTON, self.toolbarEvent)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Refresh()

    def on_paint(self, event):
        self.SetSize((settings.app_w, settings.toolbar_h))
        settings.toolbar_w,settings.toolbar_h = self.GetSize()
        self.blank_space.SetSize((settings.app_w-self.backButton.GetSize()[0]-self.quitButton.GetSize()[0], self.backButton.GetSize()[1]))
        self.backButton.SetPosition((0,0))
        self.blank_space.SetPosition((self.backButton.GetSize()[0], 0))
        self.quitButton.SetPosition((self.backButton.GetSize()[0]+self.blank_space.GetSize()[0], 0))
        self.backButton.Refresh()
        self.quitButton.Refresh()
        self.blank_space.Refresh()


    def toolbarEvent(self, event):
        cmd=event.GetEventObject().name
        if cmd == self.quitButton.name:
            self.GetParent().Destroy()
        if cmd == self.backButton.name:
            settings.goto_prev_page()

