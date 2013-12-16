import wx
import math
from GUI.settings import *

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def gen_circle_points(x, y, r):
    points=[]
    for theta in drange(0, 2*math.pi, .1):
        points.append([x+(r*math.cos(theta)), y+(r*math.sin(theta))])
    return points

def main():
    app = wx.App()
    frm = wx.Frame(None, size=(200,200))
    def changeSize(event):
        w,h = frm.GetSize()
        min_dim = min(h, w)
        x,y = 0,0 #frm.GetPosition()
        dc = wx.ClientDC(frm)
        rect = wx.Rect(x, y, w, h)
        dc.SetClippingRegionAsRegion(wx.RegionFromPoints(gen_circle_points(w/2, h/2, min_dim/2)))
        dc.GradientFillConcentric(rect, defaultBackground, defaultForeground, wx.Point(x+w/2, y+h/2))

    frm.Bind(wx.EVT_SIZE, changeSize)
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
