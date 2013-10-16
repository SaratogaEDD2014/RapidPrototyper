import wx
import copy
import AppSettings
import BubbleMenu
import MainMenu

class ProtoFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(800, 510))
        self.imagePath=AppSettings.IMAGE_PATH+"Main/"
        self.title=title
        self.menu=MainMenu.MainMenu(self)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.menu)
        self.SetSizer(sizer)


def main():
    ProtoApp = wx.App()
    frame = ProtoFrame(None, -1, 'Blue Streaks EDD')
    frame.Show(True)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()

