import wx
import sys
import os

#Resources Information:
PATH=os.path.dirname(os.path.realpath(__file__))+'/'
IMAGE_PATH=PATH+"images/"
sys.path.append(PATH[:PATH.rfind("GUI")])

#Matt's part
cfg= wx.Config('config')

#Runtime information
prev_page=[]
currentPage=None

def add_prev_page(page):
    if page != None:
        page.Show(False)
        prev_page.append(page)

def goto_prev_page():
    if len(prev_page)>=1:
        temp=prev_page[len(prev_page)-1]
        get_current_page().Show(False)
        prev_page.remove(temp)
        set_current_page(temp)

def get_prev_page():
    if len(prev_page)>0:
        return prev_page[len(prev_page)-1]
    return None

def set_current_page(page):
    global currentPage
    currentPage=page
    page.Show(True)

def get_current_page():
    global currentPage
    return currentPage

def set_view(view):
    """CRITICAL: This is how we change which window is being displayed, it is defined within the Frame class"""
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
icon_view=True
#Colors
defaultForeground=wx.Colour(255,255,255)
secondForeground=wx.Colour(200,200,200)
defaultBackground=wx.Colour(30,106,246)
#defaultBackground=wx.Colour(255,0,0)
secondBackground=wx.Colour(140,175,200)
defaultAccent=wx.Colour(255,125,75)
secondAccent=wx.Colour(230,70,50)

def set_property_color(self, key, color):
    cfg.WriteInt(key+'R', color.Red())
    cfg.WriteInt(key+'G', color.Green())
    cfg.WriteInt(key+'B', color.Blue())

def get_property_color(self,key):
    red=cfg.ReadInt(key+'R', color.Red())
    green=cfg.ReadInt(key+'G', color.Red())
    blue=cfg.ReadInt(key+'B', color.Red())
    return wx.Colour(red, green, blue)

def set_layer_depth(self, depth):
    cfg.WriteFloat('layerDepth', depth)

def get_layer_depth(self):
    return cfg.ReadFloat('layerDepth')
