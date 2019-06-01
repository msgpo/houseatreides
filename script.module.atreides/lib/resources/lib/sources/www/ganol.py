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
2019/5/1: Initial import to Atreides. Initial scraper done by a friend, all credit to them
'''

import re
import traceback
import urllib
import urlparse
import requests

from resources.lib.modules import log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['ganol.si', 'ganool123.com']
        self.base_link = 'https://www2.ganool.ws'
        self.search_link = '/search/?q=%s'
        self.download_links = '/loadmoviedownloadsection.php'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Ganol - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        hostDict = hostprDict + hostDict
        try:
            if url is None:
                return
            urldata = urlparse.parse_qs(url)
            urldata = dict((i, urldata[i][0]) for i in urldata)
            title = urldata['title']
            year = urldata['year']

            search = title.lower()
            url = urlparse.urljoin(self.base_link, self.search_link % (search.replace(' ', '+')))
            shell = requests.Session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            Digital = shell.get(url, headers=headers).content

            BlackFlag = re.compile(
                'data-movie-id="" class="ml-item".+?href="(.+?)" class="ml-mask jt".+?<div class="moviename">(.+?)</div>',
                re.DOTALL).findall(Digital)
            for Digibox, Powder in BlackFlag:
                if title.lower() in Powder.lower():
                    if year in str(Powder):
                        r = shell.get(Digibox, headers=headers).content
                        quality_bitches = re.compile(
                            '<strong>Quality:</strong>\s+<a href=.+?>(.+?)</a>', re.DOTALL).findall(r)

                        for url in quality_bitches:
                            if '1080' in url:
                                quality = '1080p'
                            elif '720' in url:
                                quality = '720p'
                            elif 'cam' in url:
                                quality = 'SD'
                            else:
                                quality = 'SD'

                        key = re.compile("var randomKeyNo = '(.+?)'", re.DOTALL).findall(r)
                        post_link = urlparse.urljoin(self.base_link, self.download_links)
                        payload = {'key': key}
                        suck_it = shell.post(post_link, headers=headers, data=payload)
                        response = suck_it.content

                        grab = re.compile('<a rel="\w+" href="(.+?)">\w{5}\s\w+\s\w+\s\w+\s\w{5}<\/a>', re.DOTALL).findall(response)
                        for links in grab:
                            r = shell.get(links, headers=headers).content
                            links = re.compile('<a rel="\w+" href="(.+?)" target="\w+">', re.DOTALL).findall(r)

                        for link in links:
                            valid, host = source_utils.is_host_valid(link, hostDict)
                            # openload links seem to be .rar files. the following is needed so they wont be included
                            if 'rar' in link:
                                continue
                            sources.append({'source': host, 'quality': quality, 'language': 'en',
                                            'url': link, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Ganol - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
