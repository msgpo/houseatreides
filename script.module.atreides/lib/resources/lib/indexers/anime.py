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

'''
2019/5/2:  Added PBSKids using json pulled from website. Will expand later since they give more details but lazy atm
2019/5/23: Updated root to use JSON menu system. All data scraping and working again
2019/5/25: Fixed subtitle issue and added Clips along with Clip/Episode tagging in title. Added Plot and Duration for all videos
'''

import json
import os
import re
import sys
import traceback
import urllib
import urlparse

import xbmc
import xbmcplugin

from resources.lib.modules import client, control, jsonmenu, log_utils, utils

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonFanart = control.addonFanart()


class b98tv:
    def __init__(self):
        self.base_main_link = 'https://www.b98.tv/'
        self.series_link = '/videos_categories/series'
        self.studio_link = '/videos_categories/studios'

    def root(self):
        self.addDirectoryItem('Cartoon Series - Currently Down', 'b98RabbitNav&url=%s' % (self.series_link), 'b98.png', 'DefaultTvShows.png')
        self.addDirectoryItem('Browse by Studio - Currently Down', 'b98RabbitNav&url=%s' % (self.studio_link), 'b98.png', 'DefaultTvShows.png')

        self.endDirectory(category='B98 Cartoons')

    def scrape(self, url):
        url = urlparse.urljoin(self.base_main_link, url)
        items = []

        try:
            html = client.request(url, timeout=10)
            item_list = client.parseDOM(html, 'div', attrs={'class': 'item col-lg-3 col-md-3 col-sm-12 '})
            for content in item_list:
                link = re.compile('href="(.+?)"', re.DOTALL).findall(content)[0]
                icon, title = re.compile('img src="(.+?)" alt="(.+?)"', re.DOTALL).findall(content)[0]
                try:
                    link = link.replace(self.base_main_link, '')
                    title = utils.convert(title).encode('utf-8')

                    item = control.item(label=title)
                    item.setArt({"thumb": icon, "icon": icon})

                    if 'videos_categories' in link:
                        # Still navigating categories
                        link = '%s?action=b98RabbitNav&url=%s' % (sysaddon, link)
                        items.append((link, item, True))
                    else:
                        # This is where the goodies are
                        item.setInfo(type="video", infoLabels={"Title": title, "mediatype": "video"})
                        item.setProperty("IsPlayable", "true")
                        link = '%s?action=b98CarrotLink&url=%s&title=%s&image=%s' % (sysaddon, link, title, icon)
                        items.append((link, item, False))
                except Exception:
                    failure = traceback.format_exc()
                    log_utils.log('B98 - Failed to Build: \n' + str(failure))
                    continue

            # Try doing a next hole, if available
            try:
                navi_link = re.compile('a class="next page-numbers" href="(.+?)"', re.DOTALL).findall(html)[0]
                navi_link = navi_link.replace(self.base_main_link, '')
                next_url = '%s?action=b98RabbitNav&url=%s' % (sysaddon, navi_link)
                item = control.item(label=control.lang(32053).encode('utf-8'))
                item.setArt({"thumb": control.addonNext(), "icon": control.addonNext()})
                items.append((next_url, item, True))
            except Exception:
                pass
        except Exception:
            pass
        control.addItems(syshandle, items)
        self.endDirectory(category='B98 Cartoons')

    def play(self, url, title, icon):
        url = urlparse.urljoin(self.base_main_link, url)

        try:
            html = client.request(url, timeout=10)
            vid_url = re.compile('file: "(.*?)"', re.DOTALL).findall(html)[0]
            if 'http:' in vid_url:
                vid_url = vid_url.replace('http:', 'https:')
            vid_url = '%s|User-Agent=%s' % (vid_url, client.randomagent())

            li = control.item(title, path=vid_url)
            li.setArt({"thumb": icon, "icon": icon})
            li.setInfo(type="video", infoLabels={"Title": title})
            li.setProperty('IsPlayable', 'true')

            control.resolve(handle=int(sys.argv[1]), succeeded=True, listitem=li)
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('B98 - Failed to Play: \n' + str(failure))
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

    def endDirectory(self, contentType='addons', sortMethod=xbmcplugin.SORT_METHOD_NONE, category=None):
        control.content(syshandle, contentType)
        if category is not None:
            control.category(syshandle, category)
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


class pbskids:
    def __init__(self):
        self.base_main_link = 'https://pbskids.org/video/'
        self.series_link = 'https://content.services.pbskids.org/v2/kidspbsorg/programs/%s'

    def root(self):
        rootMenu = jsonmenu.jsonMenu()
        rootMenu.load('pbskids')
        rootMenu.process('pbskids')
        self.endDirectory(sortMethod=xbmcplugin.SORT_METHOD_LABEL, category='PBS Kids')

    def scrape(self, url):
        url = self.series_link % (url)
        self.showItems = []

        try:
            html = client.request(url, timeout=10)
            results = json.loads(html)
            '''
            Promoted Content left out, cuz that is related, or unrelated content to the show. AKA, Promoted could be a different show
            so we ignore it and go on.
            '''
            # promoted = results['collections']['promoted_content']['content']
            # self.buildShows(promoted, 'Promoted')
            episodes = results['collections']['episodes']['content']
            self.buildShows(episodes, 'Episode')
            clips = results['collections']['clips']['content']
            self.buildShows(clips, 'Clip')
        except Exception:
            pass
        control.addItems(syshandle, self.showItems)
        self.endDirectory('episodes', category=results['object']['title'])

    def buildShows(self, content, content_type):
        try:
            for entry in content:
                try:
                    url = entry['mp4']
                except Exception:
                    continue

                try:
                    title = content_type + ': ' + entry['title']
                except Exception:
                    title = content_type + ': No Show Title'

                try:
                    icon = entry['images']['mezzanine']
                    fanart = icon
                except Exception:
                    icon = control.addonIcon
                    fanart = control.addonFanart

                try:
                    duration = entry['duration']
                except Exception:
                    duration = '0'

                try:
                    plot = entry['description']
                except Exception:
                    plot = entry['title']

                try:
                    capCheck = entry['closedCaptions']
                except Exception:
                    capCheck = None
                if capCheck is not None:
                    for caption in capCheck:
                        if caption['format'] == 'SRT':
                            url = url + '|' + caption['URI']
                            break

                item = control.item(label=title)
                item.setArt({"thumb": icon, "icon": icon})
                item.setProperty("IsPlayable", "true")
                item.setInfo(type="video", infoLabels={"Title": title, "mediatype": "video", 'plot': plot, 'duration': duration})
                link = '%s?action=pbsKids&playBasic=1&url=%s' % (sysaddon, url.encode('base64'))
                self.showItems.append((link, item, False))
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('PBSKids - Failed to Build: \n' + str(failure))
        return

    def play(self, url):
        try:
            url, captions = url.decode('base64').split('|', 1)
        except Exception:
            url = url.decode('base64')
            captions = ''

        html = client.request('%s?format=json' % url)
        jrequest = json.loads(html)
        url = jrequest['url']
        if url is not None:
                li = control.item(path=url)
                if len(captions) > 0:
                    li.setSubtitles([captions])
                li.setProperty("IsPlayable", "true")
                control.resolve(handle=int(sys.argv[1]), succeeded=True, listitem=li)

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

    def endDirectory(self, contentType='addons', sortMethod=xbmcplugin.SORT_METHOD_NONE, category=None):
        control.content(syshandle, contentType)
        if category is not None:
            control.category(syshandle, category)
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

