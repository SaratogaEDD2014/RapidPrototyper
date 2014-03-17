#-------------------------------------------------------------------------------
# Main Menu
# Author:      Scott Krulcik
# Created:     16/10/2013
#-------------------------------------------------------------------------------
from bubble_menu import *
import quick_print
import template_chooser
import open_recent
import advanced_setup
import application.settings_editor as settings_editor
import application.settings as settings
import wx

class MainMenu(DynamicBubbleMenu):
    def __init__(self, parent):
        super(MainMenu, self).__init__(parent, "Main Menu")
        self.imagePath=settings.IMAGE_PATH+"Main/"
        self.parent=parent

        self.quickPrintView=quick_print.QuickPrint(self.parent)
        self.advanced_setup_view=advanced_setup.AdvancedSetup(self.parent)
        self.templatesView=template_chooser.TemplateChooser(self.parent)
        self.openRecentView=open_recent.OpenRecent(self.parent)
        self.settings_view = settings_editor.SettingsEditor(self.parent)
        self.wireless_view = None

        if(settings.icon_view):
            self.quickPrint = MenuButton(self, wx.Bitmap(self.imagePath+"QuickPrint.png"), wx.Bitmap(self.imagePath+"QuickPrintPress.png"), target=self.quickPrintView)
            self.advanced_setup = MenuButton(self, wx.Bitmap(self.imagePath+"AdvancedSetup.png"), wx.Bitmap(self.imagePath+"AdvancedSetupPress.png"), target= self.advanced_setup_view)
            self.templates = MenuButton(self, wx.Bitmap(self.imagePath+"Templates.png"), wx.Bitmap(self.imagePath+"TemplatesPress.png"), target=self.templatesView)
            self.openRecent = MenuButton(self, wx.Bitmap(self.imagePath+"OpenRecent.png"), wx.Bitmap(self.imagePath+"OpenRecentPress.png"), target=self.openRecentView)
        else:
            self.quickPrint = DynamicButton(self, name='Quick\nPrint', target=self.quickPrintView)
            self.advanced_setup = DynamicButton(self,name='Advanced\nSetup', target= self.advanced_setup_view)
            self.templates = DynamicButton(self, name='Templates', target=self.templatesView)
            self.openRecent = DynamicButton(self, name='Open\nRecent', target=self.openRecentView)
            self.edit_settings = DynamicButton(self, name='Settings', target=self.settings_view)
            self.wireless = DynamicButton(self, name='Wireless', target=self.wireless_view)

        self.buttonList=[self.quickPrint, self.advanced_setup, self.templates, self.openRecent, self.edit_settings, self.wireless]
        self.setChildren(self.buttonList)

if __name__ == "__main__":
    app = wx.App()
    frm = wx.Frame(None, size=(600,400))
    menu = MainMenu(frm)
    frm.Show(True)
    menu.Show(True)
    menu.SendSizeEvent()
    menu.CenterOnParent()
    app.MainLoop()