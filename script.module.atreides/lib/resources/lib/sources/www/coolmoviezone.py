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
2019/4/17: Readded this one, fix by SC
'''

import re
import urlparse
import traceback

from resources.lib.modules import cfscrape, cleantitle, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['coolmoviezone.online', 'coolmoviezone.co']
        self.base_link = 'https://coolmoviezone.io'
        self.search_link = '/%s-%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (title, year)))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CoolMovieZone - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = self.scraper.get(url).content
            match = re.compile('<td align="center"><strong><a href="(.+?)"').findall(r)
            for url in match:
                quality = source_utils.check_sd_url(url)
                valid, host = source_utils.is_host_valid(url, hostDict)
                sources.append({'source': host, 'quality': quality, 'language': 'en',
                                'url': url, 'direct': False, 'debridonly': False})
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CoolMovieZone - Exception: \n' + str(failure))
            return
        return sources

    def resolve(self, url):
        return url
