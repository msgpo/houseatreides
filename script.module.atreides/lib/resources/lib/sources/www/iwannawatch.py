# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# @shellc0de wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

import re
import urlparse
import requests
import traceback

from resources.lib.modules import cleantitle, source_utils, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['iwannawatch.is']
        self.base_link = 'https://www.iwannawatch.is'
        self.search_link = '/%s-%s-full-movie/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (title, year)))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('IwannaWatch - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            r = requests.get(url, headers=headers).content
            quality_check = re.compile('class="quality">(.+?)<').findall(r)

            for quality in quality_check:

                if 'HD' in quality:
                    quality = '720p'
                else:
                    quality = 'SD'

            links = re.compile('li class=.+?data-href="(.+?)"').findall(r)
            for url in links:

                valid, host = source_utils.is_host_valid(url, hostDict)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('IwannaWatch - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
