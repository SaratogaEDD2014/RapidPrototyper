import wx
import copy
import AppSettings
import BubbleMenu

class ProtoFrame(wx.Frame):


    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(800, 510))
        self.imagePath=AppSettings.IMAGE_PATH+"Main/"
        self.title=title
        self.menu=BubbleMenu.BubbleMenu(self, wx.Bitmap(self.imagePath+"BubbleTitle.png"), "Shape Menu")
        self.buttonList=[BubbleMenu.BubbleButton(   self.menu, wx.Bitmap(self.imagePath+"buttonTemplate1.png"), wx.Bitmap(self.imagePath+"buttonPressed1.png")),
                            BubbleMenu.BubbleButton(self.menu, wx.Bitmap(self.imagePath+"buttonTemplate2.png"), wx.Bitmap(self.imagePath+"buttonPressed2.png")),
                            BubbleMenu.BubbleButton(self.menu, wx.Bitmap(self.imagePath+"buttonTemplate3.png"), wx.Bitmap(self.imagePath+"buttonPressed3.png")),
                            BubbleMenu.BubbleButton(self.menu, wx.Bitmap(self.imagePath+"buttonTemplate4.png"), wx.Bitmap(self.imagePath+"buttonPressed4.png")),
                            BubbleMenu.BubbleButton(self.menu, wx.Bitmap(self.imagePath+"buttonTemplate5.png"), wx.Bitmap(self.imagePath+"buttonPressed5.png")),
                            BubbleMenu.BubbleButton(self.menu, wx.Bitmap(self.imagePath+"buttonTemplate6.png"), wx.Bitmap(self.imagePath+"buttonPressed6.png")),]
        self.menu.AddMany(self.buttonList)
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

