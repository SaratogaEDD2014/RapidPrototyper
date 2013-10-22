import wx

#UI
defaultForeground=wx.Colour(0,0,0)
defaultBackground=wx.Colour(30,100,255)
secondBackground=wx.Colour(136,136,150)
defaultAccent=wx.Colour(255,100,30)
previousPage=None
currentPage=None

#PATH="/home/ubuntu/Documents/RapidPrototyper/GUI/"  #Ubuntu
#PATH="/Users/Scott/Documents/EDD/RapidPrototyper/GUI/" #MAC
#PATH="C:\\Users\\krulciks14\\Documents\\Github\\RapidPrototyper\\GUI\\" #PC (Microsoft)
PATH= "/Volumes/813-2937/RapidPrototyper/GUI/"

IMAGE_PATH=PATH+"images/"
userFilePath=PATH
recentFiles=[PATH+"examples/teapot.stl",
             PATH+"examples/magnolia.stl",
             PATH+"examples/sphere.stl",
             PATH+"examples/cube.stl",
             PATH+"examples/bottle.stl"]
#Print
LAYER_DEPTH=.01 #IN INCHES


def addRecentFile(filename):
    global recentFiles
    recentFiles.insert(0,filename)
    if len(recentFiles)>5:
        recentFiles=recentFiles[0:6]