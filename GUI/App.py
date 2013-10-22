import wx
import copy
import AppSettings
import BubbleMenu
import ProtoToolbar
import MainMenu


class ProtoFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(800, 510))
        self.imagePath=AppSettings.IMAGE_PATH+"Main/"
        self.title=title
        self.toolbar=ProtoToolbar.ProtoToolbar(self)
        self.toolbar.Show(True)
        self.menu=MainMenu.MainMenu(self)
        self.setView(self.menu)

    def setView(self, viewPanel):
        if(viewPanel!=None):
            print("Tried to show this: ",viewPanel)
            AppSettings.previousPage=AppSettings.currentPage
            if (AppSettings.previousPage != None):
                AppSettings.previousPage.Show(False)
            AppSettings.currentPage=viewPanel
            AppSettings.currentPage.Show(True)
            sizer=wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self.toolbar)
            sizer.Add(viewPanel)
            self.SetSizer(sizer)


def main():
    ProtoApp = wx.App()
    frame = ProtoFrame(None, -1, 'Blue Streaks EDD')
    frame.Show(True)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()

