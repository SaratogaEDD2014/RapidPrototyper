# Purpose:
#
# Author:      davism14
#
# Created:     24/04/2014
# Copyright:   (c) davism14 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
import wx
import re
import string
import application.settings as settings
from application.bubble_menu import DynamicButtonRect
from application.util.app_util import dim_color

class QwertyDialog(wx.Dialog):
    def __init__(self, parent, title, size=(settings.app_w*3/5,settings.app_h*3/6)):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(QwertyDialog, self).__init__(parent, -1, title, style=style, pos=(settings.app_w/4, settings.app_h/4), size=size)
        self.formula = False
        self.shift = False
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.display = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT)
        sizer.Add(self.display, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 4)
        ids={"a":61, "b":62, "c":63, "d":54, "e":65, "f":66, "g":67, "h":68, "i":69, "j":70, "k":71, "l":72, "m":73, "n":74, "o":75, "p":76, "q":77, "r":78, "s":79, "t":80, 'u':81, "v":82, "w":83, "x":84, "y":85, "z":86, "Delete":87, "Clear":88, "Space":89, "Shift":90, "`":91, ".":92, "'":93, "Done":94}
        #ids = {"a":61, "b":62,}
        #inside_color = dim_color(settings.defaultAccent, -30)
        #outside_color = dim_color(settings.defaultAccent, 20)
        self.upper_gs = wx.GridSizer(1, 0)# 3, 3)
        self.middle_gs= wx.GridSizer(1,0)
        self.lower_gs= wx.GridSizer(1,0)
        self.bottom_gs= wx.GridSizer(1,0)

        self.upper_butt_list = [(wx.Button(self, id=ids['q'], label='Q'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['w'], label='W'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['e'], label='E'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['r'], label='R'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['t'], label='T'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['y'], label='Y'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['u'], label='U'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['i'], label='I'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['o'], label='O'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['p'], label='P'), 0, wx.EXPAND),]

        self.upper_gs.AddMany(self.upper_butt_list)

        self.middle_butt_list=[(wx.Button(self, id=ids['a'], label='A'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['s'], label='S'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['d'], label='D'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['f'], label='F'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['g'], label='G'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['h'], label='H'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['j'], label='J'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['k'], label='K'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['l'], label='L'), 0, wx.EXPAND),]
                        #(wx.Button(self, id=ids['Clear'], label='Clear'), 0, wx.EXPAND),]

        self.middle_gs.AddSpacer(3)
        self.middle_gs.AddMany(self.middle_butt_list)
        self.middle_gs.AddSpacer(3)

        self.lower_butt_list=[(wx.Button(self, id=ids['Shift'], label='Shift'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['z'], label='Z'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['x'], label='X'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['c'], label='C'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['v'], label='V'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['b'], label='B'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['n'], label='N'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['m'], label='M'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['Delete'], label='Delete'), 0, wx.EXPAND),]

        self.lower_gs.AddMany(self.lower_butt_list)

        self.bottom_butt_list=[(wx.Button(self, id=ids['Clear'], label='Clear'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['Space'], label='Space'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['Done'], label='Done'), 0, wx.EXPAND)]

        self.bottom_gs.AddMany(self.bottom_butt_list)

        sizer.Add(self.upper_gs, 1, wx.EXPAND)
        sizer.Add(self.middle_gs, 1, wx.EXPAND)
        sizer.Add(self.lower_gs, 1, wx.EXPAND)
        sizer.Add(self.bottom_gs, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.OnClear, id=ids['Clear'])
        self.Bind(wx.EVT_BUTTON, self.OnBackspace, id=ids['Delete'])
        self.Bind(wx.EVT_BUTTON, self.OnA, id=ids['a'])
        self.Bind(wx.EVT_BUTTON, self.OnB, id=ids['b'])
        self.Bind(wx.EVT_BUTTON, self.OnC, id=ids['c'])
        self.Bind(wx.EVT_BUTTON, self.OnD, id=ids['d'])
        self.Bind(wx.EVT_BUTTON, self.OnE, id=ids['e'])
        self.Bind(wx.EVT_BUTTON, self.OnF, id=ids['f'])
        self.Bind(wx.EVT_BUTTON, self.OnG, id=ids['g'])
        self.Bind(wx.EVT_BUTTON, self.OnH, id=ids['h'])
        self.Bind(wx.EVT_BUTTON, self.OnI, id=ids['i'])
        self.Bind(wx.EVT_BUTTON, self.OnJ, id=ids['j'])
        self.Bind(wx.EVT_BUTTON, self.OnK, id=ids['k'])
        self.Bind(wx.EVT_BUTTON, self.OnL, id=ids['l'])
        self.Bind(wx.EVT_BUTTON, self.OnM, id=ids['m'])
        self.Bind(wx.EVT_BUTTON, self.OnN, id=ids['n'])
        self.Bind(wx.EVT_BUTTON, self.OnO, id=ids['o'])
        self.Bind(wx.EVT_BUTTON, self.OnP, id=ids['p'])
        self.Bind(wx.EVT_BUTTON, self.OnQ, id=ids['q'])
        self.Bind(wx.EVT_BUTTON, self.OnR, id=ids['r'])
        self.Bind(wx.EVT_BUTTON, self.OnS, id=ids['s'])
        self.Bind(wx.EVT_BUTTON, self.OnT, id=ids['t'])
        self.Bind(wx.EVT_BUTTON, self.OnU, id=ids['u'])
        self.Bind(wx.EVT_BUTTON, self.OnV, id=ids['v'])
        self.Bind(wx.EVT_BUTTON, self.OnW, id=ids['w'])
        self.Bind(wx.EVT_BUTTON, self.OnX, id=ids['x'])
        self.Bind(wx.EVT_BUTTON, self.OnY, id=ids['y'])
        self.Bind(wx.EVT_BUTTON, self.OnZ, id=ids['z'])
        self.Bind(wx.EVT_BUTTON, self.OnSpace, id=ids['Space'])
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=ids['Done'])
        self.Bind(wx.EVT_BUTTON, self.OnShift, id=ids['Shift'])

    def OnClear(self, event):
            self.display.Clear()

    def OnBackspace(self, event):
        formula = self.display.GetValue()
        self.display.Clear()
        self.display.SetValue(formula[:-1])

    def OnClose(self, event):
        self.OnEqual(event)
        self.Close()

    def OnA(self, event):
        if self.shift:
            self.display.AppendText('A')
            self.shift=False
            return
        self.display.AppendText('a')

    def OnB(self, event):
        if self.shift:
            self.display.AppendText('B')
            self.shift=False
            return
        self.display.AppendText('b')

    def OnC(self, event):
        if self.shift:
            self.display.AppendText('C')
            self.shift=False
            return
        self.display.AppendText('c')

    def OnD(self, event):
        if self.shift:
            self.display.AppendText('D')
            self.shift=False
            return
        self.display.AppendText('d')

    def OnE(self, event):
        if self.shift:
            self.display.AppendText('E')
            self.shift=False
            return
        self.display.AppendText('e')

    def OnF(self, event):
        if self.shift:
            self.display.AppendText('F')
            self.shift=False
            return
        self.display.AppendText('f')

    def OnG(self, event):
        if self.shift:
            self.display.AppendText('G')
            self.shift=False
            return
        self.display.AppendText('g')

    def OnH(self, event):
        if self.shift:
            self.display.AppendText('H')
            self.shift=False
            return
        self.display.AppendText('h')

    def OnI(self, event):
        if self.shift:
            self.display.AppendText('I')
            self.shift=False
            return
        self.display.AppendText('i')

    def OnJ(self, event):
        if self.shift:
            self.display.AppendText('J')
            self.shift=False
            return
        self.display.AppendText('j')

    def OnK(self, event):
        if self.shift:
            self.display.AppendText('K')
            self.shift=False
            return
        self.display.AppendText('k')

    def OnL(self, event):
        if self.shift:
            self.display.AppendText('L')
            self.shift=False
            return
        self.display.AppendText('l')

    def OnM(self, event):
        if self.shift:
            self.display.AppendText('M')
            self.shift=False
            return
        self.display.AppendText('m')

    def OnN(self, event):
        if self.shift:
            self.display.AppendText('N')
            self.shift=False
            return
        self.display.AppendText('n')

    def OnO(self, event):
        if self.shift:
            self.display.AppendText('O')
            self.shift=False
            return
        self.display.AppendText('o')

    def OnP(self, event):
        if self.shift:
            self.display.AppendText('P')
            self.shift=False
            return
        self.display.AppendText('p')

    def OnQ(self, event):
        if self.shift:
            self.display.AppendText('Q')
            self.shift=False
            return
        self.display.AppendText('q')

    def OnR(self, event):
        if self.shift:
            self.display.AppendText('R')
            self.shift=False
            return
        self.display.AppendText('r')

    def OnS(self, event):
        if self.shift:
            self.display.AppendText('S')
            self.shift=False
            return
        self.display.AppendText('s')

    def OnT(self, event):
        if self.shift:
            self.display.AppendText('T')
            self.shift=False
            return
        self.display.AppendText('t')

    def OnU(self, event):
        if self.shift:
            self.display.AppendText('U')
            self.shift=False
            return
        self.display.AppendText('u')

    def OnV(self, event):
        if self.shift:
            self.display.AppendText('V')
            self.shift=False
            return
        self.display.AppendText('v')

    def OnW(self, event):
        if self.shift:
            self.display.AppendText('W')
            self.shift=False
            return
        self.display.AppendText('w')

    def OnX(self, event):
        if self.shift:
            self.display.AppendText('X')
            self.shift=False
            return
        self.display.AppendText('x')

    def OnY(self, event):
        if self.shift:
            self.display.AppendText('Y')
            self.shift=False
            return
        self.display.AppendText('y')

    def OnZ(self, event):
        if self.shift:
            self.display.AppendText('Z')
            self.shift=False
            return
        self.display.AppendText('z')

    def OnSpace(self, event):
        if self.formula:
            return
        self.display.AppendText(' ')

    def OnShift(self, event):
        self.shift=True

    def OnEqual(self, event):
        if self.formula:
            return
        return self.display.GetValue()

    def _parse_to_double(self, formula):
        _last_num_index=-0
        i=0
        while i<len(formula)-2:
            if formula[i] in string.digits and formula[i+1] not in string.digits:
                if '.' not in formula[_last_num_index:i+2]:
                    formula=formula[:i+1]+'.0'+formula[i+1:]
                _last_num_index=i
            i+=1
        #if '.' not in formula[_last_num_index:]:
        #    formula+='.0'
        #formula+='*1.0'#Allows user to enter a plain number
        return formula

    def SetValue(self, value):
        self.display.SetValue(value)
    def GetValue(self):
        return self.display.GetValue()

def text_value(parent=None, title='Edit Dimension:', default = ""):
    dialog = QwertyDialog(parent, title)
    dialog.SetValue(default)
    dialog.CenterOnScreen()
    dialog.ShowModal()
    val = dialog.GetValue()
    dialog.Destroy()
    return val


if __name__ == '__main__':
    app = wx.App()
    print text_value()
    app.MainLoop()
