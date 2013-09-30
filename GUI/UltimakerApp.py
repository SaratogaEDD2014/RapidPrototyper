import wx
import copy
import UMToolbar
import DataEntryRegion
import ShapesRegion

class Ultimaker(wx.Frame):
    
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(800, 510))
        self.imagePath='/Users/Scott/Documents/Design/Ultimaker/GUI/images/'
        self.title=title
        
        toolbar=UMToolbar.UMToolbar(self, -1)
        shapes=ShapesRegion.ShapesRegion(self)
        dataEntry=DataEntryRegion.DataEntryRegion(self)
        
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(toolbar)                 #,        (0,0),  (4,80))
        sizer.Add(shapes)             #,      (4, 41),(39,39))
        sizer.Add(dataEntry)       #,(44,41),(4,39))
        self.SetSizer(sizer)
        


class MyApp(wx.App):
    def OnInit(self):
        frame = Ultimaker(None, -1, 'Ultimaker')
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
