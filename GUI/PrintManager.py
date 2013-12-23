import wx
import GUI.settings as settings

class PrintManager(wx.Panel):
    def __init__(self, parent, id=-1, position=(0,40), size=wx.Size(800,400)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.Show(False)
        wx.StaticText(self, -1,"PrintManager")
        self.SetBackgroundColour(AppSettings.defaultBackground)
        
        
#----------------------------------------------------------------------------------
def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Print stuff', size=(800,400))

    sizer=wx.BoxSizer(wx.HORIZONTAL)
    panel=PrintManager(frm)
    sizer.Add(panel)
    panel.Show(True)

    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()
