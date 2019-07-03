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

from resources.lib.modules import cleantitle, control, source_utils, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['goldmovies.xyz']
        self.base_link = 'http://goldmovies.xyz'
        self.search_link = '/?s=%s'
        self.postlink = 'https://tinyurl.com/gold-post'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoldMovies - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoldMovies - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoldMovies - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = '%s Season %d Episode %d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))if 'tvshowtitle' in data else '%s' % (data['title'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            year = data['year']
            kcus_snwolc = cleantitle.getsearch(query.lower())
            url = urlparse.urljoin(self.base_link, self.search_link % (kcus_snwolc.replace(' ', '+')))

            timer = control.Time(start=True)

            shell = requests.Session()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            r = shell.get(url, headers=headers).content

            scrape = re.compile('<div data-movie-id=.+?class="ml-item">\s+<a href="(.+?)" data-url="" class="ml-mask jt".+?oldtitle="(.+?)"').findall(r)

            for url, title_data in scrape:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('GoldMovies - Timeout Reached')
                    break

                if cleantitle.getsearch(query).lower() == cleantitle.getsearch(title_data).lower():
                    r = shell.get(url, headers=headers).content
                    year_data = re.compile('<strong>Release:\s+</strong>\s+<a href=.+?rel="tag">(.+?)</a>').findall(r)
                    if year in str(year_data):
                        if 'tvshowtitle' in data:
                            year is None

                    regex_a_bitch = re.compile('<input type="hidden" id="link" name="link" value="(.+?)"').findall(r)
                    for url in regex_a_bitch:
                        post_link = 'http://instalyser.com/form3.php'
                        payload = {'title': url, 'submit': 'Download'}
                        post_it = shell.post(post_link, headers=headers, data=payload)
                        response = post_it.content

                        gold_links = re.findall(r'<[^\d]\s\w+\=\"(.+?)\"\s[^\d]{6}\=\"\w{6}\">', response)
                        for url in gold_links:
                            quality, info = source_utils.get_release_quality(url, url)
                            sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': True, 'debridonly': False})

                return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoldMovies - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
