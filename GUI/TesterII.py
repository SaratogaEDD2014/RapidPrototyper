import wx
import wx.lib.plot as plot

class TemplatePane(wx.Panel):
    def __init__(self, parent):
        super(TemplatePane, self).__init__(parent)
        client = plot.PlotCanvas(self)
        line = plot.PolyLine([(1,2),(2,4),(3,9),(4,16),(5,25)], legend='', colour='pink', width=1)
        gc = plot.PlotGraphics([line], 'Line Graph', 'X Axis', 'Y Axis')
        client.Draw(gc,  xAxis= (0,15), yAxis= (0,15))
        self.Show(True)

def main():
    ProtoApp = wx.App()
    """
    frame = wx.Frame(None, -1, 'Blue Streaks EDD')
    sizer=wx.BoxSizer(wx.VERTICAL)
    sizer.Add(TemplatePane(frame))
    frame.SetSizer(sizer)
    frame.Show(True)"""
    frm = wx.Frame(None, -1, 'line', size=(600,450))
    TemplatePane(frm)
    frm.Show(True)
    ProtoApp.MainLoop()

if __name__ == '__main__':
    main()