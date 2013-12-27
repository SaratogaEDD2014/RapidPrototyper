#-------------------------------------------------------------------------------
# Main Menu
# Author:      Scott Krulcik
# Created:     16/10/2013
#-------------------------------------------------------------------------------
from BubbleMenu import *
import QuickPrint
import TemplateChooser
import OpenRecent
import AdvancedSetup
import GUI.settings as settings
import wx

class MainMenu(BubbleMenu):
    def __init__(self, parent):
        BubbleMenu.__init__(self, parent, wx.Bitmap(settings.IMAGE_PATH+"Main/"+"BubbleTitle.png"), "Main Menu", size=wx.Size(440,440))
        self.imagePath=settings.IMAGE_PATH+"Main/"
        self.parent=parent

        self.quickPrintView=QuickPrint.QuickPrint(self.parent)
        self.advancedSetupView=AdvancedSetup.AdvancedSetup(self.parent)
        self.templatesView=TemplateChooser.TemplateChooser(self.parent)
        self.openRecentView=OpenRecent.OpenRecent(self.parent)

        if(settings.icon_view):
            self.quickPrint = MenuButton(self, wx.Bitmap(self.imagePath+"QuickPrint.png"), wx.Bitmap(self.imagePath+"QuickPrintPress.png"), target=self.quickPrintView)
            self.advancedSetup = MenuButton(self, wx.Bitmap(self.imagePath+"AdvancedSetup.png"), wx.Bitmap(self.imagePath+"AdvancedSetupPress.png"), target= self.advancedSetupView)
            self.templates = MenuButton(self, wx.Bitmap(self.imagePath+"Templates.png"), wx.Bitmap(self.imagePath+"TemplatesPress.png"), target=self.templatesView)
            self.openRecent = MenuButton(self, wx.Bitmap(self.imagePath+"OpenRecent.png"), wx.Bitmap(self.imagePath+"OpenRecentPress.png"), target=self.openRecentView)
        else:
            self.quickPrint = DynamicButton(self, name='Quick\nPrint', target=self.quickPrintView)
            self.advancedSetup = DynamicButton(self,name='Advanced\nSetup', target= self.advancedSetupView)
            self.templates = DynamicButton(self, name='Templates', target=self.templatesView)
            self.openRecent = DynamicButton(self, name='Open\nRecent', target=self.openRecentView)

        self.buttonList=[self.quickPrint, self.advancedSetup, self.templates, self.openRecent]
        self.setChildren(self.buttonList)