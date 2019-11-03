# -*- coding: utf-8 -*-

#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################


import os
import re
import traceback

import xbmcgui

from resources.lib.dialogs import themecontrol
from resources.lib.modules import control, log_utils


def ChangelogViewer(cl_text=None):
    class Changelog_Window(xbmcgui.WindowXMLDialog):
        def onInit(self):
            self.colors = themecontrol.ThemeColors()

            self.cl_text = cl_text

            self.skin_text = 102
            self.btn_close = 202

            self.showdialog()

        def showdialog(self):
            self.setProperty('dhtext', self.colors.dh_color)
            self.getControl(self.skin_text).setText(self.cl_text)
            self.setFocusId(self.btn_close)

        def onClick(self, controlId):
            if controlId == self.btn_close:
                self.close()

        def onAction(self, action):
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()

    changelogfile = os.path.join(control.addonPath, 'changelog.txt')
    r = open(changelogfile)
    cl_text = r.read()
    r.close()
    viewer = Changelog_Window('Changelog.xml', control.skinModule(), control.skinTheme(), '1080i', cl_text=cl_text)
    viewer.doModal()
    del viewer
