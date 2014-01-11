import wx
import sys
import os

test = False

#Resources Information:
NAME = 'Charlie'
PATH=os.path.dirname(os.path.realpath(__file__))+'/'
IMAGE_PATH=PATH+"images/"
sys.path.append(PATH[:PATH.rfind("GUI")])
main_window=None
display_part=True

#Matt's part
cfg= wx.Config('config')

#Runtime information
prev_page=[]
global currentPage
currentPage=None

def add_prev_page(page):
    if page != None:
        page.Show(False)
        prev_page.append(page)

def goto_prev_page():
    if len(prev_page)>=1:
        temp=prev_page[len(prev_page)-1]
        current=get_current_page()
        current.Show(False)
        prev_page.remove(temp)
        set_current_page(temp)#Do not "set_view" because that will add to previous pages
        refresh_view_panel()
def get_prev_page():
    if len(prev_page)>0:
        return prev_page[len(prev_page)-1]
    return None

def set_current_page(page):
    global currentPage
    currentPage=page
    #page.Show(True)

def get_current_page():
    global currentPage
    return currentPage

def set_view(view):
    pass
def refresh_view_panel():
    pass

#Recent and example files
userFilePath=PATH
recentFiles=[PATH+"examples/teapot.stl",
             PATH+"examples/magnolia.stl",
             PATH+"examples/sphere.stl",
             PATH+"examples/cube.stl",
             PATH+"examples/bottle.stl"]
def addRecentFile(filename):
    global recentFiles
    recentFiles.insert(0,filename)
    if len(recentFiles)>5:
        recentFiles=recentFiles[0:6]



#Print Operations----------------------------------------------------------
LAYER_DEPTH=.01 #IN INCHES


#UI------------------------------------------------------------------------
icon_view = True
toolbar_h = 40
toolbar_w = 800
app_w = 800
app_h = 440
#Colors
defaultForeground = wx.Colour(255,255,255)
secondForeground = wx.Colour(200,200,200)
defaultBackground = wx.Colour(30,106,246)
#defaultBackground = wx.Colour(255,0,0)
secondBackground = wx.Colour(140,175,200)
defaultAccent = wx.Colour(255,125,75)
secondAccent = wx.Colour(230,70,50)
button_inside = wx.Colour(0,0,255)
button_outside = wx.Colour(0,0,255)
button_outline = wx.Colour(255,255,255)
button_text = wx.Colour(255,255,255)
toolbar_bottom = wx.Colour(177, 177, 177)
toolbar_top = wx.Colour(228, 228, 228)

def set_property_color(key, color):
    cfg.WriteInt(key+'R', color.Red())
    cfg.WriteInt(key+'G', color.Green())
    cfg.WriteInt(key+'B', color.Blue())

def get_property_color(key, defaults=[0,0,0]):
    red=cfg.ReadInt(key+'R', defaults[0])
    green=cfg.ReadInt(key+'G', defaults[1])
    blue=cfg.ReadInt(key+'B', defaults[2])
    return wx.Colour(red, green, blue)

def set_layer_depth(depth):
    cfg.WriteFloat('layerDepth', depth)

def get_layer_depth():
    return cfg.ReadFloat('layerDepth')

get_property_color("default_background")
