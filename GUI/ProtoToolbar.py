import wx
import copy
import ToolbarButton
import AppSettings
import BubbleEvent

class ProtoToolbar(wx.Panel):
    def __init__(self, parent, id=-1, position=wx.DefaultPosition, size=wx.Size(800,40)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.imagePath=AppSettings.IMAGE_PATH

        self.backButton=  ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'back.png'),         wx.Bitmap(self.imagePath+'back_select.png'), wx.Bitmap(self.imagePath+'back_disable.png'), name="back")
        self.quitButton=  ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'quit.png'),         wx.Bitmap(self.imagePath+'quit_select.png'), name="quit")
        self.blankButton1=ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton2=ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton3=ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton4=ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton5=ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton1.Disable()
        self.blankButton2.Disable()
        self.blankButton3.Disable()
        self.blankButton4.Disable()
        self.blankButton5.Disable()

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
        if cmd == self.backButton.name and AppSettings.previousPage!= None:
            self.GetParent().setView(AppSettings.previousPage)