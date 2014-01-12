#Scott Krulcik Oct 2013
import wx

class BubbleEvent(wx.CommandEvent):
    def __init__(self, evtObj, target):
        wx.CommandEvent.__init__(self)
        self.SetEventObject(evtObj)
        self.SetEventType(wx.EVT_BUTTON.typeId)
        self.target=target

    def getTarget(self):
        return self.target
    def setTarget(self, targ):
        self.target=targ