# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides


import json
import re
import time
import urllib
import urlparse

from resources.lib.modules import cache
from resources.lib.modules import cleandate
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils
from resources.lib.modules import utils

BASE_URL = 'http://api.trakt.tv'
V2_API_KEY = '7a422607d83d5efb71f30b1f8a2be8ed730795cd337ec1177891ca4085d007d2'
CLIENT_SECRET = '78b43ad3c3b1a7907c39b37fa12482733248d08f71bb63a5b35fe101916d5293'
REDIRECT_URI = 'http://www.tantrumtv.com'


def __getTrakt(url, post=None):
    try:
        url = urlparse.urljoin(BASE_URL, url)
        post = json.dumps(post) if post else None
        headers = {'Content-Type': 'application/json', 'trakt-api-key': V2_API_KEY, 'trakt-api-version': 2}

        if getTraktCredentialsInfo():
            headers.update({'Authorization': 'Bearer %s' % control.setting('trakt.token')})

        result = client.request(url, post=post, headers=headers, output='extended', error=True)

        resp_code = result[1]
        resp_header = result[2]
        result = result[0]

        if resp_code in ['500', '502', '503', '504', '520', '521', '522', '524']:
            log_utils.log('Temporary Trakt Error: %s' % resp_code, log_utils.LOGWARNING)
            return
        elif resp_code in ['404']:
            log_utils.log('Object Not Found : %s' % resp_code, log_utils.LOGWARNING)
            return
#        elif resp_code in ['429']:
#            log_utils.log('Trakt Rate Limit Reached: %s' % resp_code, log_utils.LOGWARNING)
#            return

        if resp_code not in ['401', '405']:
            return result, resp_header

        oauth = urlparse.urljoin(BASE_URL, '/oauth/token')
        opost = {'client_id': V2_API_KEY, 'client_secret': CLIENT_SECRET, 'redirect_uri': REDIRECT_URI,
                 'grant_type': 'refresh_token', 'refresh_token': control.setting('trakt.refresh')}

        result = client.request(oauth, post=json.dumps(opost), headers=headers)
        result = utils.json_loads_as_str(result)

        token, refresh = result['access_token'], result['refresh_token']

        control.setSetting(id='trakt.token', value=token)
        control.setSetting(id='trakt.refresh', value=refresh)

        headers['Authorization'] = 'Bearer %s' % token

        result = client.request(url, post=post, headers=headers, output='extended', error=True)
        return result[0], result[2]
    except Exception as e:
        log_utils.log('Unknown Trakt Error: %s' % e, log_utils.LOGWARNING)
        pass


def getTraktAsJson(url, post=None):
    try:
        r, res_headers = __getTrakt(url, post)
        r = utils.json_loads_as_str(r)
        if 'X-Sort-By' in res_headers and 'X-Sort-How' in res_headers:
            r = sort_list(res_headers['X-Sort-By'], res_headers['X-Sort-How'], r)
        return r
    except Exception:
        pass


def authTrakt():
    try:
        if getTraktCredentialsInfo() is True:
            if control.yesnoDialog(
                    control.lang(32511).encode('utf-8'),
                    control.lang(32512).encode('utf-8'),
                    '', 'Trakt'):
                control.setSetting(id='trakt.user', value='')
                control.setSetting(id='trakt.token', value='')
                control.setSetting(id='trakt.refresh', value='')
            raise Exception()

        result = getTraktAsJson('/oauth/device/code', {'client_id': V2_API_KEY})
        verification_url = (control.lang(32513) % result['verification_url']).encode('utf-8')
        user_code = (control.lang(32514) % result['user_code']).encode('utf-8')
        expires_in = int(result['expires_in'])
        device_code = result['device_code']
        interval = result['interval']

        progressDialog = control.progressDialog
        progressDialog.create('Trakt', verification_url, user_code)

        for i in range(0, expires_in):
            try:
                if progressDialog.iscanceled():
                    break
                time.sleep(1)
                if not float(i) % interval == 0:
                    raise Exception()
                r = getTraktAsJson(
                    '/oauth/device/token',
                    {'client_id': V2_API_KEY, 'client_secret': CLIENT_SECRET, 'code': device_code})
                if 'access_token' in r:
                    break
            except Exception:
                pass

        try:
            progressDialog.close()
        except Exception:
            pass

        token, refresh = r['access_token'], r['refresh_token']

        headers = {'Content-Type': 'application/json', 'trakt-api-key': V2_API_KEY,
                   'trakt-api-version': 2, 'Authorization': 'Bearer %s' % token}

        result = client.request(urlparse.urljoin(BASE_URL, '/users/me'), headers=headers)
        result = utils.json_loads_as_str(result)

        user = result['username']

        control.setSetting(id='trakt.user', value=user)
        control.setSetting(id='trakt.token', value=token)
        control.setSetting(id='trakt.refresh', value=refresh)
        raise Exception()
    except Exception:
        control.openSettings('3.1')


def getTraktCredentialsInfo():
    user = control.setting('trakt.user').strip()
    token = control.setting('trakt.token')
    refresh = control.setting('trakt.refresh')
    if (user == '' or token == '' or refresh == ''):
        return False
    return True


def getTraktIndicatorsInfo():
    indicators = control.setting('indicators') if getTraktCredentialsInfo(
    ) is False else control.setting('indicators.alt')
    indicators = True if indicators == '1' else False
    return indicators


def getTraktAddonMovieInfo():
    try:
        scrobble = control.addon('script.trakt').getSetting('scrobble_movie')
    except Exception:
        scrobble = ''
    try:
        ExcludeHTTP = control.addon('script.trakt').getSetting('ExcludeHTTP')
    except Exception:
        ExcludeHTTP = ''
    try:
        authorization = control.addon('script.trakt').getSetting('authorization')
    except Exception:
        authorization = ''
    if scrobble == 'true' and ExcludeHTTP == 'false' and not authorization == '':
        return True
    else:
        return False


def getTraktAddonEpisodeInfo():
    try:
        scrobble = control.addon('script.trakt').getSetting('scrobble_episode')
    except Exception:
        scrobble = ''
    try:
        ExcludeHTTP = control.addon('script.trakt').getSetting('ExcludeHTTP')
    except Exception:
        ExcludeHTTP = ''
    try:
        authorization = control.addon('script.trakt').getSetting('authorization')
    except Exception:
        authorization = ''
    if scrobble == 'true' and ExcludeHTTP == 'false' and not authorization == '':
        return True
    else:
        return False


def manager(name, imdb, tvdb, content):
    try:
        post = {"movies": [{"ids": {"imdb": imdb}}]} if content == 'movie' else {"shows": [{"ids": {"tvdb": tvdb}}]}

        items = [(control.lang(32516).encode('utf-8'), '/sync/collection')]
        items += [(control.lang(32517).encode('utf-8'), '/sync/collection/remove')]
        items += [(control.lang(32518).encode('utf-8'), '/sync/watchlist')]
        items += [(control.lang(32519).encode('utf-8'), '/sync/watchlist/remove')]
        items += [(control.lang(32520).encode('utf-8'), '/users/me/lists/%s/items')]

        result = getTraktAsJson('/users/me/lists')
        lists = [(i['name'], i['ids']['slug']) for i in result]
        lists = [lists[i//2] for i in range(len(lists)*2)]
        for i in range(0, len(lists), 2):
            lists[i] = ((control.lang(32521) % lists[i][0]).encode('utf-8'), '/users/me/lists/%s/items' % lists[i][1])
        for i in range(1, len(lists), 2):
            lists[i] = ((control.lang(32522) % lists[i][0]).encode('utf-8'),
                        '/users/me/lists/%s/items/remove' % lists[i][1])
        items += lists

        select = control.selectDialog([i[0] for i in items], control.lang(32515).encode('utf-8'))

        if select == -1:
            return
        elif select == 4:
            t = control.lang(32520).encode('utf-8')
            k = control.keyboard('', t)
            k.doModal()
            new = k.getText() if k.isConfirmed() else None
            if (new is None or new == ''):
                return
            result = __getTrakt('/users/me/lists', post={"name": new, "privacy": "private"})[0]

            try:
                slug = utils.json_loads_as_str(result)['ids']['slug']
            except Exception:
                return control.infoDialog(
                    control.lang(32515).encode('utf-8'),
                    heading=str(name),
                    sound=True, icon='ERROR')
            result = __getTrakt(items[select][1] % slug, post=post)[0]
        else:
            result = __getTrakt(items[select][1], post=post)[0]

        icon = control.infoLabel('ListItem.Icon') if result is not None else 'ERROR'

        control.infoDialog(control.lang(32515).encode('utf-8'), heading=str(name), sound=True, icon=icon)
    except Exception:
        return


def slug(name):
    name = name.strip()
    name = name.lower()
    name = re.sub('[^a-z0-9_]', '-', name)
    name = re.sub('--+', '-', name)
    return name


def sort_list(sort_key, sort_direction, list_data):
    reverse = False if sort_direction == 'asc' else True
    if sort_key == 'rank':
        return sorted(list_data, key=lambda x: x['rank'], reverse=reverse)
    elif sort_key == 'added':
        return sorted(list_data, key=lambda x: x['listed_at'], reverse=reverse)
    elif sort_key == 'title':
        return sorted(list_data, key=lambda x: utils.title_key(x[x['type']].get('title')), reverse=reverse)
    elif sort_key == 'released':
        return sorted(list_data, key=lambda x: _released_key(x[x['type']]), reverse=reverse)
    elif sort_key == 'runtime':
        return sorted(list_data, key=lambda x: x[x['type']].get('runtime', 0), reverse=reverse)
    elif sort_key == 'popularity':
        return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
    elif sort_key == 'percentage':
        return sorted(list_data, key=lambda x: x[x['type']].get('rating', 0), reverse=reverse)
    elif sort_key == 'votes':
        return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
    else:
        return list_data


def _released_key(item):
    if 'released' in item:
        return item['released']
    elif 'first_aired' in item:
        return item['first_aired']
    else:
        return 0


def getActivity():
    try:
        i = getTraktAsJson('/sync/last_activities')

        activity = []
        activity.append(i['movies']['collected_at'])
        activity.append(i['episodes']['collected_at'])
        activity.append(i['movies']['watchlisted_at'])
        activity.append(i['shows']['watchlisted_at'])
        activity.append(i['seasons']['watchlisted_at'])
        activity.append(i['episodes']['watchlisted_at'])
        activity.append(i['lists']['updated_at'])
        activity.append(i['lists']['liked_at'])
        activity = [int(cleandate.iso_2_utc(i)) for i in activity]
        activity = sorted(activity, key=int)[-1]

        return activity
    except Exception:
        pass


def getWatchedActivity():
    try:
        i = getTraktAsJson('/sync/last_activities')

        activity = []
        activity.append(i['movies']['watched_at'])
        activity.append(i['episodes']['watched_at'])
        activity = [int(cleandate.iso_2_utc(i)) for i in activity]
        activity = sorted(activity, key=int)[-1]

        return activity
    except Exception:
        pass


def cachesyncMovies(timeout=0):
    indicators = cache.get(syncMovies, timeout, control.setting('trakt.user').strip())
    return indicators


def timeoutsyncMovies():
    timeout = cache.timeout(syncMovies, control.setting('trakt.user').strip())
    return timeout


def syncMovies(user):
    try:
        if getTraktCredentialsInfo() is False:
            return
        indicators = getTraktAsJson('/users/me/watched/movies')
        indicators = [i['movie']['ids'] for i in indicators]
        indicators = [str(i['imdb']) for i in indicators if 'imdb' in i]
        return indicators
    except Exception:
        pass


def cachesyncTVShows(timeout=0):
    indicators = cache.get(syncTVShows, timeout, control.setting('trakt.user').strip())
    return indicators


def timeoutsyncTVShows():
    timeout = cache.timeout(syncTVShows, control.setting('trakt.user').strip())
    return timeout


def syncTVShows(user):
    try:
        if getTraktCredentialsInfo() is False:
            return
        indicators = getTraktAsJson('/users/me/watched/shows?extended=full')
        indicators = [(i['show']['ids']['tvdb'], i['show']['aired_episodes'], sum(
            [[(s['number'], e['number']) for e in s['episodes']] for s in i['seasons']], [])) for i in indicators]
        indicators = [(str(i[0]), int(i[1]), i[2]) for i in indicators]
        return indicators
    except Exception:
        pass


def syncSeason(imdb):
    try:
        if getTraktCredentialsInfo() is False:
            return
        indicators = getTraktAsJson('/shows/%s/progress/watched?specials=false&hidden=false' % imdb)
        indicators = indicators['seasons']
        indicators = [(i['number'], [x['completed'] for x in i['episodes']]) for i in indicators]
        indicators = ['%01d' % int(i[0]) for i in indicators if False not in i[1]]
        return indicators
    except Exception:
        pass


def markMovieAsWatched(imdb):
    if not imdb.startswith('tt'):
        imdb = 'tt' + imdb
    return __getTrakt('/sync/history', {"movies": [{"ids": {"imdb": imdb}}]})[0]


def markMovieAsNotWatched(imdb):
    if not imdb.startswith('tt'):
        imdb = 'tt' + imdb
    return __getTrakt('/sync/history/remove', {"movies": [{"ids": {"imdb": imdb}}]})[0]


def markTVShowAsWatched(tvdb):
    return __getTrakt('/sync/history', {"shows": [{"ids": {"tvdb": tvdb}}]})[0]


def markTVShowAsNotWatched(tvdb):
    return __getTrakt('/sync/history/remove', {"shows": [{"ids": {"tvdb": tvdb}}]})[0]


def markEpisodeAsWatched(tvdb, season, episode):
    season, episode = int('%01d' % int(season)), int('%01d' % int(episode))
    return __getTrakt(
        '/sync/history',
        {"shows": [{"seasons": [{"episodes": [{"number": episode}],
                                 "number": season}],
                    "ids": {"tvdb": tvdb}}]})[0]


def markEpisodeAsNotWatched(tvdb, season, episode):
    season, episode = int('%01d' % int(season)), int('%01d' % int(episode))
    return __getTrakt(
        '/sync/history/remove',
        {"shows": [{"seasons": [{"episodes": [{"number": episode}],
                                 "number": season}],
                    "ids": {"tvdb": tvdb}}]})[0]


def getMovieTranslation(id, lang, full=False):
    url = '/movies/%s/translations/%s' % (id, lang)
    try:
        item = getTraktAsJson(url)[0]
        return item if full else item.get('title')
    except Exception:
        pass


def getTVShowTranslation(id, lang, season=None, episode=None, full=False):
    if season and episode:
        url = '/shows/%s/seasons/%s/episodes/%s/translations/%s' % (id, season, episode, lang)
    else:
        url = '/shows/%s/translations/%s' % (id, lang)

    try:
        item = getTraktAsJson(url)[0]
        return item if full else item.get('title')
    except Exception:
        pass


def getMovieAliases(id):
    try:
        return getTraktAsJson('/movies/%s/aliases' % id)
    except Exception:
        return []


def getTVShowAliases(id):
    try:
        return getTraktAsJson('/shows/%s/aliases' % id)
    except Exception:
        return []


def getMovieSummary(id, full=True):
    try:
        url = '/movies/%s' % id
        if full:
            url += '?extended=full'
        return getTraktAsJson(url)
    except Exception:
        return


def getTVShowSummary(id, full=True):
    try:
        url = '/shows/%s' % id
        if full:
            url += '?extended=full'
        return getTraktAsJson(url)
    except Exception:
        return


def getPeople(id, content_type, full=True):
    try:
        url = '/%s/%s/people' % (content_type, id)
        if full:
            url += '?extended=full'
        return getTraktAsJson(url)
    except Exception:
        return


def SearchAll(title, year, full=True):
    try:
        return SearchMovie(title, year, full) + SearchTVShow(title, year, full)
    except Exception:
        return


def SearchMovie(title, year, full=True):
    try:
        url = '/search/movie?query=%s' % urllib.quote_plus(title)

        if year:
            url += '&year=%s' % year
        if full:
            url += '&extended=full'
        return getTraktAsJson(url)
    except Exception:
        return


def SearchTVShow(title, year, full=True):
    try:
        url = '/search/show?query=%s' % urllib.quote_plus(title)

        if year:
            url += '&year=%s' % year
        if full:
            url += '&extended=full'
        return getTraktAsJson(url)
    except Exception:
        return


def IdLookup(content, type, type_id):
    try:
        r = getTraktAsJson('/search/%s/%s?type=%s' % (type, type_id, content))
        return r[0].get(content, {}).get('ids', [])
    except Exception:
        return {}


def getGenre(content, type, type_id):
    try:
        r = '/search/%s/%s?type=%s&extended=full' % (type, type_id, content)
        r = getTraktAsJson(r)
        r = r[0].get(content, {}).get('genres', [])
        return r
    except Exception:
        return []
