import wx
import BubbleMenu


class ShapesRegion(wx.Panel):
    def __init__(self, parent, id=-1, position=wx.DefaultPosition, size=(390,390)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.imagePath='/Users/Scott/Documents/Design/Ultimaker/GUI/images/'
        self.buttonList=[BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"ellipse_standby.png"), wx.Bitmap(self.imagePath+"BubbleButtonPressed.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"rectangle_standby.png"), wx.Bitmap(self.imagePath+"BubbleButtonPressed.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"tri_standby.png"), wx.Bitmap(self.imagePath+"BubbleButtonPressed.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"circle_standby.png"), wx.Bitmap(self.imagePath+"BubbleButtonPressed.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"curve_standby.png"), wx.Bitmap(self.imagePath+"BubbleButtonPressed.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"line_standby.png"), wx.Bitmap(self.imagePath+"BubbleButtonPressed.png")),]
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