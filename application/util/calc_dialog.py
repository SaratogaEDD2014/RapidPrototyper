import wx
import re
import string
import application.settings as settings
from application.bubble_menu import DynamicButtonRect
from application.util.app_util import dim_color

class CalcDialog(wx.Dialog):
    def __init__(self, parent, title):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(CalcDialog, self).__init__(parent, -1, title, style=style, pos=(settings.app_w/4, settings.app_h/4), size=(settings.app_w/2,settings.app_h/2))
        self.formula = False
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.display = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT)
        sizer.Add(self.display, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 4)

        ids={"1":51, "2":52, "3":53, "4":54, "5":55, "6":56, "7":57, "8":58, "9":59, "0":60, "Clr":61, "Del":62, "=":63, "Done":wx.OK, "/":64, "*":65, "-":66, ".":67, "+":68, '(':69, ')':70}

        #inside_color = dim_color(settings.defaultAccent, -30)
        #outside_color = dim_color(settings.defaultAccent, 20)
        gs = wx.GridSizer(5, 4, 4, 4)
        gs.AddMany([(wx.Button(self, id=ids['Clr'], label='Clr'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['Del'], label='Del'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['('], label='('), 0, wx.EXPAND),
                        (wx.Button(self, id=ids[')'], label=')'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['7'], label='7'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['8'], label='8'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['9'], label='9'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['/'], label='/'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['4'], label='4'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['5'], label='5'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['6'], label='6'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['*'], label='*'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['1'], label='1'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['2'], label='2'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['3'], label='3'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['-'], label='-'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['0'], label='0'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['.'], label='.'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['Done'], label='Done'), 0, wx.EXPAND),
                        (wx.Button(self, id=ids['+'], label='+'), 0, wx.EXPAND) ])

        sizer.Add(gs, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.OnClear, id=ids['Clr'])
        self.Bind(wx.EVT_BUTTON, self.OnBackspace, id=ids['Del'])
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=ids['Done'])
        self.Bind(wx.EVT_BUTTON, self.OnSeven, id=ids['7'])
        self.Bind(wx.EVT_BUTTON, self.OnEight, id=ids['8'])
        self.Bind(wx.EVT_BUTTON, self.OnNine, id=ids['9'])
        self.Bind(wx.EVT_BUTTON, self.OnDivide, id=ids['/'])
        self.Bind(wx.EVT_BUTTON, self.OnFour, id=ids['4'])
        self.Bind(wx.EVT_BUTTON, self.OnFive, id=ids['5'])
        self.Bind(wx.EVT_BUTTON, self.OnSix, id=ids['6'])
        self.Bind(wx.EVT_BUTTON, self.OnMultiply, id=ids['*'])
        self.Bind(wx.EVT_BUTTON, self.OnOne, id=ids['1'])
        self.Bind(wx.EVT_BUTTON, self.OnTwo, id=ids['2'])
        self.Bind(wx.EVT_BUTTON, self.OnThree, id=ids['3'])
        self.Bind(wx.EVT_BUTTON, self.OnMinus, id=ids['-'])
        self.Bind(wx.EVT_BUTTON, self.OnZero, id=ids['0'])
        self.Bind(wx.EVT_BUTTON, self.OnDot, id=ids['.'])
        self.Bind(wx.EVT_BUTTON, self.OnPlus, id=ids['+'])
        self.Bind(wx.EVT_BUTTON, self.OnLeftP, id=ids['('])
        self.Bind(wx.EVT_BUTTON, self.OnRightP, id=ids[')'])

    def OnClear(self, event):
            self.display.Clear()

    def OnBackspace(self, event):
        formula = self.display.GetValue()
        self.display.Clear()
        self.display.SetValue(formula[:-1])

    def OnClose(self, event):
        self.OnEqual(event)
        self.Close()

    def OnDivide(self, event):
        if self.formula:
            return
        self.display.AppendText('/')

    def OnMultiply(self, event):
        if self.formula:
            return
        self.display.AppendText('*')

    def OnMinus(self, event):
        if self.formula:
            return
        self.display.AppendText('-')

    def OnPlus(self, event):
        if self.formula:
            return
        self.display.AppendText('+')

    def OnDot(self, event):
        if self.formula:
            return
        self.display.AppendText('.')

    def OnEqual(self, event):
        if self.formula:
            return
        expression = self.display.GetValue()
        expression = self._parse_to_double(expression)

        self.formula = False
        try:
            self.display.Clear()
            output = eval(expression)
            self.SetValue(str(output))
        except StandardError:
            self.SetValue('0')

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

    def OnZero(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('0')

    def OnOne(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('1')

    def OnTwo(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('2')

    def OnThree(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('3')

    def OnFour(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('4')

    def OnFive(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('5')

    def OnSix(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('6')

    def OnSeven(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('7')

    def OnEight(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('8')

    def OnNine(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('9')

    def OnRightP(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText(')')
    def OnLeftP(self, event):
        if self.formula:
            self.display.Clear()
            self.formula = False
        self.display.AppendText('(')

    def SetValue(self, value):
        self.display.SetValue(value)
    def GetValue(self):
        return self.display.GetValue()

def calc_value(parent=None, title='Edit Dimension:'):
    dialog = CalcDialog(parent, title)
    dialog.Center()
    dialog.ShowModal()
    val = dialog.GetValue()
    dialog.Destroy()
    return val


if __name__ == '__main__':
    app = wx.App()
    print calc_value()
    app.MainLoop()
