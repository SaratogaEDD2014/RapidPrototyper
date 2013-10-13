#Scott Krulcik 10/9/13

import wx
import copy
import BubbleMenu
import AppSettings

class Ultimaker(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(800, 510))
        self.imagePath=AppSettings.IMAGE_PATH+"Main/"
        self.title=title
        
        self.buttonList=[BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate1.png"), wx.Bitmap(self.imagePath+"buttonPressed1.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate2.png"), wx.Bitmap(self.imagePath+"buttonPressed2.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate3.png"), wx.Bitmap(self.imagePath+"buttonPressed3.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate4.png"), wx.Bitmap(self.imagePath+"buttonPressed4.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate5.png"), wx.Bitmap(self.imagePath+"buttonPressed5.png")),
                            BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"buttonTemplate6.png"), wx.Bitmap(self.imagePath+"buttonPressed6.png")),]
        
        shapes=BubbleMenu.BubbleMenu( self, wx.Bitmap(self.imagePath+"BubbleTitle.png"), name="Test Menu", children=[])
        shapes.addMany(self.buttonList)
        
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(shapes)             #,      (4, 41),(39,39))
        self.SetSizer(sizer)
        


class MyApp(wx.App):
    def OnInit(self):
        frame = Ultimaker(None, -1, 'TEST for DLP App')
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
