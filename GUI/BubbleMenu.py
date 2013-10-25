import wx
import BubbleEvent
import AppSettings

class BubbleMenu(wx.Window):
    def __init__(self, parent, bitmap, name="", children=[], id=-1, position=(0,40), size=(360, 360)):
        super(BubbleMenu, self).__init__(parent, id, wx.DefaultPosition, size=size)
        self.Show(False)
        self.bitmap=bitmap
        self.name=name
        self.children=children
        self.pos=[]
        self.button=BubbleButton(self, bitmap)
        self.button.Disable()
        self.childIndex=0
        self.SetBackgroundColour(AppSettings.defaultBackground)

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
        self.Bind(wx.EVT_BUTTON, self.onClick)

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
                    sizer.Add(wx.Panel(self, size=(90,90), id=1000+i), flag=self.alignIndices[i])
            sizer.Remove(4)
            sizer.Insert(4, self.button, flag=wx.ALIGN_CENTER)
            self.SetSizer(sizer)

    def nextChild(self):
        self.childIndex+=1
        return self.children[self.childIndex-1]

    def onClick(self, event):
        source=event.GetEventObject()
        if source in self.children:
            #So if this menu is the parent
            self.parent.setView(source.target)



class BubbleButton(wx.PyControl):
    def __init__(self, parent, normal, pressed=None, name="", target=None):
        super(BubbleButton, self).__init__(parent, -1, style=wx.BORDER_NONE)
        self.style=wx.BORDER_NONE
        self.normal = normal
        self.pressed = pressed
        self.name=name
        self.target=target
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
        event = BubbleEvent.BubbleEvent(self, self.target)
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
