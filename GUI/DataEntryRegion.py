import wx

class DataEntryRegion(wx.StaticBox):
    def __init__(self, parent, attributeList=("x","y","z"), pos=(0,410), size=(360,80)):
        wx.Window.__init__(self, parent, pos=pos, size=size, name='Enter Coordinates:')
        self.attributes=attributeList
        self.SetBackgroundColour(wx.Colour(200,220,220))
        sizer= wx.GridSizer(len(self.attributes), 2, 3, 3)
        for i in range(0,len(self.attributes)):
            sizer.Add(wx.StaticText(self, label=self.attributes[i]),0,wx.EXPAND)
            sizer.Add(wx.TextCtrl(self),0,wx.EXPAND)
        self.SetSizer(sizer)