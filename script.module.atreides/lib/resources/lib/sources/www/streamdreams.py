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
import requests
import traceback

from resources.lib.modules import cleantitle
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['streamdreams.org']
        self.base_link = 'https://streamdreams.org'
        self.api_link = 'https://api.searchiq.co/api/search/results'
        self.headers = {'Host': 'api.searchiq.co', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Origin': 'https://streamdreams.org',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
                'Referer': 'https://streamdreams.org/results?r=', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9'}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search = cleantitle.getsearch(imdb)
            url = self.api_link
            payload = {'q': search, 'engineKey': '2b67dc761b36dcd1434c6c1bb370d9dd', 'page': '0',
                    'itemsPerPage': '15', 'group': '0', 'sortby': 'relevance', 'autocomplete': '0'}
            r = requests.get(url, params=payload, headers=self.headers)
            response = r.content
            Yourmouth = re.compile('"title":"(.+?)".+?"url":"(.+?)"', re.DOTALL).findall(response)
            for Mycock, Mynuts, in Yourmouth:
                if cleantitle.get(title) in cleantitle.get(Mycock):
                    return Mynuts
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('StreamDreams - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            search = cleantitle.getsearch(imdb)
            url = self.api_link
            payload = {'q': search, 'engineKey': '2b67dc761b36dcd1434c6c1bb370d9dd', 'page': '0',
                    'itemsPerPage': '15', 'group': '0', 'sortby': 'relevance', 'autocomplete': '0'}
            r = requests.get(url, params=payload, headers=self.headers)
            response = r.content
            Yourmouth = re.compile('"title":"(.+?)".+?"url":"(.+?)"', re.DOTALL).findall(response)
            for Mycock, Mynuts, in Yourmouth:
                if cleantitle.get(tvshowtitle) in cleantitle.get(Mycock):
                    return Mynuts
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('StreamDreams - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url + '?session=%s&episode=%s' % (season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('StreamDreams - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources

            hostDict = hostprDict + hostDict
            headers = {'Referer': url, 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            r = requests.get(url, headers=headers).content
            links = re.compile("data-href='(.+?)'\s+data", re.DOTALL).findall(r)
            for link in links:

                if 'BDRip' in link:
                    quality = '720p'
                elif 'HD' in link:
                    quality = '720p'
                else:
                    quality = 'SD'

                info = source_utils.get_release_quality(url)
                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].split('.')[0].title()
                valid, host = source_utils.is_host_valid(link, hostDict)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('StreamDreams - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
