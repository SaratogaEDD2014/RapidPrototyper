#!/usr/bin/python
import wx
import copy
import AppSettings
import ProtoToolbar
import MainMenu


class ProtoFrame(wx.Frame):
    def __init__(self, parent, id, title):
        super(ProtoFrame, self).__init__(parent, id, title, size=wx.Size(800, 480))
        self.SetBackgroundColour(AppSettings.defaultBackground)
        self.imagePath=AppSettings.IMAGE_PATH+"Main/"
        self.title=title
        self.toolbar=ProtoToolbar.ProtoToolbar(self)
        self.toolbar.Show(True)
        self.menu=MainMenu.MainMenu(self)
        self.setView(self.menu)

    def setView(self, viewPanel):
        if(viewPanel!=None):
            AppSettings.previousPage=AppSettings.currentPage
            if (AppSettings.previousPage != None):
                AppSettings.previousPage.Show(False)
            AppSettings.currentPage=viewPanel
            AppSettings.currentPage.Show(True)
            mastersizer=wx.BoxSizer(wx.VERTICAL)
            mastersizer.Add(self.toolbar)
            sizer=wx.BoxSizer()
            sizer.Add(wx.Panel(self, size=((800-AppSettings.currentPage.GetSize()[0])/2,20)))
            sizer.Add(AppSettings.currentPage)
            mastersizer.Add(sizer)
            self.SetSizer(mastersizer)
            wx.PostEvent(AppSettings.currentPage, wx.SizeEvent()) #Without this, panel appears in wrong spot


def main():
    ProtoApp = wx.App()
    frame = ProtoFrame(None, -1, 'Blue Streaks EDD')
    frame.Show(True)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()
