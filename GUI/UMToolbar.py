import wx
import copy
import ToolbarButton
import AppSettings

class UMToolbar(wx.Panel):
    
    
    def __init__(self, parent, id, position=wx.DefaultPosition, size=wx.Size(800,40)):
        self.imagePath=AppSettings.IMAGE_PATH+"Main/"
        
        wx.Panel.__init__(self, parent, id, position, size)
        self.parent=parent
        
        self.backButton=  ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'back.png'),         wx.Bitmap(self.imagePath+'back_select.png'), wx.Bitmap(self.imagePath+'back_disable.png'), name="back")
        self.printButton= ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'print_standby.png'),wx.Bitmap(self.imagePath+'print_select.png'),  wx.Bitmap(self.imagePath+'print_select.png'), "print")
        self.cutButton=   ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'cut_standby.png'),  wx.Bitmap(self.imagePath+'cut_select.png'), wx.Bitmap(self.imagePath+'cut_select.png'), "cut")
        self.millButton=  ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'mill_standby.png'), wx.Bitmap(self.imagePath+'mill_select.png'), wx.Bitmap(self.imagePath+'mill_select.png'), "mill")
        self.quitButton=  ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'quit.png'),         wx.Bitmap(self.imagePath+'quit_select.png'), name="quit")
        self.blankButton= ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton2=ToolbarButton.ToolbarButton(self, wx.Bitmap(self.imagePath+'menublank.png'))
        self.blankButton.Disable()
        self.blankButton2.Disable()
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
        
        self.Bind(wx.EVT_BUTTON, self.machineSelector)
    
    def machineSelector(self, event):
        cmd=event.GetEventObject().name
        if cmd ==self.quitButton.name:
            self.parent.Destroy()
        if cmd != self.backButton.name:
            machines=(self.cutButton,self.millButton,self.printButton)
            for m in machines:
                if m.name==cmd:
                    m.Disable()
                    self.parent.SetTitle(self.parent.title+': '+cmd.capitalize())
                else:
                    if not m.IsEnabled():
                        m.Enable()
            del machines

