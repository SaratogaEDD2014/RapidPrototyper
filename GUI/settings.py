import wx

#Resources Information:
NAME = 'Charlie'
PATH = ''   #to be set in App.py
IMAGE_PATH = ''#to Be set in App.py
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
        del current
        prev_page.remove(temp)
        set_current_page(temp)#Do not "set_view" because that will add to previous pages

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
LAYER_DEPTH=.012 #IN INCHES
BUILD_PIXELS = (1080, 960)
BUILD_AREA = (9.0, 6.5, 8)
BUILD_PPI = (BUILD_PIXELS[0]/BUILD_AREA[0], BUILD_PIXELS[1]/BUILD_AREA[1])

#UI------------------------------------------------------------------------
icon_view = True
temp_app = wx.App()
app_x, app_y = 0,0
app_w, app_h = wx.GetDisplaySize()
default_touchscreen = True
if default_touchscreen:
    for i in range(0, wx.Display.GetCount()):
        xo,yo,w,h = wx.Display(i).GetGeometry()
        if h== 600 and w==1024:
            #Is the default touchscreen
            app_x, app_y = xo, yo
            app_w, app_h = 1024, 600
toolbar_h = 40
toolbar_w = app_w
temp_app.Destroy()

schemes = {"BLUE":1, "GREEN":2, 'PINK':3, 'RED':4}
invert_color = False
scheme = schemes["BLUE"]* (-1 if invert_color else 1)
#Colors
if scheme == 1:
    defaultForeground = wx.Colour(30,75,205)
    secondForeground = wx.Colour(200,200,200)
    defaultBackground = wx.Colour(245,245,245)
    secondBackground = wx.Colour(140,175,200)
    defaultAccent = wx.Colour(255,125,75)
    secondAccent = wx.Colour(230,70,50)
    button_inside = wx.Colour(51, 123, 255)
    button_outside = wx.Colour(0, 75, 225)
    button_outline = wx.Colour(255,255,255)
    button_text = wx.Colour(255,255,255)
    toolbar_bottom = wx.Colour(177, 177, 177)
    toolbar_top = wx.Colour(228, 228, 228)
elif scheme == 2:
    defaultForeground = wx.Colour(16, 167, 91)
    secondForeground = wx.Colour(200,200,200)
    defaultBackground = wx.Colour(245,245,245)
    secondBackground = wx.Colour(120,200,150)
    defaultAccent = wx.Colour(16, 42, 167)
    secondAccent = wx.Colour(205, 127, 50)
    button_inside = wx.Colour(51, 255, 123)
    button_outside = wx.Colour(20, 200, 75)
    button_outline = wx.Colour(255,255,255)
    button_text = wx.Colour(255,255,255)
    toolbar_bottom = wx.Colour(177, 177, 177)
    toolbar_top = wx.Colour(228, 228, 228)
elif scheme == 3:
    defaultForeground = wx.Colour(243, 146, 146)
    secondForeground = wx.Colour(200,200,200)
    defaultBackground = wx.Colour(245,245,245)
    secondBackground = wx.Colour(200,175,140)
    defaultAccent = wx.Colour(250, 175, 250)
    secondAccent = wx.Colour(50, 128, 205)
    button_inside = wx.Colour(255, 150, 150)
    button_outside = wx.Colour(233, 120, 120)
    button_outline = wx.Colour(255,255,255)
    button_text = wx.Colour(255,255,255)
    toolbar_bottom = wx.Colour(177, 177, 177)
    toolbar_top = wx.Colour(228, 228, 228)
elif scheme == 4:
    defaultForeground = wx.Colour(255, 50, 30)
    secondForeground = wx.Colour(200,200,200)
    defaultBackground = wx.Colour(245,245,245)
    secondBackground = wx.Colour(200,100,140)
    defaultAccent = wx.Colour(45, 45, 220)
    secondAccent = wx.Colour(16, 167, 91)
    button_inside = wx.Colour(255, 90, 90)
    button_outside = wx.Colour(230, 10, 10)
    button_outline = wx.Colour(255,255,255)
    button_text = wx.Colour(255,255,255)
    toolbar_bottom = wx.Colour(177, 177, 177)
    toolbar_top = wx.Colour(228, 228, 228)
#Inverted schemes
if scheme == -1:
    defaultForeground  = wx.Colour(245,245,245)
    secondForeground = wx.Colour(140,175,200)
    defaultBackground = wx.Colour(30,75,205)
    secondBackground = wx.Colour(200,200,200)
    defaultAccent = wx.Colour(255,125,75)
    secondAccent = wx.Colour(230,70,50)
    button_inside = wx.Colour(255,255,255)
    button_outside = wx.Colour(220,220,220)
    button_outline =wx.Colour(245,245,245)
    button_text = wx.Colour(30,75,205)
    toolbar_bottom = wx.Colour(177, 177, 177)
    toolbar_top = wx.Colour(228, 228, 228)
elif scheme == -2:
    defaultForeground = wx.Colour(245,245,245)
    secondForeground = wx.Colour(120,200,150)
    defaultBackground = wx.Colour(16, 167, 91)
    secondBackground = wx.Colour(200,200,200)
    defaultAccent = wx.Colour(16, 42, 167)
    secondAccent = wx.Colour(205, 127, 50)
    button_inside = wx.Colour(255,255,255)
    button_outside = wx.Colour(220,220,220)
    button_outline = wx.Colour(245,245,245)
    button_text = wx.Colour(16, 167, 91)
    toolbar_bottom = wx.Colour(177, 177, 177)
    toolbar_top = wx.Colour(228, 228, 228)
elif scheme == -3:
    defaultForeground = wx.Colour(245,245,245)
    secondForeground = wx.Colour(200,175,140)
    defaultBackground = wx.Colour(243, 96, 96)
    secondBackground = wx.Colour(200,200,200)
    defaultAccent = wx.Colour(45, 45, 190)
    secondAccent = wx.Colour(50, 128, 205)
    button_inside = wx.Colour(255,255,255)
    button_outside = wx.Colour(220,220,220)
    button_outline = wx.Colour(245,245,245)
    button_text = wx.Colour(243, 96, 96)
    toolbar_bottom = wx.Colour(177, 177, 177)
    toolbar_top = wx.Colour(228, 228, 228)
elif scheme == -4:
    defaultForeground = wx.Colour(245,245,245)
    secondForeground = wx.Colour(200,100,140)
    defaultBackground = wx.Colour(255, 50, 30)
    secondBackground = wx.Colour(200,200,200)
    defaultAccent = wx.Colour(45, 45, 220)
    secondAccent = wx.Colour(16, 167, 91)
    button_inside = wx.Colour(255,255,255)
    button_outside = wx.Colour(220,220,220)
    button_outline = wx.Colour(245,245,245)
    button_text = wx.Colour(255, 50, 30)
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
