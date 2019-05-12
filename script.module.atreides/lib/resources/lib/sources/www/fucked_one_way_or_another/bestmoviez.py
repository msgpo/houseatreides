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

import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cfscrape, client, debrid, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['best-moviez.ws']
        self.base_link = 'http://www.best-moviez.ws'
        self.search_link = '/%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('BestMoviez - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('BestMoviez - Exception: \n' + str(failure))
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
            log_utils.log('BestMoviez - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            # title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            # hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s s%02de%02d' % (
                data['tvshowtitle'],
                int(data['season']),
                int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
                data['title'],
                data['year'])
            query = re.sub('[\\\\:;*?"<>|/ \+\']+', '-', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            r = self.scraper.get(url).content

            r = client.parseDOM(r, "div", attrs={'class': 'entry-content'})[0]
            r = re.sub('shareaholic-canvas.+', '', r, flags=re.DOTALL)

            a_txt = ''
            a_url = ''
            a_txt = client.parseDOM(r, "a", attrs={'href': '.+?'})
            a_url = client.parseDOM(r, "a", ret="href")
            r = re.sub('<a .+?</a>', '', r, flags=re.DOTALL)
            r = re.sub('<img .+?>', '', r, flags=re.DOTALL)

            size = ''
            pre_txt = []
            pre_url = []
            pres = client.parseDOM(r, "pre", attrs={'style': '.+?'})
            for pre in pres:
                try:
                    size = re.findall('([0-9,\.]+ ?(?:GB|GiB|MB|MiB))', pre)[0]
                except Exception:
                    pass

                url0 = re.findall('https?://[^ <"\'\s]+', pre, re.DOTALL)
                txt0 = [size] * len(url0)
                pre_url = pre_url + url0
                pre_txt = pre_txt + txt0

            r = re.sub('<pre .+?</pre>', '', r, flags=re.DOTALL)

            size = ''
            if 'tvshowtitle' not in data:
                try:
                    size = " " + re.findall('([0-9,\.]+ ?(?:GB|GiB|MB|MiB))', r)[0]
                except Exception:
                    pass

            raw_url = re.findall('https?://[^ <"\'\s]+', r, re.DOTALL)
            raw_txt = [size] * len(raw_url)

            pairs = zip(a_url+pre_url+raw_url, a_txt+pre_txt+raw_txt)

            for pair in pairs:
                try:
                    url = str(pair[0])
                    info = re.sub('<.+?>', '', pair[1])

                    if any(x in url for x in ['.rar', '.zip', '.iso']):
                        raise Exception()
                    if not query.lower() in re.sub('[\\\\:;*?"<>|/ \+\'\.]+', '-', url+info).lower():
                        raise Exception()

                    size0 = info + " " + size

                    try:
                        size0 = re.findall('([0-9,\.]+ ?(?:GB|GiB|MB|MiB))', size0)[0]
                        div = 1 if size0.endswith(('GB', 'GiB')) else 1024
                        size0 = float(re.sub('[^0-9\.]', '', size0)) / div
                        size0 = '%.2f GB' % size0
                    except Exception:
                        size0 = ''
                        pass

                    quality, info = source_utils.get_release_quality(url, info)
                    info.append(size0)
                    info = ' | '.join(info)

                    url = url.encode('utf-8')
                    hostDict = hostDict + hostprDict

                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if not valid:
                        continue
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url,
                                    'info': info, 'direct': False, 'debridonly': debrid.status()})

                except Exception:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('BestMoviez - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url