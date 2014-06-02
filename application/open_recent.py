import wx
from wx.lib.buttons import GenBitmapTextButton
import application.settings as settings

class OpenRecent(wx.Panel):
    def __init__(self, parent, id=-1, position=(0,40), size=wx.Size(800,400)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.Show(False)
        self.SetBackgroundColour(settings.secondBackground)
        master_sizer= wx.GridSizer(2,1)
        top_sizer=wx.GridSizer(1,0)
        bottom_sizer=wx.GridSizer(1,0)
        i=0
        self.top_butt_list=[]
        self.bottom_butt_list=[]
        w,h = self.GetSize()

        ###make a event with sizing next time
        j=0
        for file_info in settings.recentFiles:

            recent = file_info[0]
            icon= file_info[1]
            recent=recent[recent.index('/')+1:]
            recent=recent[recent.index('/')+1:]
            if len(settings.recentFiles)==2:
                button=GenBitmapTextButton(self, 1, wx.Bitmap(settings.IMAGE_PATH+'stl_icon_1.png'), recent)
                button.SetBestSize( (w/1+.1,  h/2.2))
                button.SetBezelWidth(w/70)
                top_butt_list.append(button)
                if (i==1):
                    button=GenBitmapTextButton(self, 1, wx.Bitmap(settings.IMAGE_PATH+'stl_icon_1.png'), recent)
                    button.SetBestSize( (w/1+.1,  h/2.2))
                    button.SetBezelWidth(w/70)
                    bottom_butt_list.append(button)
            if(i<2):
                button=GenBitmapTextButton(self, 1, wx.Bitmap(settings.IMAGE_PATH+'stl_icon_1.png'), recent)
                button.SetBestSize( (w/min(2, len(settings.recentFiles))+.1,  h/2.2))
                button.SetBezelWidth(w/70)
                j+=1
                #top_sizer.Add(button, wx.EXPAND)
                self.top_butt_list.append(button)
            else:
                button=GenBitmapTextButton(self, 1, wx.Bitmap(settings.IMAGE_PATH+'stl_icon_1.png'), recent)
                button.SetBestSize((w/max(1, len(settings.recentFiles)-j),  h/2.2 ))
                button.SetBezelWidth(w/70)
                #bottom_sizer.Add(button, wx.EXPAND)
                self.bottom_butt_list.append(button)
            i+=1
        top_sizer.AddMany(self.top_butt_list)
        bottom_sizer.AddMany(self.bottom_butt_list)
        master_sizer.Add(top_sizer, 1, wx.EXPAND)
        master_sizer.Add(bottom_sizer, 1, wx.EXPAND)
        self.SetSizer(master_sizer)

if __name__ == '__main__':
    app = wx.App()
    frm = wx.Frame(None, size=wx.Size(800,400))
    panel = OpenRecent(frm)
    panel.Show()
    frm.Show()
    app.MainLoop()