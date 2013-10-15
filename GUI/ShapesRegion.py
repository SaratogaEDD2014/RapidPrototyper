import wx
import BubbleMenu
import AppSettings


class ShapesRegion(wx.Panel):
    def __init__(self, parent, id=-1, position=wx.DefaultPosition, size=(390,390)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.imagePath=AppSettings.IMAGE_PATH
        self.buttonList=[BubbleMenu.BubbleButton(   self, wx.Bitmap(self.imagePath+"buttonTemplate1.png"), wx.Bitmap(self.imagePath+"buttonPressed1.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate2.png"), wx.Bitmap(self.imagePath+"buttonPressed2.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate3.png"), wx.Bitmap(self.imagePath+"buttonPressed3.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate4.png"), wx.Bitmap(self.imagePath+"buttonPressed4.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate5.png"), wx.Bitmap(self.imagePath+"buttonPressed5.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate6.png"), wx.Bitmap(self.imagePath+"buttonPressed6.png")),]
        self.menu=BubbleMenu.BubbleMenu(self, wx.Bitmap(self.imagePath+"BubbleTitle.png"), "Shape Menu", self.buttonList)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.menu)
        self.SetSizer(sizer)

        

def main():
    app = wx.App()
    frame = wx.Frame(None, -1, 'Bubble Menu test', size=(400,400))
    panel = ShapesRegion(frame)
    #panel.SetBackgroundColour(wx.Colour(200,0,0))
    sizer=wx.BoxSizer(wx.VERTICAL)
    sizer.Add(panel)
    frame.SetSizer(sizer)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
