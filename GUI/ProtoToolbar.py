import wx
import copy
from ToolbarButton import *
import GUI.settings as settings
import BubbleEvent

class ProtoToolbar(wx.Panel):
    def __init__(self, parent, id=-1, position=(0,-80), size=wx.Size(800,40)):
        super(ProtoToolbar, self).__init__(parent, id, position, size)
        #self.Show(False)
        self.imagePath=settings.IMAGE_PATH

        self.backButton=  ToolbarButton(self, wx.Bitmap(self.imagePath+'back.png'),         wx.Bitmap(self.imagePath+'back_select.png'), wx.Bitmap(self.imagePath+'back_disable.png'), name="back")
        self.quitButton=  ToolbarButton(self, wx.Bitmap(self.imagePath+'quit.png'),         wx.Bitmap(self.imagePath+'quit_select.png'), name="quit")
        self.blankButton1=ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton2=ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton3=ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton4=ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton1.Disable()
        self.blankButton2.Disable()
        self.blankButton3.Disable()
        self.blankButton4.Disable()

        toolbarSizer=wx.BoxSizer(wx.HORIZONTAL)
        toolbarSizer.Add(self.backButton)
        toolbarSizer.Add(self.blankButton1)
        toolbarSizer.Add(self.blankButton2)
        toolbarSizer.Add(self.blankButton3)
        toolbarSizer.Add(self.blankButton4)
        toolbarSizer.Add(self.quitButton)
        self.SetSizer(toolbarSizer)

        self.Bind(wx.EVT_BUTTON, self.toolbarEvent)

    def toolbarEvent(self, event):
        cmd=event.GetEventObject().name
        if cmd ==self.quitButton.name:
            self.GetParent().Destroy()
        if cmd == self.backButton.name:
            settings.goto_prev_page()