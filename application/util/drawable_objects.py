#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      gabayj14
#
# Created:     16/01/2014
# Copyright:   (c) gabayj14 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import math
import wx

### Shadow figures have been ommited, as drawing code may change ###

#Returns the distance between two points
def get_distance(p1, p2):
	return math.sqrt( (math.pow(p1.x - p2[0], 2) + math.pow(p1.y - p2[1], 2) ) )


class figure:
	points = []
	def __init__(self):
		self.parent = None

	def set_parent(self, parent):
		self.parent = parent

   	def get_parent(self):
		temp = self

		while True:
			if temp.parent == None:
				break
			else:
				temp = temp.parent

		return temp

	def get_points(self):
		return self.points

#Basic geometry object, used throughout the code
class point(figure):
	x = 0
	y = 0

	parent = None #default standalone point

	def __init__(self, coords):
		self.x = coords[0]
		self.y = coords[1]

	def draw(self, canvas):
		dc = wx.MemoryDC(canvas)
		dc.SetPen(wx.BLACK_PEN)
		dc.SetBrush(wx.BLACK_BRUSH)

		dc.DrawCircle(self.x, self.y, 5)

		return canvas


	#Given a coordinate set, returns true of false if the click was within a radius, used for click detection.
	def check_if_selected(self, click_loc):
		radius = 5 # move this into config files?

		return (get_distance(self, click_loc) < radius )

class line(figure):
	def __init__(self, start, end):
		figure.__init__(self)

		self.start_point = start
		self.end_point = end

		self.points = [start, end]

		self.start_point.set_parent(self)
		self.end_point.set_parent(self)


	def draw(self, canvas):
		dc = wx.MemoryDC(canvas)
		dc.SetPen(wx.BLACK_PEN)
		dc.SetBrush(wx.BLACK_BRUSH)

		canvas = self.start_point.draw(canvas)
		canvas = self.end_point.draw(canvas)

		dc.DrawLine(self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y)

		dc.SelectObject(wx.NullBitmap)

		print 'debug: line drawn, @ Drawable objects ln 46'

		return canvas


class line_shadow():
 	def __init__(self, canvas, ret):
		self.canvas = canvas
		self.dc = wx.BufferedDC(wx.ClientDC(self.canvas))
		self.ret = ret

  		self.sx, self.sy = canvas.ScreenToClient(wx.GetMousePosition())

		self.dc.SetBrush(wx.Brush((0,0,0)))
		self.dc.SetPen(wx.Pen(wx.Colour(0,0,0), 2, wx.LONG_DASH))
		self.dc.DrawCircle(self.sx,self.sy,5)

		self.canvas.Bind(wx.EVT_MOTION, self.on_move)
		self.canvas.Bind(wx.EVT_LEFT_UP, self.finalize)


	def on_move(self, event):
		self.canvas.Refresh()
		self.dc.Clear()
		cx, cy = self.canvas.ScreenToClient(wx.GetMousePosition())

		self.dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
		self.dc.DrawCircle(self.sx,self.sy,5)
		self.dc.DrawCircle(cx,cy,5)

		self.dc.SetPen(wx.Pen(wx.Colour(0,0,0), 2, wx.LONG_DASH))
		self.dc.DrawLine(cx,cy,self.sx,self.sy)

	def finalize(self, e):
		print 'debug: line created  @ Drawable Objects ln 76'

		cx, cy = self.canvas.ScreenToClient(wx.GetMousePosition())

		self.canvas.Unbind(wx.EVT_MOTION)
		self.canvas.Unbind(wx.EVT_LEFT_UP)

		new_line = line(point( (self.sx,self.sy) ), point( (cx,cy) ))

		#Draw final line into canvas
		bitmap = self.canvas.GetBitmap()
		new_line.draw(bitmap)
		self.canvas.SetBitmap(bitmap)

		self.ret.__call__(new_line)

class rect(figure):
	def __init__(self, start, end):
		#Takes the start and end points (points as given by mouse) and generates lines and points
		#height = start.y - end.y //Not needed anymore?
		#width = start.x - end.x
		self.parent = None
		self.lines = []

		p1 = point((start.x, start.y))
		p2 = point((end.x, start.y))
		p3 = point((end.x, end.y))
		p4 = point((start.x, end.y))

		self.points = [p1, p2, p3, p4]

		self.lines.append(line(p1, p2))
   		self.lines.append(line(p2, p3))
		self.lines.append(line(p3, p4))
		self.lines.append(line(p4, p1))

		for i in self.lines:
			i.set_parent(self)

	def draw(self, canvas):
		dc = wx.MemoryDC(canvas)
		dc.SetPen(wx.BLACK_PEN)
		dc.SetBrush(wx.BLACK_BRUSH)

		for i in self.lines:
			canvas = i.draw(canvas)

		return canvas

class rect_shadow():
 	def __init__(self, canvas, ret):
		self.canvas = canvas
		self.dc = wx.BufferedDC(wx.ClientDC(self.canvas))
		self.ret = ret

  		self.sx, self.sy = canvas.ScreenToClient(wx.GetMousePosition())

		self.dc.SetBrush(wx.Brush((0,0,0)))
		self.dc.SetPen(wx.Pen(wx.Colour(0,0,0), 2, wx.LONG_DASH))
		self.dc.DrawCircle(self.sx,self.sy,5)

		self.canvas.Bind(wx.EVT_MOTION, self.on_move)
		self.canvas.Bind(wx.EVT_LEFT_UP, self.finalize)


	def on_move(self, event):
		self.canvas.Refresh()
		self.dc.Clear()
		cx, cy = self.canvas.ScreenToClient(wx.GetMousePosition())

  		self.dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
		points = [point((self.sx, self.sy)), point((cx, self.sy)), point((cx, cy)), point((self.sx, cy))]

		for i in points:
			i.draw(self.canvas.GetBitmap())

		self.dc.SetPen(wx.Pen(wx.Colour(0,0,0), 2, wx.LONG_DASH))

		self.dc.DrawLine(points[0].x, points[0].y, points[1].x, points[1].y)
		self.dc.DrawLine(points[1].x, points[1].y, points[2].x, points[2].y)
		self.dc.DrawLine(points[2].x, points[2].y, points[3].x, points[3].y)
		self.dc.DrawLine(points[3].x, points[3].y, points[0].x, points[0].y)


	def finalize(self, e):
		print 'debug: RECT created  @ Drawable Objects ln 76'

		cx, cy = self.canvas.ScreenToClient(wx.GetMousePosition())

		self.canvas.Unbind(wx.EVT_MOTION)
		self.canvas.Unbind(wx.EVT_LEFT_UP)

		new_rect = rect(point( (self.sx,self.sy) ), point( (cx,cy) ))

		#Draw final rect into canvas
		bitmap = self.canvas.GetBitmap()
		new_rect.draw(bitmap)
		self.canvas.SetBitmap(bitmap)

		self.ret.__call__(new_rect)

class arc(figure):
	def _init_(start, end, mid):
		self.start = start
		self.end = end
		self.mid = mid

		self.start.set_parent(self)
		self.end.set_parent(self)
		self.mid.set_parent(self)

		self.points = [start, end, mid]

	def draw(self, canvas):
		dc = wx.MemoryDC(canvas)
		dc.SetPen(wx.BLACK_PEN)
		dc.SetBrush(wx.BLACK_BRUSH)

		dc.DrawArc(self.start.x, self.start.y, self.end.x, self.end.y, self.mid.x, self.mid.y)

#class arc_shadow:
	#TODO: IMPLEMENT


