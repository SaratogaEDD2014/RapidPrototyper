import wx
from Templates import Gear
import GUI.settings as settings
import util.plot as plot

class TemplateEditor(wx.Panel):
    def __init__(self, parent, template=None ,id=-1, position=wx.DefaultPosition, size=wx.Size(800,400)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.Show(False)
        self.shape=template
        self.SetBackgroundColour(settings.defaultBackground)

    def setShape(self, shape):
        self.shape=shape
        self.drawPart()

    def getShape():
        return self.shape

    def drawPart(self):
        client = plot.PlotCanvas(self)
        gc = plot.PlotGraphics(self.shape.getLines())#, self.shape.getDescription())
        sizer=wx.BoxSizer(wx.VERTICAL)
        client.Draw(gc, xAxis=(-10,10), yAxis=(-10,20))
        sizer.Add(client)
        sizer.Add(self.shape.getGearDimensionEditor())
        self.SetSizer(sizer)

def main():
    ProtoApp = wx.App()
    frame = wx.Frame(None, -1, 'Blue Streaks EDD', size=(800,400))
    sizer=wx.BoxSizer(wx.VERTICAL)
    gearEditor=TemplateEditor(frame)
    gearEditor.setShape(Gear.Gear(gearEditor))
    sizer.Add(gearEditor)
    frame.SetSizer(sizer)
    frame.Show(True)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()
