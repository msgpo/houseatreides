# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# @tantrumdev wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

import re
import traceback

from resources.lib.modules import cfscrape, cleantitle, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['spacemov.is', 'spacemov.cc']
        self.base_link = 'https://spacemov.cc'
        self.search_link = '/search-query/%s+%s/'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('-', '+')
            r = self.base_link + self.search_link % (title, year)
            r = self.scraper.get(r).content
            url = re.findall('a href="(.+?)" class="ml-mask jt"', r)[0]
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SpaceMov - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            url = url + 'watching/?ep=1'
            r = self.scraper.get(url).content
            r = re.compile('a title="(.+?)" data-svv.+?="(.+?)"').findall(r)
            for title, url in r:
                if 'HD' in title:
                    quality = '720p'
                elif 'CAM' in title:
                    quality = 'CAM'
                else:
                    quality = 'SD'
                if 'vidcloud' in url:
                    r = self.scraper.get(url).content
                    t = re.findall('li data-status=".+?" data-video="(.+?)"', r)
                    for url in t:
                        if 'vidcloud' in url:
                            continue
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            sources.append({'source': host, 'quality': quality, 'language': 'en',
                                            'url': url, 'direct': False, 'debridonly': False})
                if 'vidcloud' in url:
                    continue

                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en',
                                    'url': url, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SpaceMov - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url
