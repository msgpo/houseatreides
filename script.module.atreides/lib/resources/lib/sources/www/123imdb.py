# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# As long as you retain this notice you can do whatever you want with
# this stuff. If we meet some day, and you think this stuff is worth it,
# you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

'''
2019/5/21: Since spacemov.cc has a captcha on the main page, we will now scrape
their sister site 123imdb. Also completely rewrote the script for better
accuracy
2019/07/17: Minor tweaks
'''

import re
import urlparse
import requests
import traceback

from resources.lib.modules import cleantitle, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['123imdb.to']
        self.base_link = 'https://123imdb.to'
        self.search_link = '/movie/%s-%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (title, year)))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('123IMDB - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostprDict + hostDict

            timer = control.Time(start=True)

            '''
            Sometimes this source url will have extra characters after /movie/%s-%s/.
            Site will automatically forward us to the correct page for the movie. So
            using title-year in the url string works everytime.
            '''
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            '''
            However we will need to capture that redirect before joining the end of
            the url.
            '''
            r = requests.get(url, headers=headers).url
            if r is None or r == self.base_link:
                '''
                Invalid info or movie not hosted by 123imdb (or site has wrong year like with Alita: Battle Angel)
                '''
                return sources
            url = urlparse.urljoin(r, 'watching/?ep=1')

            r = requests.get(url, headers=headers).content

            quality_scrape = re.compile('<span class="quality"><a href=.+?rel="tag">(.+?)</a>', re.DOTALL).findall(r)

            # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
            # We stop here even though no loop in case the request went too long
            if timer.elapsed() > sc_timeout:
                log_utils.log('123IMDB - Timeout Reached')
                return sources

            if 'HD' in quality_scrape:
                quality = '720p'
            elif 'CAM' in quality_scrape:
                quality = 'CAM'
            else:
                quality = 'SD'

            # We pull the only playable link
            try:
                movie_scrape = re.findall('<a title=.+?data-svv1="(.+?)"', r, re.DOTALL)[0]
            except Exception:
                return sources

            valid, host = source_utils.is_host_valid(movie_scrape, hostDict)
            if not valid:
                return sources
            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': movie_scrape, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('123IMDB - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url
