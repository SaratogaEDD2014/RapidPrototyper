import wx
import AppSettings

class QuickPrint(wx.Panel):
    def __init__(self, parent, id=-1, pos=(0,40), size=wx.Size(800,440)):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.SetBackgroundColour(AppSettings.secondBackground)
        self.Show(False)
        sizer=wx.StaticBoxSizer(wx.StaticBox(self, -1, "Choose a file", size=(240, 170)),wx.VERTICAL)

        sizer.Add(wx.FilePickerCtrl(self, -1, AppSettings.userFilePath,"Choose a file:",pos=(20,20), size=(350,-1)))
        temp=wx.Panel(self,size=(40,40))
        temp.SetBackgroundColour(self.GetBackgroundColour())
        sizer.Add(temp)
        sizer2=wx.BoxSizer()
        sizer2.Add(wx.Button(self, label="Cancel", pos=(20,100)))
        temp=wx.Panel(self,size=(40,40))
        temp.SetBackgroundColour(self.GetBackgroundColour())
        sizer2.Add(temp)
        sizer2.Add(wx.Button(self, label="Print",pos=(120,100)))
        sizer.Add(sizer2)

        self.SetSizer(sizer)
