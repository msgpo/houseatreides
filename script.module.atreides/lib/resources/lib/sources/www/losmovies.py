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
2019/5/12: Work done by SC, added today
'''

import re
import traceback
import urlparse

from resources.lib.modules import cleantitle, client, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['losmovies.sh']
        self.base_link = 'http://losmovies.pro'
        self.search_link = '/movies-found?type=movies&q=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search.replace(':', ' ').replace(' ', '+'))
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            r = client.request(url, headers=headers)
            Yourmouth = re.compile('class="showRow showRowImage showRowImage"><a href="(.+?)".+?<h4 class="showRow showRowName showRowText">(.+?)<', re.DOTALL).findall(r)
            for Myballs, Mycock in Yourmouth:
                Myass = self.base_link + Myballs
                if cleantitle.get(title) in cleantitle.get(Mycock):
                    return Myass
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('LOSMovies - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources

            hostDict = hostprDict + hostDict
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

            r = client.request(url, headers=headers)
            links = re.compile('class="linkHidden linkHiddenUrl".+?>(.+?)</td>', re.DOTALL).findall(r)

            for link in links:
                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].split('.')[0].title()
                valid, host = source_utils.is_host_valid(link, hostDict)
                sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('LOSMovies - Exception: \n' + str(failure))
            return sources
        return sources

    def resolve(self, url):
        return url
