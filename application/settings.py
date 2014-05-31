import wx

cfg= wx.Config('config')
def set_name(n):
    cfg.Write('name', n)
def get_name():
    return cfg.Read('name', defaultVal="Charlie")

temp_app = wx.App()
#Resources Information:
NAME = get_name()# will be 'Charlie' in future
USER_NAME = 'Kristi!'
PATH = ''   #to be set in app.py
IMAGE_PATH = ''#to Be set in app.py
main_window=None
display_part=True
debug = True
if debug:
    import os
    import sys
    PATH = os.path.dirname(os.path.realpath(sys.argv[0]))+'/'
    sys.path.append(PATH[:PATH.rfind("application")])
    PATH = PATH[:PATH.rfind("application")+12]
    IMAGE_PATH = PATH + 'appearance/'
    USER_PATH = PATH +'examples/'


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
unit_factors = {'mm':25.40,
                    'cm':2.54,
                    'in':1.00,
                    'ft':1/12.,
                    'm':.0254}
def set_units(unit_type):
    if unit_type.__class__ is str and unit_factors.has_key(unit_type):
        cfg.Write("units", unit_type)
    elif not cfg.HasEntry("units"):
        cfg.Write("units", 'in')
def get_units():
    return cfg.Read('units', defaultVal='in')
units = property(get_units, set_units, doc="The type of units the files the user is entering are using.")


def get_layer_depth():
    return cfg.ReadFloat('layerDepth', defaultVal=.012)

def get_layer_cure_time():
    return cfg.ReadInt('layerCureTime', defaultVal=2)

base_depth = .125 #Height of pad that rests below part
##_off_x = 0.0
##def get_off_x():
##    return _off_x
##def set_off_x(val):
##    _off_x = val
##_off_y = 0.0
##def get_off_y():
##    return _off_y
##def set_off_y(val):
##    _off_y = val
##_off_z = 0.0
##def get_off_z():
##    return _off_z
##def set_off_z(val):
##    _off_z = val
OFFSET_X = 0.0
OFFSET_Y = 0.0
OFFSET_Z = 0.0
SCALE_X = 1.0
SCALE_Y = 1.0
SCALE_Z = 1.0
SERIAL_PORT = 'COM5'
LAYER_DEPTH = get_layer_depth() #IN INCHES
LAYER_CURE_TIME = get_layer_cure_time()
BUILD_PIXELS = (1280, 800)
BUILD_AREA = (8,6,5.5)#(9.0, 6.5, 8)
BUILD_PPI = (BUILD_PIXELS[0]/BUILD_AREA[0], BUILD_PIXELS[1]/BUILD_AREA[1])
BUILD_PEN = wx.Pen(wx.Colour(255,255,255))
BUILD_BACKGROUND = wx.Brush(wx.Colour(0,0,0))
BUILD_SUPPORT = wx.BrushFromBitmap(wx.Bitmap(PATH+'/appearance/brushes/AutoSupportMed.png'))
BUILD_FILL = wx.BrushFromBitmap(wx.Bitmap(PATH+'/appearance/brushes/honey_comb_thick.png'))#wx.Brush(wx.Colour(255,255,255), wx.CROSSDIAG_HATCH)
BUILD_FLAT_BRUSH = wx.Brush(wx.Colour(255,255,255))
x_factor = lambda: unit_factors[get_units()]*SCALE_X
y_factor = lambda: unit_factors[get_units()]*SCALE_Y
z_factor = lambda: unit_factors[get_units()]*SCALE_Z


#UI------------------------------------------------------------------------
def get_resolution():
    return (cfg.ReadInt('projw', defaultVal=1280), cfg.ReadInt('projh', defaultVal=800))
def set_resolution(w=1280, h=800):
    cfg.WriteInt('projw', w)
    cfg.WriteInt('projh', h)
if debug:
    set_resolution()

icon_view = False
app_x, app_y = 0,0
app_w, app_h = wx.GetDisplaySize()
projw, projh = get_resolution()
projx, projy = 0,0
touchw, touchh = 1024,600
if debug:
    projx = 800
    app_w, app_h = 800,600
default_touchscreen = True
if default_touchscreen:
    for i in range(0, wx.Display.GetCount()):
        xo,yo,w,h = wx.Display(i).GetGeometry()
        if h== touchh and w==touchw:
            #Is the default touchscreen
            app_x, app_y = xo, yo
            app_w, app_h = touchw, touchh
        elif w == projw and h == projh:
            projx, projy = xo, yo
toolbar_h = 40
toolbar_w = app_w

#Colors-initialize to None, allow globals to be set in function
defaultForeground = None
secondForeground = None
defaultBackground = None
secondBackground = None
defaultAccent = None
secondAccent = None
button_inside = None
button_outside = None
button_outline = None
button_text = None
toolbar_bottom = None
toolbar_top = None
#Schemes
schemes = {"BLUE":1, "GREEN":2, 'PINK':3, 'RED':4}
invert_color = False
def update_scheme():
    global defaultForeground, secondForeground, defaultBackground, secondBackground
    global defaultAccent, secondAccent, button_inside, button_outside, button_outline
    global button_text, button_text, toolbar_bottom, toolbar_top
    scheme = schemes[cfg.Read('color_scheme', "BLUE")]* (-1 if cfg.ReadBool('invert_color', True) else 1)
    if scheme>0:
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
    else:
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
update_scheme()
def set_scheme(theme_color, inverted):
    col = theme_color if schemes.has_key(theme_color) else "BLUE"
    cfg.Write('color_scheme', col)
    cfg.WriteBool('invert_color', inverted)
    update_scheme()

def get_scheme():
    return cfg.Read('color_scheme', "BLUE")

def set_resolution(w = projw, h = projh):
    cfg.WriteInt('projw',w)
    cfg.WriteInt('projh',h)

def set_property_color(key, color):
    cfg.WriteInt(key+'R', color.Red())
    cfg.WriteInt(key+'G', color.Green())
    cfg.WriteInt(key+'B', color.Blue())

def get_property_color(key, defaults=[0,0,0]):
    red=cfg.ReadInt(key+'R', defaults[0])
    green=cfg.ReadInt(key+'G', defaults[1])
    blue=cfg.ReadInt(key+'B', defaults[2])
    return wx.Colour(red, green, blue)

def set_layer_cure_time(time):
    cfg.WriteInt('layerCureTime',time)

def set_name(name):
    cfg.WriteInt('name', name) #To be changed to String in future

def set_layer_depth(depth):
    cfg.WriteFloat('layerDepth', depth)


temp_app.Destroy()
