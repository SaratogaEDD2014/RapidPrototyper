import wx
import GUI.settings as settings

class Figure:
    def __init__(self, draw_function=None, arguements=[], pen=None):
        self.func=draw_function
        self.args=arguements
        self.pen=pen

    def draw_self(self):
        if self.func != None:
            self.func(self.args)

    def set_pen(self, pen):
        self.pen=pen
    def get_pen(self, pen):
        if self.pen == None:
            self.pen=wx.Pen("BLACK")
        return pen
    pen=property(get_pen, set_pen)

    def set_arguements(self, args):
        self.args=args
    def get_arguements(self, args):
        return self.args
    args=property(get_arguements, set_arguements)

    def add_arguement(self, arg):
        self.args.append(arg)


class EditablePane(wx.Panel):
    def __init__(self, parent, id=-1, pos=(0,0), size=(400,400)):
        super(EditablePane, self).__init__(parent, id, pos, size)
        self.on_create(wx.PaintEvent())
        self.draw=False
        self.currentFigure=[]
        self.figures=[]
        self.mode='lines'
        self._draw_methods={'lines':self._dc.DrawLines,
                                'circle':self._dc.DrawCircle,
                                'ellipse':self._dc.DrawEllipse,
                                'arc':self._dc.DrawArc,
                                'polygon':self._dc.DrawPolygon,
                                'spline':self._dc.DrawSpline,
                                'text':self._dc.DrawText}
        self.pen_color="BLACK"
        self.pen_weight=1
        self.pen_style=wx.Solid
        px,py=self.GetPosition()
        sx,sy=self.GetSize()
        self._area=wx.Region(px,py,sx,sy)
        self.SetBackgroundColour(wx.Colour(255,255,255))

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_LEFT_UP, self.on_up)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_dclick)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_click(self, event):
        x, y = event.GetPosition()
        self.currentFigure.append((x,y))

    def on_dclick(self, event):
        self.draw= not self.draw
        fig=Figure(self._draw_methods[self.mode], self.currentFigure, wx.Pen(self.pen_color, self.pen_weight, wx.Solid))
        self.figures.append(fig)
        self.currentFigure=[]
        self._dc.Clear()
        for figure in self.figures:
            self._dc.SetPen(figure.pen)
            figure.draw_self()
        self._dc.SetPen(wx.Pen(self.pen_color,1, wx.Dot))

    def on_up(self, event):
        self._dc.DrawLines(self.currentFigure, 0,0)

    def on_paint(self, event):
        self._dc.Clear()
        self._dc.SetPen(wx.Pen(self.pen_color, 1, wx.DOT))

    def on_create(self, event):
        self._dc=wx.PaintDC(self)

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
        self.draw_space.pen_color="BLUE"

    def on_black(self, event):
        self.draw_space.pen_color="BLACK"



def main():
    app = wx.App(False)
    frame = wx.Frame(None, title="Paint", size=(800,400))
    panel = Editor(frame)
    frame.Show(True)
    frame.Center()
    app.MainLoop()

main()