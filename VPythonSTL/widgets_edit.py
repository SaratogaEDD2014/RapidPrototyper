from __future__ import division, print_function
from visual import *
from visual.filedialog import get_file
import wx

w = window(width=400, height=500,
           menus=False, title='Widgets')
def add_display(win):
    display(window=win, x=100, y=100, width=400, height=400, forward=-vector(0,1,2))
    boxer = box(color = color.red)
    w.win.SendSizeEvent()
add_display(w)
# wx is the wxPython library (see wxpython.org)

# wxPython is a Python library that makes it possible to create
# windows and handle events cross-platform, with native look-and-feel on
# Windows, Mac, and Linux. This program widgets.py uses VPython to handle
# 3D graphics, and wxPython statements to create buttons, sliders, etc.
# Among the documentation mentioned at wxpython.org, a particularly
# useful reference manual is docs.wxwidgets.org/2.8/wx_contents.html.
# (VPython uses wxPython 2.9, but the 2.8 documentation is similar,
# and at the time of writing the 2.9 documentation is labeled at
# wxwidgets.org/docs as being in "testing" mode.)

# At that site, the section "Classes by category" gives a useful
# overview of the components of wxPython, and the category "Controls"
# describes all the things you can do with buttons, sliders, etc.
# One needs to know that when you see "wxButton" that actually means
# wx.Button, after importing wx. Also, it is helpful to know that
# wxPython is based on wxWidgets, a library for C++ programs, and the
# documentation for wxPython and wxWidgets is very similar.

# For simplicity, this program places various widgets at specific
# positions within the window. However, wxPython also offers the
# option to allow it to rearrange the positioning of widgets as
# a function of window size and shape. A good tutorial on wxPython,
# which includes a discussion of "Layout Management", is found at
# zetcode.com/wxpython.

# Functions that are called on various events

##def setleft(evt): # called on "Rotate left" button event
##    cube.dir = -1
##
##def setright(evt): # called on "Rotate right" button event
##    cube.dir = 1
##
##def setred(evt): # called by "Make red" menu item
##    cube.color = color.red
##    t1.SetSelection(0) # set the top radio box button (red)
##
##def setcyan(evt): # called by "Make cyan" menu item
##    cube.color = color.cyan
##    t1.SetSelection(1) # set the bottom radio box button (cyan)
##
##def togglecubecolor(evt): # called by radio box (a set of two radio buttons)
##    choice = t1.GetSelection()
##    if choice == 0: # upper radio button (choice = 0)
##        cube.color = color.red
##    else: # lower radio button (choice = 1)
##        cube.color = color.cyan
##
##def cuberate(value):
##    cube.dtheta = 2*value*pi/1e4
##
##def setrate(evt): # called on slider events
##    value = s1.GetValue()
##    cuberate(value) # value is min-max slider position, 0 to 100
##
##def stl_to_faces(fileinfo): # specify file
##    # Accept a file name or a file descriptor; make sure mode is 'rb' (read binary)
##    if isinstance(fileinfo, str):
##        fd = open(fileinfo, mode='rb')
##    elif isinstance(fileinfo, file):
##        if fileinfo.mode != 'rb':
##            filename = fileinfo.name
##            fileinfo.close()
##            fd = open(filename, mode='rb')
##        else:
##            fd = fileinfo
##    else:
##        raise TypeError, "Specify a file"
##    text = fd.read()
##    if chr(0) in text: # if binary file
##        text = text[84:]
##        L = len(text)
##        N = 2*(L//25) # 25/2 floats per point: 4*3 float32's + 1 uint16
##        triNor = zeros((N,3), dtype=float32)
##        triPos = zeros((N,3), dtype=float32)
##        n = i = 0
##        while n < L:
##            if n % 200000 == 0:
##                print ("%d" % (100*n/L))+"%",
##            triNor[i] = fromstring(text[n:n+12], float32)
##            triPos[i] = fromstring(text[n+12:n+24], float32)
##            triPos[i+1] = fromstring(text[n+24:n+36], float32)
##            triPos[i+2] = fromstring(text[n+36:n+48], float32)
##            colors = fromstring(text[n+48:n+50], uint16)
##            if colors != 0:
##                print('%x' % colors)
##            if triNor[i].any():
##                triNor[i] = triNor[i+1] = triNor[i+2] = norm(vector(triNor[i]))
##            else:
##                triNor[i] = triNor[i+1] = triNor[i+2] = \
##                    norm(cross(triPos[i+1]-triPos[i],triPos[i+2]-triPos[i]))
##            n += 50
##            i += 3
##    else:
##        fd.seek(0)
##        fList = fd.readlines()
##        triPos = []
##        triNor = []
##
##        # Decompose list into vertex positions and normals
##        for line in fList:
##            FileLine = line.split( )
##            if FileLine[0] == 'facet':
##                for n in range(3):
##                    triNor.append( [ float(FileLine[2]), float(FileLine[3]), float(FileLine[4]) ]  )
##            elif FileLine[0] == 'vertex':
##                triPos.append( [ float(FileLine[1]), float(FileLine[2]), float(FileLine[3]) ]  )
##
##        triPos = array(triPos)
##        triNor = array(triNor)
##
##    # Compose faces in default frame
##    f = frame()
##    return faces(frame=f, pos=triPos, normal=triNor)
##
##L = 320
### Create a window. Note that w.win is the wxPython "Frame" (the window).
### window.dwidth and window.dheight are the extra width and height of the window
### compared to the display region inside the window. If there is a menu bar,
### there is an additional height taken up, of amount window.menuheight.
##w = window(width=2*(L+window.dwidth), height=L+window.dheight+window.menuheight,
##           menus=True, title='Widgets')
##
### Place a 3D display widget in the left half of the window.
##d = 20
##display(window=w, x=d, y=d, width=L-2*d, height=L-2*d, forward=-vector(0,1,2))
##cube = box(color=color.red)
##fd = get_file()
##newobject = stl_to_faces(fd)
##newobject.smooth() # average normals at a vertex
##
### Examples of modifying the returned object:
####        newobject.frame.pos = (-1,-1,-0.5)
####        newobject.frame.axis = (0,1,0)
##newobject.color = color.blue
##newobject.material = materials.plastic
##
### Place buttons, radio buttons, a scrolling text object, and a slider
### in the right half of the window. Positions and sizes are given in
### terms of pixels, and pos(0,0) is the upper left corner of the window.
##p = w.panel # Refers to the full region of the window in which to place widgets
##
##wx.StaticText(p, pos=(d,4), size=(L-2*d,d), label='A 3D canvas',
##              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
##
##left = wx.Button(p, label='Rotate left', pos=(L+10,15))
##left.Bind(wx.EVT_BUTTON, setleft)
##
##right = wx.Button(p, label='Rotate right', pos=(1.5*L+10,15))
##right.Bind(wx.EVT_BUTTON, setright)
##
##t1 = wx.RadioBox(p, pos=(1.0*L,0.3*L), size=(0.25*L, 0.25*L),
##                 choices = ['Red', 'Cyan'], style=wx.RA_SPECIFY_ROWS)
##t1.Bind(wx.EVT_RADIOBOX, togglecubecolor)
##
### On the Mac, wx.TextCtrl is resized when the window is resized.
### This resizing does not occur on Windows or Linux. Unlike for
### wx.StaticText used above, there is no wx.ST_NO_AUTORESIZE option.
##tc = wx.TextCtrl(p, pos=(1.4*L,90), value='You can type here:\n',
##            size=(150,90), style=wx.TE_MULTILINE)
##tc.SetInsertionPoint(len(tc.GetValue())+1) # position cursor at end of text
##tc.SetFocus() # so that keypresses go to the TextCtrl without clicking it
##
##s1 = wx.Slider(p, pos=(1.0*L,0.8*L), size=(0.9*L,20), minValue=0, maxValue=100)
##s1.Bind(wx.EVT_SCROLL, setrate)
##wx.StaticText(p, pos=(1.0*L,0.75*L), label='Set rotation rate')
##
### Create a menu of options (Rotate right, Rotate right, Make red, Make cyan).
### Currently, menus do not work on the Macintosh.
##m = w.menubar # Refers to the menubar, which can have several menus
##
##menu = wx.Menu()
##item = menu.Append(-1, 'Rotate left', 'Make box rotate to the left')
##w.win.Bind(wx.EVT_MENU, setleft, item)
##
##item = menu.Append(-1, 'Rotate right', 'Make box rotate to the right')
##w.win.Bind(wx.EVT_MENU, setright, item)
##
##item = menu.Append(-1, 'Make red', 'Make box red')
##w.win.Bind(wx.EVT_MENU, setred, item)
##
##item = menu.Append(-1, 'Make cyan', 'Make box cyan')
##w.win.Bind(wx.EVT_MENU, setcyan, item)
##
### Add this menu to an Options menu next to the default File menu in the menubar
##m.Append(menu, 'Options')
##
### Initializations
##s1.SetValue(70) # update the slider
##cuberate(s1.GetValue()) # set the rotation rate of the cube
##cube.dir = -1 # set the rotation direction of the cube

# A VPython program that uses these wxPython capabilities should always end
# with an infinite loop containing a rate statement, as future developments
# may require this to keep a display active.
while True:
    rate(100)
##    cube.rotate(axis=(0,1,0), angle=cube.dir*cube.dtheta)

