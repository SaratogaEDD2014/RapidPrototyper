import wx
import AppSettings

class BubbleMenu(wx.Window):
    def __init__(self, parent, bitmap, name="", children=[], id=-1, position=(0,40),size=(360, 360)):
        wx.Window.__init__(self, parent, id, wx.DefaultPosition, size=size)
        self.bitmap=bitmap
        self.name=name
        self.children=children
        self.pos=[]
        self.button=BubbleButton(self, bitmap)
        self.button.Disable()
        self.childIndex=0
        self.blank=wx.Panel(self, size=(90,90))
        self.SetBackgroundColour(AppSettings.backgroundColor)
        """Stupid Idea
        self.ZERO= [0,wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM]
        self.ONE=  [1,wx.ALIGN_CENTER]
        self.TWO=  [2,wx.ALIGN_LEFT | wx.ALIGN_BOTTOM]
        self.THREE=[3,wx.ALIGN_CENTER]
        self.FIVE= [5,wx.ALIGN_CENTER]
        self.SIX=  [6,wx.ALIGN_RIGHT | wx.ALIGN_TOP]
        self.SEVEN=[7,wx.ALIGN_CENTER]
        self.EIGHT=[8,wx.ALIGN_LEFT | wx.ALIGN_TOP]
        self.positions=[[self.SEVEN],
                        [self.THREE,self.FIVE],
                        [self.SIX,self.ONE,self.EIGHT],
                        [self.ZERO,self.TWO,self.SIX,self.EIGHT],
                        [self.THREE,self.FIVE,self.SIX,self.SEVEN,self.EIGHT],
                        [self.ZERO,self.THREE,self.SIX,self.TWO,self.FIVE,self.EIGHT],
                        [self.ZERO,self.TWO,self.THREE,self.FIVE,self.SIX,self.SEVEN,self.EIGHT],
                        [self.ZERO,self.ONE,self.TWO,self.THREE,self.FIVE,self.SIX,self.SEVEN,self.EIGHT]]
        """
        self.posIndices=[[7],
                        [3,5],
                        [6,1,8],
                        [0,2,6,8],
                        [3,5,6,7,8],
                        [0,3,6,2,5,8],
                        [0,2,3,5,6,7,8],
                        [0,1,2,3,5,6,7,8]]
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
        
    def Add(self, button):
        self.children.append(button)
        self.updateChildren()

    def AddMany(self, buttonList):
        self.Add(buttonList)

    def updateChildren(self):
        if len(self.children)>0:
            sizer=wx.GridSizer(3,3)
            for i in range(9):
                if (self.posIndices[len(self.children)-1].count(i)>0):
                    sizer.Add(self.nextChild(), 1, self.alignIndices[i])
                else:
                    sizer.Add(wx.Window(self, id=1000+i),1,self.alignIndices[i])
            sizer.Remove(4)
            sizer.Insert(4, self.button)
            self.SetSizer(sizer)
    
    def nextChild(self):
        self.childIndex+=1
        return self.children[self.childIndex-1]



class BubbleButton(wx.PyControl):
    def __init__(self, parent, normal, pressed=None, name=""):
        super(BubbleButton, self).__init__(parent, -1, style=wx.BORDER_NONE)
        self.style=wx.BORDER_NONE
        self.normal = normal
        self.pressed = pressed
        self.name=name
        #Region is the area that is "clickable"
        #It consists of the PNG minus the transparent areas
        self.region = wx.RegionFromBitmapColour(normal, wx.Colour(0, 0, 0, 0))
        self._clicked = False
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        #events
        self.Bind(wx.EVT_SIZE, self.on_size)                    #Used to make button fit as best as possible
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_window)
    
    def DoGetBestSize(self):
        return self.normal.GetSize()
    
    def post_event(self):
        event = wx.CommandEvent()
        event.SetEventObject(self)
        event.SetEventType(wx.EVT_BUTTON.typeId)
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
