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
2019/07/18: Add back to Atreides and updated to work.
'''

import re
import traceback
import urlparse

from resources.lib.modules import cleantitle, client, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['cmovies.cc']
        self.base_link = 'https://cmovies.cc'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search_id.replace(':', ' ').replace(' ', '+'))
            search_results = client.request(url)
            match = re.findall('<span class="project-details"><a href="(.+?)">(.+?)</a>', search_results, re.DOTALL)
            for row_url, row_title in match:
                if cleantitle.get(title) in cleantitle.get(row_title):
                    if year in str(row_title):
                        return row_url
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CMovies - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            hostDict = hostDict + hostprDict

            timer = control.Time(start=True)

            html = client.request(url)
            links = re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(html)
            for link in links:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('CMovies - Timeout Reached')
                    break

                if not link.startswith('http'):
                    link = "https:" + link
                valid, host = source_utils.is_host_valid(link, hostDict)
                if not valid:
                    continue

                quality, info = source_utils.get_release_quality(link, link)
                sources.append({'source': host, 'quality': quality, 'language': 'en',
                                'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CMovies - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
