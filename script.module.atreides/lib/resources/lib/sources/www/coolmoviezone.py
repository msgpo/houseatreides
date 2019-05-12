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

'''
2019/4/17: Readded this one, fix by SC
'''

import re
import traceback

from resources.lib.modules import cfscrape, cleantitle, client, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['coolmoviezone.online']
        self.base_link = 'https://coolmoviezone.co'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + '/%s-%s' % (title, year)
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
                host = url.split('//')[1].replace('www.', '')
                host = host.split('/')[0].split('.')[0].title()
                quality = source_utils.check_sd_url(url)
                sources.append({'source': host, 'quality': quality, 'language': 'en',
                                'url': url, 'direct': False, 'debridonly': False})
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CoolMovieZone - Exception: \n' + str(failure))
            return
        return sources

    def resolve(self, url):
        return url