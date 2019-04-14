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

import os
import re
import sys
import urllib
import urlparse

import xbmc

from resources.lib.modules import cleantitle, client, control

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
        self.addDirectoryItem('Cartoon Series', 'b98RabbitNav&url=%s' % (self.series_link), 'b98.png', 'DefaultTvShows.png')
        self.addDirectoryItem('Browse by Studio', 'b98RabbitNav&url=%s' % (self.studio_link), 'b98.png', 'DefaultTvShows.png')

        self.endDirectory()

    def scrape(self, url):
        url = urlparse.urljoin(self.base_main_link, url)

        try:
            html = client.request(url, timeout=10)
            item_list = client.parseDOM(html, 'div', attrs={'class': 'item col-lg-3 col-md-3 col-sm-12 '})
            for content in item_list:
                link = re.compile('href="(.+?)"', re.DOTALL).findall(content)[0]
                icon, title = re.compile('img src="(.+?)" alt="(.+?)"', re.DOTALL).findall(content)[0]
                try:
                    link = link.replace(self.base_main_link, '')
                    title = cleantitle.normalize(title)
                    if 'videos_categories' in link:
                        # Let's add another menu item to go down the rabbit hole
                        self.addDirectoryItem(title, 'b98RabbitNav&url=%s' % (link), icon, icon)
                    else:
                        # Otherwise, display the carrot link
                        self.addDirectoryItem(title, 'b98CarrotLink&url=%s' % (link), icon, icon)
                except Exception:
                    continue

            # Try doing a next hole, if available
            try:
                navi_link = re.compile('a class="next page-numbers" href="(.+?)"', re.DOTALL).findall(html)[0]
                self.addDirectoryItem(control.lang(32053).encode('utf-8'), 'b98RabbitNav&url=%s' % (navi_link), control.addonNext(), 'DefaultTvShows.png')
            except Exception:
                pass
        except Exception:
            pass

        self.endDirectory()

    def play(self, url):
        url = urlparse.urljoin(self.base_main_link, url)

        try:
            html = client.request(url, timeout=10)
            vid_url = re.compile('file: "(.*?)"', re.DOTALL).findall(html)[0]
            if 'http:' in vid_url:
                vid_url = vid_url.replace('http:', 'https:')
            vid_url = vid_url + '|User-Agent=' + client.randomagent()
            xbmc.executebuiltin("PlayMedia(%s)" % (vid_url))
            quit()
            return
        except Exception:
            pass

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

    def endDirectory(self):
        control.content(syshandle, 'addons')
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
