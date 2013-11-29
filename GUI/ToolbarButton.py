import wx

class ToolbarButton(wx.PyControl):
    def __init__(self, parent, normal, pressed=None, disabled=None, name=None):
        super(ToolbarButton, self).__init__(parent, -1, style=wx.BORDER_NONE)
        self.normal = normal
        self.pressed = pressed
        self.disabled=disabled
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
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_window)

    def DoGetBestSize(self):
        return self.normal.GetSize()

    def post_event(self):
        event = wx.CommandEvent()
        event.SetEventObject(self)
        event.SetEventType(wx.EVT_BUTTON.typeId)
        wx.PostEvent(self, event)

    def Enable(self, *args, **kwargs):
        super(ToolbarButton, self).Enable(*args, **kwargs)
        self.Refresh()
    def Disable(self, *args, **kwargs):
        super(ToolbarButton, self).Disable(*args, **kwargs)
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
        if not self.IsEnabled():
            bitmap = self.disabled or bitmap
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

    def on_left_up(self, event):
        if self.clicked:
            x, y = event.GetPosition()
            if self.region.Contains(x, y):
                self.post_event()
        self.clicked = False

    def on_leave_window(self, event):
        self.clicked = False

def main():
    import AppSettings
    imagePath=AppSettings.IMAGE_PATH
    def on_button(event):
        print 'Button was clicked.'
    app = wx.App()
    frame = wx.Frame(None, -1, 'Shaped Button Demo')
    panel = wx.Panel(frame, -1)
    button = ToolbarButton(panel,
                          wx.Bitmap(imagePath+'BubbleButtonTemplate.png'),
                          wx.Bitmap(imagePath+'BubbleButtonPressed.png'))
    button.Bind(wx.EVT_BUTTON, on_button)
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.AddStretchSpacer(1)
    sizer.Add(button, 0, wx.ALIGN_CENTER)
    sizer.AddStretchSpacer(1)
    panel.SetSizer(sizer)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()