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

from resources.lib.modules import cleantitle, client, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['cmovieshd.net']
        self.base_link = 'https://cmovieshd.net'
        self.search_link = '/search/?q=%s'


    '''
    Logic is not solid. Year is never presented until the actual page, so this must be checked in
    sources(). Not only that, should return a list of URLs in this case, to find the valid match
    but I am a lazy fuck and will do that later.
    '''
    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            cleaned_title = cleantitle.geturl(title).replace('-', '+')
            u = self.base_link + self.search_link % cleaned_title
            u = client.request(u)
            i = client.parseDOM(u, "div", attrs={"class": "movies-list"})
            for r in i:
                r = re.findall('<a href="(.+?)".+?title="(.+?)"', r, re.DOTALL)
                for url in r:
                    if title.lower() == url[1].lower():
                        return url[0]
                return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CMoviesHD - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            hostDict = hostDict + hostprDict

            timer = control.Time(start=True)

            url = url + 'watch/'
            r = client.request(url)
            qual = re.findall('class="quality">(.+?)<', r)


            for i in qual:
                quality, info = source_utils.get_release_quality(i, i)

            r = client.parseDOM(r, "div", attrs={"id": "list-eps"})
            for i in r:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('CMoviesHD - Timeout Reached')
                    break

                t = re.findall('href="(.+?)"', i, re.DOTALL)
                for url in t:
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('CMoviesHD - Timeout Reached')
                        break
                    t = client.request(url)
                    t = client.parseDOM(t, "div", attrs={"id": "content-embed"})

                    log_utils.log("url: " + str(url))
                    log_utils.log("t: " + str(t))
                    log_utils.log(str(qual))

                    for u in t:
                        i = re.findall('src="(.+?)"', u)[0].replace('load_player.html?e=', 'episode/embed/')
                        i = client.request(i).replace("\\", "")
                        u = re.findall('"(https.+?)"', i)
                        for url in u:
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if not valid:
                                continue
                            sources.append({'source': host, 'quality': quality, 'language': 'en',
                                            'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CMoviesHD - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
