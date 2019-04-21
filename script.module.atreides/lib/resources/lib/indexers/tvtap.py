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

# Inspired by the Swift Streamz Jen Plugin by MuadDib (uses very similar json results from host)
# As such, based off the modules written by RACC and all initial credit goes to that developer

'''
2019/4/13: Upgraded for new API by myself. Decryption done by RACC for new Auth
2019/4/21: Upgraded for pure python decryption by myself. Kodi 17 compatibility
'''

import json
import os
import sys
import traceback
import urllib

import xbmc
import xbmcgui
import xbmcplugin

from base64 import b64encode, b64decode
from binascii import a2b_hex

from resources.lib.modules import client, control, log_utils, pyaes, pydes, pyrsa

try:
    from urllib.parse import quote_from_bytes as orig_quote
except ImportError:
    from urllib import quote as orig_quote

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonIcon = control.addonIcon()
addonFanart = control.addonFanart()


def quote(s, safe=""):
    return orig_quote(s.encode("utf-8"), safe.encode("utf-8"))


class tvtap:
    def __init__(self):
        self.User_Agent = 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)'
        self.Player_User_Agent = 'mediaPlayerhttp/1.9 (Linux;Android 5.1) ExoPlayerLib/2.6.1'

        self.token_url = 'https://taptube.net/tv/index.php?case=get_channel_link_with_token_latest'
        self.list_url = 'https://taptube.net/tv/index.php?case=get_all_channels'
        self.icon_url = 'https://taptube.net/tv/%s|User-Agent=%s' % ('%s', self.User_Agent)

    def root(self):
        headers = {"app-token": "37a6259cc0c1dae299a7866489dff0bd"}
        data = {"payload": payload(), "username": "603803577"}
        try:
            try:
                response = client.request(self.list_url, post=data, headers=headers)
                if 'could not connect' in str(response).lower() or 'some error occurred' in str(response).lower():
                    self.addDirectoryItem('[B]System down for maintenance[/B]',
                                          'sectionItem', 'tools.png', 'DefaultTvShows.png')
                else:
                    response = json.loads(response)
                    if response["success"] == 1:
                        category_list = []
                        for a in response['msg']['channels']:
                            try:
                                name = a['cat_name']
                                if name not in category_list:
                                    category_list.append(name)
                                    id = a['cat_id']
                                    try:
                                        icon = self.icon_url % (a['img'])
                                    except Exception:
                                        icon = addonIcon
                                    self.addDirectoryItem(name, 'tvtapCat&url=%s' % (id), icon, 'DefaultTvShows.png')
                            except Exception:
                                pass
                    else:
                        self.addDirectoryItem('[B]System down for maintenance[/B]', 'sectionItem', 'tools.png', 'DefaultTvShows.png')
                        self.endDirectory()
                        return
            except Exception:
                self.addDirectoryItem('[B]Issue connecting to server. Try again later.[/B]',
                                      'sectionItem', 'tools.png', 'DefaultTvShows.png')
                self.endDirectory()
                return
        except Exception:
            pass
        self.endDirectory(sortMethod=xbmcplugin.SORT_METHOD_LABEL)

    def tvtapCategory(self, id):
        headers = {"app-token": "37a6259cc0c1dae299a7866489dff0bd"}
        data = {"payload": payload(), "username": "603803577"}
        try:
            items = []
            try:
                response = client.request(self.list_url, post=data, headers=headers)
                if 'could not connect' in str(response).lower() or 'some error occurred' in str(response).lower():
                    self.addDirectoryItem('[B]System down for maintenance[/B]',
                                          'sectionItem', 'tools.png', 'DefaultTvShows.png')
                else:
                    countries = control.setting('tv.tvtap.poached')
                    if countries == '':
                        countries = 'All'
                    response = json.loads(response)
                    if response["success"] == 1:
                        for a in response['msg']['channels']:
                            try:
                                if a['cat_id'] == id:
                                    country = a['country']
                                    if country == countries or countries == 'All':
                                        if countries == 'All':
                                            name = a['channel_name'].rstrip('.,-') + ' (' + str(country) + ')'
                                        else:
                                            name = a['channel_name'].rstrip('.,-')
                                        chan_id = a["pk_id"]
                                        icon = self.icon_url % (a['img'])

                                        item = control.item(label=name)
                                        item.setProperty("IsPlayable", "true")
                                        item.setArt({"thumb": icon, "icon": icon})
                                        item.setInfo(type="video", infoLabels={"Title": name, "mediatype": "video"})
                                        try:
                                            item.setContentLookup(False)
                                        except AttributeError:
                                            pass
                                        url = '%s?action=tvtapPlay&url=%s' % (sysaddon, chan_id)
                                        items.append((url, item, False))
                                    else:
                                        continue
                            except Exception:
                                pass
                    else:
                        self.addDirectoryItem('[B]System down for maintenance[/B]', 'sectionItem', 'tools.png', 'DefaultTvShows.png')
                        self.endDirectory()
                        return
                    control.addItems(syshandle, items)
            except Exception:
                self.addDirectoryItem('[B]Issue connecting to server. Try again later.[/B]',
                                      'sectionItem', 'tools.png', 'DefaultTvShows.png')
                self.endDirectory()
                return
        except Exception:
            pass
        self.endDirectory(sortMethod=xbmcplugin.SORT_METHOD_LABEL)

    def tvtapPlay(self, chan_id):
        headers = {"app-token": "37a6259cc0c1dae299a7866489dff0bd"}
        data = {"payload": payload(), "channel_id": chan_id, "username": "603803577"}
        try:
            response = client.request(self.token_url, post=data, headers=headers)
            if 'could not connect' in str(response).lower() or 'some error occurred' in str(response).lower():
                from resources.lib.dialogs import ok
                ok.load('Connection Error', '[B]Issue connecting to server. Try again later.[/B]')
            else:
                response = json.loads(response)
                if response["success"] == 1:
                    links = []
                    for stream in response["msg"]["channel"][0].keys():
                        if "stream" in stream or "chrome_cast" in stream:
                            _crypt_link = response["msg"]["channel"][0][stream]
                        if _crypt_link:
                            d = pydes.des(b"98221122")
                            # d = DES.new(b"98221122", DES.MODE_ECB)
                            link = d.decrypt(b64decode(_crypt_link))
                            link = unpad(link, 8).decode("utf-8")
                            # link = unpad(d.decrypt(b64decode(_crypt_link)), 8).decode("utf-8")
                            if not link == "dummytext" and link not in links:
                                links.append(link)

                    lazy_mode = control.setting('tv.tvtap.lazymode')
                    if lazy_mode == '' or lazy_mode == 'true':
                        link = links[0]
                    else:
                        dialog = xbmcgui.Dialog()
                        ret = dialog.select("Choose Stream", links)
                        link = links[ret]

                    if link.startswith("http"):
                        media_url = "%s|User-Agent=%s" % (link, quote(self.Player_User_Agent))
                    else:
                        media_url = link

                    title = response["msg"]["channel"][0]['channel_name']
                    image = response["msg"]["channel"][0]['img']

                    li = control.item(title, path=media_url)
                    li.setArt({"thumb": image, "icon": image})
                    li.setInfo(type="video", infoLabels={"Title": title})

                    if "playlist.m3u8" in media_url:
                        inputstream = control.setting('tv.tvtap.inputstream')
                        if inputstream == '' or inputstream == 'true':
                            li.setMimeType("application/vnd.apple.mpegurl")
                            li.setProperty("inputstreamaddon", "inputstream.adaptive")
                            li.setProperty("inputstream.adaptive.manifest_type", "hls")
                            li.setProperty("inputstream.adaptive.stream_headers", media_url.split("|")[-1])
                            li.setProperty('IsPlayable', 'true')
                        else:
                            li.setMimeType("application/vnd.apple.mpegurl")
                            li.setProperty('IsPlayable', 'true')
                    else:
                        li.setProperty('IsPlayable', 'true')

                    try:
                        li.setContentLookup(False)
                    except AttributeError:
                        pass
                    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
                else:
                    self.addDirectoryItem('[B]System down for maintenance[/B]', 'sectionItem', 'tools.png', 'DefaultTvShows.png')
                    self.endDirectory()
                    return
        except Exception:
            from resources.lib.dialogs import ok
            ok.load('Connection Error', '[B]Error finding streams. Try again later.[/B]')
            failure = traceback.format_exc()
            log_utils.log('TV Tap - Exception: \n' + str(failure))
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
        scrambled_eggs = control.setting('tv.tvtap.frytheeggs')
        if scrambled_eggs == '' or scrambled_eggs == 'true':
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
                    item.setInfo("type", "video")
                    # item.setProperty('IsPlayable', 'true')

                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except Exception:
                pass

        control.content(syshandle, 'tvshows')
        control.directory(syshandle, cacheToDisc=True)


def payload():
    _pub_x = a2b_hex(
            "30819f300d06092a864886f70d010101050003818d003081890281"
            "8100bfa5514aa0550688ffde568fd95ac9130fcdd8825bdecc46f1"
            "8f6c6b440c3685cc52ca03111509e262dba482d80e977a938493ae"
            "aa716818efe41b84e71a0d84cc64ad902e46dbea2ec61071958826"
            "4093e20afc589685c08f2d2ae70310b92c04f9b4c27d79c8b5dbb9"
            "bd8f2003ab6a251d25f40df08b1c1588a4380a1ce8030203010001"
        )

    _pubkey = pyrsa.PublicKey.load_pkcs1_openssl_der(_pub_x)
    _msg = a2b_hex(
        "7b224d4435223a22695757786f45684237686167747948392b58563052513d3d5c6e222c22534"
        "84131223a2242577761737941713841327678435c2f5450594a74434a4a544a66593d5c6e227d"
    )
    cipher = pyrsa.encrypt(_msg, _pubkey)
    return b64encode(cipher)


def unpad(padded_data, block_size, style='pkcs7'):
    """Remove standard padding.

    :Parameters:
      padded_data : byte string
        A piece of data with padding that needs to be stripped.
      block_size : integer
        The block boundary to use for padding. The input length
        must be a multiple of ``block_size``.
      style : string
        Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.
    :Return:
        Data without padding.
    :Raises ValueError:
        if the padding is incorrect.
    """

    '''
    FIXIT: Py3 should use bord() and bchr()
    '''

    pdata_len = len(padded_data)
    if pdata_len % block_size:
        raise ValueError("Input data is not padded")
    if style in ('pkcs7', 'x923'):
        padding_len = ord(padded_data[-1])
        if padding_len < 1 or padding_len > min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if style == 'pkcs7':
            if padded_data[-padding_len:] != chr(padding_len)*padding_len:
                raise ValueError("PKCS#7 padding is incorrect.")
        else:
            if padded_data[-padding_len:-1] != chr(0)*(padding_len-1):
                raise ValueError("ANSI X.923 padding is incorrect.")
    elif style == 'iso7816':
        padding_len = pdata_len - padded_data.rfind(chr(128))
        if padding_len < 1 or padding_len > min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if padding_len > 1 and padded_data[1-padding_len:] != chr(0)*(padding_len-1):
            raise ValueError("ISO 7816-4 padding is incorrect.")
    else:
        raise ValueError("Unknown padding style")
    return padded_data[:-padding_len]
