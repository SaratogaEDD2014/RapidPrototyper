import wx
import draw_pane

def main():
	app = wx.App()

	mainframe = wx.Frame(None, -1, 'drawpane testing')
	mainframe.SetDimensions(0,0,600,600)
	mainframe.Show(True)

	draw_pane = draw_pane.drawing_area(mainframe,-1,(0,0),mainframe.GetSize())

	draw_pane.Show(True)

	app.MainLoop()

if __name__ == '__main__':
	main()


#Next step: in the redraw method, draw everything onto a blank png file
