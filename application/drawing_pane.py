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
import wx
import util.drag
import util.drawable_objects


class drawing_area(wx.Panel):
	def __init__(self, parent, id, pos, size):
		wx.Panel.__init__(self, parent, id, pos, size)

		self.canvas = wx.StaticBitmap(self, pos=(50,0), size=wx.Size(550,600))
		self.canvas.SetBitmap(wx.EmptyBitmapRGBA(550,600,0,255,255,255))
		self.canvas.Show()
		self.Refresh()

		self.tool_bar = tool_menu(self)
		self.Refresh()

		self.SetBackgroundColour((255,255,255))
		self.Show(True)
		self.canvas.Bind(wx.EVT_LEFT_DOWN, self.on_click)

		self.dc = wx.ClientDC(self.canvas)
		self.dc.SetPen(wx.Pen(wx.Colour(0,0,0), 2))
		self.dc.SetBrush(wx.Brush(wx.Colour(0,0,0)))

		self.current_action = self.select
		self.objects = []

	#Drawing tips
	def update_tip(self, tip):
		tips = {'select':self.select, 'line':self.create_line, 'box':self.create_box, 'arc':self.create_arc, 'delete':self.delete()}

		self.current_action = tips[tip]

	def select(self,e):
		print 'selecting'
		for i in self.objects:
			if i.checkTouch(e.GetPositionTuple()):
				i.touch()

	def create_line(self,e):
		l = DrawableObjects.line_shadow(self.canvas, self.finish_create)

	def create_box(self,e):
		pass
	def create_arc(self,e):
		pass
	def delete(self, e):
		pass

	def on_click(self, e):
		self.current_action.__call__(e)


	def finish_create(self, new_obj):
		self.objects.append(new_obj)
	#	self.redraw()

	def redraw(self):
		bitmap = self.canvas.GetBitmap()
		print bitmap.GetSize()
		print str(len(self.objects))

		for i in self.objects:
			bitmap = i.draw(bitmap)

		self.canvas.SetBitmap(bitmap)
		self.canvas.Refresh()
	#	self.dc.DrawBitmap(bitmap, 0,0)
		print 'debug: redraw called, finished.'


class tool_menu(wx.Panel):
	def __init__(self,parent,id = -1,pos=(0,0),size=(50,600)):
		wx.Panel.__init__(self, parent, id, pos, size)
		self.SetBackgroundColour(wx.Colour(0,0,0,255))
		self.Show(True)
		self.parent = parent

		select_button = menu_item(self, 1, 'select', (2,15))
		line_button = menu_item(self, 2, 'line', (2, 65))
		box_button = menu_item(self, 3, 'box', (2, 115))
		arc_button = menu_item(self, 4, 'arc', (2, 165))
		del_button = menu_item(self, 5, 'delete', (2, 215))

		select_button.Bind(wx.EVT_BUTTON, self.select_button)
		line_button.Bind(wx.EVT_BUTTON, self.line_button)
		box_button.Bind(wx.EVT_BUTTON, self.box_button)
		arc_button.Bind(wx.EVT_BUTTON, self.arc_button)
		del_button.Bind(wx.EVT_BUTTON, self.del_button)

	def select_button(self, e):
		# Is this 'proper' code?
		self.parent.update_tip('select')
	def line_button(self, e):
		self.parent.update_tip('line')
	def box_button(self, e):
		self.parent.update_tip('box')
	def arc_button(self, e):
		self.parent.update_tip('arc')
	def del_button(self, e):
		self.parent.update_tip('delete')

class menu_item(wx.Button):
	def __init__(self, parent, id, label, pos, size=(46,46)):
		wx.Button.__init__(self, parent, id, label, pos, size)


