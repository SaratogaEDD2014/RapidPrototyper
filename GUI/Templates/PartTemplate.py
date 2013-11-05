#Scott Krulcik 11/1/13
#Superclass for template objects
import AppSettings

class PartTemplate():
    def __init__(self, lines=[], editor=None):
        if editor==None:
            editor=wx.Panel(None, size=)
        self.editor=editor
        self.lines=lines
        
    def getEditor(self):
        self.editor.SetBackgroundColour(AppSetings.defaultBackground)
        return self.editor

    def setEditor(self, panel):
        self.editor=panel

    def setLines(self, nlines):
        self.lines=nlines

    def getLines(self):
        return self.lines

    def addLines(self, nlines):
        self.lines.append(nlines)

    def onGraphClick(self, event):
        pass