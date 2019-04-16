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

from resources.lib.modules import cfscrape, cleantitle, directstream, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['downflix.win']
        self.base_link = 'https://en.downflix.win'
        self.search_link = '/%s-%s/'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.search_link % (title, year)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DownFlix - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return
            holder = self.scraper.get(url).content
            Alternates = re.compile('<button class="text-capitalize dropdown-item" value="(.+?)"',
                                    re.DOTALL).findall(holder)
            for alt_link in Alternates:
                alt_url = alt_link.split("e=")[1]
                valid, host = source_utils.is_host_valid(alt_url, hostDict)
                sources.append({'source': host, 'quality': '1080p', 'language': 'en',
                                'url': alt_url, 'info': [], 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DownFlix - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return directstream.googlepass(url)
