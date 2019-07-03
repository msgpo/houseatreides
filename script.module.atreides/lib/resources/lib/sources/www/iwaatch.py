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
import urllib
import urlparse
import requests
import traceback

from resources.lib.modules import cleantitle, control, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['iwaatch.com']
        self.base_link = 'https://iwaatch.com'
        self.search_link = '/?q=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('iWAATCH - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title']
            year = data['year']

            search_id = cleantitle.getsearch(title.lower())
            url = urlparse.urljoin(self.base_link, self.search_link % (search_id.replace(' ', '+')))
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                'Accept': '*/*',
                'Accept-Encoding': 'identity;q=1, *;q=0',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'DNT': '1'
            }

            timer = control.Time(start=True)

            shell = requests.Session()
            r = shell.get(url, headers=headers).content
            movie_scrape = re.compile('<h2 class="h2 p-title.+?a href="(.+?)".+?div class="post-title">(.+?)<', re.DOTALL).findall(r)

            for movie_url, movie_title in movie_scrape:
                 # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('IWaatch - Timeout Reached')
                    break

                if cleantitle.getsearch(title).lower() == cleantitle.getsearch(movie_title).lower():

                    r = shell.get(movie_url, headers=headers).content
                    year_data = re.compile('<h2 style="margin-bottom: 0">(.+?)</h2>', re.DOTALL).findall(r)
                    if year in str(year_data):
                        links = re.findall(r"<a href='(.+?)'>(\d+)p<\/a>", r)

                        for link, quality in links:

                            if '1080' in quality:
                                quality = '1080p'
                            elif '720' in quality:
                                quality = '720p'
                            elif '480' in quality:
                                quality = 'SD'
                            else:
                                quality = 'SD'

                            sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': link+'|Referer=https://iwaatch.com/movie/' + title, 'direct': True, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('iWAATCH - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
