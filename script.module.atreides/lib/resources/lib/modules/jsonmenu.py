# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# @tantrumdev wrote this file.  As long as you retain this notice you can do whatever you want with this
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
import traceback
import urlparse

from resources.lib.modules import client, control, log_utils


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
            log_utils.log('Last Check: ' + str(lastCheck))
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

            log_utils.log('Version: ' + str(version))

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
                if remote_version < version:
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