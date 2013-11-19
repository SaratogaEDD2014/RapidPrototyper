import wx
import sys
import os

#UI------------------------------------------------------------------------
#Colors
defaultForeground=wx.Colour(255,255,255)
secondForeground=wx.Colour(200,200,200)
defaultBackground=wx.Colour(30,106,246)
secondBackground=wx.Colour(140,175,200)
defaultAccent=wx.Colour(255,125,75)
secondAccent=wx.Colour(230,70,50)

#Appinfo
previousPage=None
currentPage=None

#Resources:
PATH=os.getcwd()
PATH=PATH[:PATH.rfind("GUI")+3] + "/"
IMAGE_PATH=PATH+"images/"
sys.path.append(os.getcwd())

userFilePath=PATH
recentFiles=[PATH+"examples/teapot.stl",
             PATH+"examples/magnolia.stl",
             PATH+"examples/sphere.stl",
             PATH+"examples/cube.stl",
             PATH+"examples/bottle.stl"]
#Print Operations----------------------------------------------------------
LAYER_DEPTH=.01 #IN INCHES


def addRecentFile(filename):
    global recentFiles
    recentFiles.insert(0,filename)
    if len(recentFiles)>5:
        recentFiles=recentFiles[0:6]
