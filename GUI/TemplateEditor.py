import wx
from Templates import Gear
import AppSettings
import wx.lib.plot as plot

class TemplateEditor(wx.Panel):
    def __init__(self, parent, template=Gear.Gear(3,20) ,id=-1, position=wx.DefaultPosition, size=wx.Size(800,400)):
        wx.Panel.__init__(self, parent, id, position, size)
        self.Show(False)
        self.shape=template
        self.SetBackgroundColour(AppSettings.defaultBackground)
        self.drawPart()

    def drawPart(self):
        client = plot.PlotCanvas(self)
        lines=[]
        for line in self.shape.getData():
            print("Adding this data: ", line)
            lines.append(plot.PolyLine(line, legend='', colour='pink', width=1))
        gc = plot.PlotGraphics(lines)#, self.shape.getDescription())
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(client)
        self.SetSizer(sizer)
        client.Draw(gc, xAxis=(-10,10), yAxis=(-10,20))
        self.Show(True)

def main():
    ProtoApp = wx.App()
    frame = wx.Frame(None, -1, 'Blue Streaks EDD')
    sizer=wx.BoxSizer(wx.VERTICAL)
    sizer.Add(TemplateEditor(frame))
    frame.SetSizer(sizer)
    frame.Show(True)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()
