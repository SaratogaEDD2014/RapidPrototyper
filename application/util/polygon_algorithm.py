from numpy import *
from wx import *

tri1 = [(0,0),(1,0)]
tri2 = [(1,0),(0,1)]
tri3 = [(0,1),(0,0)]

rect1 = [(1,1),(1,2)]
rect2 = [(3,1),(3,2)]
rect3 = [(1,1),(3,1)]
rect4 = [(3,2),(1,2)]

app = App()
frm = Frame(None, size=(400,400))
frm.Show(True)

def process_couplet(couplet, runs):
    attached = False
    for run in runs:
        i=0
        while not attached and i<len(run):
            if run[i][1] == couplet[0]:
                if len(run) <= i+1:
                    #Is the next point in the run
                    run.append(couplet)
                    attached = True
                else:
                    #Two possibilities:
                    #1. Same segment again, happens a lot, do not repeat segment,
                    #    leave opportunity for shared border polygons by not
                    #    setting as attached
                    #2. Different segmenet comes after, signifying definite
                    #    side-sharing, so again leave attached False
                    #Both cases show opportunity for another poly, so leave unnattached
                    #so that a new run may be generated
                    pass
            i+=1
    return attached

def process_polygons(new_poly, polys):
        for i in range(len(polys)):
            if new_poly[0] == polys[i][len(polys[i])-1]:
                #first element in new polygon is last in another
                if len(new_poly)>1:
                    polys[i] += new_poly[1:]#combine elements of polygons
                    return True
            elif new_poly[len(new_poly)-1] == polys[i][0]:
                #last element in new polygon equals first in another
                if len(polys[i])>1:
                    polys[i] = new_poly + polys[i][1:]#combine elements, new first
                    return True
        return False

def draw(event):
    couplets = [tri1, tri2, tri3]
    couplets += [rect1, rect3, rect2, rect4]
    runs = [[]]
    runs[0].append(couplets[0])  #Initialize the first polygon with the first line

    if len(couplets) > 0:
        for couplet in couplets[1:]:
            success = process_couplet(couplet, runs)
            if not success:
                runs.append([couplet]) #Create new
        print runs
        polys = []
        for run in runs:
            new_poly = []
            new_poly.append(run[0][0])
            for couplet in run:
                new_poly.append(couplet[1])
            print 'new poly', new_poly
            if len(polys) > 0:
                success = process_polygons(new_poly, polys)
                if not success:
                    invert = new_poly[:]#copy, don't mess up original
                    invert.reverse() #try re-ordering, but maintain couplets
                    success = process_polygons(invert, polys)
                    if not success:
                        polys.append(new_poly)

            else:
                polys.append(new_poly)


        dc = wx.ClientDC(frm)
        print 'polygons',polys
        for poly in polys:
            dc.DrawPolygon(array(poly)*(100,100))

        background = []
        foreground = []
        for tester in polys:
            if len(background)>0:
                in_front = False
                for other in background:
                    if tester != other:
                        is_in_left  = tester.min(axis=0) > other.min(axis=0)
                        is_in_right  = tester.max(axis=0) > other.max(axis=0)
                        is_inside = is_in_left[0] and is_in_left[1] and is_in_right[0] and is_in_right[1]
                        if is_inside:
                            in_front = True
            else:
                background.append(tester)

        for poly in foreground:
            dc.DrawPolygon(array(poly)*(100,100))
        for poly in background:
            dc.DrawPolygon(array(poly)*(100,100))

frm.draw = draw
frm.Bind(wx.EVT_PAINT, frm.draw)
app.MainLoop()

