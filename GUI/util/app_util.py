import wx
import GUI.settings as settings

class BlankGradient(wx.Window):
    def __init__(self, parent=None, pos=wx.DefaultPosition, size=wx.DefaultSize, col1=wx.Colour(0, 0, 0), col2=wx.Colour(255, 255, 255), orientation=wx.NORTH):
        super(BlankGradient, self).__init__(parent, pos=pos, size=size)
        self.color1 = col1
        self.color2 = col2
        self.orientation = orientation
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):
            dc = wx.PaintDC(self)
            dc.Clear()
            w,h = self.GetSize()
            dc.GradientFillLinear((0, 0, w, h), self.color1, self.color2, self.orientation)

class DynamicPanel(wx.Panel):
    def __init__(self, parent, size=(200, 200)):
        super(DynamicPanel, self).__init__(parent, size=size)
        self.SetBackgroundColour(wx.Colour(255,200,160))
        self.elements =[]
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_size(self, event):
        self.SetSize(self.GetParent().GetSize())
        w,h = self.GetSize()
        element_h = int(h*.8/(len(self.elements)+1))
        buff = element_h/2
        dim = buff
        p = (0,buff)
        s = (w, dim)
        buffers = []
        for element in self.elements:
            spacer = wx.Panel(self, pos=p, size=s)
            buffers.append(spacer)
            p = (p[0], p[1]+dim)
            element.SetSize(s)
            element.SetPosition(p)
            p = (p[0], p[1]+dim)
"""
class DynamicPanelBox(DynamicPanel):
    def __init__(self, parent, name=None, size=(200,200)):
        super(DynamicPanelBox, self).__init__(parent, size=(size[0]*.9, size[1]*.9))
        self.name = name
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):
        event.Skip()
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(settings.defaultForeground, 3))
        dc.SetTextForeground(settings.defaultForeground)
        w,h = self.GetSize()
        w = (w*.9)
        h = (h*.85)
        fillet = int(min(self.GetSize())*.1)
        if self.name!=None:
            text_width = dc.GetTextExtent(self.name)[0]
            dc.DrawText(self.name, fillet+5, 5)
        else:
            text_width = 0
        dc.DrawArc(fillet,1, 1,fillet, fillet, fillet)
        dc.DrawArc(1,h-fillet, fillet,h, fillet, h-fillet)
        dc.DrawArc(w,fillet, w-fillet,1, w-fillet,fillet)
        dc.DrawArc(w-fillet,h, w,h-fillet, w-fillet,h-fillet)"""

def dim_color(color, dim_value=10):
    r = max(color.Red()-25, 0)
    g = max(color.Green()-25, 0)
    b = max(color.Blue()-25, 0)
    return wx.Colour(r,g,b)

def draw_centered_text(obj, text, scale=1.0, font=None, dc = None):
    """Draws given string centered on given object"""
    text_area_width = obj.GetSize()[0]*scale
    text_point_size = int((text_area_width/7.11222063894596))
    if font == None:
        #not set as default parameter because wx.Font obj cannot be created before wx.App
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    font.SetPointSize(text_point_size)
    if dc == None:
        dc = wx.ClientDC(obj)
    dc.SetFont(font)
    dc.SetTextForeground(settings.button_text)
    #use object and text width to center it
    w,h = obj.GetSize()
    tw,th = dc.GetTextExtent(text)
    dc.DrawText(text, (w-tw)/2, (h-th)/2)

def main():
    app = wx.App()
    frm = wx.Frame(None)
    panel = DynamicPanel(frm, size=(800, 800))
    text  = wx.StaticText(panel, label="test 1")
    text2 = wx.StaticText(panel, label="test 2")
    text3 = wx.StaticText(panel, label="test 3")
    text4 = wx.StaticText(panel, label="test 4")
    elements = [text, text2, text3, text4]
    panel.elements = elements
    frm.Show(True)
    app.MainLoop()
#main()