from nested_visual import *
import application.settings as settings
import wx


def color_to_ones(color):
    return array(color.Get())/255.


class PartEnvironment(object):
    def __init__(self, window=None, build_area=(10,10,10), fore=wx.Colour(180,180,180), back=wx.Colour(0,0,0), h=400, w=400, accent=wx.Colour(255,100,100)):
        self.window = None
        self.fore = fore
        self.back = back
        self.accent = accent
        self.build_area = build_area
        self.parts = []
        self.h = h
        self.w = w

    def setup(self):
        background = color_to_ones(self.back)
        foreground = color_to_ones(self.fore)
        self.display = display(window=self.window, x=0, y=40, width=(self.w*2)/3,
                                height=self.h, up=(0,0,1), forward=vector(-1,-1,-1),
                                background=background, foreground=foreground)
        self.display.select()
        self.base_frame = frame() #May be useful for future positioning
        build_l, build_w, build_h = self.build_area
        build_z = .02
        self.x_axis = arrow(pos=(0,0,0), axis=(int(build_l*1.2),0,0), shaftwidth=.02, headwidth=.08,color=color_to_ones(self.accent), opacity=.5, frame=self.base_frame,fixedwidth = True)
        self.x_label = label(text='X', xoffset=1, yoffset= 1, space=0.2, pos=(int(build_l*1.2),0,0), box=False, frame=self.base_frame)
        self.y_axis = arrow(pos=(0,0,0), axis=(0,int(build_w*1.2),0), shaftwidth=.02, headwidth=.08, color=color_to_ones(self.accent), opacity=.5, frame=self.base_frame,fixedwidth = True)
        self.y_label = label(text='y', xoffset=1, yoffset= 0, space=0.2, pos=(0,int(build_w*1.2),0), box=False, frame=self.base_frame)
        self.z_axis = arrow(pos=(0,0,0), axis=(0,0,int(build_h*1.2)), shaftwidth=.02, headwidth=.08, color=color_to_ones(self.accent), opacity=.5, frame=self.base_frame,fixedwidth = True)
        self.z_label = label(text='Z', xoffset=1, yoffset= 1, space=0.2, pos=(0,0,int(build_h*1.2)), box=False, frame=self.base_frame)
        self.platform = box(pos=(build_l/2, build_w/2, -build_z/2),
                                length=build_l, width=build_z, height=build_w, opacity=0.2,
                                color=color_to_ones(settings.secondBackground), frame=self.base_frame)
    def add_part_to_display(self, part_file):
        self.display.select()
        part_frame = frame()
        from application.util.stl import PartFile
        model = PartFile(str(part_file), part_frame)
        model.generate_faces()
        self.parts.append(model)
        #model.faces.smooth()
        self.display.autocenter = True

    def stay_active(self):
        while settings.visual_showing:
            rate(100)