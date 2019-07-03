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
import traceback
import urlparse

from resources.lib.modules import cfscrape, cleantitle, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['movie4k.is', 'movie4k.ws']
        self.base_link = 'https://www1.movie4k.is'
        self.search_link = '/?s=%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search.replace(':', ' ').replace(' ', '+'))

            r = self.scraper.get(url).content
            Yourmouth = re.compile(
                '<div class="boxinfo".+?href="(.+?)".+?<h2>(.+?)</h2>.+?class="year">(.+?)</span>', re.DOTALL).findall(r)
            for Myballs, Mycock, Myjizz in Yourmouth:
                if cleantitle.get(title) in cleantitle.get(Mycock):
                    if year in str(Myjizz):
                        return Myballs
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Movie4kis - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostprDict + hostDict
            # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

            timer = control.Time(start=True)

            r = self.scraper.get(url).content
            qual = re.compile('<span class="calidad2">(.+?)</span>').findall(r)
            for url in qual:
                if '1080' in url:
                    quality = '1080p'
                elif '720' in url:
                    quality = '720p'
                elif 'HD' in url:
                    quality = 'HD'
                else:
                    quality = 'SD'

            links = re.compile('<iframe src="(.+?)"', re.DOTALL).findall(r)

            for link in links:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('Movie4kis - Timeout Reached')
                    break

                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].split('.')[0].title()
                valid, host = source_utils.is_host_valid(link, hostDict)
                sources.append({'source': host, 'quality': quality, 'language': 'en',
                                'url': link, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Movie4kis - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
