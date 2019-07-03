# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

'''
2019/5/1: Initial import to Atreides. Initial scraper done by a friend, all credit to them
'''

import re
import traceback

from resources.lib.modules import cleantitle, client, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['123moviehd.cc']
        self.base_link = 'https://123moviehd.cc'
        self.search_link = '/%s-%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.search_link % (title, year)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('123MovieHD - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            r = client.request(url)
            try:
                qual = re.compile('class="quality">(.+?)<').findall(r)
                for i in qual:
                    if 'HD' in i:
                        quality = '1080p'
                    else:
                        quality = 'SD'
                match = re.compile('<iframe.+?src="(.+?)"').findall(r)
                for url in match:
                    if 'youtube' in url:
                        continue
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('123MovieHD - Exception: \n' + str(failure))
                return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('123MovieHD - Exception: \n' + str(failure))
            return
        return sources

    def resolve(self, url):
        return url
