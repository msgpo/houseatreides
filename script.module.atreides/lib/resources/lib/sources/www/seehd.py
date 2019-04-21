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
2019/4/17: fix by SC
'''

import re
import traceback
import urlparse

from resources.lib.modules import cfscrape, cleantitle, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['seehd.pl']
        self.base_link = 'http://www.seehd.pl'
        self.search_link = '/?s=%s'
        self.tv_link = '/%s-%s-watch-online/'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search = cleantitle.getsearch(imdb)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search.replace(':', ' ').replace(' ', '+'))
            r = self.scraper.get(url).content
            Yourmouth = re.compile(
                '<div class="post_thumb".+?href="(.+?)"><h2 class="thumb_title">(.+?)</h2>', re.DOTALL).findall(r)
            for Myballs, Mycock in Yourmouth:
                if cleantitle.get(title) in cleantitle.get(Mycock):
                    return Myballs
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SEEHD - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SEEHD - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            title = url
            season = '%02d' % int(season)
            episode = '%02d' % int(episode)
            se = 's%se%s' % (season, episode)
            url = self.base_link + self.tv_link % (title, se)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SEEHD - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostprDict + hostDict

            r = self.scraper.get(url).content
            links = re.compile('<iframe.+?src="(.+?)://(.+?)/(.+?)"', re.DOTALL).findall(r)
            for http, host, url in links:
                host = host.replace('www.', '')
                url = '%s://%s/%s' % (http, host, url)
                if '24hd' in url:
                    continue
                sources.append({'source': host, 'quality': '720p', 'language': 'en',
                                'url': url, 'direct': False, 'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SEEHD - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
