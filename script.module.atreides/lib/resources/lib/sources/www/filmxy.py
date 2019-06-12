# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

'''
2019/5/24: Removed filter function, as its not needed anymore. Updated/tweaked regex
to pull both iframes. Added some quality checking from source_utils.
2019/6/12: Added cfscrape
'''

import re
import urlparse
import traceback

from resources.lib.modules import cleantitle, log_utils, source_utils, cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['filmxy.me', 'filmxy.one', 'filmxy.ws']
        self.base_link = 'https://www.filmxy.live'
        self.search_link = '/%s-%s'
        self.cfscraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (title, year)))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FilmXY - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources
            # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            result = self.cfscraper.get(url).content
            streams = re.compile('data-player="&lt;[A-Za-z]{6}\s[A-Za-z]{3}=&quot;(.+?)&quot;', re.DOTALL).findall(result)

            for link in streams:
                quality = source_utils.check_sd_url(link)
                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].lower()
                '''
                Now source_utils can't strip quality on some of these links. It will drop them
                down to SD. So i say we try this as most if not all links are HD
                '''
                if quality == 'SD':
                    sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
                else:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FilmXY - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
