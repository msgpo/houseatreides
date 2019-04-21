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

from resources.lib.modules import cfscrape, client, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['putlockers.movie', 'putlockerr.is']
        self.base_link = 'https://putlockerr.is'
        self.search_link = '/embed/%s/'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url + '/%s-%s/' % (season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = self.scraper.get(url).content
            try:
                match = re.compile('<iframe src="(.+?)://(.+?)/(.+?)"').findall(r)
                for http, host, url in match:
                    url = '%s://%s/%s' % (http, host, url)
                    sources.append({'source': host, 'quality': 'HD', 'language': 'en',
                                    'url': url, 'direct': False, 'debridonly': False})
            except Exception:
                return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return sources
        return sources

    def resolve(self, url):
        return url
