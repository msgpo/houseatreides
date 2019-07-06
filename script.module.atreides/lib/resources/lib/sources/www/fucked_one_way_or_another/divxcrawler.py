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


import re
import traceback
import urllib
import urlparse

from resources.lib.modules import client, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['divxcrawler.club']
        self.base_link = 'http://www.divxcrawler.club'
        self.search_link = '/latest.htm'
        self.search_link2 = '/streaming.htm'
        self.search_link3 = '/movies.htm'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DivxCrawler - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            imdb = data['imdb']

            link = ''

            try:
                query = urlparse.urljoin(self.base_link, self.search_link)
                result = client.request(query)
                m = re.findall('Movie Size:(.+?)<.+?href="(.+?)".+?href="(.+?)"\s*onMouse', result, re.DOTALL)
                m = [(i[0], i[1], i[2]) for i in m if imdb in i[1]]
                if m:
                    link = m
                else:
                    query = urlparse.urljoin(self.base_link, self.search_link2)

                    timer = control.Time(start=True)

                    result = client.request(query)
                    m = re.findall('Movie Size:(.+?)<.+?href="(.+?)".+?href="(.+?)"\s*onMouse', result, re.DOTALL)
                    m = [(i[0], i[1], i[2]) for i in m if imdb in i[1]]
                    if m:
                        link = m
                    else:
                        query = urlparse.urljoin(self.base_link, self.search_link3)
                        result = client.request(query)
                        m = re.findall('Movie Size:(.+?)<.+?href="(.+?)".+?href="(.+?)"\s*onMouse', result, re.DOTALL)
                        m = [(i[0], i[1], i[2]) for i in m if imdb in i[1]]
                        if m:
                            link = m
            except Exception:
                return

            if link == '':
                return sources

            for item in link:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('DivxCrawler - Timeout Reached')
                    break

                try:
                    quality, info = source_utils.get_release_quality(item[2], None)
                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', item[0])[-1]
                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                        size = '%.2f GB' % size
                        info.append(size)
                    except Exception:
                        pass
                    info = ' | '.join(info)
                    url = item[2]
                    if any(x in url for x in ['.rar', '.zip', '.iso']):
                        raise Exception()
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                    'direct': True, 'debridonly': False})
                except Exception:
                    pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DivxCrawler - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
