import application.settings as settings
import wx
from application.bubble_menu import DynamicButtonRect
from application.util.app_util import color_to_ones
from application.util.stl_to_bitmap import process_file
from nested_visual import *
from numpy import array
from visual.filedialog import get_file

class STLViewer(wx.Panel):
    def __init__(self, parent, stl_file="", pos=(0,80), size=(settings.app_w,settings.app_h)):
        super(STLViewer, self).__init__(parent, pos=pos, size=size)
        self.file = stl_file
        self.title = wx.StaticText(self, label="Printer View Screen", pos=(settings.app_w*3/4, 30))
        self.title.SetForegroundColour(wx.Colour(255,255,255))
        self.printb = DynamicButtonRect(self, "Print")
        self.printb.SetSize((settings.app_w/4, settings.app_h/7))
        self.printb.SetPosition((int(settings.app_w*.7), 10))
        self.cancelb = DynamicButtonRect(self, "Cancel")
        self.cancelb.SetSize((settings.app_w/4, settings.app_h/7))
        self.cancelb.SetPosition((int(settings.app_w*.7), settings.app_h/5))
        self.Bind(wx.EVT_BUTTON, self.on_print, self.printb)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancelb)
        self.viewer = None
        self.Show(False)

    def Show(self, visible):
        super(STLViewer, self).Show(visible)
        if visible:
            if settings.display_part:
                if self.viewer == None:
                    w = settings.main_v_window
                    background = color_to_ones(settings.defaultBackground)
                    foreground = color_to_ones(settings.defaultForeground)
                    self.display = display(window=w, x=0, y=settings.toolbar_h, width=(settings.app_w*2)/3, height=settings.app_h, up=(0,0,1), forward=vector(-1,-1,-1), background=background, foreground=foreground)
                    self.base_frame = frame()
                    self.part_frame = frame()
                    build_l, build_w, build_h = settings.BUILD_AREA
                    build_z = .02
                    self.x_axis = arrow(pos=(0,0,0), axis=(int(build_l*1.2),0,0), shaftwidth=.02, headwidth=.08,color=color_to_ones(settings.defaultAccent), opacity=.5, frame=self.base_frame,fixedwidth = True)
                    self.x_label = label(text='X', xoffset=1, yoffset= 1, space=0.2, pos=(int(build_l*1.2),0,0), box=False, frame=self.base_frame)
                    self.y_axis = arrow(pos=(0,0,0), axis=(0,int(build_w*1.2),0), shaftwidth=.02, headwidth=.08, color=color_to_ones(settings.defaultAccent), opacity=.5, frame=self.base_frame,fixedwidth = True)
                    self.y_label = label(text='y', xoffset=1, yoffset= 0, space=0.2, pos=(0,int(build_w*1.2),0), box=False, frame=self.base_frame)
                    self.z_axis = arrow(pos=(0,0,0), axis=(0,0,int(build_h*1.2)), shaftwidth=.02, headwidth=.08, color=color_to_ones(settings.defaultAccent), opacity=.5, frame=self.base_frame,fixedwidth = True)
                    self.z_label = label(text='Z', xoffset=1, yoffset= 1, space=0.2, pos=(0,0,int(build_h*1.2)), box=False, frame=self.base_frame)
                    self.platform = box(pos=(build_l/2, build_w/2, -build_z/2),
                        length=build_l, width=build_z, height=build_w, opacity=0.2,
                        color=color_to_ones(settings.secondBackground), frame=self.base_frame)
                    w.panel.SetSize(((settings.app_w*2)/3,settings.app_h))
                    w.win.SendSizeEvent()
                settings.display_part = False
                #self.display.autocenter =True
                if self.file != "":
                    self.model = stl_to_faces(file(self.file), self.part_frame)
                    self.model.smooth()
##                    self.label = label(pos=self.model.pos, text=self.file,
##                        xoffset=1, line=0, yoffset=100, space=100,)
                    n = self.file
                    n = n.replace('\\', '/')
                    n = n[n.rfind('/')+1:]
                    self.title = label(text=n, xoffset=0, z=build_h*.75, line=0, pos=(0,0), opacity=0.5)
                    while not settings.display_part:
                        rate(100)

        else:
            settings.display_part=True

    def on_print(self, event):
        self.dialog = wx.ProgressDialog("Processing "+self.file[self.file.rfind('/'):]+":", "Process is 10% complete.", 100, self)
        process_file(self.file, dialog = self.dialog)
        self.dialog.Destroy()
    def on_cancel(self, event):
        settings.main_v_window.panel.SetSize((1,1))  #Makes display invisible, invoking the private _destroy removes whole window, not just display
        settings.goto_prev_page()


def stl_to_faces(fileinfo, frm=None): # specify file
    # Accept a file name or a file descriptor; make sure mode is 'rb' (read binary)
    if isinstance(fileinfo, str):
        fd = open(fileinfo, mode='rb')
    elif isinstance(fileinfo, file):
        if fileinfo.mode != 'rb':
            filename = fileinfo.name
            fileinfo.close()
            fd = open(filename, mode='rb')
        else:
            fd = fileinfo
    else:
        raise TypeError, "Specify a file"
    text = fd.read()
    if chr(0) in text: # if binary file
        text = text[84:]
        L = len(text)
        N = 2*(L//25) # 25/2 floats per point: 4*3 float32's + 1 uint16
        triNor = zeros((N,3), dtype=float32)
        triPos = zeros((N,3), dtype=float32)
        n = i = 0
        while n < L:
            if n % 200000 == 0:
                print ("%d" % (100*n/L))+"%",
            triNor[i] = fromstring(text[n:n+12], float32)
            triPos[i] = fromstring(text[n+12:n+24], float32)
            triPos[i+1] = fromstring(text[n+24:n+36], float32)
            triPos[i+2] = fromstring(text[n+36:n+48], float32)
            colors = fromstring(text[n+48:n+50], uint16)
            if colors != 0:
                print '%x' % colors
            if triNor[i].any():
                triNor[i] = triNor[i+1] = triNor[i+2] = norm(vector(triNor[i]))
            else:
                triNor[i] = triNor[i+1] = triNor[i+2] = \
                    norm(cross(triPos[i+1]-triPos[i],triPos[i+2]-triPos[i]))
            n += 50
            i += 3
    else:
        fd.seek(0)
        fList = fd.readlines()
        triPos = []
        triNor = []

        # Decompose list into vertex positions and normals
        for line in fList:
            FileLine = line.split( )
            if FileLine[0] == 'facet':
                for n in range(3):
                    triNor.append( [ float(FileLine[2]), float(FileLine[3]), float(FileLine[4]) ]  )
            elif FileLine[0] == 'vertex':
                triPos.append( [ float(FileLine[1]), float(FileLine[2]), float(FileLine[3]) ]  )

        triPos = array(triPos)
        triNor = array(triNor)

    # Compose faces in default frame
    if frm == None:
        f = frame()
    else:
        f = frm
    return faces(frame=f, pos=triPos, normal=triNor)





"""
    #From Visual Example:---------------------------------------------------------------------------------
    def stl_to_faces(fileinfo): # specify file
    # Accept a file name or a file descriptor; make sure mode is 'rb' (read binary)
    if isinstance(fileinfo, str):
    fd = open(fileinfo, mode='rb')
    elif isinstance(fileinfo, file):
    if fileinfo.mode != 'rb':
    filename = fileinfo.name
    fileinfo.close()
    fd = open(filename, mode='rb')
    else:
    fd = fileinfo
    else:
    raise TypeError, "Specify a file"
    text = fd.read()
    if chr(0) in text: # if binary file
    text = text[84:]
    L = len(text)
    N = 2*(L//25) # 25/2 floats per point: 4*3 float32's + 1 uint16
    triNor = zeros((N,3), dtype=float32)
    triPos = zeros((N,3), dtype=float32)
    n = i = 0
    while n < L:
    if n % 200000 == 0:
    print ("%d" % (100*n/L))+"%",
    triNor[i] = fromstring(text[n:n+12], float32)
    triPos[i] = fromstring(text[n+12:n+24], float32)
    triPos[i+1] = fromstring(text[n+24:n+36], float32)
    triPos[i+2] = fromstring(text[n+36:n+48], float32)
    colors = fromstring(text[n+48:n+50], uint16)
    if colors != 0:
    print '%x' % colors
    if triNor[i].any():
    triNor[i] = triNor[i+1] = triNor[i+2] = norm(vector(triNor[i]))
    else:
    triNor[i] = triNor[i+1] = triNor[i+2] = \
    norm(cross(triPos[i+1]-triPos[i],triPos[i+2]-triPos[i]))
    n += 50
    i += 3
    else:
    fd.seek(0)
    fList = fd.readlines()
    triPos = []
    triNor = []

    # Decompose list into vertex positions and normals
    for line in fList:
    FileLine = line.split( )
    if FileLine[0] == 'facet':
    for n in range(3):
    triNor.append( [ float(FileLine[2]), float(FileLine[3]), float(FileLine[4]) ]  )
    elif FileLine[0] == 'vertex':
    triPos.append( [ float(FileLine[1]), float(FileLine[2]), float(FileLine[3]) ]  )

    triPos = array(triPos)
    triNor = array(triNor)

    # Compose faces in default frame
    f = frame()
    return faces(frame=f, pos=triPos, normal=triNor)

    if __name__ == '__main__':
    #print "Choose an stl file to display. Rotate!"
    # Open .stl file
    while True:
    fd = get_file()
    if not fd: continue

    scene.width = scene.height = 800
    scene.autocenter = True
    newobject = stl_to_faces(fd)
    newobject.smooth() # average normals at a vertex

    # Examples of modifying the returned object:
    ##        newobject.frame.pos = (-1,-1,-0.5)
    ##        newobject.frame.axis = (0,1,0)
    newobject.color = color.orange
    newobject.material = materials.wood
    break"""
