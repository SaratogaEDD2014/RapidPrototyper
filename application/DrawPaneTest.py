import wx
import DrawPane

def main():
	app = wx.App()

	mainframe = wx.Frame(None, -1, 'drawpane testing')
	mainframe.SetDimensions(0,0,600,600)
	mainframe.Show(True)

	drawPane = DrawPane.drawing_area(mainframe,-1,(0,0),mainframe.GetSize())

	drawPane.Show(True)

	app.MainLoop()

if __name__ == '__main__':
	main()


#Next step: in the redraw method, draw everything onto a blank png file
