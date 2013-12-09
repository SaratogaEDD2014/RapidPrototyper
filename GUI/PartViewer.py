import wx
import AppSettings
from visual import *
from visual.filedialog import get_file

class STLViewer(wx.Panel):
    def __init__(self, parent, stl_file="", pos=wx.DefaultPosition, size=(800,400)):
        super(STLViewer, self).__init__(parent, pos=pos, size=size)
        try:
            if stl_file == "":
                self.file=AppSettings.PATH+"examples/bottle.stl"
            else:
                self.file=stl_file
        except IOError:
            dlg = wx.MessageDialog(self, 'Error: Not a valid filename.', 'Error Opening File', wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        l,w=self.GetSize()
        self._part_viewer = display(window=self, x=10, y=10, width=w, height=w, forward=-vector(0,1,2))
        newobject = stl_to_faces(fd)
        newobject.smooth()
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._part_viewer,1)
        sizer.Add(self._control_panel,1)
        self.SetSizer(sizer)


def generate_view(parent=None, filename=None):
    if filename==None:
        filename=get_file()
    return STLViewer(parent, filename)


#----------------------------------------------------------------------------------
def main():
    ProtoApp = wx.App()
    frm = wx.Frame(None, -1, 'Gear Display', size=(800,400))
    
    sizer=wx.BoxSizer(wx.HORIZONTAL)
    panel=generate_view(frm)
    sizer.Add(panel)
    panel.Show(True)
    
    frm.SetSizer(sizer)
    frm.Show(True)
    ProtoApp.MainLoop()


if __name__ == '__main__':
    main()
    


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