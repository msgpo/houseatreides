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
2019/5/12: Work done by SC, added today
2019/5/28: Fixed. Had to make a few adj cause they changed how the search works.
2019/5/30: Rewrite for better accuracy and speed
'''

import re
import urllib
import traceback
import urlparse
import requests

from resources.lib.modules import cleantitle, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['losmovies.sh']
        self.base_link = 'http://losmovies.pro'
        self.search_link = '/the-movies-found'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('LosMovies - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title']
            year = data['year']

            search = cleantitle.getsearch(title.lower())
            url = urlparse.urljoin(self.base_link, self.search_link)
            headers = {'Referer': self.base_link, 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}

            with requests.Session() as shell:

                r = shell.get(url, headers=headers).content
                t = re.compile('<input type="hidden" name="t" value="(.+?)"', re.DOTALL).findall(r)[0]
                payload = {'type': 'movies', 't': t, 'q': search}
                r = shell.get(url, params=payload, headers=headers).content
                Yourmouth = re.compile('class="showRow showRowImage showRowImage"><a href="(.+?)".+?<h4 class="showRow showRowName showRowText">(.+?)<', re.DOTALL).findall(r)

                for Myballs, Mycock in Yourmouth:
                    Myass = urlparse.urljoin(self.base_link, Myballs)
                    if cleantitle.getsearch(title).lower() == cleantitle.getsearch(Mycock).lower():

                        r = shell.get(Myass).content
                        year_data = re.compile('<div class="showValue showValueRelease">(.+?)</div>', re.DOTALL).findall(r)
                        if year in str(year_data):

                            links = re.compile('class="linkHidden linkHiddenUrl".+?>(.+?)</td>', re.DOTALL).findall(r)

                            for link in links:
                                if 'moviebyid' in link:
                                    continue
                                valid, host = source_utils.is_host_valid(link, hostDict)
                                sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('LosMovies - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
