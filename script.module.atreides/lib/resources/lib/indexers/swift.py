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

# Inspired by the Jen Plugin by MuadDib
# As such, based off the modules written by RACC and all initial credit goes to that developer

'''
2019/4/8:  Updated API code for new URLs and JSON format
2019/4/12: Updated Auth Code per RACC's changes
2019/4/17: Fuck PyCrypto. Rewrote Encryption to use PyAES myself to support Kodi 17 and 18 without trickery
2019/5/25: Converting root category menu to use Atreides json menus
'''
import json
import os
import requests
import sys
import time
import traceback
import urllib

# from Cryptodome.Cipher import AES
from hashlib import md5
from binascii import b2a_hex

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.modules import client, control, jsonbm, jsonmenu, log_utils, pyaes, utils

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonIcon = control.addonIcon()
addonFanart = control.addonFanart()


class swift:
    def __init__(self):
        self.User_Agent = 'okhttp/3.10.0'
        self.Play_User_Agent = 'Lavf/56.15.102'

        self.base_api_url = 'http://swiftstreamz.com/SwiftPanel/api.php?get_category'
        self.base_dta_url = 'http://swiftstreamz.com/SwiftPanel/swiftlive.php'
        self.base_cat_url = 'http://swiftstreamz.com/SwiftPanel/api.php?get_channels_by_cat_id=%s'

        self.filter_mov = control.setting('tv.swift.filtermov')
        self.filter_spo = control.setting('tv.swift.filtersports')
        self.filter_tvl = control.setting('tv.swift.filtertv')

    def root(self):
        rootMenu = jsonmenu.jsonMenu()
        rootMenu.load('channels')

        for item in rootMenu.menu['swift_categories']:
            try:
                title = utils.convert(item['title']).encode('utf-8')
                if self.filter_mov == 'true' and 'vod' in item['cattype']:
                    continue
                if self.filter_spo == 'true' and 'sports' in title.lower():
                    continue
                if self.filter_tvl == 'true' and 'live' in item['cattype']:
                    continue
                id = item['cid']

                icon = item['thumbnail']
                link = 'swiftCat&url=%s' % (id)
                self.addDirectoryItem(title, link, icon, icon)
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('Channels - Failed to Build: \n' + str(failure))

        self.endDirectory(sortMethod=xbmcplugin.SORT_METHOD_LABEL)

    def swiftCategory(self, id):
        url = self.base_cat_url % (id)
        headers = {'Authorization': 'Basic @Swift11#:@Swift11#', 'User-Agent': self.User_Agent}
        response = client.request(url, headers=headers)

        items = []
        try:
            if 'Erreur 503' in str(response):
                self.addDirectoryItem('[B]System down for maintenance[/B]',
                                      'sectionItem', 'tools.png', 'DefaultTvShows.png')
            else:
                response = json.loads(response)
                for a in response['LIVETV']:
                    streams = []
                    for entry in a['stream_list']:
                        if '.m3u8' in entry['stream_url'] or '.2ts' in entry['stream_url']:
                            streams.append(entry)

                    if len(streams) == 0:
                        continue

                    name = a['channel_title']
                    icon = a['channel_thumbnail']

                    # For now, just supporting the first stream, even when multiple available. Cuz I am fat and lazy
                    url = streams[0]['stream_url']
                    token = streams[0]['token']

                    playencode = '%s|%s|%s' % (name, url, token)

                    item = control.item(label=name)
                    item.setProperty("IsPlayable", "true")
                    item.setArt({"thumb": icon, "icon": icon})
                    item.setInfo(type="video", infoLabels={"Title": name, "mediatype": "video"})

                    '''
                    Let's build out this context menu bitches
                    '''
                    try:
                        cm = jsonbm.jsonBookmarks().build_cm('Channels', name=name, id=a['id'], action='swiftPlay', icon=icon, url=playencode.encode('base64'))
                        if len(cm) > 0:
                            item.addContextMenuItems(cm)
                    except Exception:
                        failure = traceback.format_exc()
                        log_utils.log('Swift Streamz - BM Exception: \n' + str(failure))

                    try:
                        item.setContentLookup(False)
                    except AttributeError:
                        pass
                    url = '%s?action=swiftPlay&url=%s' % (sysaddon, playencode.encode('base64'))

                    items.append((url, item, False))
                control.addItems(syshandle, items)
        except Exception:
            pass

        self.endDirectory('files', xbmcplugin.SORT_METHOD_LABEL)

    def swiftPlay(self, url):
        url = url.decode('base64')
        tmp = url.split('|', 2)
        title = tmp[0]
        url = tmp[1]
        token = tmp[2]

        data = {"data": get_post_data()}
        token_url = 'http://swiftstreamz.com/newapptoken%s.php' % (token)
        get_token = requests.post(token_url, headers={"User-Agent": self.User_Agent}, data=data, timeout=10)
        auth_token = get_token.text.partition('=')[2]

        auth_token = "".join(
            [
                auth_token[:-59],
                auth_token[-58:-47],
                auth_token[-46:-35],
                auth_token[-34:-23],
                auth_token[-22:-11],
                auth_token[-10:],
            ]
        )
        try:
            url = url + '?wmsAuthSign=' + auth_token + '|User-Agent=%s' % (self.Play_User_Agent)

            item = control.item(title, path=url)
            item.setArt({"thumb": addonIcon, "icon": addonIcon})
            item.setInfo(type="video", infoLabels={"Title": title})
            item.setProperty('IsPlayable', 'true')

            if 'playlist.m3u8' in url or '.2ts' in url:
                inputstream = control.setting('tv.swift.inputstream')
                if inputstream == '' or inputstream == 'true':
                    item.setMimeType("application/vnd.apple.mpegurl")
                    item.setProperty("inputstreamaddon", "inputstream.adaptive")
                    item.setProperty("inputstream.adaptive.manifest_type", "hls")
                    item.setProperty("inputstream.adaptive.stream_headers", url.split("|")[-1])
                else:
                    item.setMimeType("application/vnd.apple.mpegurl")
            else:
                item.setMimeType("video/x-mpegts")

            try:
                item.setContentLookup(False)
            except AttributeError:
                pass
            xbmcplugin.setResolvedUrl(handle=syshandle, succeeded=True, listitem=item)
        except Exception:
            from resources.lib.dialogs import ok
            ok.load('Connection Error', '[B]Error finding streams. Try again later.[/B]')
            failure = traceback.format_exc()
            log_utils.log('Swift Streamz - Exception: \n' + str(failure))
            return

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

    def endDirectory(self, contentType='addons', sortMethod=xbmcplugin.SORT_METHOD_NONE):
        control.content(syshandle, contentType)
        sort_clowns = control.setting('tv.swift.sorttheclowns')
        if sort_clowns == '' or sort_clowns == 'true':
            control.sortMethod(syshandle, xbmcplugin.SORT_METHOD_LABEL)
        else:
            control.sortMethod(syshandle, sortMethod)
        control.directory(syshandle, cacheToDisc=True)

    def addDirectory(self, items, queue=False, isFolder=True):
        if items is None or len(items) is 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif artPath is not None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                item = control.item(label=name)

                if isFolder:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % urllib.quote_plus(i['url'])
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'false')
                else:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % i['url']
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'true')
                    item.setInfo("mediatype", "video")
                    item.setInfo("audio", '')

                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except Exception:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


def get_post_data():
    _key = b"cLt3Gp39O3yvW7Gw"
    _iv = b"bRRhl2H2j7yXmuk4"
    cipher = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(_key, _iv))
    ciphertext = ''
    _time = str(int(time.time()))
    _hash = md5("{0}e31Vga4MXIYss1I0jhtdKlkxxwv5N0CYSnCpQcRijIdSJYg".format(_time).encode("utf-8")).hexdigest()
    _plain = "{0}&{1}".format(_time, _hash).ljust(48).encode("utf-8")
    ciphertext += cipher.feed(_plain)
    ciphertext += cipher.feed()
    return b2a_hex(ciphertext[:-16]).decode("utf-8")
