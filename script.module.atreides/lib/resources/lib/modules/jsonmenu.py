# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

import json
import os
import time
import sys
import traceback
import urlparse

from resources.lib.modules import client, control, log_utils

import xbmcplugin

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonFanart = control.addonFanart()


class jsonMenu(object):
    def __init__(self):
        # Default root locations, if none is set by the indexer
        self.menu_file = None
        self.local_root = os.path.join(control.addonPath, 'menu')
        self.remote_root = 'SaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9ob3VzZWF0cmVpZGVzL21hc3Rlci9wbHVnaW4udmlkZW8uYXRyZWlkZXMvbWVudS8='[1:].decode('base64')
        self.menu = None

        self.agent = 'hQXRyZWlkZXMgSlNPTiBNZW51'[1:].decode('base64')

    def load(self, menu_file, refresh=False):
        menu_file = menu_file + '.json'
        try:
            self.menu_file = os.path.join(self.local_root, menu_file)
            fileref = control.openFile(self.menu_file)
            content = fileref.read()
            fileref.close()
            self.menu = json.loads(content)
            '''
            Now lets handle the versioning side of things
            '''
            try:
                lastCheck = self.menu["menu_file"]["checked"]
            except Exception:
                lastCheck = '1'
            lastCheck = int(float(lastCheck))
            if time.time() < lastCheck:
                return

            '''
            Time check done, so let's check online for a newer version
            '''
            try:
                version = self.menu["menu_file"][0]["version"]
            except Exception:
                version = '0'
            version = int(float(version))

            try:
                header = {'User-Agent': self.agent}
                url = urlparse.urljoin(self.remote_root, menu_file)
                response = client.request(url, headers=header)
                remote_menu = json.loads(response)

                try:
                    remote_version = remote_menu["menu_file"][0]["version"]
                except Exception:
                    remote_version = '0'
                remote_version = int(float(remote_version))
                if remote_version > version:
                    self.menu = remote_menu
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('jsonMenu - Open Remote Exception: \n' + str(failure))

            lastCheck = time.time() + (60 * 60 * 24)
            self.menu["menu_file"][0]["checked"] = str(lastCheck)
            self.save()
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('jsonMenu - Open Local Exception: \n' + str(failure))

    def save(self):
        with open(self.menu_file, 'w') as json_file:
            json.dump(self.menu, json_file, indent=4)
            json_file.close()

    def process(self, menu_section):
        for item in self.menu[menu_section]:
            try:
                '''
                First things first, let's see if this is an entry with on/off settings and if we should display it.
                '''
                try:
                    toggle = item.get('toggle', None)
                    if toggle is not None:
                        is_enabled = control.setting(toggle).strip()
                        if (is_enabled == '' or is_enabled == 'false'):
                            continue
                except Exception:
                    pass

                '''
                Language file support can be done this way
                '''
                title = item.get('title', 'No Title Given')
                try:
                    title = control.lang(int(title)).encode('utf-8')
                except Exception:
                    pass
                link = item.get('action', None)

                try:
                    url = item.get('url', None)
                    link = '%s&url=%s' % (link, url) if url is not None else link
                except Exception:
                    pass
                try:
                    listid = item.get('list_id', None)
                    listtype = item.get('list_type', None)
                    link = '%s&listid=%s&listtype=%s' % (link, listid, listtype) if listid is not None else link
                except Exception:
                    pass
                try:
                    menu_file = item.get('menu_file', None)
                    menu_section = item.get('menu_section', None)
                    link = '%s&menu_file=%s&menu_section=%s' % (link, menu_file, menu_section) if menu_file is not None else link
                except Exception:
                    pass
                try:
                    query = item.get('query', None)
                    link = '%s&query=%s' % (link, query) if query is not None else link
                except Exception:
                    pass

                isAction = True if item.get('nolink', None) is None else False

                self.addDirectoryItem(title, link, item['thumbnail'], item['thumbnail'], isAction=isAction)
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('Process Menu - Failed to Build: \n' + str(failure))

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        if 'http' not in thumb:
            thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []

        queueMenu = control.lang(32065).encode('utf-8')

        if queue is True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
