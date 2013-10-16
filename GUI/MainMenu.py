#-------------------------------------------------------------------------------
# Main Menu
# Author:      Scott Krulcik
# Created:     16/10/2013
#-------------------------------------------------------------------------------
import BubbleMenu
import AppSettings
import wx

class MainMenu(BubbleMenu.BubbleMenu):
    def __init__(self, parent):
        BubbleMenu.BubbleMenu.__init__(self, parent, wx.Bitmap(AppSettings.IMAGE_PATH+"Main/"+"BubbleTitle.png"), "Shape Menu", size=wx.DefaultSize)
        self.imagePath=AppSettings.IMAGE_PATH+"Main/"

        self.quickPrint=BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"QuickPrint.png"), wx.Bitmap(self.imagePath+"QuickPrintPress.png"))
        self.advancedSetup=BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"AdvancedSetup.png"), wx.Bitmap(self.imagePath+"AdvancedSetupPress.png"))
        self.templates=BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"Templates.png"), wx.Bitmap(self.imagePath+"TemplatesPress.png"))
        self.openRecent=BubbleMenu.BubbleButton(self, wx.Bitmap(self.imagePath+"OpenRecent.png"), wx.Bitmap(self.imagePath+"OpenRecentPress.png"))

        self.buttonList=[quickPrint, advancedSetup, templates, openRecent]
        self.AddMany(self.buttonList)