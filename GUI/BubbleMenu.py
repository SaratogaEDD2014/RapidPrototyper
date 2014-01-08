from GUI.util.app_util import dim_color
import wx
import BubbleEvent
import GUI.settings as settings
import platform
import math

class BubbleMenu(wx.Window):
    def __init__(self, parent, bitmap, name="", children=[], id=-1, pos=wx.DefaultPosition, size=(400, 400)):
        super(BubbleMenu, self).__init__(parent, id, pos=pos, size=size)
        self.Show(False)
        self.bitmap=bitmap
        self.name=name
        self.children=children
        self.pos=[]
        self.button=BubbleButton(self, bitmap)
        self.button.Disable()
        self.childIndex=0
        self.SetBackgroundColour(settings.defaultBackground)

        #Gives the best positions to put the buttons given a certain number of them
        self.posIndices=[[7],
                        [3,5],
                        [6,1,8],
                        [0,2,6,8],
                        [0,2,6,7,8],
                        [0,2,3,5,6,8],
                        [0,2,3,5,6,7,8],
                        [0,1,2,3,5,6,7,8]]

        #Gives the best alignment flags for each index to give the menu a "circular" look
        self.alignIndices=[wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                           wx.ALIGN_CENTER,
                           wx.ALIGN_LEFT | wx.ALIGN_BOTTOM,
                           wx.ALIGN_CENTER,
                           wx.ALIGN_CENTER,
                           wx.ALIGN_CENTER,
                           wx.ALIGN_RIGHT | wx.ALIGN_TOP,
                           wx.ALIGN_CENTER,
                           wx.ALIGN_LEFT | wx.ALIGN_TOP]

        if len(self.children)>0:
            self.updateChildren()
        self.Center()
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_size(self, event):
        event.Skip(True)
        min_dim = min(settings.app_w, settings.app_h)
        min_dim = int(.95*min_dim)
        self.SetSize((min_dim, min_dim))

        button_size = int((self.GetSize()[0]/3.0)*.7)
        #for butt in (range(4)+range(5, len(self.children))):
        #    self.children[butt].SetSize((button_size, button_size))
        #    self.children[butt].Refresh()
        self.Refresh()

    def SetSize(self, size):
        """Ensures menu is always a square"""
        min_dim = min(size[0], size[1])
        super(BubbleMenu, self).SetSize((min_dim, min_dim))

    def Add(self, button):
        self.AddMany([button])

    def AddMany(self, buttonList):
        for butt in buttonList:
            self.children.append(butt)
        self.updateChildren()

    def setChildren(self, buttonList):
        self.children=[]
        self.AddMany(buttonList)

    def updateChildren(self):
        self.childIndex=0
        if len(self.children)>0:
            sizer=wx.GridSizer(3,3)
            for i in range(9):
                if (self.posIndices[len(self.children)-1].count(i)>0):
                    sizer.Add(self.nextChild(), flag=self.alignIndices[i])
                else:
                    temp=wx.Panel(self, size=(1,1), id=1000+i)
                    temp.SetBackgroundColour(self.GetBackgroundColour())
                    sizer.Add(temp, flag=self.alignIndices[i])
            sizer.Remove(4)
            sizer.Insert(4, self.button, flag=wx.ALIGN_CENTER)
            self.SetSizer(sizer)

    def nextChild(self):
        self.childIndex+=1
        return self.children[self.childIndex-1]

class DynamicBubbleMenu(BubbleMenu):
    def __init__(self, parent, name="", children=[], id=-1, pos=wx.DefaultPosition, size=(400, 400)):
        super(DynamicBubbleMenu, self).__init__(parent, None, name, children, id, pos, size)
        self.button=DynamicButton(self, self.name, settings.defaultForeground, settings.defaultForeground, settings.defaultBackground, settings.defaultBackground)
        self.button.Disable()

    def on_size(self, event):
        event.Skip(True)
        min_dim = min(settings.app_w, settings.app_h)
        min_dim = int(.95*min_dim)
        self.SetSize((min_dim, min_dim))

        title_size = int((min_dim/3.0))
        button_size = int(title_size*.7)
        for butt in self.children:
            butt.SetSize((button_size, button_size))
            butt.Refresh()
        self.button.SetSize((title_size, title_size))



class BubbleButton(wx.PyControl):
    def __init__(self, parent, normal=None, pressed=None, name=""):
        super(BubbleButton, self).__init__(parent, -1, style=wx.BORDER_NONE)
        self.style=wx.BORDER_NONE
        if normal != None:
            self.normal = normal
            self.pressed = pressed
        else:
            self.normal=wx.Bitmap(settings.IMAGE_PATH+"BubbleButtonTemplate.png")
            if pressed != None:
                self.pressed = pressed
            else:
                self.pressed=wx.Bitmap(settings.IMAGE_PATH+"BubbleButtonPressed.png")
        self.name=name
        #Region is the area that is "clickable"
        #It consists of the PNG minus the transparent areas
        self.region = wx.RegionFromBitmapColour(self.normal, wx.Colour(0, 0, 0, 0))
        self._clicked = False
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        #events
        self.Bind(wx.EVT_SIZE, self.on_size) #Used to make button fit as best as possible
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_window)

    def DoGetBestSize(self):
        return self.normal.GetSize()

    def post_event(self):
        event = BubbleEvent.BubbleEvent(self, None)
        wx.PostEvent(self, event)

    def Enable(self, *args, **kwargs):
        super(BubbleButton, self).Enable(*args, **kwargs)
        self.Refresh()
    def Disable(self, *args, **kwargs):
        super(BubbleButton, self).Disable(*args, **kwargs)
        self.Refresh()

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()
        bitmap = self.normal
        if self.clicked:
            bitmap = self.pressed or bitmap
        dc.DrawBitmap(bitmap, 0, 0)


    def set_clicked(self, clicked):
        if clicked != self._clicked:
            self._clicked = clicked
            self.Refresh()

    def get_clicked(self):
        return self._clicked
    clicked = property(get_clicked, set_clicked)

    def on_left_down(self, event):
        x, y = event.GetPosition()
        if self.region.Contains(x, y):
            self.clicked = True

    def on_left_dclick(self, event):
        self.on_left_down(event)

    def on_left_up(self, event):
        if self.clicked:
            x, y = event.GetPosition()
            if self.region.Contains(x, y):
                self.post_event()
        self.clicked = False

    def on_motion(self, event):
        if self.clicked:
            x, y = event.GetPosition()
            if not self.region.Contains(x, y):
                self.clicked = False

    def on_leave_window(self, event):
        self.clicked = False

class MenuButton(BubbleButton):
    def __init__(self, parent, normal=None, pressed=None, name="", target=None):
        super(MenuButton, self).__init__(parent, normal, pressed, name)
        self.target=target

    #@overrides(BubbleButton)
    def on_left_up(self, event):
        if self.clicked:
            x, y = event.GetPosition()
            if self.region.Contains(x, y):
                self.post_event()
                if self.target !=None:
                    settings.set_view(self.target)
        self.clicked = False

    #overrides (BubbleButton)
    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()
        #if settings.icon_view:
        bitmap = self.normal
        if self.clicked:
            bitmap = self.pressed or bitmap
        dc.DrawBitmap(bitmap, 0, 0)
        #else:
        #if self.clicked:
        #    dc.SetBrush(wx.Brush(settings.secondBackground))
        #else:
        #    dc.SetBrush(wx.Brush(settings.defaultForeground))
        #dc.SetPen(wx.Pen(settings.defaultAccent, 5))
        w,h=self.GetSize()
        #dc.DrawCircle(w/2, h/2, int(h*.35))
        if self.name!="":
            _butt_font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
            dc.SetFont(_butt_font)
            dc.SetTextForeground(settings.defaultForeground)
            dc.DrawText(self.name, int((w-len(self.name)*8)/2), int((h-16)/2))

class DynamicButton(BubbleButton):
    def __init__(self, parent, name="", inner_color=settings.button_inside, outer_color=settings.button_outside, text_color=settings.button_text, outline=settings.button_outline, target=None):
        super(DynamicButton, self).__init__(parent, None, None, name)
        self.target=target
        self.inner_color = inner_color
        self.outer_color = outer_color
        self.clicked_color = dim_color(self.inner_color, 80)
        self.text_color = text_color
        self.outline = outline

    def DoGetBestSize(self):
        return self.GetSize()

    #@overrides(BubbleButton)
    def on_left_up(self, event):
        if self.clicked:
            x, y = event.GetPosition()
            if self.region.Contains(x, y):
                self.post_event()
                if self.target !=None:
                    settings.set_view(self.target)
        self.clicked = False

    #overrides (BubbleButton)
    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()
        dc.SetPen(wx.Pen(self.outline, 5))
        w,h = self.GetSize()
        min_dim = min(h, w)

        rect = wx.Rect(0, 0, w, h)
        #print("dimensions= "+str((w,h)))
        self.region=wx.RegionFromPoints(gen_circle_points(w/2, h/2, min_dim/2))
        dc.SetClippingRegionAsRegion(self.region)
        inner = self.clicked_color if self.clicked else self.inner_color
        dc.GradientFillConcentric(rect, inner, self.outer_color, wx.Point(w/2, h/2))

        if self.name!="" :
            length_calc = self.name
            num_lines = (self.name.count("\n")+1)
            text_area_factor = .95 #percent of horizontal area available for text
            if num_lines > 1:
                text_area_factor = .85
                index = length_calc.find("\n")
                length_calc = length_calc[0:index]

            #find desired text area
            text_area_width = self.GetSize()[0]*text_area_factor
            text_point_size = int((text_area_width/7.11222063894596))
            _butt_font = wx.Font(text_point_size, wx.SWISS, wx.NORMAL, wx.BOLD)
            dc.SetFont(_butt_font)
            dc.SetTextForeground(self.text_color)
            #use object and text width to center it
            w,h = self.GetSize()
            tw,th = dc.GetTextExtent(length_calc)
            dc.DrawText(self.name, (w-tw)/2, (h-(th*num_lines))/2)

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def gen_circle_points(x, y, r):
    points=[]
    for theta in drange(0, 2*math.pi, .005):
        points.append([x+(r*math.cos(theta)), y+(r*math.sin(theta))])
    return points

#----------------------------------------------------------------------------------
def dynamic_demo():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,400))
    imagePath= settings.IMAGE_PATH+"Main/"
    settings.icon_view=False
    panel4 = DynamicButton(frm, "Test\nwho")
    frm.Show(True)
    ProtoApp.MainLoop()

def main():
    app = wx.App()
    frm = wx.Frame(None, size=(800,800))
    settings.icon_view = False
    menu = DynamicBubbleMenu(frm)
    menu.extrude=DynamicButton(menu, name='Extrusion')
    menu.gear=   DynamicButton(menu, name='Gear')
    menu.mug=    DynamicButton(menu, name='Mug')
    menu.ring=   DynamicButton(menu, name='Ring')
    menu.ring2=  DynamicButton(menu, name='Revolve')
    menu.vase=   DynamicButton(menu, name='Temp')
    menu.buttonList=[menu.extrude, menu.gear, menu.mug, menu.ring, menu.ring2, menu.vase]
    menu.setChildren(menu.buttonList)

    frm.Show(True)
    menu.Show(True)
    menu.SendSizeEvent()
    menu.CenterOnParent()
    app.MainLoop()


if __name__ == '__main__':
    main()