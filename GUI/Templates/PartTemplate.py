#Scott Krulcik 11/1/13
#Superclass for template objects
import wx

class PartTemplate(object):
    def __init__(self, lines=[], editor=None):
        self.editor=self.setEditor(editor)
        self.lines=lines

    def getEditor(self):
        return self.editor

    def setEditor(self, panel):
        self.editor=panel
        if self.editor!=None:
            self.editor.SetBackgroundColour(AppSetings.defaultBackground)

    def setLines(self, nlines):
        self.lines=nlines

    def getLines(self):
        return self.lines

    def addLines(self, nlines):
        self.lines.append(nlines)

    def onGraphClick(self, event):
        pass