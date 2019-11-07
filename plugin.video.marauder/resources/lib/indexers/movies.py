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


import datetime
import json
import os
import re
import sys
import urllib
import urlparse

from resources.lib.indexers import navigator
from resources.lib.modules import (
    cache, cleangenre, cleantitle, client, control, metacache, playcount,
    trakt, utils, views, workers)

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', ''))) if len(sys.argv) > 1 else dict()

action = params.get('action')


class movies:
    def __init__(self):
        self.list = []

        self.imdb_link = 'https://www.imdb.com'
        self.trakt_link = 'https://api.trakt.tv'
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.year_date = (self.datetime - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tm_user = control.setting('tm.user')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = str(control.setting('fanart.tv.user')) + str(control.setting('tm.user'))
        self.lang = control.apiLanguage()['trakt']
        self.hidecinema = control.setting('hidecinema')

        self.search_link = 'https://api.trakt.tv/search/movie?limit=20&page=1&query='
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/movies/%s'
        self.fanart_tv_level_link = 'http://webservice.fanart.tv/v3/level'
        self.tm_art_link = 'http://api.themoviedb.org/3/movie/%s/images?api_key=%s&language=en-US&include_image_language=en,%s,null' % (
            '%s', self.tm_user, self.lang)
        self.tm_img_link = 'https://image.tmdb.org/t/p/w%s%s'

        self.persons_link = 'https://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'https://www.imdb.com/search/name?count=100&gender=male,female'
        self.person_link = 'https://www.imdb.com/search/title?title_type=movie,short,tvMovie&production_status=released&role=%s&sort=year,desc&count=40&start=1'
        self.keyword_link = 'https://www.imdb.com/search/title?title_type=movie,short,tvMovie,documentary&num_votes=100,&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=40&start=1'
        self.oscars_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&production_status=released&groups=oscar_best_picture_winners&sort=year,desc&count=40&start=1'
        self.theaters_link = 'https://www.imdb.com/search/title?title_type=feature&num_votes=1000,&release_date=date[120],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.year_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=100,&production_status=released&year=%s,%s&sort=moviemeter,asc&count=40&start=1'

        if self.hidecinema == 'true':
            self.popular_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=1000,&production_status=released&groups=top_1000&release_date=,date[90]&sort=moviemeter,asc&count=40&start=1'
            self.views_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=1000,&production_status=released&sort=num_votes,desc&release_date=,date[90]&count=40&start=1'
            self.featured_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=1000,&production_status=released&release_date=date[365],date[90]&sort=moviemeter,asc&count=40&start=1'
            self.genre_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[90]&genres=%s&sort=moviemeter,asc&count=40&start=1'
            self.language_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&release_date=,date[90]&count=40&start=1'
            self.certification_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=100,&production_status=released&certificates=us:%s&sort=moviemeter,asc&release_date=,date[90]&count=40&start=1'
            self.boxoffice_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&production_status=released&sort=boxoffice_gross_us,desc&release_date=,date[90]&count=40&start=1'
        else:
            self.popular_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=1000,&production_status=released&groups=top_1000&sort=moviemeter,asc&count=40&start=1'
            self.views_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=1000,&production_status=released&sort=num_votes,desc&count=40&start=1'
            self.featured_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=1000,&production_status=released&release_date=date[365],date[60]&sort=moviemeter,asc&count=40&start=1'
            self.genre_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=40&start=1'
            self.language_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=40&start=1'
            self.certification_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&num_votes=100,&production_status=released&certificates=us:%s&sort=moviemeter,asc&count=40&start=1'
            self.boxoffice_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&production_status=released&sort=boxoffice_gross_us,desc&count=40&start=1'

        self.added_link = 'https://www.imdb.com/search/title?title_type=movie,tvMovie&languages=en&num_votes=500,&production_status=released&release_date=%s,%s&sort=release_date,desc&count=20&start=1' % (
            self.year_date, self.today_date)
        self.trending_link = 'https://api.trakt.tv/movies/trending?limit=40&page=1'

        self.hacktheplanet_link = 'https://api.trakt.tv/users/rendom/lists/hack-the-planet-compilation/items'

        self.traktlists_link = 'https://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'https://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'https://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'https://api.trakt.tv/users/me/collection/movies'
        self.traktwatchlist_link = 'https://api.trakt.tv/users/me/watchlist/movies'
        self.traktfeatured_link = 'https://api.trakt.tv/recommendations/movies?limit=40'
        self.trakthistory_link = 'https://api.trakt.tv/users/me/history/movies?limit=40&page=1'
        self.onDeck_link = 'https://api.trakt.tv/sync/playback/movies?extended=full&limit=20'
        self.imdblists_link = 'https://www.imdb.com/user/ur%s/lists?tab=all&sort=modified&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'https://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=movie,short,tvMovie&start=1'
        self.imdblist2_link = 'https://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=movie,short,tvMovie&start=1'
        self.imdbwatchlist_link = 'https://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user
        self.imdbwatchlist2_link = 'https://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user

################# Top250 IMDB Lists ####################
        self.topgreatest_link = 'https://www.imdb.com/search/title?groups=top_250&sort=user_rating,desc/items&start=1'
        self.topaction_link = 'https://www.imdb.com/search/title?title_type=feature&genres=action&groups=top_250/items&start=1'
        self.topadventure_link = 'https://www.imdb.com/search/title?title_type=feature&genres=adventure&groups=top_250/items'
        self.topanimation_link = 'https://www.imdb.com/search/title?title_type=feature&genres=animation&groups=top_250/items'
        self.topcomedy_link = 'https://www.imdb.com/search/title?title_type=feature&genres=comedy&groups=top_250/items'
        self.topcrime_link = 'https://www.imdb.com/search/title?title_type=feature&genres=crime&groups=top_250/items'
        self.topdocumentary_link = 'https://www.imdb.com/search/title?title_type=https%3A//www.imdb.com/search/title%3Ftitle_type%3Dfeature&genres=documentary&genres=documentary&groups=top_250/items'
        self.topdrama_link = 'https://www.imdb.com/search/title?title_type=feature&genres=drama&groups=top_250/items'
        self.topfamily_link = 'https://www.imdb.com/search/title?title_type=feature&genres=family&groups=top_250/items'
        self.topfantasy_link = 'https://www.imdb.com/search/title?title_type=feature&genres=fantasy&groups=top_250/items'
        self.tophistory_link = 'https://www.imdb.com/search/title?title_type=feature&genres=history&groups=top_250/items'
        self.tophorror_link = 'https://www.imdb.com/search/title?title_type=feature&genres=horror&groups=top_250/items'
        self.topmusic_link = 'https://www.imdb.com/search/title?title_type=feature&genres=music&groups=top_250/items'
        self.topmystery_link = 'https://www.imdb.com/search/title?title_type=feature&genres=mystery&groups=top_250/items'
        self.topromance_link = 'https://www.imdb.com/search/title?title_type=feature&genres=romance&groups=top_250/items'
        self.topsci_fi_link = 'https://www.imdb.com/search/title?title_type=feature&genres=sci_fi&groups=top_250/items'
        self.topsport_link = 'https://www.imdb.com/search/title?title_type=feature&genres=sport&groups=top_250/items'
        self.topthriller_link = 'https://www.imdb.com/search/title?title_type=feature&genres=thriller&groups=top_250/items'
        self.topwar_link = 'https://www.imdb.com/search/title?title_type=feature&genres=war&groups=top_250/items'
        self.topwestern_link = 'https://www.imdb.com/search/title?title_type=feature&genres=western&groups=top_250/items'
################# Top250 IMDB Lists ####################

################# Collections ####################
        self.survival_link = 'https://api.trakt.tv/users/istoit/lists/movies-to-make-you-rethink-your-survival-plan/items'
        self.vacation_link = 'https://api.trakt.tv/users/istoit/lists/movies-to-make-you-cancel-that-vacation/items'
        self.move_link = 'https://api.trakt.tv/users/istoit/lists/movies-to-make-you-pick-up-and-move/items'
        self.parenthood_link = 'https://api.trakt.tv/users/istoit/lists/movies-to-make-you-reconsider-parenthood/items'
        self.fairytale_link = 'https://api.trakt.tv/users/istoit/lists/fairy-tales/items'
        self.sports_link = 'https://api.trakt.tv/users/istoit/lists/sport-movies/items'
        self.crime_link = 'https://api.trakt.tv/users/istoit/lists/crime/items'
        self.alien_link = 'https://api.trakt.tv/users/istoit/lists/alien-invasion/items'
        self.psychological_link = 'https://api.trakt.tv/users/istoit/lists/psychological-thrillers/items'
        self.epic_link = 'https://api.trakt.tv/users/istoit/lists/epic/items'
        self.coen_link = 'https://api.trakt.tv/users/istoit/lists/coen-brothers/items'
        self.tarantino_link = 'https://api.trakt.tv/users/istoit/lists/tarantino-greats/items'
        self.cyber_link = 'https://www.imdb.com/search/title?count=100&keywords=cyberpunk&num_votes=3000,&title_type=feature&ref_=gnr_kw_cy,desc&count=40&start=1'
        self.espionage_link = 'https://www.imdb.com/search/title?count=100&keywords=espionage&num_votes=3000,&title_type=feature&ref_=gnr_kw_es,desc&count=40&start=1'
        self.spy_link = 'https://www.imdb.com/list/ls066367722/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.femme_link = 'https://www.imdb.com/search/title?count=100&keywords=femme-fatale&num_votes=3000,&title_type=feature&ref_=gnr_kw_ff,desc&count=40&start=1'
        self.futuristic_link = 'https://www.imdb.com/search/title?count=100&keywords=futuristic&num_votes=3000,&title_type=feature&ref_=gnr_kw_fu,desc&count=40&start=1'
        self.gangster_link = 'https://www.imdb.com/list/ls066176690/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.heist_link = 'https://www.imdb.com/search/title?count=100&keywords=heist&num_votes=3000,&title_type=feature&ref_=gnr_kw_he,desc&count=40&start=1'
        self.monsters_link = 'https://api.trakt.tv/users/istoit/lists/monsters/items'
        self.music_link = 'https://www.imdb.com/list/ls066191116/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.apocalypse_link = 'https://www.imdb.com/search/title?count=100&keywords=post-apocalypse&num_votes=3000,&title_type=feature&ref_=gnr_kw_pp,desc&count=40&start=1'
        self.revenge_link = 'https://www.imdb.com/list/ls066797820/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.satire_link = 'https://www.imdb.com/search/title?count=100&keywords=satire&num_votes=3000,&title_type=feature&ref_=gnr_kw_sa,desc&count=40&start=1'
        self.slasher_link = 'https://www.imdb.com/search/title?count=100&keywords=slasher&num_votes=3000,&title_type=feature&ref_=gnr_kw_sl,desc&count=40&start=1'
        self.killer_link = 'https://www.imdb.com/list/ls063841856/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.spoof_link = 'https://www.imdb.com/search/title?count=100&keywords=spoof&num_votes=3000,&title_type=feature&ref_=gnr_kw_sf,desc&count=40&start=1'
        self.superhero_link = 'https://www.imdb.com/search/title?count=100&keywords=superhero&num_votes=3000,&title_type=feature&ref_=gnr_kw_su,desc&count=40&start=1'
        self.supernatural_link = 'https://www.imdb.com/search/title?count=100&keywords=supernatural&num_votes=3000,&title_type=feature&ref_=gnr_kw_sn,desc&count=40&start=1'
        self.tech_link = 'https://www.imdb.com/search/title?count=100&keywords=tech-noir&num_votes=3000,&title_type=feature&ref_=gnr_kw_tn,desc&count=40&start=1'
        self.time_link = 'https://www.imdb.com/search/title?count=100&keywords=time-travel&num_votes=3000,&title_type=feature&ref_=gnr_kw_tt,desc&count=40&start=1'
        self.imdb44_link = 'https://www.imdb.com/list/ls066184124/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.twist_link = 'https://www.imdb.com/list/ls066370089/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.parody_link = 'https://www.imdb.com/search/title?count=100&keywords=parody&num_votes=3000,&title_type=feature&ref_=gnr_kw_pd,desc&count=40&start=1'
        self.biker_link = 'https://www.imdb.com/search/title?count=100&keywords=biker&num_votes=3000,&title_type=feature&ref_=gnr_kw_bi,desc&count=40&start=1'
        self.caper_link = 'https://www.imdb.com/search/title?count=100&keywords=caper&num_votes=3000,&title_type=feature&ref_=gnr_kw_ca,desc&count=40&start=1'
        self.business_link = 'https://www.imdb.com/search/title?count=100&keywords=business&num_votes=3000,&title_type=feature&ref_=gnr_kw_bu,desc&count=40&start=1'
        self.chick_link = 'https://www.imdb.com/search/title?count=100&keywords=chick-flick&num_votes=3000,&title_type=feature&ref_=gnr_kw_cf,desc&count=40&start=1'
        self.steampunk_link = 'https://www.imdb.com/search/title?count=100&keywords=steampunk&num_votes=3000,&title_type=feature&ref_=gnr_kw_sk,desc&count=40&start=1'
        self.mock_link = 'https://www.imdb.com/search/title?count=100&keywords=mockumentary&num_votes=3000,&title_type=feature&ref_=gnr_kw_mo,desc&count=40&start=1'
        self.mot_link = 'https://www.imdb.com/list/ls066222382/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.competition_link = 'https://www.imdb.com/search/title?count=100&keywords=competition&num_votes=3000,&title_type=feature&ref_=gnr_kw_cp,desc&count=40&start=1'
        self.cult_link = 'https://www.imdb.com/search/title?count=100&keywords=cult&num_votes=3000,&title_type=feature&ref_=gnr_kw_cu,desc&count=40&start=1'
        self.breaking_link = 'https://www.imdb.com/search/title?count=100&keywords=breaking-the-fourth-wall&num_votes=3000,&title_type=feature&ref_=gnr_kw_bw,desc&count=40&start=1'
        self.bmovie_link = 'https://www.imdb.com/search/title?count=100&keywords=b-movie&num_votes=3000,&title_type=feature&ref_=gnr_kw_bm,desc&count=40&start=1'
        self.anime_link = 'https://www.imdb.com/search/title?count=100&genres=animation&keywords=anime&num_votes=1000,&explore=title_type&ref_=gnr_kw_an,desc&count=40&start=1'
        self.neo_link = 'https://www.imdb.com/search/title?count=100&keywords=neo-noir&num_votes=3000,&title_type=feature&ref_=gnr_kw_nn,desc&count=40&start=1'
        self.farce_link = 'https://www.imdb.com/search/title?count=100&keywords=farce&num_votes=3000,&title_type=feature&ref_=gnr_kw_fa,desc&count=40&start=1'
        self.vr_link = 'https://www.imdb.com/search/title?count=100&keywords=virtual-reality&num_votes=3000,&title_type=feature&ref_=gnr_kw_vr,desc&count=40&start=1'
        self.dystopia_link = 'https://www.imdb.com/search/title?count=100&keywords=dystopia&num_votes=3000,&title_type=feature&ref_=gnr_kw_dy,desc&count=40&start=1'
        self.avant_link = 'https://www.imdb.com/search/title?count=100&keywords=avant-garde&num_votes=3000,&title_type=feature&ref_=gnr_kw_ag,desc&count=40&start=1'
        # self.halloween_link = 'https://www.imdb.com/search/title?count=100&keywords=halloween&num_votes=3000,&title_type=feature&ref_=gnr_kw_ag,desc&count=40&start=1'
        self.xmass_link = 'https://www.imdb.com/search/title?count=100&keywords=christmas&num_votes=3000,&title_type=feature&ref_=gnr_kw_ag,desc&count=40&start=1'
        self.bio_link = 'https://www.imdb.com/list/ls057785252/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.true_link = 'https://www.imdb.com/search/title?count=100&keywords=based-on-true-story&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.drugs_link = 'https://www.imdb.com/list/ls066788382/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.dc_link = 'https://www.imdb.com/search/title?count=100&keywords=dc-comics&sort=alpha,asc&mode=detail&page=1&title_type=movie%2CtvMovie&ref_=kw_ref_typ=dc-comics%2Csuperhero&mode=detail&page=1&title_type=video%2Cmovie%2CtvMovie&ref_=kw_ref_typ&sort=alpha,asc'
        self.marvel_link = 'https://www.imdb.com/search/title?count=100&keywords=marvel-comics&mode=detail&page=1&title_type=movie,tvMovie&sort=alpha,asc&ref_=kw_ref_typ'
        self.disney_link = 'https://www.imdb.com/list/ls000013316/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.private_link = 'https://www.imdb.com/list/ls003062015/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.sci_link = 'https://www.imdb.com/list/ls009668082/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.teen_link = 'https://www.imdb.com/list/ls066113037/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.nature_link = 'https://www.imdb.com/list/ls064685738/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.sleeper_link = 'https://www.imdb.com/list/ls027822154/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.star_link = 'https://www.imdb.com/search/title?count=100&keywords=star-wars&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.bond_link = 'https://www.imdb.com/search/title?count=100&keywords=official-james-bond-series'
################# /Collections ####################

################# The Movie Chest ####################
        self.imdb1_link = 'http://www.imdb.com/list/ls068378568/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb2_link = 'http://www.imdb.com/list/ls068149653/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb3_link = 'http://www.imdb.com/list/ls068611765/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb4_link = 'http://www.imdb.com/list/ls064420276/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb5_link = 'http://www.imdb.com/list/ls068357194/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb6_link = 'http://www.imdb.com/list/ls025535788/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb7_link = 'http://www.imdb.com/list/ls066920520/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb8_link = 'http://www.imdb.com/list/ls025535170/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb9_link = 'http://www.imdb.com/list/ls068149239/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb10_link = 'http://www.imdb.com/list/ls062383146/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb11_link = 'http://www.imdb.com/list/ls064861637/?view=detail&sort=date_added,desc&title_type=movie,tvMovie&start=1'
        self.imdb12_link = 'http://www.imdb.com/list/ls062397638/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb13_link = 'http://www.imdb.com/list/ls021029406/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb14_link = 'http://www.imdb.com/list/ls068611532/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb15_link = 'http://www.imdb.com/list/ls068357301/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb16_link = 'http://www.imdb.com/list/ls068378545/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb17_link = 'http://www.imdb.com/list/ls020817082/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb18_link = 'http://www.imdb.com/list/ls020020591/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb19_link = 'http://www.imdb.com/list/ls062631100/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb20_link = 'http://www.imdb.com/list/ls025052797/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb21_link = 'http://www.imdb.com/list/ls021022434/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb22_link = 'http://www.imdb.com/list/ls068611122/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb23_link = 'http://www.imdb.com/list/ls021553769/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb24_link = 'http://www.imdb.com/list/ls068180952/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb25_link = 'http://www.imdb.com/list/ls068127829/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb26_link = 'http://www.imdb.com/list/ls062342107/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb27_link = 'http://www.imdb.com/list/ls062342447/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb28_link = 'http://www.imdb.com/list/ls020822170/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb29_link = 'http://www.imdb.com/list/ls066981315/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb30_link = 'http://www.imdb.com/list/ls062385060/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb31_link = 'http://www.imdb.com/list/ls068121716/?view=detail&sort=date_added,desc&title_type=movie,tvMovie&start=1'
        self.imdb32_link = 'http://www.imdb.com/list/ls068125553/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb33_link = 'http://www.imdb.com/list/ls068125506/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb34_link = 'http://www.imdb.com/list/ls027396970/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb35_link = 'http://www.imdb.com/list/ls068579013/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb36_link = 'http://www.imdb.com/list/ls062383589/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb37_link = 'http://www.imdb.com/list/ls062308457/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb38_link = 'http://www.imdb.com/list/ls066987111/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb39_link = 'http://www.imdb.com/list/ls068235832/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb40_link = 'http://www.imdb.com/list/ls068378573/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb41_link = 'http://www.imdb.com/list/ls068121593/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb42_link = 'http://www.imdb.com/list/ls062628411/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb43_link = 'http://www.imdb.com/list/ls020822780/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb44_link = 'http://www.imdb.com/list/ls021124461/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb45_link = 'http://www.imdb.com/list/ls027010992/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb46_link = 'http://www.imdb.com/list/ls021536537/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb47_link = 'http://www.imdb.com/list/ls068125014/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb48_link = 'http://www.imdb.com/list/ls068125626/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb49_link = 'http://www.imdb.com/list/ls025714819/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb50_link = 'http://www.imdb.com/list/ls068629589/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb51_link = 'http://www.imdb.com/list/ls066920006/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb52_link = 'http://www.imdb.com/list/ls068206439/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb53_link = 'http://www.imdb.com/list/ls062350563/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb54_link = 'http://www.imdb.com/list/ls025476090/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb55_link = 'http://www.imdb.com/list/ls068357382/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb56_link = 'http://www.imdb.com/list/ls068281386/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb57_link = 'http://www.imdb.com/list/ls068237089/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb58_link = 'http://www.imdb.com/list/ls020817511/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb59_link = 'http://www.imdb.com/list/ls068121011/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb60_link = 'http://www.imdb.com/list/ls025052109/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb61_link = 'http://www.imdb.com/list/ls062397839/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb62_link = 'http://www.imdb.com/list/ls068121901/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb63_link = 'http://www.imdb.com/list/ls020817577/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb64_link = 'http://www.imdb.com/list/ls066981095/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb65_link = 'http://www.imdb.com/list/ls068127865/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb66_link = 'http://www.imdb.com/list/ls068611545/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb67_link = 'http://www.imdb.com/list/ls068127923/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb68_link = 'http://www.imdb.com/list/ls027803647/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb69_link = 'http://www.imdb.com/list/ls064861302/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb70_link = 'http://www.imdb.com/list/ls025535794/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb71_link = 'http://www.imdb.com/list/ls068120888/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb72_link = 'http://www.imdb.com/list/ls062147615/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb73_link = 'http://www.imdb.com/list/ls068127811/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb74_link = 'http://www.imdb.com/list/ls025770015/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb75_link = 'http://www.imdb.com/list/ls064468734/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb76_link = 'http://www.imdb.com/list/ls066940425/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb77_link = 'http://www.imdb.com/list/ls068120998/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb78_link = 'http://www.imdb.com/list/ls068378026/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb79_link = 'http://www.imdb.com/list/ls068378091/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb80_link = 'http://www.imdb.com/list/ls068378067/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb81_link = 'http://www.imdb.com/list/ls068378532/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb82_link = 'http://www.imdb.com/list/ls068379883/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb83_link = 'http://www.imdb.com/list/ls066987240/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb84_link = 'http://www.imdb.com/list/ls025013860/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb85_link = 'http://www.imdb.com/list/ls068171557/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb86_link = 'http://www.imdb.com/list/ls020559815/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb87_link = 'http://www.imdb.com/list/ls068148722/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb88_link = 'http://www.imdb.com/list/ls021199581/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb89_link = 'http://www.imdb.com/list/ls068148158/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb90_link = 'http://www.imdb.com/list/ls068180906/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb91_link = 'http://www.imdb.com/list/ls020558058/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb92_link = 'http://www.imdb.com/list/ls066809103/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb93_link = 'http://www.imdb.com/list/ls062364634/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb94_link = 'http://www.imdb.com/list/ls068357601/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb95_link = 'http://www.imdb.com/list/ls025052166/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb96_link = 'http://www.imdb.com/list/ls068180423/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb97_link = 'http://www.imdb.com/list/ls068121722/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb98_link = 'http://www.imdb.com/list/ls068121482/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb99_link = 'http://www.imdb.com/list/ls068149622/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb100_link = 'http://www.imdb.com/list/ls068125515/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb101_link = 'http://www.imdb.com/list/ls021122966/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb102_link = 'http://www.imdb.com/list/ls068237506/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb103_link = 'http://www.imdb.com/list/ls068148753/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb104_link = 'http://www.imdb.com/list/ls068378081/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb105_link = 'http://www.imdb.com/list/ls062344080/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb106_link = 'http://www.imdb.com/list/ls020255560/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb107_link = 'http://www.imdb.com/list/ls062382738/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb108_link = 'http://www.imdb.com/list/ls068611588/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb109_link = 'http://www.imdb.com/list/ls068611770/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb110_link = 'http://www.imdb.com/list/ls025756159/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb111_link = 'http://www.imdb.com/list/ls020559885/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb112_link = 'http://www.imdb.com/list/ls068149252/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb113_link = 'http://www.imdb.com/list/ls027750478/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb114_link = 'http://www.imdb.com/list/ls062364491/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb115_link = 'http://www.imdb.com/list/ls066987613/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb116_link = 'http://www.imdb.com/list/ls068149613/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb117_link = 'http://www.imdb.com/list/ls068611179/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb118_link = 'http://www.imdb.com/list/ls020559982/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb119_link = 'http://www.imdb.com/list/ls066920504/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb120_link = 'http://www.imdb.com/list/ls066920143/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb121_link = 'http://www.imdb.com/list/ls066920709/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb122_link = 'http://www.imdb.com/list/ls025659539/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb123_link = 'http://www.imdb.com/list/ls062785596/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb124_link = 'http://www.imdb.com/list/ls025013844/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb125_link = 'http://www.imdb.com/list/ls027399642/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb126_link = 'http://www.imdb.com/list/ls025756125/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb127_link = 'http://www.imdb.com/list/ls068121021/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb128_link = 'http://www.imdb.com/list/ls066985623/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb129_link = 'http://www.imdb.com/list/ls066945033/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb130_link = 'http://www.imdb.com/list/ls068127406/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb131_link = 'http://www.imdb.com/list/ls068148539/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb132_link = 'http://www.imdb.com/list/ls068149650/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb133_link = 'http://www.imdb.com/list/ls068237093/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb134_link = 'http://www.imdb.com/list/ls062628498/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb135_link = 'http://www.imdb.com/list/ls062383177/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb136_link = 'http://www.imdb.com/list/ls068393041/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb137_link = 'http://www.imdb.com/list/ls068281621/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb138_link = 'http://www.imdb.com/list/ls068180623/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb139_link = 'http://www.imdb.com/list/ls062350759/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb140_link = 'http://www.imdb.com/list/ls068127413/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb141_link = 'http://www.imdb.com/list/ls025535768/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb142_link = 'http://www.imdb.com/list/ls068180487/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb143_link = 'http://www.imdb.com/list/ls068378557/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb144_link = 'http://www.imdb.com/list/ls068235847/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb145_link = 'http://www.imdb.com/list/ls068611719/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb146_link = 'http://www.imdb.com/list/ls020020521/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb147_link = 'http://www.imdb.com/list/ls068121770/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb148_link = 'http://www.imdb.com/list/ls068281214/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb149_link = 'http://www.imdb.com/list/ls021024339/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb150_link = 'http://www.imdb.com/list/ls025013823/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb151_link = 'http://www.imdb.com/list/ls068611166/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb152_link = 'http://www.imdb.com/list/ls021533491/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb153_link = 'http://www.imdb.com/list/ls062626796/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb154_link = 'http://www.imdb.com/list/ls025535746/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb155_link = 'http://www.imdb.com/list/ls068378513/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb156_link = 'http://www.imdb.com/list/ls068611186/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb157_link = 'http://www.imdb.com/list/ls068127976/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb158_link = 'http://www.imdb.com/list/ls068611794/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb159_link = 'http://www.imdb.com/list/ls020837498/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb160_link = 'http://www.imdb.com/list/ls025052744/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb161_link = 'http://www.imdb.com/list/ls068378079/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb162_link = 'http://www.imdb.com/list/ls068127280/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb163_link = 'http://www.imdb.com/list/ls068127267/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb164_link = 'http://www.imdb.com/list/ls068121494/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb165_link = 'http://www.imdb.com/list/ls020832135/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb166_link = 'http://www.imdb.com/list/ls068357345/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb167_link = 'http://www.imdb.com/list/ls021533884/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb168_link = 'http://www.imdb.com/list/ls068357364/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb169_link = 'http://www.imdb.com/list/ls025013969/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb170_link = 'http://www.imdb.com/list/ls068127499/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb171_link = 'http://www.imdb.com/list/ls066985320/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb172_link = 'http://www.imdb.com/list/ls068611772/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb173_link = 'http://www.imdb.com/list/ls025876353/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb174_link = 'http://www.imdb.com/list/ls020840979/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb175_link = 'http://www.imdb.com/list/ls062397114/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb176_link = 'http://www.imdb.com/list/ls027435712/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb177_link = 'http://www.imdb.com/list/ls068378009/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb178_link = 'http://www.imdb.com/list/ls025052713/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb179_link = 'http://www.imdb.com/list/ls027392005/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb180_link = 'http://www.imdb.com/list/ls020817131/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb181_link = 'http://www.imdb.com/list/ls062147286/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb182_link = 'http://www.imdb.com/list/ls027605507/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb183_link = 'http://www.imdb.com/list/ls066987428/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb184_link = 'http://www.imdb.com/list/ls068378501/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb185_link = 'http://www.imdb.com/list/ls068379841/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb186_link = 'http://www.imdb.com/list/ls020860923/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb187_link = 'http://www.imdb.com/list/ls066964882/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb188_link = 'http://www.imdb.com/list/ls068148709/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb189_link = 'http://www.imdb.com/list/ls066985395/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb190_link = 'http://www.imdb.com/list/ls025756791/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb191_link = 'http://www.imdb.com/list/ls068235882/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb192_link = 'http://www.imdb.com/list/ls025052544/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb193_link = 'http://www.imdb.com/list/ls066920068/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb194_link = 'http://www.imdb.com/list/ls025052777/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb195_link = 'http://www.imdb.com/list/ls068379836/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb196_link = 'http://www.imdb.com/list/ls062008395/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb197_link = 'http://www.imdb.com/list/ls066987307/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb198_link = 'http://www.imdb.com/list/ls025013934/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb199_link = 'http://www.imdb.com/list/ls021590727/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb200_link = 'http://www.imdb.com/list/ls068237028/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb201_link = 'http://www.imdb.com/list/ls068357348/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb202_link = 'http://www.imdb.com/list/ls066968822/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb203_link = 'http://www.imdb.com/list/ls068149286/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb204_link = 'http://www.imdb.com/list/ls068125653/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb205_link = 'http://www.imdb.com/list/ls068121700/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb206_link = 'http://www.imdb.com/list/ls062346792/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb207_link = 'http://www.imdb.com/list/ls068611724/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb208_link = 'http://www.imdb.com/list/ls066940926/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb209_link = 'http://www.imdb.com/list/ls062364756/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb210_link = 'http://www.imdb.com/list/ls062343380/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb211_link = 'http://www.imdb.com/list/ls021124908/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb212_link = 'http://www.imdb.com/list/ls027531965/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb213_link = 'http://www.imdb.com/list/ls062399644/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb214_link = 'http://www.imdb.com/list/ls068148595/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb215_link = 'http://www.imdb.com/list/ls064420695/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb216_link = 'http://www.imdb.com/list/ls068149631/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb217_link = 'http://www.imdb.com/list/ls068127886/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb218_link = 'http://www.imdb.com/list/ls068180465/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb219_link = 'http://www.imdb.com/list/ls068148576/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb220_link = 'http://www.imdb.com/list/ls068148710/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb221_link = 'http://www.imdb.com/list/ls025013870/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb222_link = 'http://www.imdb.com/list/ls025052706/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb223_link = 'http://www.imdb.com/list/ls066920764/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb224_link = 'http://www.imdb.com/list/ls027531819/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb225_link = 'http://www.imdb.com/list/ls068127872/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb226_link = 'http://www.imdb.com/list/ls062628853/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb227_link = 'http://www.imdb.com/list/ls020817067/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb228_link = 'http://www.imdb.com/list/ls068121535/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb229_link = 'http://www.imdb.com/list/ls020822735/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb230_link = 'http://www.imdb.com/list/ls025052722/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb231_link = 'http://www.imdb.com/list/ls066987766/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb232_link = 'http://www.imdb.com/list/ls068125395/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb233_link = 'http://www.imdb.com/list/ls068148545/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb234_link = 'http://www.imdb.com/list/ls021568747/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb235_link = 'http://www.imdb.com/list/ls068180914/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb236_link = 'http://www.imdb.com/list/ls066920637/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb237_link = 'http://www.imdb.com/list/ls068148783/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb237_link = 'http://www.imdb.com/list/ls068149237/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb238_link = 'http://www.imdb.com/list/ls062399815/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb239_link = 'http://www.imdb.com/list/ls066985205/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb240_link = 'http://www.imdb.com/list/ls062397715/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb241_link = 'http://www.imdb.com/list/ls068149225/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb242_link = 'http://www.imdb.com/list/ls068121959/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb243_link = 'http://www.imdb.com/list/ls066809098/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb244_link = 'http://www.imdb.com/list/ls068120847/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb245_link = 'http://www.imdb.com/list/ls068379876/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb246_link = 'http://www.imdb.com/list/ls068149661/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb247_link = 'http://www.imdb.com/list/ls021024111/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb248_link = 'http://www.imdb.com/list/ls025758775/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb249_link = 'http://www.imdb.com/list/ls020860830/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb250_link = 'http://www.imdb.com/list/ls068121552/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb251_link = 'http://www.imdb.com/list/ls068127421/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb252_link = 'http://www.imdb.com/list/ls025052780/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb253_link = 'http://www.imdb.com/list/ls062342317/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb254_link = 'http://www.imdb.com/list/ls068128422/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb255_link = 'http://www.imdb.com/list/ls068127853/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb256_link = 'http://www.imdb.com/list/ls068121442/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb257_link = 'http://www.imdb.com/list/ls020558000/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb258_link = 'http://www.imdb.com/list/ls068127908/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb259_link = 'http://www.imdb.com/list/ls068127930/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb260_link = 'http://www.imdb.com/list/ls066987885/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb261_link = 'http://www.imdb.com/list/ls066920305/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb262_link = 'http://www.imdb.com/list/ls062382393/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb263_link = 'http://www.imdb.com/list/ls068121524/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb264_link = 'http://www.imdb.com/list/ls062641169/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb265_link = 'http://www.imdb.com/list/ls068121042/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
################# /The Movie Chest ####################

################# Movie Mosts ####################
        self.played1_link = 'https://api.trakt.tv/movies/played/weekly?limit=40&page=1'
        self.played2_link = 'https://api.trakt.tv/movies/played/monthly?limit=40&page=1'
        self.played3_link = 'https://api.trakt.tv/movies/played/yearly?limit=40&page=1'
        self.played4_link = 'https://api.trakt.tv/movies/played/all?limit=40&page=1'
        self.collected1_link = 'https://api.trakt.tv/movies/collected/weekly?limit=40&page=1'
        self.collected2_link = 'https://api.trakt.tv/movies/collected/monthly?limit=40&page=1'
        self.collected3_link = 'https://api.trakt.tv/movies/collected/yearly?limit=40&page=1'
        self.collected4_link = 'https://api.trakt.tv/movies/collected/all?limit=40&page=1'
        self.watched1_link = 'https://api.trakt.tv/movies/watched/weekly?limit=40&page=1'
        self.watched2_link = 'https://api.trakt.tv/movies/watched/monthly?limit=40&page=1'
        self.watched3_link = 'https://api.trakt.tv/movies/watched/yearly?limit=40&page=1'
        self.watched4_link = 'https://api.trakt.tv/movies/watched/all?limit=40&page=1'
################# /Movie Mosts ####################

    def get(self, url, idx=True, create_directory=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass

            try:
                u = urlparse.urlparse(url).netloc.lower()
            except:
                pass

            if u in self.trakt_link and '/users/' in url:
                try:
                    if url == self.trakthistory_link:
                        raise Exception()
                    if not '/users/me/' in url:
                        raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user):
                        raise Exception()
                    self.list = cache.get(self.trakt_list, 720, url, self.trakt_user)
                except:
                    self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)

                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: utils.title_key(k['title']))

                if idx == True:
                    self.worker()

            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx == True:
                    self.worker(level=0)

            elif u in self.trakt_link and '/sync/playback/' in url:
                self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)
                if idx == True:
                    self.worker()

            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx == True:
                    self.worker()

            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 0, url)
                if idx == True:
                    self.worker()

            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 24, url)
                if idx == True:
                    self.worker()

            if idx == True and create_directory == True:
                self.movieDirectory(self.list)
            return self.list
        except:
            pass

    def widget(self):
        setting = control.setting('movie.widget')

        if setting == '2':
            self.get(self.trending_link)
        elif setting == '3':
            self.get(self.popular_link)
        elif setting == '4':
            self.get(self.theaters_link)
        elif setting == '5':
            self.get(self.added_link)
        else:
            self.get(self.featured_link)

    def search(self):

        navigator.navigator().addDirectoryItem(32603, 'movieSearchnew', 'search.png', 'DefaultMovies.png')
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()

        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS movies (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
        except:
            pass

        dbcur.execute("SELECT * FROM movies ORDER BY ID DESC")
        lst = []

        delete_option = False
        for (id, term) in dbcur.fetchall():
            if term not in str(lst):
                delete_option = True
                navigator.navigator().addDirectoryItem(term.title(), 'movieSearchterm&name=%s' % term, 'search.png', 'DefaultMovies.png')
                lst += [(term)]
        dbcur.close()

        if delete_option:
            navigator.navigator().addDirectoryItem(32605, 'clearCacheSearch&select=movies', 'tools.png', 'DefaultAddonProgram.png')

        navigator.navigator().endDirectory(False)

    def search_new(self):
            control.idle()

            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t)
            k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''):
                return
            q = q.lower()
            try:
                from sqlite3 import dbapi2 as database
            except:
                from pysqlite2 import dbapi2 as database

            dbcon = database.connect(control.searchFile)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM movies WHERE term = ?", (q,))
            dbcur.execute("INSERT INTO movies VALUES (?,?)", (None, q))
            dbcon.commit()
            dbcur.close()
            url = self.search_link + urllib.quote_plus(q)
            if int(control.getKodiVersion()) >= 18:
                self.get(url)
            else:
                url = '%s?action=moviePage&url=%s' % (sys.argv[0], urllib.quote_plus(url))
                control.execute('Container.Update(%s)' % url)

    def search_term(self, q):
            control.idle()
            q = q.lower()

            try:
                from sqlite3 import dbapi2 as database
            except:
                from pysqlite2 import dbapi2 as database

            dbcon = database.connect(control.searchFile)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM movies WHERE term = ?", (q,))
            dbcur.execute("INSERT INTO movies VALUES (?,?)", (None, q))
            dbcon.commit()
            dbcur.close()
            url = self.search_link + urllib.quote_plus(q)
            if int(control.getKodiVersion()) >= 18:
                self.get(url)
            else:
                url = '%s?action=moviePage&url=%s' % (sys.argv[0], urllib.quote_plus(url))
                control.execute('Container.Update(%s)' % url)

    def person(self):
        try:
            control.idle()

            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t)
            k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''):
                return

            url = self.persons_link + urllib.quote_plus(q)
            if int(control.getKodiVersion()) >= 18:
                self.persons(url)
            else:
                url = '%s?action=moviePersons&url=%s' % (sys.argv[0], urllib.quote_plus(url))
                control.execute('Container.Update(%s)' % url)
        except:
            return

    def genres(self):
        genres = [
            ('Action', 'action', True),
            ('Adventure', 'adventure', True),
            ('Animation', 'animation', True),
            ('Anime', 'anime', False),
            ('Biography', 'biography', True),
            ('Comedy', 'comedy', True),
            ('Crime', 'crime', True),
            ('Documentary', 'documentary', True),
            ('Drama', 'drama', True),
            ('Family', 'family', True),
            ('Fantasy', 'fantasy', True),
            ('History', 'history', True),
            ('Horror', 'horror', True),
            ('Music ', 'music', True),
            ('Musical', 'musical', True),
            ('Mystery', 'mystery', True),
            ('Romance', 'romance', True),
            ('Science Fiction', 'sci_fi', True),
            ('Sport', 'sport', True),
            ('Thriller', 'thriller', True),
            ('War', 'war', True),
            ('Western', 'western', True)
        ]

        for i in genres:
            self.list.append(
                {
                    'name': cleangenre.lang(i[0], self.lang),
                    'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1],
                    'image': 'genres.png',
                    'action': 'movies'
                })

        self.addDirectory(self.list)
        return self.list

    def languages(self):
        languages = [
            ('Arabic', 'ar'),
            ('Bosnian', 'bs'),
            ('Bulgarian', 'bg'),
            ('Chinese', 'zh'),
            ('Croatian', 'hr'),
            ('Dutch', 'nl'),
            ('English', 'en'),
            ('Finnish', 'fi'),
            ('French', 'fr'),
            ('German', 'de'),
            ('Greek', 'el'),
            ('Hebrew', 'he'),
            ('Hindi ', 'hi'),
            ('Hungarian', 'hu'),
            ('Icelandic', 'is'),
            ('Italian', 'it'),
            ('Japanese', 'ja'),
            ('Korean', 'ko'),
            ('Macedonian', 'mk'),
            ('Norwegian', 'no'),
            ('Persian', 'fa'),
            ('Polish', 'pl'),
            ('Portuguese', 'pt'),
            ('Punjabi', 'pa'),
            ('Romanian', 'ro'),
            ('Russian', 'ru'),
            ('Serbian', 'sr'),
            ('Slovenian', 'sl'),
            ('Spanish', 'es'),
            ('Swedish', 'sv'),
            ('Turkish', 'tr'),
            ('Ukrainian', 'uk')
        ]

        for i in languages:
            self.list.append({'name': str(i[0]), 'url': self.language_link % i[1],
                              'image': 'languages.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def certifications(self):
        certificates = ['G', 'PG', 'PG-13', 'R', 'NC-17']

        for i in certificates:
            self.list.append({'name': str(i), 'url': self.certification_link % str(i),
                              'image': 'certificates.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def years(self):
        year = (self.datetime.strftime('%Y'))

        for i in range(int(year)-0, 1900, -1):
            self.list.append({'name': str(i), 'url': self.year_link % (
                str(i), str(i)), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            activity = trakt.getActivity()
        except:
            pass

        try:
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user):
                    raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass
        try:
            self.list = []
            if self.imdb_user == '':
                raise Exception()
            userlists += cache.get(self.imdb_user_list, 0, self.imdblists_link)
        except:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user):
                    raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except:
            pass

        self.list = userlists
        for i in range(0, len(self.list)):
            self.list[i].update({'image': 'userlists.png', 'action': 'movies'})
        self.addDirectory(self.list, queue=True)
        return self.list

    def trakt_list(self, url, user):
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q

            result = trakt.getTraktAsJson(u)

            items = []
            for i in result:
                try:
                    items.append(i['movie'])
                except:
                    pass
            if len(items) == 0:
                items = result
        except:
            return

        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            if not int(q['limit']) == len(items):
                raise Exception()
            q.update({'page': str(int(q['page']) + 1)})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = item['title']
                title = client.replaceHTMLCodes(title)

                year = item['year']
                year = re.sub('[^0-9]', '', str(year))

                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()

                imdb = item['ids']['imdb']
                if imdb == None or imdb == '':
                    raise Exception()
                imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

                tmdb = str(item.get('ids', {}).get('tmdb', 0))

                try:
                    premiered = item['released']
                except:
                    premiered = '0'
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'

                try:
                    genre = item['genres']
                except:
                    genre = '0'
                genre = [i.title() for i in genre]
                if genre == []:
                    genre = '0'
                genre = ' / '.join(genre)

                try:
                    duration = str(item['runtime'])
                except:
                    duration = '0'
                if duration == None:
                    duration = '0'

                try:
                    rating = str(item['rating'])
                except:
                    rating = '0'
                if rating == None or rating == '0.0':
                    rating = '0'

                try:
                    votes = str(item['votes'])
                except:
                    votes = '0'
                try:
                    votes = str(format(int(votes), ',d'))
                except:
                    pass
                if votes == None:
                    votes = '0'

                try:
                    mpaa = item['certification']
                except:
                    mpaa = '0'
                if mpaa == None:
                    mpaa = '0'

                try:
                    plot = item['overview']
                except:
                    plot = '0'
                if plot == None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)

                try:
                    tagline = item['tagline']
                except:
                    tagline = '0'
                if tagline == None:
                    tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)

                self.list.append(
                    {'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'genre': genre,
                     'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot,
                     'tagline': tagline, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'poster': '0', 'next': next})
            except:
                pass

        return self.list

    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
        except:
            pass

        for item in items:
            try:
                try:
                    name = item['list']['name']
                except:
                    name = item['name']
                name = client.replaceHTMLCodes(name)

                try:
                    url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except:
                    url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list

    def imdb_list(self, url):
        try:
            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' %
                                  i, (self.datetime - datetime.timedelta(days=int(i))).strftime('%Y-%m-%d'))

            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url), 'meta', ret='content', attrs={'property': 'pageId'})[0]

            if url == self.imdbwatchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url

            elif url == self.imdbwatchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist2_link % url

            result = client.request(url)

            result = result.replace('\n', ' ')

            items = client.parseDOM(result, 'div', attrs={'class': 'lister-item .+?'})
            items += client.parseDOM(result, 'div', attrs={'class': 'list_item.+?'})
        except:
            return

        try:
            next = client.parseDOM(result, 'a', ret='href', attrs={'class': '.+?ister-page-nex.+?'})

            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs={'class': 'pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]

            next = url.replace(urlparse.urlparse(url).query, urlparse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[1]
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = client.parseDOM(item, 'span', attrs={'class': 'lister-item-year.+?'})
                year += client.parseDOM(item, 'span', attrs={'class': 'year_type'})
                try:
                    year = re.compile('(\d{4})').findall(year)[0]
                except:
                    year = '0'
                year = year.encode('utf-8')

                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = imdb.encode('utf-8')

                try:
                    poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except:
                    poster = '0'
                if '/nopicture/' in poster:
                    poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try:
                    genre = client.parseDOM(item, 'span', attrs={'class': 'genre'})[0]
                except:
                    genre = '0'
                genre = ' / '.join([i.strip() for i in genre.split(',')])
                if genre == '':
                    genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try:
                    duration = re.findall('(\d+?) min(?:s|)', item)[-1]
                except:
                    duration = '0'
                duration = duration.encode('utf-8')

                rating = '0'
                try:
                    rating = client.parseDOM(item, 'span', attrs={'class': 'rating-rating'})[0]
                except:
                    pass
                try:
                    rating = client.parseDOM(rating, 'span', attrs={'class': 'value'})[0]
                except:
                    rating = '0'
                try:
                    rating = client.parseDOM(item, 'div', ret='data-value', attrs={'class': '.*?imdb-rating'})[0]
                except:
                    pass
                if rating == '' or rating == '-':
                    rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try:
                    votes = client.parseDOM(item, 'div', ret='title', attrs={'class': '.*?rating-list'})[0]
                except:
                    votes = '0'
                try:
                    votes = re.findall('\((.+?) vote(?:s|)\)', votes)[0]
                except:
                    votes = '0'
                if votes == '':
                    votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                try:
                    mpaa = client.parseDOM(item, 'span', attrs={'class': 'certificate'})[0]
                except:
                    mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED':
                    mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                try:
                    director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', item)[0]
                except:
                    director = '0'
                director = client.parseDOM(director, 'a')
                director = ' / '.join(director)
                if director == '':
                    director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try:
                    cast = re.findall('Stars(?:s|):(.+?)(?:\||</div>)', item)[0]
                except:
                    cast = '0'
                cast = client.replaceHTMLCodes(cast)
                cast = cast.encode('utf-8')
                cast = client.parseDOM(cast, 'a')
                if cast == []:
                    cast = '0'

                plot = '0'
                try:
                    plot = client.parseDOM(item, 'p', attrs={'class': 'text-muted'})[0]
                except:
                    pass
                try:
                    plot = client.parseDOM(item, 'div', attrs={'class': 'item_description'})[0]
                except:
                    pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                plot = re.sub('<.+?>|</.+?>', '', plot)
                if plot == '':
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'genre': genre,
                                  'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa,
                                  'director': director, 'cast': cast, 'plot': plot, 'tagline': '0', 'imdb': imdb,
                                  'tmdb': '0', 'tvdb': '0', 'poster': poster, 'next': next})
            except:
                pass

        return self.list

    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'div', attrs={'class': '.+?etail'})
        except:
            return

        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = client.parseDOM(item, 'img', ret='src')[0]
                # if not ('._SX' in image or '._SY' in image): raise Exception()
                image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'li', attrs={'class': 'ipl-zebra-list__item user-list'})
        except:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list

    def worker(self, level=1):
        self.meta = []
        total = len(self.list)

        self.fanart_tv_headers = {'api-key': 'NGQ4ZjJjMTU5MjZkNDNiNDQzNzc0MmNkOTY4ODc2ZjI='.decode('base64')}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})

        for i in range(0, total):
            self.list[i].update({'metacache': False})

        self.list = metacache.fetch(self.list, self.lang, self.user)

        for r in range(0, total, 40):
            threads = []
            for i in range(r, r+40):
                if i <= total:
                    threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            if self.meta:
                metacache.insert(self.meta)

        self.list = [i for i in self.list if not i['imdb'] == '0']

        self.list = metacache.local(self.list, self.tm_img_link, 'poster3', 'fanart2')

        if self.fanart_tv_user == '':
            for i in self.list:
                i.update({'clearlogo': '0', 'clearart': '0'})

    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True:
                raise Exception()

            imdb = self.list[i]['imdb']

            item = trakt.getMovieSummary(imdb)

            title = item.get('title')
            title = client.replaceHTMLCodes(title)

            originaltitle = title

            year = item.get('year', 0)
            year = re.sub('[^0-9]', '', str(year))

            imdb = item.get('ids', {}).get('imdb', '0')
            imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

            tmdb = str(item.get('ids', {}).get('tmdb', 0))

            premiered = item.get('released', '0')
            try:
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except:
                premiered = '0'

            genre = item.get('genres', [])
            genre = [x.title() for x in genre]
            genre = ' / '.join(genre).strip()
            if not genre:
                genre = '0'

            duration = str(item.get('Runtime', 0))

            rating = item.get('rating', '0')
            if not rating or rating == '0.0':
                rating = '0'

            votes = item.get('votes', '0')
            try:
                votes = str(format(int(votes), ',d'))
            except:
                pass

            mpaa = item.get('certification', '0')
            if not mpaa:
                mpaa = '0'

            tagline = item.get('tagline', '0')

            plot = item.get('overview', '0')

            people = trakt.getPeople(imdb, 'movies')

            director = writer = ''
            if 'crew' in people and 'directing' in people['crew']:
                director = ', '.join([director['person']['name'] for director in people['crew']
                                      ['directing'] if director['job'].lower() == 'director'])
            if 'crew' in people and 'writing' in people['crew']:
                writer = ', '.join([writer['person']['name'] for writer in people['crew']['writing']
                                    if writer['job'].lower() in ['writer', 'screenplay', 'author']])

            cast = []
            for person in people.get('cast', []):
                cast.append({'name': person['person']['name'], 'role': person['character']})
            cast = [(person['name'], person['role']) for person in cast]

            try:
                if self.lang == 'en' or self.lang not in item.get('available_translations', [self.lang]):
                    raise Exception()

                trans_item = trakt.getMovieTranslation(imdb, self.lang, full=True)

                title = trans_item.get('title') or title
                tagline = trans_item.get('tagline') or tagline
                plot = trans_item.get('overview') or plot
            except:
                pass

            try:
                artmeta = True
                #if self.fanart_tv_user == '': raise Exception()
                art = client.request(self.fanart_tv_art_link %
                                     imdb, headers=self.fanart_tv_headers, timeout='10', error=True)
                try:
                    art = json.loads(art)
                except:
                    artmeta = False
            except:
                pass

            try:
                poster2 = art['movieposter']
                poster2 = [x for x in poster2 if x.get('lang') == self.lang][::-1] + [x for x in poster2 if x.get(
                    'lang') == 'en'][::-1] + [x for x in poster2 if x.get('lang') in ['00', '']][::-1]
                poster2 = poster2[0]['url'].encode('utf-8')
            except:
                poster2 = '0'

            try:
                if 'moviebackground' in art:
                    fanart = art['moviebackground']
                else:
                    fanart = art['moviethumb']
                fanart = [x for x in fanart if x.get('lang') == self.lang][:: -1] + [x for x in fanart
                                                                                     if x.get('lang') == 'en'][:: -1] + [x for x in fanart if x.get('lang') in['00', '']][:: -1]
                fanart = fanart[0]['url'].encode('utf-8')
            except:
                fanart = '0'

            try:
                banner = art['moviebanner']
                banner = [x for x in banner if x.get('lang') == self.lang][:: -1] + [x for x in banner
                                                                                     if x.get('lang') == 'en'][:: -1] + [x for x in banner if x.get('lang') in['00', '']][:: -1]
                banner = banner[0]['url'].encode('utf-8')
            except:
                banner = '0'

            try:
                if 'hdmovielogo' in art:
                    clearlogo = art['hdmovielogo']
                else:
                    clearlogo = art['clearlogo']
                clearlogo = [x for x in clearlogo if x.get('lang') == self.lang][::-1] + [x for x in clearlogo if x.get(
                    'lang') == 'en'][::-1] + [x for x in clearlogo if x.get('lang') in ['00', '']][::-1]
                clearlogo = clearlogo[0]['url'].encode('utf-8')
            except:
                clearlogo = '0'

            try:
                if 'hdmovieclearart' in art:
                    clearart = art['hdmovieclearart']
                else:
                    clearart = art['clearart']
                clearart = [x for x in clearart if x.get('lang') == self.lang][::-1] + [x for x in clearart if x.get(
                    'lang') == 'en'][::-1] + [x for x in clearart if x.get('lang') in ['00', '']][::-1]
                clearart = clearart[0]['url'].encode('utf-8')
            except:
                clearart = '0'

            try:
                if self.tm_user == '':
                    raise Exception()

                art2 = client.request(self.tm_art_link % imdb, timeout='10', error=True)
                art2 = json.loads(art2)
            except:
                pass

            try:
                poster3 = art2['posters']
                poster3 = [x for x in poster3 if x.get('iso_639_1') == self.lang] + [x for x in poster3 if x.get(
                    'iso_639_1') == 'en'] + [x for x in poster3 if x.get('iso_639_1') not in [self.lang, 'en']]
                poster3 = [(x['width'], x['file_path']) for x in poster3]
                poster3 = [(x[0], x[1]) if x[0] < 300 else ('300', x[1]) for x in poster3]
                poster3 = self.tm_img_link % poster3[0]
                poster3 = poster3.encode('utf-8')
            except:
                poster3 = '0'

            try:
                fanart2 = art2['backdrops']
                fanart2 = [x for x in fanart2 if x.get('iso_639_1') == self.lang] + [x for x in fanart2 if x.get(
                    'iso_639_1') == 'en'] + [x for x in fanart2 if x.get('iso_639_1') not in [self.lang, 'en']]
                fanart2 = [x for x in fanart2 if x.get('width') == 1920] + [x for x in fanart2 if x.get('width') < 1920]
                fanart2 = [(x['width'], x['file_path']) for x in fanart2]
                fanart2 = [(x[0], x[1]) if x[0] < 1280 else ('1280', x[1]) for x in fanart2]
                fanart2 = self.tm_img_link % fanart2[0]
                fanart2 = fanart2.encode('utf-8')
            except:
                fanart2 = '0'

            item = {'title': title, 'originaltitle': originaltitle, 'year': year, 'imdb': imdb, 'tmdb': tmdb,
                    'poster': '0', 'poster2': poster2, 'poster3': poster3, 'banner': banner, 'fanart': fanart,
                    'fanart2': fanart2, 'clearlogo': clearlogo, 'clearart': clearart, 'premiered': premiered,
                    'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa,
                    'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}
            item = dict((k, v) for k, v in item.iteritems() if not v == '0')
            self.list[i].update(item)

            if artmeta == False:
                raise Exception()

            meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)
        except:
            pass

    def movieDirectory(self, items):
        if items == None or len(items) == 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()

        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        try:
            isOld = False
            control.item().getArt('type')
        except:
            isOld = True

        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'

        indicators = playcount.getMovieIndicators(
            refresh=True) if action == 'movies' else playcount.getMovieIndicators()

        playbackMenu = control.lang(32063).encode(
            'utf-8') if control.setting('hosts.mode') == '2' else control.lang(32064).encode('utf-8')

        watchedMenu = control.lang(32068).encode(
            'utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')

        unwatchedMenu = control.lang(32069).encode(
            'utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')

        queueMenu = control.lang(32065).encode('utf-8')

        traktManagerMenu = control.lang(32070).encode('utf-8')

        nextMenu = control.lang(32053).encode('utf-8')

        addToLibrary = control.lang(32551).encode('utf-8')

        clearProviders = control.lang(32081).encode('utf-8')

        findSimilar = control.lang(32100).encode('utf-8')

        infoMenu = control.lang(32101).encode('utf-8')

        for i in items:
            try:
                label = '%s (%s)' % (i['title'], i['year'])
                imdb, tmdb, title, year = i['imdb'], i['tmdb'], i['originaltitle'], i['year']
                sysname = urllib.quote_plus('%s (%s)' % (title, year))
                systitle = urllib.quote_plus(title)

                meta = dict((k, v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tmdb_id': tmdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(label))})
                #meta.update({'trailer': 'plugin://script.extendedinfo/?info=playtrailer&&id=%s' % imdb})
                if not 'duration' in i:
                    meta.update({'duration': '120'})
                elif i['duration'] == '0':
                    meta.update({'duration': '120'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except:
                    pass

                poster = [i[x] for x in ['poster3', 'poster', 'poster2'] if i.get(x, '0') != '0']
                poster = poster[0] if poster else addonPoster
                meta.update({'poster': poster})

                sysmeta = urllib.quote_plus(json.dumps(meta))

                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (
                    sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)

                path = '%s?action=play&title=%s&year=%s&imdb=%s' % (sysaddon, systitle, year, imdb)

                cm = []

                cm.append(
                    (findSimilar,
                     'ActivateWindow(10025,%s?action=movies&url=https://api.trakt.tv/movies/%s/related,return)' %
                     (sysaddon, imdb)))

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                if traktCredentials == True:
                    cm.append(
                        (traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' %
                         (sysaddon, sysname, imdb)))

                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                if isOld == True:
                    cm.append((infoMenu, 'Action(Info)'))

                cm.append(
                    (addToLibrary, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' %
                     (sysaddon, sysname, systitle, year, imdb, tmdb)))

                cm.append((clearProviders, 'RunPlugin(%s?action=clearCacheProviders)' % sysaddon))

                item = control.item(label=label)

                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster})

                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                else:
                    art.update({'banner': addonBanner})

                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})

                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})

                if settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                    item.setProperty('Fanart_Image', i['fanart2'])
                elif settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='Video', infoLabels=control.metadataClean(meta))

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                pass

        try:
            url = items[0]['next']
            if url == '':
                raise Exception()

            icon = control.addonNext()
            url = '%s?action=moviePage&url=%s' % (sysaddon, urllib.quote_plus(url))

            item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None:
                item.setProperty('Fanart_Image', addonFanart)

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        control.sleep(1000)
        views.setView('movies', {'skin.estuary': 55, 'skin.confluence': 500})

    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        queueMenu = control.lang(32065).encode('utf-8')

        playRandom = control.lang(32535).encode('utf-8')

        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath == None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib.quote_plus(i['url'])
                except:
                    pass

                cm = []

                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=movie&url=%s)' %
                           (sysaddon, urllib.quote_plus(i['url']))))

                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    cm.append((addToLibrary, 'RunPlugin(%s?action=moviesToLibrary&url=%s)' %
                               (sysaddon, urllib.quote_plus(i['context']))))
                except:
                    pass

                item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
