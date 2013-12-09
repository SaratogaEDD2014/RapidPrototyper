prev_page=[]
currentPage=None
import wx

cfg= wx.Config('config')

def add_prev_page(page):
    prev_page.append(page)
    
def goto_prev_page():
    global currentPage
    if len(prev_page)>1:
        temp=prev_page[len(prev_page)-1]
        prev_page.remove(temp)
        currentPage=prev_page[len(prev_page)-1]
        print len(prev_page)
        return temp
    else:
        currentPage=None
        return None
        
def get_prev_page():
    if len(prev_page)>0:
        return prev_page[len(prev_page)-1]
    return None
    
def set_current_page(page):
    global currentPage
    currentPage=page
    add_prev_page(currentPage)
    
def get_current_page():
    return currentPage
    
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
