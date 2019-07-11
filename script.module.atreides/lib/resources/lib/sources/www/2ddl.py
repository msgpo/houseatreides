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
2019/04/15: Domain name change/update
2019/07/05: Rewrite due to site changes
2019/07/06: Note to self - I fucked size checks and need to rewrite it but too lazy to right now
'''

import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cfscrape, cleantitle, client, control, debrid, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['2ddl.ws']
        self.base_link = 'https://2ddl.vg'
        self.search_link = '/search/%s/feed/rss2/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = title.replace('\'', '').replace(',', '').replace('-', '').replace(':', '')
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('2DDL - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = tvshowtitle.replace('\'', '').replace(',', '').replace('-', '').replace(':', '')
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('2DDL - Exception: \n' + str(failure))
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
            log_utils.log('2DDL - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            scraper = cfscrape.create_scraper()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
                data['tvshowtitle'],
                int(data['season']),
                int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
                data['title'],
                data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            timer = control.Time(start=True)

            html = scraper.get(url).content
            posts = client.parseDOM(html, 'item')

            items = []

            for post in posts:
                try:
                    t = re.findall('<title>(.+?)</title>', post, re.IGNORECASE)[0]
                    u = re.findall('<link>(.+?)</link>', post, re.IGNORECASE)[0]
                    # "Quick" check to reduce invalid results
                    if data['year'] in t:
                        items += [(t, u)]
                except Exception:
                    pass

            for item in items:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('2DDL - Timeout Reached')
                    break

                try:
                    if cleantitle.query(title).lower() not in item[0].lower():
                        continue

                    url = item[1]
                    html = scraper.get(url).content

                    try:
                        link_areas = client.parseDOM(html, 'div', attrs={'class': 'multilink_lnks'})
                        for area in link_areas:
                            link_boxes = re.findall('<div class="anch_multilink">(.+?)</div>', area, re.DOTALL)
                            for link_section in link_boxes:
                                try:
                                    url = re.findall('href="(.+?)"', link_section, re.DOTALL)[0]
                                    url = client.replaceHTMLCodes(url)
                                    url = url.encode('utf-8')
                                    valid, host = source_utils.is_host_valid(url, hostDict)
                                    if not valid:
                                        continue

                                    name = item[0]
                                    name = client.replaceHTMLCodes(name)

                                    # t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name, flags=re.I)

                                    if not cleantitle.get(title) in cleantitle.get(name):
                                        continue

                                    y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', name)[-1].upper()

                                    if not y == hdlr:
                                        continue

                                    quality, info = source_utils.get_release_quality(name, url)

                                    try:
                                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', item[2])[-1]
                                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                                        size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                                        size = '%.2f GB' % size
                                        info.append(size)
                                    except Exception:
                                        pass

                                    info = ' | '.join(info)
                                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                                    'direct': False, 'debridonly': debrid.status()})
                                except Exception:
                                    log_utils.log('2DDL - Fuckup in Download Area')
                                    continue
                    except Exception:
                        # No section found, report to debugger and quit working this one
                        log_utils.log('2DDL - Download Area not found')
                        continue
                except Exception:
                    pass

            check = [i for i in sources if not i['quality'] == 'CAM']
            if check:
                sources = check

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('2DDL - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
