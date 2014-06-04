import wx
from wx.lib.buttons import GenBitmapTextButton
import application.settings as settings

class OpenRecent(wx.Panel):
    def __init__(self, parent, id=-1, position=(0,40), size=wx.Size(800,400)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.Show(False)
        self.SetBackgroundColour(settings.secondBackground)
        self.master_sizer= wx.GridSizer(2,1)
        self.top_sizer=wx.GridSizer(1,0)
        self.bottom_sizer=wx.GridSizer(1,0)
        w,h = self.GetSize()

        i=0
        for file_info in settings.recentFiles:

            recent = file_info[0]
            icon= file_info[1]
            recent=recent[recent.index('/')+1:]
            recent=recent[recent.index('/')+1:]
            button=GenBitmapTextButton(self, 1, wx.Bitmap(settings.IMAGE_PATH+'stl_icon_1.png'), recent)
            length=len(settings.recentFiles)
            length=length+.00
            if length==1:
                button.SetBestSize((w/1.02, h/1.11))
                button.SetBezelWidth(w/70)
                self.master_sizer.Add(button)

            elif length%2==0:
                button.SetBestSize((w/(min(length/2, 2)+.01),  h/2.2))
                button.SetBezelWidth(w/70)

                if i<length/2:
                        self.top_sizer.Add(button, wx.EXPAND)
                else:
                    self.bottom_sizer.Add(button, wx.EXPAND)
            else:
                button.SetBezelWidth(w/70)

                if i<(length/2.0+.5):
                    button.SetBestSize((w/(min(length/2.0 +.5, 3)+.01),  h/2.2))
                    self.top_sizer.Add(button)
                else:
                    button.SetBestSize((w/(min(length/2.0 -.5, 3)+.01),  h/2.2))
                    self.bottom_sizer.Add(button)
            i+=1

        if length>1:
            self.master_sizer.Add(self.top_sizer, 1, wx.EXPAND)
            self.master_sizer.Add(self.bottom_sizer, 1, wx.EXPAND)
        self.SetSizer(self.master_sizer)




if __name__ == '__main__':
    app = wx.App()
    frm = wx.Frame(None, size=wx.Size(800,400))
    panel = OpenRecent(frm)
    panel.Show()
    frm.Show()
    app.MainLoop()