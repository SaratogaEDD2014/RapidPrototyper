import wx
import GUI.settings as settings
from myvisual import *
from visual.filedialog import get_file

class STLViewer(wx.Panel):
    def __init__(self, parent, stl_file="", pos=(0,80), size=(settings.app_w,settings.app_h)):
        super(STLViewer, self).__init__(parent, pos=pos, size=size)
        self.file = stl_file
        self.title = wx.StaticText(self, label="Printer View Screen", pos=(settings.app_w*3/4, 30))
        self.title.SetForegroundColour(wx.Colour(255,255,255))
        self.printb = wx.Button(self, label="Print", pos=(settings.app_w*3/4, 50))
        self.cancelb = wx.Button(self, label="Cancel", pos=(settings.app_w*3/4 -90, 50))
        self.viewer = None
        self.Show(False)

    def Show(self, visible):
        super(STLViewer, self).Show(visible)
        if visible:
            if settings.display_part:
                if self.viewer == None:
                    self.viewer = display(window=None, x=0, y=settings.toolbar_h+30, width=(settings.app_w*2)/3, height=settings.app_h, forward=-vector(0,1,2), background=(1,1,1), foreground=(0.086,0.702,0.870))
                settings.display_part=False
                scene.width = scene.height = 480
                scene.autocenter = True
                self.model = stl_to_faces(self.file)
                if self.file != "":
                    self.model = stl_to_faces(self.file)
                    self.model.smooth()
                while not settings.display_part:
                    rate(100)
        else:
            settings.display_part=True
            #self.viewer.window._OnExitApp(wx.CommandEvent())


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