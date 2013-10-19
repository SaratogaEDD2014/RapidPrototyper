import wx
import copy
import ToolbarButton
import AppSettings

class ProtoToolbar(wx.Panel):
    
    
    def __init__(self, parent, id=-1, position=wx.DefaultPosition, size=wx.Size(800,40)):
        self.imagePath=AppSettings.IMAGE_PATH+"Main/"
        
        wx.Panel.__init__(self, parent, id, position, size)
        self.parent=parent
        
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
        self.backButton.Disable()
        
        toolbarSizer=wx.GridBagSizer()
        toolbarSizer.Add(self.backButton,  (0,0),  span=(1,2))
        toolbarSizer.Add(self.blankButton, (0,2),  span=(1,3))
        toolbarSizer.Add(self.printButton, (0,5),  span=(1,2))
        toolbarSizer.Add(self.cutButton,   (0,7),  span=(1,2))
        toolbarSizer.Add(self.millButton,  (0,9),  span=(1,2))
        toolbarSizer.Add(self.blankButton2,(0,11), span=(1,3))
        toolbarSizer.Add(self.quitButton,  (0,14), span=(1,2))
        self.SetSizer(toolbarSizer)
        
        self.Bind(wx.EVT_BUTTON, self.toolbarEvent)
    
    def toolbarEvent(self, event):
        cmd=event.GetEventObject().name
        if cmd ==self.quitButton.name:
            self.parent.Destroy()
        if cmd == self.backButton.name:
            self.parent.SetView(AppSettings.previousPage)

