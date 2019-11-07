# -*- coding: utf-8 -*-

#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

'''
2019/11/07: Fixed typo missed when importing from Atreides
'''

import os
import requests
import xml.etree.ElementTree as ET

import xbmcaddon

from resources.lib.modules import control

ACTION_PREVIOUS_MENU = 10  # ESC action
ACTION_NAV_BACK = 92  # Backspace action
ACTION_MOVE_LEFT = 1  # Left arrow key
ACTION_MOVE_RIGHT = 2  # Right arrow key
ACTION_MOVE_UP = 3  # Up arrow key
ACTION_MOVE_DOWN = 4  # Down arrow key
ACTION_MOUSE_WHEEL_UP = 104  # Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN = 105  # Mouse wheel down
ACTION_MOVE_MOUSE = 107  # Down arrow key
ACTION_SELECT_ITEM = 7  # Number Pad Enter
ACTION_BACKSPACE = 110  # ?
ACTION_MOUSE_LEFT_CLICK = 100
ACTION_MOUSE_LONG_CLICK = 108

MENU_ACTIONS = [ACTION_MOVE_UP, ACTION_MOVE_DOWN, ACTION_MOUSE_WHEEL_UP, ACTION_MOUSE_WHEEL_DOWN, ACTION_MOVE_MOUSE]

artPath = control.artPath()
skinSubPath = control.skinSubPath()
_addon = xbmcaddon.Addon(id='plugin.video.marauder')
addonname = _addon.getAddonInfo('name')

bg_news = os.path.join(artPath, 'newsbg.png')
bg_mid = os.path.join(artPath, 'bg_mid.png')
bg_ok = os.path.join(artPath, 'okbg.png')
bg_mdialog = os.path.join(artPath, 'mdialogbg.png')
btn_focus = os.path.join(artPath, 'onfocus.png')
btn_nofocus = os.path.join(artPath, 'onnofocus.png')
trakt_icon = os.path.join(artPath, 'trakticon.png')


class ThemeColors():
    def __init__(self):
        self.colors()

    def colors(self):
        tree = ET.parse(os.path.join(skinSubPath, 'colors', 'colors.xml'))
        root = tree.getroot()
        for item in root.findall('color'):
            self.dh_color = item.find('dialogheader').text
            self.dt_color = item.find('dialogtext').text
            self.mh_color = item.find('menuheader').text
            self.mt_color = item.find('menutext').text
            self.link_color = item.find('link').text
            self.focus_textcolor = item.find('focustext').text
            self.btn_focus = item.find('focusbutton').text


def getDialogText(url):
    try:
        message = requests.get(url).content

        if message is None:
            return 'Nothing today! Blame CNN'
        if '[link]' in message:
            tcolor = '[COLOR %s]' % (self.colors.link_color)
            message = message.replace('[link]', tcolor).replace('[/link]', '[/COLOR]')
        return message
    except Exception:
        return 'Nothing today! Blame CNN'

