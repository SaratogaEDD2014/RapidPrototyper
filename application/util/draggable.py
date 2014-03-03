#-------------------------------------------------------------------------------
# Name:		module1
# Purpose:
#
# Author:	  Joseph
#
# Created:	 02/02/2014
# Copyright:   (c) Joseph 2014
# Licence:	 <your licence>
#-------------------------------------------------------------------------------

import wx

#Dragging code
class draggable(wx.Panel):
	clickDelta = (0,0)
	isDragging = False

	def __init__(self, parent, id, pos, size):
		wx.Panel.__init__(self, parent, id, pos, size)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
		self.Bind(wx.EVT_LEFT_UP, self.OnRelease)
		self.Bind(wx.EVT_MOTION, self.OnMouseMove)
	def OnClick(self, e):
		self.clickDelta = e.GetPositionTuple()
		self.Refresh()
		self.isDragging = True

	def OnRelease(self, e):
		self.Refresh()
		self.isDragging = False
	def OnMouseMove(self, e):
		if self.isDragging:
			dx, dy = self.clickDelta
			mx, my = e.GetPositionTuple()
			x,y = self.GetPositionTuple()

			x += mx-dx
			y += my-dy

			self.clickDelta = e.GetPositionTuple()
			self.SetPosition((x,y))

			self.Refresh()
