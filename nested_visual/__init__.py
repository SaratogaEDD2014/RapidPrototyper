from __future__ import print_function
# Variables starting with "_" are not accessible to the importing program

# TODO: keyboard; display.keys is an "atomic queue" of strings
# TODO: improve rate function
# TODO: site settings?
# TODO: window and canvas objects
# TODO: fullscreen
# TODO: I disabled distance attentuation on points.cpp -- is that a problem?

# I get this mouse error: attempt to release mouse, but this window hasn't captured it

# d = display(visible=False): the display still appears. Likewise, d.visible = False fails.
# electric_motor slower in 2.7 than 3.2; might be rate, which needs work?
# glinfo does nothing: "Renderer inactive"

# Changes to API:
# To use graph, controls, etc., must also import visual or vis

# http://d0t.dbclan.de/snippets/gltext.html: wx text-to-OpenGL-texture

##https://groups.google.com/forum/?fromgroups=&hl=en#!topic/wxpython-users/lbzhzaBNkxQ
##On Linux one has to pass the depth buffer attribute like this:
##
##  attribs=[WX_GL_DEPTH_SIZE,16,0];  # Needed by wxGTK; the defaults are not enough
##  glcanvas.GLCanvas.__init__(self, parent, -1,attribList=attribs)
##
##I struggled for many days and tried most of the samples google could find.
##The fundamental problem seems to be that very few have been tested under X.

# https://github.com/melanke/Watch.JS makes it easy to watch for changes in an object.

from visual.visual_all import * # this statement not included in vis/__init__.py
#from visual_common.create_display import *
from nested_create_display import *

scene = display()
