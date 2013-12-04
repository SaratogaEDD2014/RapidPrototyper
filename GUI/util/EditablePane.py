import wx

class EditablePane(wx.Panel):
    def __init__(self, parent, id=-1, pos=(0,0), size=(400,400)):
        super(EditablePane, self).__init__(parent, id, pos, size)
        self._dc=None
        self._points_list=[]
        px,py=self.GetPosition()
        sx,sy=self.GetSize()
        self._area=wx.Region(px,py,sx,sy)

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_LEFT_UP, self.on_up)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_click(self, event):
        x, y = event.GetPosition()
        self._points_list.append((x,y))

    def on_up(self, event):
        self._dc.DrawLines(self._points_list, 0,0)

    def on_paint(self, event):
        self._dc=wx.PaintDC(self)
        self._dc.Clear()
        self._dc.SetPen(wx.Pen("BLACK", 4))

class Editor(wx.Panel):
    def __init__(self, parent, id=-1, pos=(0,0), size=(800,400)):
        super(Editor, self).__init__(parent, id, pos, size)
        self.draw_space=EditablePane(self)
        self.blue=wx.Button(self, label="Blue")
        self.black=wx.Button(self, label="Black")
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.draw_space)
        sizer.Add(self.blue)
        sizer.Add(self.black)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.on_black, self.black)
        self.Bind(wx.EVT_BUTTON, self.on_blue, self.blue)

    def on_blue(self, event):
        self.draw_space._dc.SetPen(wx.Pen("BLUE", 4))

    def on_black(self, event):
        self.draw_space._dc.SetPen(wx.Pen("BLACK", 4))



def main():
    app = wx.App(False)
    frame = wx.Frame(None, title="Paint")
    panel = Editor(frame)
    frame.Show(True)
    app.MainLoop()

main()