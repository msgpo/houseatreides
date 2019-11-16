# -*- coding: utf-8 -*-

'''
    Marauder Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import os
import sys
import urlparse

from resources.lib.modules import cache, control, trakt

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])

artPath = control.artPath()
addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
    def root(self):
        self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('navi.imdbtop') is True:
            self.addDirectoryItem('IMDB Top 250', 'imdbtop250', 'imdb.png', 'Defaultmovies.png')

        if self.getMenuEnabled('navi.moviechest') is True:
            self.addDirectoryItem('The Movie Chest', 'moviechest', 'chest.png', 'Defaultmovies.png')
        if self.getMenuEnabled('navi.hack') is True:
            self.addDirectoryItem('Hack The Planet', 'movies&url=hacktheplanet', 'hack.png', 'playlist.jpg')

        if self.getMenuEnabled('navi.boxsets') is True:
            self.addDirectoryItem('Boxsets', 'boxsetNavigator', 'boxsets.png', 'DefaultBoxSets.png')

        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

        if not control.setting('movie.widget') == '0':
            self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem(32006, 'tvWidget', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png')

        if self.getMenuEnabled('navi.channels') is True:
            self.addDirectoryItem(32007, 'channels', 'channels.png', 'DefaultMovies.png')
        if not control.setting('furk.api') == '':
            self.addDirectoryItem('Furk.net', 'furkNavigator', 'movies.png', 'movies.png')
        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')

        downloads = True if control.setting('downloads') == 'true' and(
            len(control.listDir(control.setting('movie.download.path'))[0]) > 0
            or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultFolder.png')

        self.endDirectory()

    def furk(self):
        self.addDirectoryItem('User Files', 'furkUserFiles', 'mytvnavigator.png', 'mytvnavigator.png')
        self.addDirectoryItem('Search', 'furkSearch', 'search.png', 'search.png')
        self.endDirectory(category='Furk')

    def movies(self, lite=False):
        if self.getMenuEnabled('navi.movietheaters') is True:
            self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.movietrending') is True:
            self.addDirectoryItem(32017, 'movies&url=trending', 'people-watching.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.moviepopular') is True:
            self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieviews') is True:
            self.addDirectoryItem(32019, 'movies&url=views', 'most-voted.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieboxoffice') is True:
            self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieoscars') is True:
            self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.ccollect') is True:
            self.addDirectoryItem('Collections', 'movieCollections', 'collections.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviemosts') is True:
            self.addDirectoryItem('Movie Mosts', 'movieMosts', 'featured.png', 'playlist.jpg')
        if self.getMenuEnabled('navi.moviegenre') is True:
            self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieyears') is True:
            self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviepersons') is True:
            self.addDirectoryItem(32013, 'moviePersons', 'people.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movielanguages') is True:
            self.addDirectoryItem(32014, 'movieLanguages', 'languages.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviecerts') is True:
            self.addDirectoryItem(32015, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory(category=control.lang(32001).encode('utf-8'))

    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32094, 'movies&url=onDeck', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32094, 'movies&url=onDeck', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32077, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory(category=control.lang(32003).encode('utf-8'))

    def tvshows(self, lite=False):
        if self.getMenuEnabled('navi.tvGenres') is True:
            self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvNetworks') is True:
            self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvLanguages') is True:
            self.addDirectoryItem(32014, 'tvLanguages', 'languages.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvCerts') is True:
            self.addDirectoryItem(32015, 'tvCertificates', 'certificates.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvTrending') is True:
            self.addDirectoryItem(32017, 'tvshows&url=trending', 'people-watching.png', 'DefaultRecentlyAddedEpisodes.png')
        if self.getMenuEnabled('navi.tvPopular') is True:
            self.addDirectoryItem(32018, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvRating') is True:
            self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvViews') is True:
            self.addDirectoryItem(32019, 'tvshows&url=views', 'most-voted.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvMosts') is True:
            self.addDirectoryItem('TV Show Mosts', 'showMosts', 'featured.png', 'playlist.jpg')
        if self.getMenuEnabled('navi.tvAiring') is True:
            self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvPremier') is True:
            self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvActive') is True:
            self.addDirectoryItem(32006, 'calendar&url=added', 'latest-episodes.png',
                                  'DefaultRecentlyAddedEpisodes.png', queue=True)
        if self.getMenuEnabled('navi.tvCalendar') is True:
            self.addDirectoryItem(32027, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory(category=control.lang(32002).encode('utf-8'))

    def mytvshows(self, lite=False):
        try:
            self.accountCheck()

            if traktCredentials == True and imdbCredentials == True:

                self.addDirectoryItem(32094, 'calendar&url=onDeck', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(
                    32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png',
                    context=(32551, 'tvshowsToLibrary&url=traktcollection'))
                self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
                self.addDirectoryItem(
                    32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png',
                    context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
                self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png',
                                      'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png',
                                      'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

            elif traktCredentials == True:
                self.addDirectoryItem(32094, 'calendar&url=onDeck', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(
                    32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png',
                    context=(32551, 'tvshowsToLibrary&url=traktcollection'))
                self.addDirectoryItem(
                    32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png',
                    context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
                self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png',
                                      'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png',
                                      'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

            elif imdbCredentials == True:
                self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32077, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

            self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')

            if lite == False:
                self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

            self.endDirectory(category=control.lang(32004).encode('utf-8'))
        except:
            print("ERROR")

    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'):
            return False
        return True

    def moviechest(self):
        self.addDirectoryItem('Films that are mostly taking place in one room',
                              'movies&url=imdb1', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies Based On True Story', 'movies&url=imdb2', 'chest.png', 'chest.png')
        self.addDirectoryItem('Best Movies Set in the 60s', 'movies&url=imdb3', 'chest.png', 'chest.png')
        self.addDirectoryItem('80s Movies', 'movies&url=imdb4', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies from the 80s you DIDNT know you should watch before you die.',
                              'movies&url=imdb5', 'chest.png', 'chest.png')
        self.addDirectoryItem('100 Best Action Movies of All Time', 'movies&url=imdb6', 'chest.png', 'chest.png')
        self.addDirectoryItem('Best of 80s, 90s, 00s Action', 'movies&url=imdb7', 'chest.png', 'chest.png')
        self.addDirectoryItem('Top 250 Action Movies', 'movies&url=imdb8', 'chest.png', 'chest.png')
        self.addDirectoryItem('Adventure-Fantasy Films 1970 to 1996', 'movies&url=imdb9', 'chest.png', 'chest.png')
        self.addDirectoryItem('Great Kids Adventures Movies', 'movies&url=imdb10', 'chest.png', 'chest.png')  # start
        self.addDirectoryItem('Movies dealing in some way with the afterlife',
                              'movies&url=imdb11', 'chest.png', 'chest.png')
        self.addDirectoryItem('Against All Odds - Survival of the fittest',
                              'movies&url=imdb12', 'chest.png', 'chest.png')
        self.addDirectoryItem('Agoraphobia ( Fear of going Outside )', 'movies&url=imdb13', 'chest.png', 'chest.png')
        self.addDirectoryItem('Airplane Movies', 'movies&url=imdb14', 'chest.png', 'chest.png')
        self.addDirectoryItem('Alien Life: Friendly aliens movies', 'movies&url=imdb15', 'chest.png', 'chest.png')
        self.addDirectoryItem('Aliens: Movies with Aliens', 'movies&url=imdb16', 'chest.png', 'chest.png')
        self.addDirectoryItem('Angels In Movies', 'movies&url=imdb17', 'chest.png', 'chest.png')
        self.addDirectoryItem('Animation: Best Achievements in Animation',
                              'movies&url=imdb18', 'chest.png', 'chest.png')
        self.addDirectoryItem('Anime/Animated', 'movies&url=imdb19', 'chest.png', 'chest.png')
        self.addDirectoryItem('Archery: Movies involving archery', 'movies&url=imdb20', 'chest.png', 'chest.png')
        self.addDirectoryItem('Atmospheric Movies', 'movies&url=imdb21', 'chest.png', 'chest.png')
        self.addDirectoryItem('Australian Summer', 'movies&url=imdb22', 'chest.png', 'chest.png')
        self.addDirectoryItem('Aviation: Pilots, Flight Attendants, Airports or Planes',
                              'movies&url=imdb23', 'chest.png', 'chest.png')
        self.addDirectoryItem('Awesome movies with a child/teenager in the leading role',
                              'movies&url=imdb24', 'chest.png', 'chest.png')
        self.addDirectoryItem('B-Movies: 80s 90s Sci-Fi & B-movies', 'movies&url=imdb25', 'chest.png', 'chest.png')
        self.addDirectoryItem('Bad Guy Wins', 'movies&url=imdb26', 'chest.png', 'chest.png')
        self.addDirectoryItem('Bad Luck - Characters Down on Their Luck', 'movies&url=imdb27', 'chest.png', 'chest.png')
        self.addDirectoryItem('BANNED: Video Nasties, The Complete 72 Banned UK Titles List',
                              'movies&url=imdb28', 'chest.png', 'chest.png')
        self.addDirectoryItem('Baseball Movies', 'movies&url=imdb29', 'chest.png', 'chest.png')
        self.addDirectoryItem('Before They were famous', 'movies&url=imdb30', 'chest.png', 'chest.png')
        self.addDirectoryItem('Best Buddies Movies', 'movies&url=imdb31', 'chest.png', 'chest.png')
        self.addDirectoryItem('Best Conspiracy Thrillers', 'movies&url=imdb32', 'chest.png', 'chest.png')
        self.addDirectoryItem('Best films about Civil Rights / Racism', 'movies&url=imdb33', 'chest.png', 'chest.png')
        self.addDirectoryItem('Best Movie Remakes of All Time', 'movies&url=imdb34', 'chest.png', 'chest.png')
        self.addDirectoryItem('Best of Jackie Chan', 'movies&url=imdb35', 'chest.png', 'chest.png')
        self.addDirectoryItem('Best Opening Scenes In Movies', 'movies&url=imdb36', 'chest.png', 'chest.png')
        self.addDirectoryItem('Best Special Effects in Movies', 'movies&url=imdb37', 'chest.png', 'chest.png')
        self.addDirectoryItem('Best Teen Movies of All Time', 'movies&url=imdb38', 'chest.png', 'chest.png')
        self.addDirectoryItem('Biggest names among movies: the huge, the classic and the beautiful',
                              'movies&url=imdb39', 'chest.png', 'chest.png')
        self.addDirectoryItem('Biography: The Best Biographical Films', 'movies&url=imdb40', 'chest.png', 'chest.png')
        self.addDirectoryItem('Biopic: Top 50 Greatest Biopics of All Time',
                              'movies&url=imdb41', 'chest.png', 'chest.png')
        self.addDirectoryItem('Blaxploitation Movies - Greatest Ones', 'movies&url=imdb42', 'chest.png', 'chest.png')
        self.addDirectoryItem('Body Switch Movies', 'movies&url=imdb43', 'chest.png', 'chest.png')
        self.addDirectoryItem('Boogeyman in Movies', 'movies&url=imdb44', 'chest.png', 'chest.png')
        self.addDirectoryItem('Book: A list of Movies Based on Books', 'movies&url=imdb45', 'chest.png', 'chest.png')
        self.addDirectoryItem('Bullying in Movies', 'movies&url=imdb46', 'chest.png', 'chest.png')
        self.addDirectoryItem('Campy Movies!', 'movies&url=imdb47', 'chest.png', 'chest.png')
        self.addDirectoryItem('Cartoons', 'movies&url=imdb48', 'chest.png', 'chest.png')
        self.addDirectoryItem('Chased/Sought after', 'movies&url=imdb49', 'chest.png', 'chest.png')
        self.addDirectoryItem('Cheesy love / drama / sad movies', 'movies&url=imdb50', 'chest.png', 'chest.png')
        self.addDirectoryItem('Christmas Movies', 'movies&url=imdb51', 'chest.png', 'chest.png')
        self.addDirectoryItem('Cities: Movies where the city is practically a character',
                              'movies&url=imdb52', 'chest.png', 'chest.png')
        self.addDirectoryItem('Clever Movies', 'movies&url=imdb53', 'chest.png', 'chest.png')
        self.addDirectoryItem('Clones Movies And Shows', 'movies&url=imdb54', 'chest.png', 'chest.png')
        self.addDirectoryItem('Coen Brothers Filmography', 'movies&url=imdb55', 'chest.png', 'chest.png')
        self.addDirectoryItem('The 100 Best Comedies of the 80s', 'movies&url=imdb56', 'chest.png', 'chest.png')
        self.addDirectoryItem('Top 200 Comedy Movies', 'movies&url=imdb57', 'chest.png', 'chest.png')
        self.addDirectoryItem('Comfy, cozy, chamber movies', 'movies&url=imdb58', 'chest.png', 'chest.png')
        self.addDirectoryItem('Coming of age: The Ultimate list', 'movies&url=imdb59', 'chest.png', 'chest.png')
        self.addDirectoryItem('Confessions, Diaries, Or Both', 'movies&url=imdb60', 'chest.png', 'chest.png')
        self.addDirectoryItem('Cops', 'movies&url=imdb61', 'chest.png', 'chest.png')
        self.addDirectoryItem('Cops: Dirty Cop Movies', 'movies&url=imdb62', 'chest.png', 'chest.png')
        self.addDirectoryItem('Cozy Winter Movies', 'movies&url=imdb63', 'chest.png', 'chest.png')
        self.addDirectoryItem('Crime Shows/Documentaries', 'movies&url=imdb64', 'chest.png', 'chest.png')
        self.addDirectoryItem('Crime: Best Crime Movies:The Ultimate List',
                              'movies&url=imdb65', 'chest.png', 'chest.png')
        self.addDirectoryItem('Cruise Ships Movies', 'movies&url=imdb66', 'chest.png', 'chest.png')
        self.addDirectoryItem('Cult: The Ultimate Cult Movie List', 'movies&url=imdb67', 'chest.png', 'chest.png')
        self.addDirectoryItem('Cyberpunk', 'movies&url=imdb68', 'chest.png', 'chest.png')
        self.addDirectoryItem('Dance movies / great list of dance movies',
                              'movies&url=imdb69', 'chest.png', 'chest.png')
        self.addDirectoryItem('Dark and Gritty Movies', 'movies&url=imdb70', 'chest.png', 'chest.png')
        self.addDirectoryItem('Dark Comedies', 'movies&url=imdb71', 'chest.png', 'chest.png')
        self.addDirectoryItem('Desert themed movies', 'movies&url=imdb72', 'chest.png', 'chest.png')
        self.addDirectoryItem('Detectives: Best Detective Films and TV series:The Ultimate List',
                              'movies&url=imdb73', 'chest.png', 'chest.png')
        self.addDirectoryItem('Direct to Video Movies That Are Actually Great',
                              'movies&url=imdb74', 'chest.png', 'chest.png')
        self.addDirectoryItem('Disaster Movies. Huge list of disaster movies',
                              'movies&url=imdb75', 'chest.png', 'chest.png')
        self.addDirectoryItem('Disney Movies - Animated', 'movies&url=imdb76', 'chest.png', 'chest.png')
        self.addDirectoryItem('Disney: Every Disney Movies', 'movies&url=imdb77', 'chest.png', 'chest.png')
        self.addDirectoryItem('Disorder: Movies about physical disability',
                              'movies&url=imdb78', 'chest.png', 'chest.png')
        self.addDirectoryItem('Disorder: Movies Depicting Mental Disorders',
                              'movies&url=imdb79', 'chest.png', 'chest.png')
        self.addDirectoryItem('Disorder: Movies with main characters that are blind',
                              'movies&url=imdb80', 'chest.png', 'chest.png')
        self.addDirectoryItem('Disorder:Brain Powers', 'movies&url=imdb81', 'chest.png', 'chest.png')
        self.addDirectoryItem('Disorder: The best movies about INSANITY', 'movies&url=imdb82', 'chest.png', 'chest.png')
        self.addDirectoryItem('Dolls, Puppets, Dummies, Mannequins, Toys, and Marionettes',
                              'movies&url=imdb83', 'chest.png', 'chest.png')
        self.addDirectoryItem('Drugs: Modern Films & TV Shows About Drugs/Pharmaceuticals',
                              'movies&url=imdb84', 'chest.png', 'chest.png')
        self.addDirectoryItem('Ethnic: Must See Movies For Black Folks', 'movies&url=imdb85', 'chest.png', 'chest.png')
        self.addDirectoryItem('Ethnic: The Best hood movies', 'movies&url=imdb86', 'chest.png', 'chest.png')
        self.addDirectoryItem('Evil Kid Horror Movies', 'movies&url=imdb87', 'chest.png', 'chest.png')
        self.addDirectoryItem('Expedition Gone Wrong Movies', 'movies&url=imdb88', 'chest.png', 'chest.png')
        self.addDirectoryItem('Fairy Tale Movies', 'movies&url=imdb89', 'chest.png', 'chest.png')
        self.addDirectoryItem('Family: 100 best family movies ever for your children',
                              'movies&url=imdb90', 'chest.png', 'chest.png')
        self.addDirectoryItem('Fantasy: Some of the best fantasy kid movies ever',
                              'movies&url=imdb90', 'chest.png', 'chest.png')
        self.addDirectoryItem('Farms', 'movies&url=imdb91', 'chest.png', 'chest.png')
        self.addDirectoryItem('Feel Good Movies', 'movies&url=imdb92', 'chest.png', 'chest.png')
        self.addDirectoryItem('Fighting Movies', 'movies&url=imdb93', 'chest.png', 'chest.png')
        self.addDirectoryItem('Films with disfigured characters', 'movies&url=imdb94', 'chest.png', 'chest.png')
        self.addDirectoryItem('Food & Restaurant Movies', 'movies&url=imdb95', 'chest.png', 'chest.png')
        self.addDirectoryItem('Foreign: Some of the Best Foreign Films', 'movies&url=imdb96', 'chest.png', 'chest.png')
        self.addDirectoryItem('Found Footage Movies', 'movies&url=imdb97', 'chest.png', 'chest.png')
        self.addDirectoryItem('Frat Pack Movies', 'movies&url=imdb98', 'chest.png', 'chest.png')
        self.addDirectoryItem('Full list of comic based movies', 'movies&url=imdb99', 'chest.png', 'chest.png')
        self.addDirectoryItem('Funny Movies of all sorts', 'movies&url=imdb100', 'chest.png', 'chest.png')
        self.addDirectoryItem('Futuristic Apocalypse Movies', 'movies&url=imdb101', 'chest.png', 'chest.png')
        self.addDirectoryItem('Futuristic: 200 futuristic apocalypse films',
                              'movies&url=imdb102', 'chest.png', 'chest.png')
        self.addDirectoryItem('Ghost Ship movies collection', 'movies&url=imdb103', 'chest.png', 'chest.png')
        self.addDirectoryItem('Ghosts: The best of Ghost Movies', 'movies&url=imdb104', 'chest.png', 'chest.png')
        self.addDirectoryItem('Great Soundtracks in Movies', 'movies&url=imdb105', 'chest.png', 'chest.png')
        self.addDirectoryItem('GREATEST MOVIES: 2000-2017', 'movies&url=imdb106', 'chest.png', 'chest.png')
        self.addDirectoryItem('Hacking / Computer Geeks', 'movies&url=imdb107', 'chest.png', 'chest.png')
        self.addDirectoryItem('Halloween Themed Movies and Movies with Halloween Scenes',
                              'movies&url=imdb108', 'chest.png', 'chest.png')
        self.addDirectoryItem('High School: Best High School Themed Movies',
                              'movies&url=imdb109', 'chest.png', 'chest.png')
        self.addDirectoryItem('Hillbillys, Rednecks & Hicks', 'movies&url=imdb110', 'chest.png', 'chest.png')
        self.addDirectoryItem('Hip-hop culture / racial discrimination and etc.',
                              'movies&url=imdb111', 'chest.png', 'chest.png')
        self.addDirectoryItem('Hipster Movies', 'movies&url=imdb112', 'chest.png', 'chest.png')
        self.addDirectoryItem('Hitmen: Great list of movies with Hitmen/Assassins',
                              'movies&url=imdb113', 'chest.png', 'chest.png')
        self.addDirectoryItem('Home Invasion movies', 'movies&url=imdb114', 'chest.png', 'chest.png')
        self.addDirectoryItem('Hood/Gangsters/Ghetto movies', 'movies&url=imdb115', 'chest.png', 'chest.png')
        self.addDirectoryItem('horror flicks based on true story', 'movies&url=imdb116', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror Movies 2017', 'movies&url=imdb117', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror movies with awesome houses', 'movies&url=imdb118', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Best Horror Movies of the 2000s', 'movies&url=imdb119', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Cabins/Cottages', 'movies&url=imdb120', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Christmas Horror', 'movies&url=imdb121', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Creeps / Stalkers', 'movies&url=imdb122', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Haunted Houses - The Ultimate List',
                              'movies&url=imdb123', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Horror movies set in asylums/ mental hospitals',
                              'movies&url=imdb124', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Korean Horror Movies', 'movies&url=imdb125', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Redneck Horror Movies', 'movies&url=imdb126', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Slashers Horror', 'movies&url=imdb127', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Slow Burn Horror', 'movies&url=imdb128', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Underlooked Gems', 'movies&url=imdb129', 'chest.png', 'chest.png')
        self.addDirectoryItem('Horror: Winter-setting horror movies', 'movies&url=imdb130', 'chest.png', 'chest.png')
        self.addDirectoryItem('Imaginary friends', 'movies&url=imdb131', 'chest.png', 'chest.png')
        self.addDirectoryItem('Inspirational movies "BASED ON TRUE STORY"',
                              'movies&url=imdb132', 'chest.png', 'chest.png')
        self.addDirectoryItem('Island: Stranded on an Island', 'movies&url=imdb133', 'chest.png', 'chest.png')
        self.addDirectoryItem('Jack Nicholson - The Filmography', 'movies&url=imdb134', 'chest.png', 'chest.png')
        self.addDirectoryItem('James Bond: The Complete Collection', 'movies&url=imdb135', 'chest.png', 'chest.png')
        self.addDirectoryItem('James Wan', 'movies&url=imdb136', 'chest.png', 'chest.png')
        self.addDirectoryItem('JcVd', 'movies&url=imdb137', 'chest.png', 'chest.png')
        self.addDirectoryItem('John Hughes Movies', 'movies&url=imdb138', 'chest.png', 'chest.png')
        self.addDirectoryItem('Jump Scares', 'movies&url=imdb139', 'chest.png', 'chest.png')
        self.addDirectoryItem('Jungle: Movies taking place in jungles', 'movies&url=imdb140', 'chest.png', 'chest.png')
        self.addDirectoryItem('Kid-friendly "Halloween" movies & TV shows',
                              'movies&url=imdb141', 'chest.png', 'chest.png')
        self.addDirectoryItem('Kid/Teens Adventures', 'movies&url=imdb142', 'chest.png', 'chest.png')
        self.addDirectoryItem('Kidnapped or Hostage movies', 'movies&url=imdb143', 'chest.png', 'chest.png')
        self.addDirectoryItem('Killer bug movies', 'movies&url=imdb144', 'chest.png', 'chest.png')
        self.addDirectoryItem('Las Vegas: List of films set in Las Vegas',
                              'movies&url=imdb145', 'chest.png', 'chest.png')
        self.addDirectoryItem('Law: Great movies with lawyers', 'movies&url=imdb146', 'chest.png', 'chest.png')
        self.addDirectoryItem('Lesbian: Huge lesbian movies list', 'movies&url=imdb147', 'chest.png', 'chest.png')
        self.addDirectoryItem('Life Lessons: Movies with life lessons', 'movies&url=imdb148', 'chest.png', 'chest.png')
        self.addDirectoryItem('Lifetime Movies That Are Great', 'movies&url=imdb149', 'chest.png', 'chest.png')
        self.addDirectoryItem('Lighthouses: Movies set in a Lighthouse', 'movies&url=imdb150', 'chest.png', 'chest.png')
        self.addDirectoryItem('Live-Action Fairy Tale Movies', 'movies&url=imdb151', 'chest.png', 'chest.png')
        self.addDirectoryItem('Losers in Movies', 'movies&url=imdb152', 'chest.png', 'chest.png')
        self.addDirectoryItem('Mafia, Gangsters, Mob Movies', 'movies&url=imdb153', 'chest.png', 'chest.png')
        self.addDirectoryItem('Magic: Movies and Shows About Magic', 'movies&url=imdb154', 'chest.png', 'chest.png')
        self.addDirectoryItem('Martial Arts: Awesome Martial Arts Movies!',
                              'movies&url=imdb155', 'chest.png', 'chest.png')
        self.addDirectoryItem('Martial Arts: The Top 250 Greatest Martial Arts Movies of All-Time',
                              'movies&url=imdb156', 'chest.png', 'chest.png')
        self.addDirectoryItem('Medieval Movies', 'movies&url=imdb157', 'chest.png', 'chest.png')
        self.addDirectoryItem('Medieval: Films set in the Middle Ages', 'movies&url=imdb158', 'chest.png', 'chest.png')
        self.addDirectoryItem('Mel Brooks Movies', 'movies&url=imdb159', 'chest.png', 'chest.png')
        self.addDirectoryItem('Military: 54 MOVIES INVOLVING MILITARY TRAINING',
                              'movies&url=imdb160', 'chest.png', 'chest.png')
        self.addDirectoryItem('Missing Person/People movie', 'movies&url=imdb161', 'chest.png', 'chest.png')
        self.addDirectoryItem('Modern (1990s-Now) Films That are Set in the 1970s',
                              'movies&url=imdb162', 'chest.png', 'chest.png')
        self.addDirectoryItem('Modern People in Historical Setting or Historical/Ancient',
                              'movies&url=imdb163', 'chest.png', 'chest.png')
        self.addDirectoryItem('Modern Westerns', 'movies&url=imdb163', 'chest.png', 'chest.png')
        self.addDirectoryItem('Monsters: Movies featuring monsters', 'movies&url=imdb165', 'chest.png', 'chest.png')
        self.addDirectoryItem('Moon: Top 10 Moon Movies', 'movies&url=imdb166', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies for High School Girls', 'movies&url=imdb167', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies inside a Video-Game', 'movies&url=imdb168', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies involving Portrayals of Real Life Teachers',
                              'movies&url=imdb169', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies set in San Francisco/ Bay Area', 'movies&url=imdb170', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies similar to the burbs', 'movies&url=imdb171', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies that keep you guessing until the end',
                              'movies&url=imdb172', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies that switch Genres halfway through',
                              'movies&url=imdb173', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies That Take Place In A Single Day', 'movies&url=imdb174', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies To Watch On a Rainy Day', 'movies&url=imdb175', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies with great aesthetics', 'movies&url=imdb176', 'chest.png', 'chest.png')
        self.addDirectoryItem('Movies written, directed and starring the same person',
                              'movies&url=imdb177', 'chest.png', 'chest.png')
        self.addDirectoryItem('Music: LIST OF 356 FILMS ABOUT OR INVOLVING MUSICIANS',
                              'movies&url=imdb178', 'chest.png', 'chest.png')
        self.addDirectoryItem('Must See World War II Documentaries', 'movies&url=imdb179', 'chest.png', 'chest.png')
        self.addDirectoryItem('Mystery Movies set in Castles and Mansions',
                              'movies&url=imdb180', 'chest.png', 'chest.png')
        self.addDirectoryItem('Narrated Movies', 'movies&url=imdb181', 'chest.png', 'chest.png')
        self.addDirectoryItem('National Lampoon Marathon!', 'movies&url=imdb182', 'chest.png', 'chest.png')
        self.addDirectoryItem('Nature Documentaries!', 'movies&url=imdb183', 'chest.png', 'chest.png')
        self.addDirectoryItem('Nature: Man vs. Nature/Animal movies', 'movies&url=imdb184', 'chest.png', 'chest.png')
        self.addDirectoryItem('Nature: Scuba / Underwater / Diving', 'movies&url=imdb185', 'chest.png', 'chest.png')
        self.addDirectoryItem('Noir: 100 Best Film-Noir movies', 'movies&url=imdb186', 'chest.png', 'chest.png')
        self.addDirectoryItem('Nostalgia Inducing Movies For People In Their Mid 20s 30s',
                              'movies&url=imdb187', 'chest.png', 'chest.png')
        self.addDirectoryItem('Ocean Adventure', 'movies&url=imdb188', 'chest.png', 'chest.png')
        self.addDirectoryItem('One Man Army', 'movies&url=imdb189', 'chest.png', 'chest.png')
        self.addDirectoryItem('Outer Space movies/Great Space Exploration',
                              'movies&url=imdb190', 'chest.png', 'chest.png')
        self.addDirectoryItem('Parallel stories ', 'movies&url=imdb191', 'chest.png', 'chest.png')
        self.addDirectoryItem('Paul Verhoeven Movies', 'movies&url=imdb192', 'chest.png', 'chest.png')
        self.addDirectoryItem('Plot Twists In Movies', 'movies&url=imdb193', 'chest.png', 'chest.png')
        self.addDirectoryItem('Politics: 150 FILMS', 'movies&url=imdb194', 'chest.png', 'chest.png')
        self.addDirectoryItem('Post-Apocalyptic Movies', 'movies&url=imdb195', 'chest.png', 'chest.png')
        self.addDirectoryItem('Prison-Jail Movies', 'movies&url=imdb196', 'chest.png', 'chest.png')
        self.addDirectoryItem('Psychological Thrillers', 'movies&url=imdb197', 'chest.png', 'chest.png')
        self.addDirectoryItem('Psychologists/Psychiatrists/Therapists', 'movies&url=imdb198', 'chest.png', 'chest.png')
        self.addDirectoryItem('Psychosexual thrillers', 'movies&url=imdb199', 'chest.png', 'chest.png')
        self.addDirectoryItem('Quotable: Top 50 Most Quotable Movies Ever',
                              'movies&url=imdb200', 'chest.png', 'chest.png')
        self.addDirectoryItem('R rated superhero movies', 'movies&url=imdb201', 'chest.png', 'chest.png')
        self.addDirectoryItem('Rape & Revenge', 'movies&url=imdb202', 'chest.png', 'chest.png')
        self.addDirectoryItem('Really Long Movies', 'movies&url=imdb203', 'chest.png', 'chest.png')
        self.addDirectoryItem('Reddit - Films Before You Die', 'movies&url=imdb204', 'chest.png', 'chest.png')
        self.addDirectoryItem('Revenge & Vigilante Movies', 'movies&url=imdb205', 'chest.png', 'chest.png')
        self.addDirectoryItem('Road Trips - Travels', 'movies&url=imdb206', 'chest.png', 'chest.png')
        self.addDirectoryItem('Robbery / Heist Movies', 'movies&url=imdb207', 'chest.png', 'chest.png')
        self.addDirectoryItem('Robot Movies', 'movies&url=imdb208', 'chest.png', 'chest.png')
        self.addDirectoryItem('Romance: Best romance in movies', 'movies&url=imdb209', 'chest.png', 'chest.png')
        self.addDirectoryItem('Romance: Bromance in Movies', 'movies&url=imdb210', 'chest.png', 'chest.png')
        self.addDirectoryItem('Romance: Forbidden Love in Movies', 'movies&url=imdb211', 'chest.png', 'chest.png')
        self.addDirectoryItem('Romance: Unconventional Romance Films', 'movies&url=imdb212', 'chest.png', 'chest.png')
        self.addDirectoryItem('Saddest Movies - Movies That Will Make You Cry',
                              'movies&url=imdb213', 'chest.png', 'chest.png')
        self.addDirectoryItem('Sailing & Seamanship Movies', 'movies&url=imdb214', 'chest.png', 'chest.png')
        self.addDirectoryItem('Sam Rockwell Movies', 'movies&url=imdb215', 'chest.png', 'chest.png')
        self.addDirectoryItem('Sci-Fi Based on Books, Short Stories, or Graphic Novels',
                              'movies&url=imdb216', 'chest.png', 'chest.png')
        self.addDirectoryItem('Sci-Fi: The Truly Ultimate Sci-Fi List: 1902-2015',
                              'movies&url=imdb217', 'chest.png', 'chest.png')
        self.addDirectoryItem('Sequels: 30 Great Sequels', 'movies&url=imdb218', 'chest.png', 'chest.png')
        self.addDirectoryItem('Serial Killer Movies', 'movies&url=imdb219', 'chest.png', 'chest.png')
        self.addDirectoryItem('Sharks, Sharks and Sharks!', 'movies&url=imdb220', 'chest.png', 'chest.png')
        self.addDirectoryItem('Sniper Movies', 'movies&url=imdb221', 'chest.png', 'chest.png')
        self.addDirectoryItem('Social Network: Movies ', 'movies&url=imdb222', 'chest.png', 'chest.png')
        self.addDirectoryItem('Some of The Best Military movies of all time',
                              'movies&url=imdb223', 'chest.png', 'chest.png')
        self.addDirectoryItem('Some Of The Most Inventive and Creative', 'movies&url=imdb224', 'chest.png', 'chest.png')
        self.addDirectoryItem('Spies: Best Spy Movies:The Ultimate List',
                              'movies&url=imdb225', 'chest.png', 'chest.png')
        self.addDirectoryItem('Steampunk', 'movies&url=imdb226', 'chest.png', 'chest.png')
        self.addDirectoryItem('Stephen King: Real Stephen King Movies / Adaptions',
                              'movies&url=imdb227', 'chest.png', 'chest.png')
        self.addDirectoryItem('Steven Spielberg Feature Filmography', 'movies&url=imdb228', 'chest.png', 'chest.png')
        self.addDirectoryItem('Strippers: Movies Featuring Strippers', 'movies&url=imdb229', 'chest.png', 'chest.png')
        self.addDirectoryItem('Submarines', 'movies&url=imdb230', 'chest.png', 'chest.png')
        self.addDirectoryItem('Suburban Nostalgia, Spider-Man, Superman, Avengers',
                              'movies&url=imdb231', 'chest.png', 'chest.png')
        self.addDirectoryItem('Super Hero Films, Superman, Avengers', 'movies&url=imdb232', 'chest.png', 'chest.png')
        self.addDirectoryItem('Surfing: Movies about surfing', 'movies&url=imdb233', 'chest.png', 'chest.png')
        self.addDirectoryItem('Tarantino-Esque Movies: THE ULTIMATE LIST',
                              'movies&url=imdb234', 'chest.png', 'chest.png')
        self.addDirectoryItem('The Best Non Animated Children, Teen and Family Movies of all Time',
                              'movies&url=imdb235', 'chest.png', 'chest.png')
        self.addDirectoryItem('The best Vampire Movies!', 'movies&url=imdb236', 'chest.png', 'chest.png')
        self.addDirectoryItem('The Criterion Collection', 'movies&url=imdb237', 'chest.png', 'chest.png')
        self.addDirectoryItem('The Finest Fantasy: 25 Must-See Sword & Sorcery Films',
                              'movies&url=imdb237', 'chest.png', 'chest.png')
        self.addDirectoryItem('The Girlfriends Corner', 'movies&url=imdb238', 'chest.png', 'chest.png')
        self.addDirectoryItem('The Greatest Acting Performances of All Time',
                              'movies&url=imdb239', 'chest.png', 'chest.png')
        self.addDirectoryItem('The One True God', 'movies&url=imdb240', 'chest.png', 'chest.png')
        self.addDirectoryItem('Time Travel Movies', 'movies&url=imdb241', 'chest.png', 'chest.png')
        self.addDirectoryItem('Top 100 Gore Films', 'movies&url=imdb242', 'chest.png', 'chest.png')
        self.addDirectoryItem('Top 240 Horror Movies 2000-2016', 'movies&url=imdb243', 'chest.png', 'chest.png')
        self.addDirectoryItem('Top50 World War II Movies', 'movies&url=imdb244', 'chest.png', 'chest.png')
        self.addDirectoryItem('Trapped Movies', 'movies&url=imdb245', 'chest.png', 'chest.png')
        self.addDirectoryItem('TV: Live-Action TV Series Based on Comics',
                              'movies&url=imdb246', 'chest.png', 'chest.png')
        self.addDirectoryItem('TV: Live-action TV series based on Marvel Comics',
                              'movies&url=imdb247', 'chest.png', 'chest.png')
        self.addDirectoryItem('Underdogs in Movies', 'movies&url=imdb248', 'chest.png', 'chest.png')
        self.addDirectoryItem('Vacations: 100+ Summer, Vacation, and Beach Movies',
                              'movies&url=imdb249', 'chest.png', 'chest.png')
        self.addDirectoryItem('Vampire and Werewolf Movies', 'movies&url=imdb250', 'chest.png', 'chest.png')
        self.addDirectoryItem('Victorian Era', 'movies&url=imdb251', 'chest.png', 'chest.png')
        self.addDirectoryItem('Video Games: Movies/Series involving video games',
                              'movies&url=imdb252', 'chest.png', 'chest.png')
        self.addDirectoryItem('Visually Striking - Good Cinematography', 'movies&url=imdb253', 'chest.png', 'chest.png')
        self.addDirectoryItem('War: 1600+ War movies list', 'movies&url=imdb254', 'chest.png', 'chest.png')
        self.addDirectoryItem('War: Top 25 Greatest War Movies of All Time',
                              'movies&url=imdb255', 'chest.png', 'chest.png')
        self.addDirectoryItem('Weather: Films Set in a Heat Wave', 'movies&url=imdb256', 'chest.png', 'chest.png')
        self.addDirectoryItem('Weed Movies', 'movies&url=imdb257', 'chest.png', 'chest.png')
        self.addDirectoryItem('Weird claustrophobic movies like Cube and Saw',
                              'movies&url=imdb258', 'chest.png', 'chest.png')
        self.addDirectoryItem('Westerns with HD releases', 'movies&url=imdb259', 'chest.png', 'chest.png')
        self.addDirectoryItem('Wilderness Survival Movies', 'movies&url=imdb260', 'chest.png', 'chest.png')
        self.addDirectoryItem('Winter and Snow Movies: The Ultimate List',
                              'movies&url=imdb261', 'chest.png', 'chest.png')
        self.addDirectoryItem('Witches: Best Witch Movies', 'movies&url=imdb262', 'chest.png', 'chest.png')
        self.addDirectoryItem('Worst Movies of All Time', 'movies&url=imdb263', 'chest.png', 'chest.png')
        self.addDirectoryItem('WTF - Weird, fcked up , Bizzare etc', 'movies&url=imdb264', 'chest.png', 'chest.png')
        self.addDirectoryItem('Zombies: Definitive zombie list', 'movies&url=imdb265', 'chest.png', 'chest.png')

        self.endDirectory(category='The Movie Chest', sortMethod=control.xDirSort.Label)

    def it250(self):
        self.addDirectoryItem('Top 250 All Time', 'movies&url=topgreatest', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Action', 'movies&url=topaction', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Adventure', 'movies&url=topadventure', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Animation', 'movies&url=topanimation', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Comedy', 'movies&url=topcomedy', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Crime', 'movies&url=topcrime', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Documentaries', 'movies&url=topdocumentary', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Drama', 'movies&url=topdrama', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Family', 'movies&url=topfamily', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Fantasy', 'movies&url=topfantasy', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 History', 'movies&url=tophistory', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Horror', 'movies&url=tophorror', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Music', 'movies&url=topmusic', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Mystery', 'movies&url=topmystery', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Romance', 'movies&url=topromance', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Sci-Fi', 'movies&url=topsci_fi', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Sports', 'movies&url=topsport', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Thriller', 'movies&url=topthriller', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 War', 'movies&url=topwar', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Top 250 Western', 'movies&url=topwestern', 'imdb.png', 'playlist.jpg')

        self.endDirectory(category='IMDB Top 250 Lists', sortMethod=control.xDirSort.Label)

    def movieCollections(self, lite=False):  # Collections ####################
        self.addDirectoryItem('Alien Invasion', 'movies&url=alien', 'alien.png', 'playlist.jpg')
        self.addDirectoryItem('Anime', 'movies&url=anime', 'anime.png', 'playlist.jpg')
        self.addDirectoryItem('Avant Garde', 'movies&url=avant', 'avant.png', 'playlist.jpg')
        self.addDirectoryItem('Based On A True Story', 'movies&url=true', 'true.png', 'playlist.jpg')
        self.addDirectoryItem('Biographical', 'movies&url=bio', 'bio.png', 'playlist.jpg')
        self.addDirectoryItem('Biker', 'movies&url=biker', 'biker.png', 'playlist.jpg')
        self.addDirectoryItem('B Movies', 'movies&url=bmovie', 'bmovie.png', 'playlist.jpg')
        self.addDirectoryItem('Breaking The Fourth Wall', 'movies&url=breaking', 'breaking.png', 'playlist.jpg')
        self.addDirectoryItem('Business', 'movies&url=business', 'business.png', 'playlist.jpg')
        self.addDirectoryItem('Capers', 'movies&url=caper', 'caper.png', 'playlist.jpg')
        self.addDirectoryItem('Chick Flix', 'movies&url=chick', 'chick.png', 'playlist.jpg')
        self.addDirectoryItem('Coen Brothers Movies', 'movies&url=coen', 'coen.png', 'playlist.jpg')
        self.addDirectoryItem('Competition', 'movies&url=competition', 'comps.png', 'playlist.jpg')
        self.addDirectoryItem('Crime', 'movies&url=crime', 'crime.png', 'playlist.jpg')
        self.addDirectoryItem('Cult', 'movies&url=cult', 'cult.png', 'playlist.jpg')
        # self.addDirectoryItem('Cult Horror Movies', 'movies&url=imdb9', 'imdb.png', 'playlist.jpg')
        self.addDirectoryItem('Cyberpunk', 'movies&url=cyber', 'cyber.png', 'playlist.jpg')
        self.addDirectoryItem('DC Universe', 'movies&url=dc', 'dc.png', 'playlist.jpg')
        self.addDirectoryItem('Disney and Pixar', 'movies&url=disney', 'disney.png', 'playlist.jpg')
        self.addDirectoryItem('Drug Addiction', 'movies&url=drugs', 'drugs.png', 'playlist.jpg')
        self.addDirectoryItem('Dystopia', 'movies&url=dystopia', 'dystopia.png', 'playlist.jpg')
        self.addDirectoryItem('Epic!', 'movies&url=epic', 'epic.png', 'playlist.jpg')
        self.addDirectoryItem('Espionage', 'movies&url=espionage', 'espionage.png', 'playlist.jpg')
        self.addDirectoryItem('Fairy Tale', 'movies&url=fairytale', 'fairytale.png', 'playlist.jpg')
        # self.addDirectoryItem('Fairy Tale', 'movies&url=fairytale', 'fairytale.png', 'playlist.jpg')
        self.addDirectoryItem('Farce', 'movies&url=farce', 'farce.png', 'playlist.jpg')
        self.addDirectoryItem('Femme Fatale', 'movies&url=femme', 'femme.png', 'playlist.jpg')
        self.addDirectoryItem('Futuristic', 'movies&url=futuristic', 'futuristic.png', 'playlist.jpg')
        self.addDirectoryItem('Gangster', 'movies&url=gangster', 'gangsters.png', 'playlist.jpg')
        # self.addDirectoryItem('Halloween', 'movies&url=halloween', 'halloween.png', 'season.jpg')
        self.addDirectoryItem('James Bond', 'movies&url=bond', 'bond.png', 'playlist.jpg')
        self.addDirectoryItem('Man Vs. Nature', 'movies&url=nature', 'man.png', 'playlist.jpg')
        self.addDirectoryItem('Marvel Universe', 'movies&url=marvel', 'marvel.png', 'playlist.jpg')
        self.addDirectoryItem('Motivational Movies', 'movies&url=mot', 'mot.png', 'playlist.jpg')
        self.addDirectoryItem('Monsters', 'movies&url=monsters', 'monster.png', 'playlist.jpg')
        self.addDirectoryItem('Movies To Make You Rethink Your Survival Plan',
                              'movies&url=survival', 'survival.png', 'playlist.jpg')
        self.addDirectoryItem('Movies To Make You Cancel That Vacation',
                              'movies&url=vacation', 'vaca.png', 'playlist.jpg')
        self.addDirectoryItem('Movies To Make You Pick Up And Move', 'movies&url=move', 'house.png', 'playlist.jpg')
        self.addDirectoryItem('Movies To Make You Reconsider Parenthood',
                              'movies&url=parenthood', 'kids.png', 'playlist.jpg')
        self.addDirectoryItem('Musical Movies', 'movies&url=music', 'musical.png', 'playlist.jpg')
        self.addDirectoryItem('Neo Noir', 'movies&url=neo', 'neo.png', 'playlist.jpg')
        self.addDirectoryItem('Parody', 'movies&url=parody', 'parody.png', 'playlist.jpg')
        self.addDirectoryItem('Post Apocalypse', 'movies&url=apocalypse', 'apocalypse.png', 'playlist.jpg')
        self.addDirectoryItem('Private Eye', 'movies&url=private', 'eye.png', 'playlist.jpg')
        self.addDirectoryItem('Psychological Thrillers', 'movies&url=psychological', 'thrill.png', 'playlist.jpg')
        self.addDirectoryItem('Revenge', 'movies&url=revenge', 'revenge.png', 'playlist.jpg')
        self.addDirectoryItem('Satire', 'movies&url=satire', 'satire.png', 'playlist.jpg')
        self.addDirectoryItem('Science Fiction', 'movies&url=sci', 'sci.png', 'playlist.jpg')
        self.addDirectoryItem('Serial Killers', 'movies&url=killer', 'killers.png', 'playlist.jpg')
        self.addDirectoryItem('Slasher', 'movies&url=slasher', 'slasher.png', 'playlist.jpg')
        self.addDirectoryItem('Sleeper Hits', 'movies&url=sleeper', 'sleeper.png', 'playlist.jpg')
        self.addDirectoryItem('Spoofs', 'movies&url=spoof', 'spoof.png', 'playlist.jpg')
        self.addDirectoryItem('Sports', 'movies&url=sports', 'sports.png', 'playlist.jpg')
        self.addDirectoryItem('SPY - CIA - KGB', 'movies&url=spy', 'spy.png', 'playlist.jpg')
        self.addDirectoryItem('Star Wars', 'movies&url=star', 'starwars.png', 'playlist.jpg')
        self.addDirectoryItem('Steampunk', 'movies&url=steampunk', 'steampunk.png', 'playlist.jpg')
        self.addDirectoryItem('Superheros', 'movies&url=superhero', 'superhero.png', 'playlist.jpg')
        self.addDirectoryItem('Supernatural', 'movies&url=supernatural', 'super.png', 'playlist.jpg')
        self.addDirectoryItem('Tarantino Films', 'movies&url=tarantino', 'tino.png', 'playlist.jpg')
        self.addDirectoryItem('Tech Noir', 'movies&url=tech', 'tech.png', 'playlist.jpg')
        self.addDirectoryItem('Teenage', 'movies&url=teen', 'teen.png', 'playlist.jpg')
        self.addDirectoryItem('Time Travel', 'movies&url=time', 'time.png', 'playlist.jpg')
        self.addDirectoryItem('Twist Ending Movies', 'movies&url=twist', 'twist.png', 'playlist.jpg')
        self.addDirectoryItem('Virtual Reality', 'movies&url=vr', 'vr.png', 'playlist.jpg')

        self.endDirectory(category='Collections', sortMethod=control.xDirSort.Label)

    def movieMosts(self):
        self.addDirectoryItem('Most Played This Week', 'movies&url=played1', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Played This Month', 'movies&url=played2', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Played This Year', 'movies&url=played3', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Played All Time', 'movies&url=played4', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Collected This Week', 'movies&url=collected1', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Collected This Month', 'movies&url=collected2', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Collected This Year', 'movies&url=collected3', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Collected All Time', 'movies&url=collected4', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Watched This Week', 'movies&url=watched1', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Watched This Month', 'movies&url=watched2', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Watched This Year', 'movies&url=watched3', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Watched All Time', 'movies&url=watched4', 'trakt.png', 'playlist.jpg')

        self.endDirectory(category='Movie Most Lists', sortMethod=control.xDirSort.Label)

    def showMosts(self):
        self.addDirectoryItem('Most Played This Week', 'tvshows&url=played1', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Played This Month', 'tvshows&url=played2', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Played This Year', 'tvshows&url=played3', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Played All Time', 'tvshows&url=played4', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Collected This Week', 'tvshows&url=collected1', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Collected This Month', 'tvshows&url=collected2', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Collected This Year', 'tvshows&url=collected3', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Collected All Time', 'tvshows&url=collected4', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Watched This Week', 'tvshows&url=watched1', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Watched This Month', 'tvshows&url=watched2', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Watched This Year', 'tvshows&url=watched3', 'trakt.png', 'playlist.jpg')
        self.addDirectoryItem('Most Watched All Time', 'tvshows&url=watched4', 'trakt.png', 'playlist.jpg')

        self.endDirectory(category='TV Shows Most Lists', sortMethod=control.xDirSort.Label)

    def tools(self):
        self.addDirectoryItem('[B]Marauder[/B] : Changelog', 'changelog', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Marauder[/B] : Log Viewer', 'logViewer', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32611, 'clearAllCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32079, 'barnaclescrapersettings', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32076, 'smuSettings', 'resolveurl.png', 'DefaultAddonProgram.png')

        if not control.condVisibility('System.HasAddon(script.module.openscrapers)'):
            self.addDirectoryItem('[B]Openscrapers[/B] : Install', 'installOpenscrapers',
                                  'openscr.png', 'DefaultAddonProgram.png')
        else:
            self.addDirectoryItem(32082, 'openscrapersettings', 'openscr.png', 'DefaultAddonProgram.png')
        if not control.condVisibility('System.HasAddon(script.module.orion)'):
            self.addDirectoryItem('[B]Orion[/B] : Install', 'installOrion', 'orion.png', 'DefaultAddonProgram.png')
        else:
            self.addDirectoryItem(32080, 'orionsettings', 'orion.png', 'DefaultAddonProgram.png')
        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32093, 'syncTraktStatus', 'trakt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('Pairing and Authorize Tools', 'pairTools', 'tools.png', 'DefaultAddonProgram.png')

        self.endDirectory(category='Tools and More')

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(
            32559, control.setting('library.movie'),
            'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

        self.endDirectory(category='Library')

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory(category='Downloads')


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')

        self.endDirectory(category='Search')

    def views(self):
        try:
            control.idle()

            items = [(control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'),
                     (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes')]

            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1:
                return

            content = items[select][1]

            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels={'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import views
            views.setView(content, {})
        except:
            return

    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
            sys.exit()

    def infoCheck(self, version):
        try:
            control.infoDialog('', control.lang(32074).encode('utf-8'), time=5000, sound=False)
            return '1'
        except:
            return '1'

    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheMeta(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheProviders(self):
        control.idle()
#        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
#        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheSearch(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_search()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheAll(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_all()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, cache=True, contentType='addons', sortMethod=control.xDirSort.NoSort, category=None):
        control.content(syshandle, contentType)
        if category is not None:
            control.category(syshandle, category)
        if sortMethod is not control.xDirSort.NoSort:
            control.sortMethod(syshandle, sortMethod)
        control.directory(syshandle, cacheToDisc=cache)
