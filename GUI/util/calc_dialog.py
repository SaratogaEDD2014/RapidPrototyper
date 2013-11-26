import wx

class CalcDialog(wx.Dialog):
    def __init__(self, parent, title, caption):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(CalcDialog, self).__init__(parent, -1, title, style=style)
        self.formula = False
        wx.EVT_MENU(self, 22, self.OnClose)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.display = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT)
        sizer.Add(self.display, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 4)

        ids={"1":51, "2":52, "3":53, "4":54, "5":55, "6":56, "7":57, "8":58, "9":59, "10":60, "Clr":61, "Del":62, "=":63, "Done":wx.OK, "/":64, "*":65, "-":66, ".":67, "+":68}

        gs = wx.GridSizer(5, 4, 3, 3)
        gs.AddMany([(wx.Button(self, ids['Clr'], 'Clr'), 0, wx.EXPAND),
                        (wx.Button(self, ids['Del'], 'Del'), 0, wx.EXPAND),
                        (wx.Button(self, ids['='], '='), 0, wx.EXPAND),
                        (wx.Button(self, ids['Done'], 'Done'), 0, wx.EXPAND),
                        (wx.Button(self, ids['7'], '7'), 0, wx.EXPAND),
                        (wx.Button(self, ids['8'], '8'), 0, wx.EXPAND),
                        (wx.Button(self, ids['9'], '9'), 0, wx.EXPAND),
                        (wx.Button(self, ids['/'], '/'), 0, wx.EXPAND),
                        (wx.Button(self, ids['4'], '4'), 0, wx.EXPAND),
                        (wx.Button(self, ids['5'], '5'), 0, wx.EXPAND),
                        (wx.Button(self, ids['6'], '6'), 0, wx.EXPAND),
                        (wx.Button(self, ids['*'], '*'), 0, wx.EXPAND),
                        (wx.Button(self, ids['1'], '1'), 0, wx.EXPAND),
                        (wx.Button(self, ids['2'], '2'), 0, wx.EXPAND),
                        (wx.Button(self, ids['3'], '3'), 0, wx.EXPAND),
                        (wx.Button(self, ids['-'], '-'), 0, wx.EXPAND),
                        (wx.Button(self, ids['0'], '0'), 0, wx.EXPAND),
                        (wx.Button(self, ids['.'], '.'), 0, wx.EXPAND),
                        (wx.StaticText(self, -1, ''), 0, wx.EXPAND),
                        (wx.Button(self, ids['+'], '+'), 0, wx.EXPAND) ])

        sizer.Add(gs, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.OnClear, id=20)
        self.Bind(wx.EVT_BUTTON, self.OnBackspace, id=21)
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=22)
        self.Bind(wx.EVT_BUTTON, self.OnSeven, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnEight, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnNine, id=3)
        self.Bind(wx.EVT_BUTTON, self.OnDivide, id=4)
        self.Bind(wx.EVT_BUTTON, self.OnFour, id=5)
        self.Bind(wx.EVT_BUTTON, self.OnFive, id=6)
        self.Bind(wx.EVT_BUTTON, self.OnSix, id=7)
        self.Bind(wx.EVT_BUTTON, self.OnMultiply, id=8)
        self.Bind(wx.EVT_BUTTON, self.OnOne, id=9)
        self.Bind(wx.EVT_BUTTON, self.OnTwo, id=10)
        self.Bind(wx.EVT_BUTTON, self.OnThree, id=11)
        self.Bind(wx.EVT_BUTTON, self.OnMinus, id=12)
        self.Bind(wx.EVT_BUTTON, self.OnZero, id=13)
        self.Bind(wx.EVT_BUTTON, self.OnDot, id=14)
        self.Bind(wx.EVT_BUTTON, self.OnEqual, id=15)
        self.Bind(wx.EVT_BUTTON, self.OnPlus, id=16)

    def OnClear(self, event):
            self.display.Clear()

    def OnBackspace(self, event):
        formula = self.display.GetValue()
        self.display.Clear()
        self.display.SetValue(formula[:-1])

    def OnClose(self, event):
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
        formula = self.display.GetValue()
        self.formula = False
        try:
            self.display.Clear()
            output = eval(formula)
            self.display.AppendText(str(output))
        except StandardError:
            self.display.AppendText("Error")

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

    def SetValue(self, value):
        self.display.SetValue(value)
    def GetValue(self):
        return self.display.GetValue()

if __name__ == '__main__':
    app = wx.App()
    dialog = CalcDialog(None, 'Title', 'Caption')
    dialog.Center()
    if dialog.ShowModal() == wx.OK:
        print dialog.GetValue()
    dialog.Destroy()
    app.MainLoop()