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

from resources.lib.modules import (cleangenre, client, control, metacache,
                                   playcount, trakt, views, workers)

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonFanart = control.addonFanart()


class boxsets:
    def __init__(self):
        self.boxset_list = []
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.tmdb_key = control.setting('tm.user')
        self.tmdb_link = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % ('%s', self.tmdb_key)
        self.tmdb_c_link = 'http://api.themoviedb.org/3/collection/%s?api_key=%s' % ('%s', self.tmdb_key)
        self.tmdb_info_link = 'http://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=credits,releases,external_ids' % ('%s', self.tmdb_key, 'en')
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tmdb_poster = 'http://image.tmdb.org/t/p/w500'
        self.tm_img_link = 'https://image.tmdb.org/t/p/w%s%s'
        self.tm_art_link = 'http://api.themoviedb.org/3/movie/%s/images?api_key=%s&language=en-US&include_image_language=en,%s,null' % (
            '%s', self.tmdb_key, 'en')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = str(control.setting('fanart.tv.user')) + str(control.setting('tm.user'))
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/movies/%s'
        self.imdbinfo = 'http://www.omdbapi.com/?i=%s&plot=short&r=json'

    def root(self):
        self.addDirectoryItem('Action', 'actionBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Adventure', 'adventureBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Animation', 'animationBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Comedy', 'comedyBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Crime', 'crimeBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Drama', 'dramaBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Family', 'familyBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Fantasy', 'fantasyBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Horror', 'horrorBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mystery', 'mysteryBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Romance', 'romanceBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Sci-Fi', 'scifiBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Thriller', 'thrillerBoxNavigator', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'search.png')

        self.endDirectory(category='Boxsets')

    def action(self):
        self.addDirectoryItem('12 Rounds', 'boxsetList&url=tmdbbox&list=13120', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('3 Ninjas', 'boxsetList&url=tmdbbox&list=13130', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('300', 'boxsetList&url=tmdbbox&list=13132', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Agent Cody Banks', 'boxsetList&url=tmdbbox&list=16496',
                              'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('American Ninja', 'boxsetList&url=tmdbbox&list=13168',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Avengers', 'boxsetList&url=tmdbbox&list=13196', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('AVP', 'boxsetList&url=tmdbbox&list=13199', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bad Ass', 'boxsetList&url=tmdbbox&list=13205', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bad Boys', 'boxsetList&url=tmdbbox&list=13208', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Batman', 'boxsetList&url=tmdbbox&list=13223', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Best Of The Best', 'boxsetList&url=tmdbbox&list=13269',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Beverly Hills Cop', 'boxsetList&url=tmdbbox&list=13272',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Big Mommas House', 'boxsetList&url=tmdbbox&list=13274',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bloodsport', 'boxsetList&url=tmdbbox&list=13281', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Blues Brother', 'boxsetList&url=tmdbbox&list=13284', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Boondock Saints', 'boxsetList&url=tmdbbox&list=13287',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bourne', 'boxsetList&url=tmdbbox&list=13288', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bruce Lee', 'boxsetList&url=tmdbbox&list=13295', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Captain America', 'boxsetList&url=tmdbbox&list=13224',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cats & Dogs', 'boxsetList&url=tmdbbox&list=16501', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Crank', 'boxsetList&url=tmdbbox&list=13273', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Crow', 'boxsetList&url=tmdbbox&list=13294', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Die Hard', 'boxsetList&url=tmdbbox&list=13302', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Dirty Harry', 'boxsetList&url=tmdbbox&list=13307', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Fast and Furious', 'boxsetList&url=tmdbbox&list=13062',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('G.I. Joe', 'boxsetList&url=tmdbbox&list=13293', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ghost Rider', 'boxsetList&url=tmdbbox&list=13290', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ghostbusters', 'boxsetList&url=tmdbbox&list=13286', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Highlander', 'boxsetList&url=tmdbbox&list=13256', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hollow Man', 'boxsetList&url=tmdbbox&list=13251', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hoodwinked!', 'boxsetList&url=tmdbbox&list=16523', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Hot Shots', 'boxsetList&url=tmdbbox&list=13242', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('How To Train Your Dragon', 'boxsetList&url=tmdbbox&list=13239',
                              'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Huntsman', 'boxsetList&url=tmdbbox&list=13235', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Independence Day', 'boxsetList&url=tmdbbox&list=13232',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Indiana Jones', 'boxsetList&url=tmdbbox&list=13231', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Inspector Gadget', 'boxsetList&url=tmdbbox&list=16492',
                              'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Ip Man', 'boxsetList&url=tmdbbox&list=13227', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Iron Fists', 'boxsetList&url=tmdbbox&list=13226', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Jackass', 'boxsetList&url=tmdbbox&list=13222', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('James Bond', 'boxsetList&url=tmdbbox&list=13221', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Johnny English', 'boxsetList&url=tmdbbox&list=13218',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Journey', 'boxsetList&url=tmdbbox&list=13216', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Judge Dredd', 'boxsetList&url=tmdbbox&list=13215', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Jump Street', 'boxsetList&url=tmdbbox&list=13213', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Justice League', 'boxsetList&url=tmdbbox&list=16491',
                              'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Karate Kid', 'boxsetList&url=tmdbbox&list=13209',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kick-Ass', 'boxsetList&url=tmdbbox&list=13207', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kickboxer', 'boxsetList&url=tmdbbox&list=13206', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kill Bill', 'boxsetList&url=tmdbbox&list=13203', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kung Fu Panda', 'boxsetList&url=tmdbbox&list=13202', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Lethal Weapon', 'boxsetList&url=tmdbbox&list=13195', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Machete', 'boxsetList&url=tmdbbox&list=13189', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mad Max', 'boxsetList&url=tmdbbox&list=13188', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Matrix', 'boxsetList&url=tmdbbox&list=13183', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Maze Runner', 'boxsetList&url=tmdbbox&list=13182', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Mechanic', 'boxsetList&url=tmdbbox&list=13181', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mission Impossible', 'boxsetList&url=tmdbbox&list=13175',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Mummy', 'boxsetList&url=tmdbbox&list=13171', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('National Treasure', 'boxsetList&url=tmdbbox&list=13167',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Never Back Down', 'boxsetList&url=tmdbbox&list=13166',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ninja', 'boxsetList&url=tmdbbox&list=13160', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Olympus Has Fallen', 'boxsetList&url=tmdbbox&list=13154',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ong Bak', 'boxsetList&url=tmdbbox&list=13151', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Pirates of The Caribbean', 'boxsetList&url=tmdbbox&list=13146',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Power Rangers', 'boxsetList&url=tmdbbox&list=16493', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Predator', 'boxsetList&url=tmdbbox&list=13136', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Protector', 'boxsetList&url=tmdbbox&list=13134', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Punisher', 'boxsetList&url=tmdbbox&list=13131', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Raid', 'boxsetList&url=tmdbbox&list=13127', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rambo', 'boxsetList&url=tmdbbox&list=13125', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('R.E.D.', 'boxsetList&url=tmdbbox&list=13124', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Red Cliff', 'boxsetList&url=tmdbbox&list=13123', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Resident Evil', 'boxsetList&url=tmdbbox&list=13122', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Riddick', 'boxsetList&url=tmdbbox&list=13121', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ride Along', 'boxsetList&url=tmdbbox&list=13119', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Robocop', 'boxsetList&url=tmdbbox&list=13115', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Romancing The Stone', 'boxsetList&url=tmdbbox&list=13112',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rush Hour', 'boxsetList&url=tmdbbox&list=13111', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Sherlock Holmes', 'boxsetList&url=tmdbbox&list=13105',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Smokey and The Bandit', 'boxsetList&url=tmdbbox&list=13101',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Spy Kids', 'boxsetList&url=tmdbbox&list=13099', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Star Trek', 'boxsetList&url=tmdbbox&list=13098', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Star Wars', 'boxsetList&url=tmdbbox&list=12741', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Starship Troopers', 'boxsetList&url=tmdbbox&list=13097',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Taken', 'boxsetList&url=tmdbbox&list=13095', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Teenage Mutant Ninja Turtles', 'boxsetList&url=tmdbbox&list=13092',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Terminator', 'boxsetList&url=tmdbbox&list=13090', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Titans', 'boxsetList&url=tmdbbox&list=13085', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Transformers', 'boxsetList&url=tmdbbox&list=13083', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Transporter', 'boxsetList&url=tmdbbox&list=13082', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tron', 'boxsetList&url=tmdbbox&list=13080', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Under Siege', 'boxsetList&url=tmdbbox&list=13078', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Underworld', 'boxsetList&url=tmdbbox&list=13077', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Undisputed', 'boxsetList&url=tmdbbox&list=13076', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Universal Soldier', 'boxsetList&url=tmdbbox&list=13075',
                              'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('xXx', 'boxsetList&url=tmdbbox&list=13068', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Young Guns', 'boxsetList&url=tmdbbox&list=13067', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Zorro', 'boxsetList&url=tmdbbox&list=13065', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Action Boxsets')

    def adventure(self):
        self.addDirectoryItem('101 Dalmations', 'boxsetList&url=tmdbbox&list=13113', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Agent Cody Banks', 'boxsetList&url=tmdbbox&list=16496', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Aladdin', 'boxsetList&url=tmdbbox&list=13155', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Alice In Wonderland', 'boxsetList&url=tmdbbox&list=13158', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('American Ninja', 'boxsetList&url=tmdbbox&list=13168', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Austin Powers', 'boxsetList&url=tmdbbox&list=13193', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Back To The Future', 'boxsetList&url=tmdbbox&list=13204', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Balto', 'boxsetList&url=tmdbbox&list=13214', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Batman', 'boxsetList&url=tmdbbox&list=13223', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bean', 'boxsetList&url=tmdbbox&list=13225', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Brother Bear', 'boxsetList&url=tmdbbox&list=13292', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Captain America', 'boxsetList&url=tmdbbox&list=13224', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Chronicles of Narnia', 'boxsetList&url=tmdbbox&list=13283', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Cloudy With A Chance of Meatballs', 'boxsetList&url=tmdbbox&list=13259', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Conan', 'boxsetList&url=tmdbbox&list=13262', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Crocodile Dundee', 'boxsetList&url=tmdbbox&list=13278', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Curious George', 'boxsetList&url=tmdbbox&list=16497', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Despicable Me', 'boxsetList&url=tmdbbox&list=13299', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Divergent', 'boxsetList&url=tmdbbox&list=13311', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('FernGully', 'boxsetList&url=tmdbbox&list=16522', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Finding Nemo', 'boxsetList&url=tmdbbox&list=16499', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Fox and The Hound', 'boxsetList&url=tmdbbox&list=13301', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Free Willy', 'boxsetList&url=tmdbbox&list=13298', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('G.I. Joe', 'boxsetList&url=tmdbbox&list=13293', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ghostbusters', 'boxsetList&url=tmdbbox&list=13286', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('A Goofy Movie', 'boxsetList&url=tmdbbox&list=16489', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Harold and Kumar', 'boxsetList&url=tmdbbox&list=13264', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Harry Potter', 'boxsetList&url=tmdbbox&list=13261', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Herbie', 'boxsetList&url=tmdbbox&list=16524', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Highlander', 'boxsetList&url=tmdbbox&list=13256', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Hobbit', 'boxsetList&url=tmdbbox&list=13252', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Homeward Bound', 'boxsetList&url=tmdbbox&list=13248', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Honey I Shrunk The Kids', 'boxsetList&url=tmdbbox&list=16471', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('How To Train Your Dragon', 'boxsetList&url=tmdbbox&list=13239', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Hunger Games', 'boxsetList&url=tmdbbox&list=13236', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Huntsman', 'boxsetList&url=tmdbbox&list=13235', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ice Age', 'boxsetList&url=tmdbbox&list=13234', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Independence Day', 'boxsetList&url=tmdbbox&list=13232', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Indiana Jones', 'boxsetList&url=tmdbbox&list=13231', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Inspector Gadget', 'boxsetList&url=tmdbbox&list=16492', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('James Bond', 'boxsetList&url=tmdbbox&list=13221', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Jaws', 'boxsetList&url=tmdbbox&list=13219', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Johnny English', 'boxsetList&url=tmdbbox&list=13218', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Journey', 'boxsetList&url=tmdbbox&list=13216', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Jungle Book', 'boxsetList&url=tmdbbox&list=13212', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Jurassic Park', 'boxsetList&url=tmdbbox&list=13211', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Justice League', 'boxsetList&url=tmdbbox&list=16491', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kung Fu Panda', 'boxsetList&url=tmdbbox&list=13202', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lady and The Tramp', 'boxsetList&url=tmdbbox&list=13200', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Land Before Time', 'boxsetList&url=tmdbbox&list=16485', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lilo & Stitch', 'boxsetList&url=tmdbbox&list=16500', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Lion King', 'boxsetList&url=tmdbbox&list=13194', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Lord of The Rings', 'boxsetList&url=tmdbbox&list=13190', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mad Max', 'boxsetList&url=tmdbbox&list=13188', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Madagascar', 'boxsetList&url=tmdbbox&list=13187', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Men in Black', 'boxsetList&url=tmdbbox&list=13178', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mission Impossible', 'boxsetList&url=tmdbbox&list=13175', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Monsters INC', 'boxsetList&url=tmdbbox&list=13174', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Monty Python', 'boxsetList&url=tmdbbox&list=13173', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mulan', 'boxsetList&url=tmdbbox&list=13172', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Mummy', 'boxsetList&url=tmdbbox&list=13171', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Muppets', 'boxsetList&url=tmdbbox&list=16494', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('National Treasure', 'boxsetList&url=tmdbbox&list=13167', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Never Ending Story', 'boxsetList&url=tmdbbox&list=13165', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('New Groove', 'boxsetList&url=tmdbbox&list=13164', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Night At The Museum', 'boxsetList&url=tmdbbox&list=16483', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Nims Island', 'boxsetList&url=tmdbbox&list=13162', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Open Season', 'boxsetList&url=tmdbbox&list=13150', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Percy Jackson', 'boxsetList&url=tmdbbox&list=13147', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Peter Pan', 'boxsetList&url=tmdbbox&list=16498', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Pink Panther', 'boxsetList&url=tmdbbox&list=13320', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Pirates of The Caribbean', 'boxsetList&url=tmdbbox&list=13146', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Planes', 'boxsetList&url=tmdbbox&list=13142', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Planet of The Apes', 'boxsetList&url=tmdbbox&list=13141', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Pocahontas', 'boxsetList&url=tmdbbox&list=13140', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Power Rangers', 'boxsetList&url=tmdbbox&list=16493', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Rambo', 'boxsetList&url=tmdbbox&list=13125', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Red Cliff', 'boxsetList&url=tmdbbox&list=13123', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Riddick', 'boxsetList&url=tmdbbox&list=13121', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rio', 'boxsetList&url=tmdbbox&list=13117', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Romancing The Stone', 'boxsetList&url=tmdbbox&list=13112', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Sammys Adventures', 'boxsetList&url=tmdbbox&list=13110', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Sherlock Holmes', 'boxsetList&url=tmdbbox&list=13105', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Shrek', 'boxsetList&url=tmdbbox&list=16470', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Smurfs', 'boxsetList&url=tmdbbox&list=13100', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Space Chimps', 'boxsetList&url=tmdbbox&list=16495', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('SpongBob Squarepants', 'boxsetList&url=tmdbbox&list=16508', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Spy Kids', 'boxsetList&url=tmdbbox&list=13099', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Star Trek', 'boxsetList&url=tmdbbox&list=13098', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Star Wars', 'boxsetList&url=tmdbbox&list=12741', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Starship Troopers', 'boxsetList&url=tmdbbox&list=13097', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Stuart Little', 'boxsetList&url=tmdbbox&list=16488', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tarzan', 'boxsetList&url=tmdbbox&list=13094', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Teenage Mutant Ninja Turtles', 'boxsetList&url=tmdbbox&list=13092', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tinker Bell', 'boxsetList&url=tmdbbox&list=13086', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Titans', 'boxsetList&url=tmdbbox&list=13085', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Transformers', 'boxsetList&url=tmdbbox&list=13083', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tron', 'boxsetList&url=tmdbbox&list=13080', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Weekend at Bernies', 'boxsetList&url=tmdbbox&list=13072', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('xXx', 'boxsetList&url=tmdbbox&list=13068', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Zorro', 'boxsetList&url=tmdbbox&list=13065', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Adventure Boxsets')

    def animation(self, lite=False):
        self.addDirectoryItem('101 Dalmations', 'boxsetList&url=tmdbbox&list=13113', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Aladdin', 'boxsetList&url=tmdbbox&list=13155', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Alice In Wonderland', 'boxsetList&url=tmdbbox&list=13158', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('All Dogs Go to Heaven', 'boxsetList&url=tmdbbox&list=16473', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Balto', 'boxsetList&url=tmdbbox&list=13214', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bambi', 'boxsetList&url=tmdbbox&list=13217', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Beauty and The Beast', 'boxsetList&url=tmdbbox&list=13229', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Brother Bear', 'boxsetList&url=tmdbbox&list=13292', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cars', 'boxsetList&url=tmdbbox&list=13244', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Charlottes Web', 'boxsetList&url=tmdbbox&list=16506', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cloudy With A Chance of Meatballs', 'boxsetList&url=tmdbbox&list=13259', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Curious George', 'boxsetList&url=tmdbbox&list=16497', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Despicable Me', 'boxsetList&url=tmdbbox&list=13299', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Fantasia', 'boxsetList&url=tmdbbox&list=16521', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('FernGully', 'boxsetList&url=tmdbbox&list=16522', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Finding Nemo', 'boxsetList&url=tmdbbox&list=16499', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Fox and The Hound', 'boxsetList&url=tmdbbox&list=13301', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Garfield', 'boxsetList&url=tmdbbox&list=16520', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('A Goofy Movie', 'boxsetList&url=tmdbbox&list=16489', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Happy Feet', 'boxsetList&url=tmdbbox&list=13265', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hoodwinked!', 'boxsetList&url=tmdbbox&list=16523', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hotel Transylvania', 'boxsetList&url=tmdbbox&list=13240', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('How To Train Your Dragon', 'boxsetList&url=tmdbbox&list=13239', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hunchback of Notre Dame', 'boxsetList&url=tmdbbox&list=13237', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ice Age', 'boxsetList&url=tmdbbox&list=13234', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Justice League', 'boxsetList&url=tmdbbox&list=16491', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kung Fu Panda', 'boxsetList&url=tmdbbox&list=13202', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lady and The Tramp', 'boxsetList&url=tmdbbox&list=13200', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Land Before Time', 'boxsetList&url=tmdbbox&list=16485', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lego Star Wars', 'boxsetList&url=tmdbbox&list=16482', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lilo & Stitch', 'boxsetList&url=tmdbbox&list=16500', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Lion King', 'boxsetList&url=tmdbbox&list=13194', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Little Mermaid', 'boxsetList&url=tmdbbox&list=13192', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Madagascar', 'boxsetList&url=tmdbbox&list=13187', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Monsters INC', 'boxsetList&url=tmdbbox&list=13174', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mulan', 'boxsetList&url=tmdbbox&list=13172', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('New Groove', 'boxsetList&url=tmdbbox&list=13164', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Open Season', 'boxsetList&url=tmdbbox&list=13150', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Planes', 'boxsetList&url=tmdbbox&list=13142', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Pocahontas', 'boxsetList&url=tmdbbox&list=13140', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Reef', 'boxsetList&url=tmdbbox&list=16490', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rio', 'boxsetList&url=tmdbbox&list=13117', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Sammys Adventures', 'boxsetList&url=tmdbbox&list=13110', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Shrek', 'boxsetList&url=tmdbbox&list=16470', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Smurfs', 'boxsetList&url=tmdbbox&list=13100', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Space Chimps', 'boxsetList&url=tmdbbox&list=16495', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('SpongBob Squarepants', 'boxsetList&url=tmdbbox&list=16508', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tarzan', 'boxsetList&url=tmdbbox&list=13094', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Thomas & Friends', 'boxsetList&url=tmdbbox&list=16503', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Tinker Bell', 'boxsetList&url=tmdbbox&list=13086', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Wallace & Gromit', 'boxsetList&url=tmdbbox&list=16504', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Animation Boxsets')

    def comedy(self, lite=False):
        self.addDirectoryItem('101 Dalmations', 'boxsetList&url=tmdbbox&list=13113', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('3 Ninjas', 'boxsetList&url=tmdbbox&list=13130', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('A Haunted House', 'boxsetList&url=tmdbbox&list=13137', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ace Ventura', 'boxsetList&url=tmdbbox&list=13145', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Adams Family', 'boxsetList&url=tmdbbox&list=13148', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Agent Cody Banks', 'boxsetList&url=tmdbbox&list=16496', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Aladdin', 'boxsetList&url=tmdbbox&list=13155', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('All Dogs Go to Heaven', 'boxsetList&url=tmdbbox&list=16473', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('American Pie', 'boxsetList&url=tmdbbox&list=13176', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Anchorman', 'boxsetList&url=tmdbbox&list=13180', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Austin Powers', 'boxsetList&url=tmdbbox&list=13193', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Babe', 'boxsetList&url=tmdbbox&list=13201', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Back To The Future', 'boxsetList&url=tmdbbox&list=13204', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bad Ass', 'boxsetList&url=tmdbbox&list=13205', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bad Boys', 'boxsetList&url=tmdbbox&list=13208', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bad Neighbors', 'boxsetList&url=tmdbbox&list=13210', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Barbershop', 'boxsetList&url=tmdbbox&list=13220', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bean', 'boxsetList&url=tmdbbox&list=13225', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Best Exotic Marigold Hotel', 'boxsetList&url=tmdbbox&list=13268', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Beverly Hills Cop', 'boxsetList&url=tmdbbox&list=13272', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Big Mommas House', 'boxsetList&url=tmdbbox&list=13274', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Blues Brother', 'boxsetList&url=tmdbbox&list=13284', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bridget Jones', 'boxsetList&url=tmdbbox&list=13289', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Brother Bear', 'boxsetList&url=tmdbbox&list=13292', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cars', 'boxsetList&url=tmdbbox&list=13244', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Casper', 'boxsetList&url=tmdbbox&list=16469', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cats & Dogs', 'boxsetList&url=tmdbbox&list=16501', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('City Slickers', 'boxsetList&url=tmdbbox&list=13253', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Clerks', 'boxsetList&url=tmdbbox&list=13255', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cloudy With A Chance of Meatballs', 'boxsetList&url=tmdbbox&list=13259', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Crocodile Dundee', 'boxsetList&url=tmdbbox&list=13278', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Curious George', 'boxsetList&url=tmdbbox&list=16497', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Daddy Daycare', 'boxsetList&url=tmdbbox&list=16487', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Despicable Me', 'boxsetList&url=tmdbbox&list=13299', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Diary of A Wimpy Kid', 'boxsetList&url=tmdbbox&list=13300', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Doctor Dolittle', 'boxsetList&url=tmdbbox&list=16505', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Dumb and Dumber', 'boxsetList&url=tmdbbox&list=13314', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Finding Nemo', 'boxsetList&url=tmdbbox&list=16499', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Friday', 'boxsetList&url=tmdbbox&list=13315', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Garfield', 'boxsetList&url=tmdbbox&list=16520', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Ghostbusters', 'boxsetList&url=tmdbbox&list=13286', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('A Goofy Movie', 'boxsetList&url=tmdbbox&list=16489', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Gremlins', 'boxsetList&url=tmdbbox&list=13280', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Grown Ups', 'boxsetList&url=tmdbbox&list=13279', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Grumpy Old Men', 'boxsetList&url=tmdbbox&list=13275', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Hangover', 'boxsetList&url=tmdbbox&list=13271', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Happy Feet', 'boxsetList&url=tmdbbox&list=13265', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Harold and Kumar', 'boxsetList&url=tmdbbox&list=13264', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Herbie', 'boxsetList&url=tmdbbox&list=16524', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Home Alone', 'boxsetList&url=tmdbbox&list=13250', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Homeward Bound', 'boxsetList&url=tmdbbox&list=13248', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Honey I Shrunk The Kids', 'boxsetList&url=tmdbbox&list=13247', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hoodwinked!', 'boxsetList&url=tmdbbox&list=16523', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Horrible Bosses', 'boxsetList&url=tmdbbox&list=13245', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hot Shots', 'boxsetList&url=tmdbbox&list=13242', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hot Tub Time Machine', 'boxsetList&url=tmdbbox&list=13241', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hotel Transylvania', 'boxsetList&url=tmdbbox&list=13240', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ice Age', 'boxsetList&url=tmdbbox&list=13234', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Inbetweeners', 'boxsetList&url=tmdbbox&list=13233', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Inspector Gadget', 'boxsetList&url=tmdbbox&list=16492', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Jackass', 'boxsetList&url=tmdbbox&list=13222', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Johnny English', 'boxsetList&url=tmdbbox&list=13218', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Jump Street', 'boxsetList&url=tmdbbox&list=13213', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kick-Ass', 'boxsetList&url=tmdbbox&list=13207', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Legally Blonde', 'boxsetList&url=tmdbbox&list=13197', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Like Mike', 'boxsetList&url=tmdbbox&list=16486', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lilo & Stitch', 'boxsetList&url=tmdbbox&list=16500', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Madagascar', 'boxsetList&url=tmdbbox&list=13187', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Major League', 'boxsetList&url=tmdbbox&list=13185', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Meet The Parents', 'boxsetList&url=tmdbbox&list=13179', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Men in Black', 'boxsetList&url=tmdbbox&list=13178', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Mighty Ducks', 'boxsetList&url=tmdbbox&list=13177', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Monsters INC', 'boxsetList&url=tmdbbox&list=13174', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Monty Python', 'boxsetList&url=tmdbbox&list=13173', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Muppets', 'boxsetList&url=tmdbbox&list=16494', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('My Big Fat Greek Wedding', 'boxsetList&url=tmdbbox&list=13170', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Naked Gun', 'boxsetList&url=tmdbbox&list=13169', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('New Groove', 'boxsetList&url=tmdbbox&list=13164', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Night At The Museum', 'boxsetList&url=tmdbbox&list=16483', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Nims Island', 'boxsetList&url=tmdbbox&list=13162', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Open Season', 'boxsetList&url=tmdbbox&list=13150', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Pink Panther', 'boxsetList&url=tmdbbox&list=13320', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Pitch Perfect', 'boxsetList&url=tmdbbox&list=13144', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Planes', 'boxsetList&url=tmdbbox&list=13142', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Police Academy', 'boxsetList&url=tmdbbox&list=13139', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Problem Child', 'boxsetList&url=tmdbbox&list=13135', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('R.E.D.', 'boxsetList&url=tmdbbox&list=13124', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ride Along', 'boxsetList&url=tmdbbox&list=13119', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rio', 'boxsetList&url=tmdbbox&list=13117', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Romancing The Stone', 'boxsetList&url=tmdbbox&list=13112', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rush Hour', 'boxsetList&url=tmdbbox&list=13111', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Sandlot', 'boxsetList&url=tmdbbox&list=16502', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Scary Movie', 'boxsetList&url=tmdbbox&list=13108', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Shrek', 'boxsetList&url=tmdbbox&list=16470', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Short Circuit', 'boxsetList&url=tmdbbox&list=13104', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Smokey and The Bandit', 'boxsetList&url=tmdbbox&list=13101', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Smurfs', 'boxsetList&url=tmdbbox&list=13100', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Space Chimps', 'boxsetList&url=tmdbbox&list=16495', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('SpongBob Squarepants', 'boxsetList&url=tmdbbox&list=16508', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Spy Kids', 'boxsetList&url=tmdbbox&list=13099', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Stuart Little', 'boxsetList&url=tmdbbox&list=16488', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Ted', 'boxsetList&url=tmdbbox&list=13093', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Teenage Mutant Ninja Turtles', 'boxsetList&url=tmdbbox&list=13092', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Teen Wolf', 'boxsetList&url=tmdbbox&list=13091', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Tooth Fairy', 'boxsetList&url=tmdbbox&list=13084', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Tremors', 'boxsetList&url=tmdbbox&list=13081', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Waynes World', 'boxsetList&url=tmdbbox&list=13073', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Weekend at Bernies', 'boxsetList&url=tmdbbox&list=13072', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Whole Nine Yards', 'boxsetList&url=tmdbbox&list=13071', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Zoolander', 'boxsetList&url=tmdbbox&list=13066', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Zorro', 'boxsetList&url=tmdbbox&list=13065', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Comedy Boxsets')

    def crime(self, lite=False):
        self.addDirectoryItem('12 Rounds', 'boxsetList&url=tmdbbox&list=13120', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bad Ass', 'boxsetList&url=tmdbbox&list=13205', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bad Boys', 'boxsetList&url=tmdbbox&list=13208', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Beverly Hills Cop', 'boxsetList&url=tmdbbox&list=13272', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Big Mommas House', 'boxsetList&url=tmdbbox&list=13274', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Blues Brother', 'boxsetList&url=tmdbbox&list=13284', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Boondock Saints', 'boxsetList&url=tmdbbox&list=13287', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Crank', 'boxsetList&url=tmdbbox&list=13273', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Dirty Harry', 'boxsetList&url=tmdbbox&list=13307', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Dragon Tattoo', 'boxsetList&url=tmdbbox&list=13313', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Fast and Furious', 'boxsetList&url=tmdbbox&list=13062', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Godfather', 'boxsetList&url=tmdbbox&list=13285', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Green Street Hooligans', 'boxsetList&url=tmdbbox&list=13282', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hannibal Lecter', 'boxsetList&url=tmdbbox&list=13270', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Horrible Bosses', 'boxsetList&url=tmdbbox&list=13245', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Infernal Affairs', 'boxsetList&url=tmdbbox&list=13230', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Judge Dredd', 'boxsetList&url=tmdbbox&list=13215', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Jump Street', 'boxsetList&url=tmdbbox&list=13213', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kill Bill', 'boxsetList&url=tmdbbox&list=13203', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lethal Weapon', 'boxsetList&url=tmdbbox&list=13195', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Machete', 'boxsetList&url=tmdbbox&list=13189', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Mechanic', 'boxsetList&url=tmdbbox&list=13181', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Naked Gun', 'boxsetList&url=tmdbbox&list=13169', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ninja', 'boxsetList&url=tmdbbox&list=13160', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Now You See Me', 'boxsetList&url=tmdbbox&list=13159', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Oceans', 'boxsetList&url=tmdbbox&list=13156', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Once Were Warriors', 'boxsetList&url=tmdbbox&list=13152', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ong Bak', 'boxsetList&url=tmdbbox&list=13151', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Pink Panther', 'boxsetList&url=tmdbbox&list=13320', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Protector', 'boxsetList&url=tmdbbox&list=13134', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Punisher', 'boxsetList&url=tmdbbox&list=13131', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Raid', 'boxsetList&url=tmdbbox&list=13127', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('R.E.D.', 'boxsetList&url=tmdbbox&list=13124', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ride Along', 'boxsetList&url=tmdbbox&list=13119', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rise of the Footsoldier', 'boxsetList&url=tmdbbox&list=13116', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Robocop', 'boxsetList&url=tmdbbox&list=13115', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rush Hour', 'boxsetList&url=tmdbbox&list=13111', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Sherlock Holmes', 'boxsetList&url=tmdbbox&list=13105', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Sin City', 'boxsetList&url=tmdbbox&list=13103', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Step Up', 'boxsetList&url=tmdbbox&list=13096', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Transporter', 'boxsetList&url=tmdbbox&list=13082', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Undisputed', 'boxsetList&url=tmdbbox&list=13076', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Weekend at Bernies', 'boxsetList&url=tmdbbox&list=13072', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Whole Nine Yards', 'boxsetList&url=tmdbbox&list=13071', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Young Guns', 'boxsetList&url=tmdbbox&list=13067', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Crime Boxsets')

    def drama(self, lite=False):
        self.addDirectoryItem('28 Days Later', 'boxsetList&url=tmdbbox&list=13126', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('All Dogs Go to Heaven', 'boxsetList&url=tmdbbox&list=16473', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Babe', 'boxsetList&url=tmdbbox&list=13201', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Balto', 'boxsetList&url=tmdbbox&list=13214', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bambi', 'boxsetList&url=tmdbbox&list=13217', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Barbershop', 'boxsetList&url=tmdbbox&list=13220', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Before', 'boxsetList&url=tmdbbox&list=13267', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Best Exotic Marigold Hotel', 'boxsetList&url=tmdbbox&list=13268', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Best Of The Best', 'boxsetList&url=tmdbbox&list=13269', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bloodsport', 'boxsetList&url=tmdbbox&list=13281', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bruce Lee', 'boxsetList&url=tmdbbox&list=13295', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cinderella', 'boxsetList&url=tmdbbox&list=13249', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Crow', 'boxsetList&url=tmdbbox&list=13294', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cube', 'boxsetList&url=tmdbbox&list=13304', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Dirty Dancing', 'boxsetList&url=tmdbbox&list=13305', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Dolphin Tale', 'boxsetList&url=tmdbbox&list=13312', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Dragon Tattoo', 'boxsetList&url=tmdbbox&list=13313', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Fly', 'boxsetList&url=tmdbbox&list=13303', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Fox and The Hound', 'boxsetList&url=tmdbbox&list=13301', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Free Willy', 'boxsetList&url=tmdbbox&list=13298', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Friday', 'boxsetList&url=tmdbbox&list=13315', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Godfather', 'boxsetList&url=tmdbbox&list=13285', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Green Street Hooligans', 'boxsetList&url=tmdbbox&list=13282', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Grumpy Old Men', 'boxsetList&url=tmdbbox&list=13275', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hannibal Lecter', 'boxsetList&url=tmdbbox&list=13270', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Homeward Bound', 'boxsetList&url=tmdbbox&list=13248', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hunchback of Notre Dame', 'boxsetList&url=tmdbbox&list=13237', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Huntsman', 'boxsetList&url=tmdbbox&list=13235', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Infernal Affairs', 'boxsetList&url=tmdbbox&list=13230', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ip Man', 'boxsetList&url=tmdbbox&list=13227', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Jaws', 'boxsetList&url=tmdbbox&list=13219', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Jungle Book', 'boxsetList&url=tmdbbox&list=13212', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Karate Kid', 'boxsetList&url=tmdbbox&list=13209', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Land Before Time', 'boxsetList&url=tmdbbox&list=16485', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Lion King', 'boxsetList&url=tmdbbox&list=13194', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Lord of The Rings', 'boxsetList&url=tmdbbox&list=13190', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Mighty Ducks', 'boxsetList&url=tmdbbox&list=13177', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('My Big Fat Greek Wedding', 'boxsetList&url=tmdbbox&list=13170', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Never Back Down', 'boxsetList&url=tmdbbox&list=13166', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Never Ending Story', 'boxsetList&url=tmdbbox&list=13165', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ninja', 'boxsetList&url=tmdbbox&list=13160', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Nymphomaniac', 'boxsetList&url=tmdbbox&list=13157', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Once Were Warriors', 'boxsetList&url=tmdbbox&list=13152', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Pocahontas', 'boxsetList&url=tmdbbox&list=13140', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Punisher', 'boxsetList&url=tmdbbox&list=13131', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Red Cliff', 'boxsetList&url=tmdbbox&list=13123', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rise of the Footsoldier', 'boxsetList&url=tmdbbox&list=13116', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rocky', 'boxsetList&url=tmdbbox&list=13114', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Sandlot', 'boxsetList&url=tmdbbox&list=16502', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Shanghai', 'boxsetList&url=tmdbbox&list=13106', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Step Up', 'boxsetList&url=tmdbbox&list=13096', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Three Colors', 'boxsetList&url=tmdbbox&list=13087', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Twilight', 'boxsetList&url=tmdbbox&list=13079', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Undisputed', 'boxsetList&url=tmdbbox&list=13076', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Woman in Black', 'boxsetList&url=tmdbbox&list=13070', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Young Guns', 'boxsetList&url=tmdbbox&list=13067', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Drama Boxsets')

    def family(self, lite=False):
        self.addDirectoryItem('3 Ninjas', 'boxsetList&url=tmdbbox&list=13130', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Alice In Wonderland', 'boxsetList&url=tmdbbox&list=13158', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Babe', 'boxsetList&url=tmdbbox&list=13201', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bambi', 'boxsetList&url=tmdbbox&list=13217', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bean', 'boxsetList&url=tmdbbox&list=13225', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Beauty and The Beast', 'boxsetList&url=tmdbbox&list=13229', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cars', 'boxsetList&url=tmdbbox&list=13244', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Casper', 'boxsetList&url=tmdbbox&list=16469', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cats & Dogs', 'boxsetList&url=tmdbbox&list=16501', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Charlottes Web', 'boxsetList&url=tmdbbox&list=16506', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Chronicles of Narnia', 'boxsetList&url=tmdbbox&list=13283', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cinderella', 'boxsetList&url=tmdbbox&list=13249', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Daddy Daycare', 'boxsetList&url=tmdbbox&list=16487', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Diary of A Wimpy Kid', 'boxsetList&url=tmdbbox&list=13300', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Doctor Dolittle', 'boxsetList&url=tmdbbox&list=16505', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Dolphin Tale', 'boxsetList&url=tmdbbox&list=13312', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Fantasia', 'boxsetList&url=tmdbbox&list=16521', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('FernGully', 'boxsetList&url=tmdbbox&list=16522', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Flintstones', 'boxsetList&url=tmdbbox&list=16474', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Free Willy', 'boxsetList&url=tmdbbox&list=13298', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Garfield', 'boxsetList&url=tmdbbox&list=16520', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Happy Feet', 'boxsetList&url=tmdbbox&list=13265', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Harry Potter', 'boxsetList&url=tmdbbox&list=13261', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Herbie', 'boxsetList&url=tmdbbox&list=16524', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Home Alone', 'boxsetList&url=tmdbbox&list=13250', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Honey I Shrunk The Kids', 'boxsetList&url=tmdbbox&list=13247', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hotel Transylvania', 'boxsetList&url=tmdbbox&list=13240', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Hunchback of Notre Dame', 'boxsetList&url=tmdbbox&list=13237', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Journey', 'boxsetList&url=tmdbbox&list=13216', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Jungle Book', 'boxsetList&url=tmdbbox&list=13212', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Karate Kid', 'boxsetList&url=tmdbbox&list=13209', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lego Star Wars', 'boxsetList&url=tmdbbox&list=16482', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Like Mike', 'boxsetList&url=tmdbbox&list=16486', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Little Mermaid', 'boxsetList&url=tmdbbox&list=13192', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Men in Black', 'boxsetList&url=tmdbbox&list=13178', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Mighty Ducks', 'boxsetList&url=tmdbbox&list=13177', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mulan', 'boxsetList&url=tmdbbox&list=13172', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Muppets', 'boxsetList&url=tmdbbox&list=16494', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('National Treasure', 'boxsetList&url=tmdbbox&list=13167', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('The Never Ending Story', 'boxsetList&url=tmdbbox&list=13165', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Night At The Museum', 'boxsetList&url=tmdbbox&list=16483', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Nims Island', 'boxsetList&url=tmdbbox&list=13162', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Percy Jackson', 'boxsetList&url=tmdbbox&list=13147', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Peter Pan', 'boxsetList&url=tmdbbox&list=16498', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Power Rangers', 'boxsetList&url=tmdbbox&list=16493', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Problem Child', 'boxsetList&url=tmdbbox&list=13135', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Reef', 'boxsetList&url=tmdbbox&list=16490', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Sammys Adventures', 'boxsetList&url=tmdbbox&list=13110', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Sandlot', 'boxsetList&url=tmdbbox&list=16502', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Short Circuit', 'boxsetList&url=tmdbbox&list=13104', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Stuart Little', 'boxsetList&url=tmdbbox&list=16488', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tarzan', 'boxsetList&url=tmdbbox&list=13094', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Thomas & Friends', 'boxsetList&url=tmdbbox&list=16503', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Tinker Bell', 'boxsetList&url=tmdbbox&list=13086', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Tooth Fairy', 'boxsetList&url=tmdbbox&list=13084', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Family Boxsets')

    def fantasy(self, lite=False):
        self.addDirectoryItem('300', 'boxsetList&url=tmdbbox&list=13132', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('A Haunted House', 'boxsetList&url=tmdbbox&list=13137', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Adams Family', 'boxsetList&url=tmdbbox&list=13148', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Beauty and The Beast', 'boxsetList&url=tmdbbox&list=13229', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Casper', 'boxsetList&url=tmdbbox&list=16469', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Chronicles of Narnia', 'boxsetList&url=tmdbbox&list=13283', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cinderella', 'boxsetList&url=tmdbbox&list=13249', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Conan', 'boxsetList&url=tmdbbox&list=13262', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Crow', 'boxsetList&url=tmdbbox&list=13294', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Doctor Dolittle', 'boxsetList&url=tmdbbox&list=16505', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Fantasia', 'boxsetList&url=tmdbbox&list=16521', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Flintstones', 'boxsetList&url=tmdbbox&list=16474', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Ghost Rider', 'boxsetList&url=tmdbbox&list=13290', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Gremlins', 'boxsetList&url=tmdbbox&list=13280', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Harry Potter', 'boxsetList&url=tmdbbox&list=13261', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Highlander', 'boxsetList&url=tmdbbox&list=13256', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Hobbit', 'boxsetList&url=tmdbbox&list=13252', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Indiana Jones', 'boxsetList&url=tmdbbox&list=13231', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lego Star Wars', 'boxsetList&url=tmdbbox&list=16482', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Like Mike', 'boxsetList&url=tmdbbox&list=16486', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Little Mermaid', 'boxsetList&url=tmdbbox&list=13192', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Lord of The Rings', 'boxsetList&url=tmdbbox&list=13190', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Monty Python', 'boxsetList&url=tmdbbox&list=13173', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Mummy', 'boxsetList&url=tmdbbox&list=13171', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Percy Jackson', 'boxsetList&url=tmdbbox&list=13147', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Peter Pan', 'boxsetList&url=tmdbbox&list=16498', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Pirates of The Caribbean', 'boxsetList&url=tmdbbox&list=13146', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Poltergeist', 'boxsetList&url=tmdbbox&list=13138', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Star Wars', 'boxsetList&url=tmdbbox&list=12741', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ted', 'boxsetList&url=tmdbbox&list=13093', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Teen Wolf', 'boxsetList&url=tmdbbox&list=13091', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Titans', 'boxsetList&url=tmdbbox&list=13085', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Tooth Fairy', 'boxsetList&url=tmdbbox&list=13084', 'boxsets.png', 'DefaultBoxSets.png')

        self.addDirectoryItem('Twilight', 'boxsetList&url=tmdbbox&list=13079', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Underworld', 'boxsetList&url=tmdbbox&list=13077', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Woman in Black', 'boxsetList&url=tmdbbox&list=13070', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Fantasy Boxsets')

    def horror(self, lite=False):
        self.addDirectoryItem('28 Days Later', 'boxsetList&url=tmdbbox&list=13126', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('A Nightmare on Elm Street', 'boxsetList&url=tmdbbox&list=13163', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Alien', 'boxsetList&url=tmdbbox&list=13161', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('AVP', 'boxsetList&url=tmdbbox&list=13199', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Childs Play', 'boxsetList&url=tmdbbox&list=13246', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Conjuring', 'boxsetList&url=tmdbbox&list=13266', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Evil Dead', 'boxsetList&url=tmdbbox&list=13308', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Exorcist', 'boxsetList&url=tmdbbox&list=13309', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Final Destination', 'boxsetList&url=tmdbbox&list=13306', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Fly', 'boxsetList&url=tmdbbox&list=13303', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Friday The 13th', 'boxsetList&url=tmdbbox&list=13296', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Gremlins', 'boxsetList&url=tmdbbox&list=13280', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Grudge', 'boxsetList&url=tmdbbox&list=13277', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Halloween', 'boxsetList&url=tmdbbox&list=13316', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hellraiser', 'boxsetList&url=tmdbbox&list=13257', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Hills Have Eyes', 'boxsetList&url=tmdbbox&list=13254', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hollow Man', 'boxsetList&url=tmdbbox&list=13251', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hostel', 'boxsetList&url=tmdbbox&list=13243', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Human Centipede', 'boxsetList&url=tmdbbox&list=13238', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Insidious', 'boxsetList&url=tmdbbox&list=13228', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Last Summer', 'boxsetList&url=tmdbbox&list=13198', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Omen', 'boxsetList&url=tmdbbox&list=13153', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Paranormal Activity', 'boxsetList&url=tmdbbox&list=13149', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Poltergeist', 'boxsetList&url=tmdbbox&list=13138', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Psycho', 'boxsetList&url=tmdbbox&list=13133', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Purge', 'boxsetList&url=tmdbbox&list=13129', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Quarantine', 'boxsetList&url=tmdbbox&list=13128', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Resident Evil', 'boxsetList&url=tmdbbox&list=13122', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Ring', 'boxsetList&url=tmdbbox&list=13118', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Saw', 'boxsetList&url=tmdbbox&list=13109', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Scream', 'boxsetList&url=tmdbbox&list=13107', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Texas Chainsaw Massacre', 'boxsetList&url=tmdbbox&list=13089', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tremors', 'boxsetList&url=tmdbbox&list=13081', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('VHS', 'boxsetList&url=tmdbbox&list=13074', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Woman in Black', 'boxsetList&url=tmdbbox&list=13070', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Wrong Turn', 'boxsetList&url=tmdbbox&list=13069', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Horror Boxsets')

    def mystery(self, lite=False):
        self.addDirectoryItem('The Conjuring', 'boxsetList&url=tmdbbox&list=13266', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cube', 'boxsetList&url=tmdbbox&list=13304', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Divergent', 'boxsetList&url=tmdbbox&list=13311', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Dragon Tattoo', 'boxsetList&url=tmdbbox&list=13313', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Friday The 13th', 'boxsetList&url=tmdbbox&list=13296', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Grudge', 'boxsetList&url=tmdbbox&list=13277', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Infernal Affairs', 'boxsetList&url=tmdbbox&list=13230', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Insidious', 'boxsetList&url=tmdbbox&list=13228', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Last Summer', 'boxsetList&url=tmdbbox&list=13198', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Now You See Me', 'boxsetList&url=tmdbbox&list=13159', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Paranormal Activity', 'boxsetList&url=tmdbbox&list=13149', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Psycho', 'boxsetList&url=tmdbbox&list=13133', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Ring', 'boxsetList&url=tmdbbox&list=13118', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Saw', 'boxsetList&url=tmdbbox&list=13109', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Scream', 'boxsetList&url=tmdbbox&list=13107', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Shanghai', 'boxsetList&url=tmdbbox&list=13106', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Three Colors', 'boxsetList&url=tmdbbox&list=13087', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Mystery Boxsets')

    def romance(self, lite=False):
        self.addDirectoryItem('American Ninja', 'boxsetList&url=tmdbbox&list=13168', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Before', 'boxsetList&url=tmdbbox&list=13267', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bridget Jones', 'boxsetList&url=tmdbbox&list=13289', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Dirty Dancing', 'boxsetList&url=tmdbbox&list=13305', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Grumpy Old Men', 'boxsetList&url=tmdbbox&list=13275', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Legally Blonde', 'boxsetList&url=tmdbbox&list=13197', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Meet The Parents', 'boxsetList&url=tmdbbox&list=13179', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('My Big Fat Greek Wedding', 'boxsetList&url=tmdbbox&list=13170', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Shanghai', 'boxsetList&url=tmdbbox&list=13106', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Think Like a Man', 'boxsetList&url=tmdbbox&list=13088', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Three Colors', 'boxsetList&url=tmdbbox&list=13087', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Twilight', 'boxsetList&url=tmdbbox&list=13079', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Romance Boxsets')

    def scifi(self, lite=False):
        self.addDirectoryItem('28 Days Later', 'boxsetList&url=tmdbbox&list=13126', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Alien', 'boxsetList&url=tmdbbox&list=13161', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Avengers', 'boxsetList&url=tmdbbox&list=13196', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('AVP', 'boxsetList&url=tmdbbox&list=13199', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Back To The Future', 'boxsetList&url=tmdbbox&list=13204', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Butterfly Effect', 'boxsetList&url=tmdbbox&list=13297', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Captain America', 'boxsetList&url=tmdbbox&list=13224', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cocoon', 'boxsetList&url=tmdbbox&list=13260', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cube', 'boxsetList&url=tmdbbox&list=13304', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Divergent', 'boxsetList&url=tmdbbox&list=13311', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Fly', 'boxsetList&url=tmdbbox&list=13303', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('G.I. Joe', 'boxsetList&url=tmdbbox&list=13293', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hollow Man', 'boxsetList&url=tmdbbox&list=13251', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hot Tub Time Machine', 'boxsetList&url=tmdbbox&list=13241', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hunger Games', 'boxsetList&url=tmdbbox&list=13236', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Independence Day', 'boxsetList&url=tmdbbox&list=13232', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Judge Dredd', 'boxsetList&url=tmdbbox&list=13215', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Jurassic Park', 'boxsetList&url=tmdbbox&list=13211', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mad Max', 'boxsetList&url=tmdbbox&list=13188', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Matrix', 'boxsetList&url=tmdbbox&list=13183', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Maze Runner', 'boxsetList&url=tmdbbox&list=13182', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Planet of The Apes', 'boxsetList&url=tmdbbox&list=13141', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Predator', 'boxsetList&url=tmdbbox&list=13136', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Purge', 'boxsetList&url=tmdbbox&list=13129', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Quarantine', 'boxsetList&url=tmdbbox&list=13128', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Resident Evil', 'boxsetList&url=tmdbbox&list=13122', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Riddick', 'boxsetList&url=tmdbbox&list=13121', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Robocop', 'boxsetList&url=tmdbbox&list=13115', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Short Circuit', 'boxsetList&url=tmdbbox&list=13104', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Star Trek', 'boxsetList&url=tmdbbox&list=13098', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Starship Troopers', 'boxsetList&url=tmdbbox&list=13097', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Terminator', 'boxsetList&url=tmdbbox&list=13090', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Transformers', 'boxsetList&url=tmdbbox&list=13083', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tron', 'boxsetList&url=tmdbbox&list=13080', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Universal Soldier', 'boxsetList&url=tmdbbox&list=13075', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Scifi Boxsets')

    def thriller(self, lite=False):
        self.addDirectoryItem('12 Rounds', 'boxsetList&url=tmdbbox&list=13120', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Boondock Saints', 'boxsetList&url=tmdbbox&list=13287', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bourne', 'boxsetList&url=tmdbbox&list=13288', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Butterfly Effect', 'boxsetList&url=tmdbbox&list=13297', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Childs Play', 'boxsetList&url=tmdbbox&list=13246', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Conjuring', 'boxsetList&url=tmdbbox&list=13266', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Crank', 'boxsetList&url=tmdbbox&list=13273', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Die Hard', 'boxsetList&url=tmdbbox&list=13302', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Dirty Harry', 'boxsetList&url=tmdbbox&list=13307', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Fast and Furious', 'boxsetList&url=tmdbbox&list=13062', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Friday The 13th', 'boxsetList&url=tmdbbox&list=13296', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ghost Rider', 'boxsetList&url=tmdbbox&list=13290', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Grudge', 'boxsetList&url=tmdbbox&list=13277', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Halloween', 'boxsetList&url=tmdbbox&list=13316', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hannibal Lecter', 'boxsetList&url=tmdbbox&list=13270', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hellraiser', 'boxsetList&url=tmdbbox&list=13257', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Hills Have Eyes', 'boxsetList&url=tmdbbox&list=13254', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hunger Games', 'boxsetList&url=tmdbbox&list=13236', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Insidious', 'boxsetList&url=tmdbbox&list=13228', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('James Bond', 'boxsetList&url=tmdbbox&list=13221', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Jaws', 'boxsetList&url=tmdbbox&list=13219', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Jurassic Park', 'boxsetList&url=tmdbbox&list=13211', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kickboxer', 'boxsetList&url=tmdbbox&list=13206', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kill Bill', 'boxsetList&url=tmdbbox&list=13203', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Last Summer', 'boxsetList&url=tmdbbox&list=13198', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lethal Weapon', 'boxsetList&url=tmdbbox&list=13195', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Machete', 'boxsetList&url=tmdbbox&list=13189', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Maze Runner', 'boxsetList&url=tmdbbox&list=13182', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Mechanic', 'boxsetList&url=tmdbbox&list=13181', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mission Impossible', 'boxsetList&url=tmdbbox&list=13175', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Now You See Me', 'boxsetList&url=tmdbbox&list=13159', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Oceans', 'boxsetList&url=tmdbbox&list=13156', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Olympus Has Fallen', 'boxsetList&url=tmdbbox&list=13154', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ong Bak', 'boxsetList&url=tmdbbox&list=13151', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Paranormal Activity', 'boxsetList&url=tmdbbox&list=13149', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Poltergeist', 'boxsetList&url=tmdbbox&list=13138', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Predator', 'boxsetList&url=tmdbbox&list=13136', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Protector', 'boxsetList&url=tmdbbox&list=13134', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Psycho', 'boxsetList&url=tmdbbox&list=13133', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Purge', 'boxsetList&url=tmdbbox&list=13129', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Quarantine', 'boxsetList&url=tmdbbox&list=13128', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Raid', 'boxsetList&url=tmdbbox&list=13127', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rambo', 'boxsetList&url=tmdbbox&list=13125', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Saw', 'boxsetList&url=tmdbbox&list=13109', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Sin City', 'boxsetList&url=tmdbbox&list=13103', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Taken', 'boxsetList&url=tmdbbox&list=13095', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Transporter', 'boxsetList&url=tmdbbox&list=13082', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Under Siege', 'boxsetList&url=tmdbbox&list=13078', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Underworld', 'boxsetList&url=tmdbbox&list=13077', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Universal Soldier', 'boxsetList&url=tmdbbox&list=13075', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('VHS', 'boxsetList&url=tmdbbox&list=13074', 'boxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('xXx', 'boxsetList&url=tmdbbox&list=13068', 'boxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category='Thriller Boxsets')

    def kidsboxsets(self):
        self.addDirectoryItem('101 Dalmatians Collection', 'boxsetList&url=tmdbbox&list=13113', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Aladdin Collection', 'boxsetList&url=tmdbbox&list=13155', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('All dogs Go To Heaven Collection', 'boxsetList&url=tmdbbox&list=16473', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Alpha and Omega Collection', 'boxsetList&url=tmdbbox&list=96010', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Balto Collection', 'boxsetList&url=tmdbbox&list=13214', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Bambi Collection', 'boxsetList&url=tmdbbox&list=13217', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Barbie A Mermaid Tale Collection', 'boxsetList&url=tmdbbox&list=96012', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Barbie Fairytopia Collection', 'boxsetList&url=tmdbbox&list=96013', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Barbie Mariposa Collection', 'boxsetList&url=tmdbbox&list=96014', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Beauty and the Beast Collection', 'boxsetList&url=tmdbbox&list=13229', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Brother Bear Collection', 'boxsetList&url=tmdbbox&list=96015', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cars Collection', 'boxsetList&url=tmdbbox&list=13244', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cinderella Collection', 'boxsetList&url=tmdbbox&list=13249', 'boxskidsboxsetsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Cloudy With A Chance Of Meatballs Collection', 'boxsetList&url=tmdbbox&list=13259', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Despicable Me Collection', 'boxsetList&url=tmdbbox&list=13299', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Finding Nemo Collection', 'boxsetList&url=tmdbbox&list=16499', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Frozen Collection', 'boxsetList&url=tmdbbox&list=96016', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Happy Feet Collection', 'boxsetList&url=tmdbbox&list=13265', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hotel Transylvania Collection', 'boxsetList&url=tmdbbox&list=13240', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('How To Train Your Dragon Collection', 'boxsetList&url=tmdbbox&list=13239', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Hunchback Of Notre Dame Collection', 'boxsetList&url=tmdbbox&list=13237', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Ice Age Collection', 'boxsetList&url=tmdbbox&list=13234', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Jungle Book Collection', 'boxsetList&url=tmdbbox&list=13212', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Kung Fu Panda Collection', 'boxsetList&url=tmdbbox&list=13202', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lady And The Tramp Collection', 'boxsetList&url=tmdbbox&list=13200', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Lion King Collection', 'boxsetList&url=tmdbbox&list=13194', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Madagascar Collection', 'boxsetList&url=tmdbbox&list=13187', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Monsters Inc Collection', 'boxsetList&url=tmdbbox&list=13174', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Mulan Collection', 'boxsetList&url=tmdbbox&list=13172', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Open Season Collection', 'boxsetList&url=tmdbbox&list=13150', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Peter Pan Collection', 'boxsetList&url=tmdbbox&list=16498', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Planes Collection', 'boxsetList&url=tmdbbox&list=13142', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Pocahontas Collection', 'boxsetList&url=tmdbbox&list=13140', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Rio Collection', 'boxsetList&url=tmdbbox&list=13117', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Shrek Collection', 'boxsetList&url=tmdbbox&list=16470', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tangled Collection', 'boxsetList&url=tmdbbox&list=96017', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tarzan Collection', 'boxsetList&url=tmdbbox&list=13094', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Croods Collection', 'boxsetList&url=tmdbbox&list=96018', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Emperors New Groove Collection', 'boxsetList&url=tmdbbox&list=96019', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Fox And The Hound Collection', 'boxsetList&url=tmdbbox&list=13301', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Land Before Time Collection', 'boxsetList&url=tmdbbox&list=16485', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('The Little Mermaid Collection', 'boxsetList&url=tmdbbox&list=13192', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Tinkerbell Collection', 'boxsetList&url=tmdbbox&list=96020', 'kidsboxsets.png', 'DefaultBoxSets.png')
        self.addDirectoryItem('Toy Story Collection', 'boxsetList&url=tmdbbox&list=96021', 'kidsboxsets.png', 'DefaultBoxSets.png')

        self.endDirectory(category=' Kids Boxsets')

    def boxsetlist(self, url, list_id):
        if url == 'tmdbbox':
            list_url = self.tmdb_link % (list_id)
            self.tmdbBoxSetParser(list_url, list_id)
            self.worker()
            self.movieDirectory(self.boxset_list)
        elif url == 'tmdbbox':
            list_url = self.tmdb_c_link % (list_id)
            self.tmdbBoxSetParser(list_url, list_id)
            self.worker()
            self.movieDirectory(self.boxset_list)

    def tmdbBoxSetParser(self, url, list_id):
        try:
            content = client.request(url, timeout=10)
            result = json.loads(content)
            items = result['items']
        except Exception:
            return

        next = ''
        for item in items:
            try:
                title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = item['release_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                tmdb = item['id']
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')

                poster = item['poster_path']
                if poster == '' or poster is None:
                    raise Exception()
                else:
                    poster = '%s%s' % (self.tmdb_poster, poster)
                poster = poster.encode('utf-8')

                fanart = item['backdrop_path']
                if fanart == '' or fanart is None:
                    fanart = '0'
                if not fanart == '0':
                    fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')

                premiered = item['release_date']
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except Exception:
                    premiered = '0'
                premiered = premiered.encode('utf-8')

                rating = str(item['vote_average'])
                if rating == '' or rating is None:
                    rating = '0'
                rating = rating.encode('utf-8')

                votes = str(item['vote_count'])
                try:
                    votes = str(format(int(votes), ',d'))
                except Exception:
                    pass
                if votes == '' or votes is None:
                    votes = '0'
                votes = votes.encode('utf-8')

                plot = item['overview']
                if plot == '' or plot is None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try:
                    tagline = tagline.encode('utf-8')
                except Exception:
                    pass

                self.boxset_list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered,
                                         'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes,
                                         'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot,
                                         'tagline': tagline, 'code': '0', 'imdb': '0', 'tmdb': tmdb, 'tvdb': '0',
                                         'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
            except Exception:
                pass

        return self.boxset_list

    def worker(self, level=1):
        self.meta = []
        total = len(self.boxset_list)

        for i in range(0, total):
            self.boxset_list[i].update({'metacache': False})
        self.boxset_list = metacache.fetch(self.boxset_list, 'en', self.user)

        for r in range(0, total, 100):
            threads = []
            for i in range(r, r+100):
                if i <= total:
                    threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

        self.boxset_list = [i for i in self.boxset_list]

        if len(self.meta) > 0:
            metacache.insert(self.meta)

    def super_info(self, i):
        try:
            if self.boxset_list[i]['metacache'] is True:
                raise Exception()

            try:
                tmdb = self.boxset_list[i]['tmdb']
            except Exception:
                tmdb = '0'

            if not tmdb == '0':
                url = self.tmdb_info_link % tmdb

            else:
                raise Exception()

            item = client.request(url, timeout='10')
            item = json.loads(item)

            title = item['title']
            if not title == '0':
                self.boxset_list[i].update({'title': title})

            year = item['release_date']
            try:
                year = re.compile('(\d{4})').findall(year)[0]
            except Exception:
                year = '0'
            if year == '' or year is None:
                year = '0'
            year = year.encode('utf-8')
            if not year == '0':
                self.boxset_list[i].update({'year': year})

            tmdb = item['id']
            if tmdb == '' or tmdb is None:
                tmdb = '0'
            tmdb = re.sub('[^0-9]', '', str(tmdb))
            tmdb = tmdb.encode('utf-8')
            if not tmdb == '0':
                self.boxset_list[i].update({'tmdb': tmdb})

            imdb = item['imdb_id']
            if imdb == '' or imdb is None:
                imdb = '0'
            imdb = imdb.encode('utf-8')
            if not imdb == '0' and "tt" in imdb:
                self.boxset_list[i].update({'imdb': imdb, 'code': imdb})

            poster = item['poster_path']
            if poster == '' or poster is None:
                poster = '0'
            if not poster == '0':
                poster = '%s%s' % (self.tmdb_poster, poster)
            poster = poster.encode('utf-8')
            if not poster == '0':
                self.boxset_list[i].update({'poster': poster})

            fanart = item['backdrop_path']
            if fanart == '' or fanart is None:
                fanart = '0'
            if not fanart == '0':
                fanart = '%s%s' % (self.tmdb_image, fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0' and self.boxset_list[i]['fanart'] == '0':
                self.boxset_list[i].update({'fanart': fanart})

            premiered = item['release_date']
            try:
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except Exception:
                premiered = '0'
            if premiered == '' or premiered is None:
                premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0':
                self.boxset_list[i].update({'premiered': premiered})

            studio = item['production_companies']
            try:
                studio = [x['name'] for x in studio][0]
            except Exception:
                studio = '0'
            if studio == '' or studio is None:
                studio = '0'
            studio = studio.encode('utf-8')
            if not studio == '0':
                self.boxset_list[i].update({'studio': studio})

            genre = item['genres']
            try:
                genre = [x['name'] for x in genre]
            except Exception:
                genre = '0'
            if genre == '' or genre is None or genre == []:
                genre = '0'
            genre = ' / '.join(genre)
            genre = genre.encode('utf-8')
            if not genre == '0':
                self.boxset_list[i].update({'genre': genre})

            try:
                duration = str(item['runtime'])
            except Exception:
                duration = '0'
            if duration == '' or duration is None:
                duration = '0'
            duration = duration.encode('utf-8')
            if not duration == '0':
                self.boxset_list[i].update({'duration': duration})

            rating = str(item['vote_average'])
            if rating == '' or rating is None:
                rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0':
                self.boxset_list[i].update({'rating': rating})

            votes = str(item['vote_count'])
            try:
                votes = str(format(int(votes), ',d'))
            except Exception:
                pass
            if votes == '' or votes is None:
                votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0':
                self.boxset_list[i].update({'votes': votes})

            mpaa = item['releases']['countries']
            try:
                mpaa = [x for x in mpaa if not x['certification'] == '']
            except Exception:
                mpaa = '0'
            try:
                mpaa = ([x for x in mpaa if x['iso_3166_1'].encode('utf-8') == 'US'] + [x for x in mpaa if not x['iso_3166_1'].encode('utf-8') == 'US'])[0]['certification']
            except Exception:
                mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0':
                self.boxset_list[i].update({'mpaa': mpaa})

            director = item['credits']['crew']
            try:
                director = [x['name'] for x in director if x['job'].encode('utf-8') == 'Director']
            except Exception:
                director = '0'
            if director == '' or director is None or director == []:
                director = '0'
            director = ' / '.join(director)
            director = director.encode('utf-8')
            if not director == '0':
                self.boxset_list[i].update({'director': director})

            writer = item['credits']['crew']
            try:
                writer = [x['name'] for x in writer if x['job'].encode('utf-8') in ['Writer', 'Screenplay']]
            except Exception:
                writer = '0'
            try:
                writer = [x for n, x in enumerate(writer) if x not in writer[:n]]
            except Exception:
                writer = '0'
            if writer == '' or writer is None or writer == []:
                writer = '0'
            writer = ' / '.join(writer)
            writer = writer.encode('utf-8')
            if not writer == '0':
                self.boxset_list[i].update({'writer': writer})

            cast = item['credits']['cast']
            try:
                cast = [(x['name'].encode('utf-8'), x['character'].encode('utf-8')) for x in cast]
            except Exception:
                cast = []
            if len(cast) > 0:
                self.boxset_list[i].update({'cast': cast})

            plot = item['overview']
            if plot == '' or plot is None:
                plot = '0'
            plot = plot.encode('utf-8')
            if not plot == '0':
                self.boxset_list[i].update({'plot': plot})

            tagline = item['tagline']
            if (tagline == '' or tagline is None) and not plot == '0':
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
            elif tagline == '' or tagline is None:
                tagline = '0'
            try:
                tagline = tagline.encode('utf-8')
            except Exception:
                pass
            if not tagline == '0':
                self.boxset_list[i].update({'tagline': tagline})

            # IMDB INFOS
            try:
                if imdb is not None or imdb == '0':
                    url = self.imdbinfo % imdb

                    item = client.request(url, timeout='10')
                    item = json.loads(item)

                    plot2 = item['Plot']
                    if plot2 == '' or plot2 is None:
                        plot = plot
                    plot = plot.encode('utf-8')
                    if not plot == '0':
                        self.boxset_list[i].update({'plot': plot})

                    rating2 = str(item['imdbRating'])
                    if rating2 == '' or rating2 is None:
                        rating = rating2
                    rating = rating.encode('utf-8')
                    if not rating == '0':
                        self.boxset_list[i].update({'rating': rating})

                    votes2 = str(item['imdbVotes'])
                    try:
                        votes2 = str(votes2)
                    except Exception:
                        pass
                    if votes2 == '' or votes2 is None:
                        votes = votes2
                    votes = votes.encode('utf-8')
                    if not votes == '0':
                        self.boxset_list[i].update({'votes': votes2})
            except Exception:
                pass
            self.meta.append(
                {'tmdb': tmdb, 'imdb': imdb, 'tvdb': '0', 'lang': 'en',
                 'item':
                 {'title': title, 'year': year, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster,
                  'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration,
                  'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast,
                  'plot': plot, 'tagline': tagline}})
        except Exception:
            pass

    def movieDirectory(self, items):
        if items is None or len(items) == 0:
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
        except Exception:
            isOld = True

        isPlayable = 'true' if 'plugin' not in control.infoLabel('Container.PluginName') else 'false'

        indicators = playcount.getMovieIndicators()
        playbackMenu = control.lang(32063).encode('utf-8') if control.setting('hosts.mode') == '2' else control.lang(32064).encode('utf-8')
        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() is True else control.lang(32066).encode('utf-8')
        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() is True else control.lang(32067).encode('utf-8')
        queueMenu = control.lang(32065).encode('utf-8')
        traktManagerMenu = control.lang(32070).encode('utf-8')
        nextMenu = control.lang(32053).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')

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
                # meta.update({'trailer': 'plugin://script.extendedinfo/?info=playtrailer&&id=%s' % imdb})
                if 'duration' not in i:
                    meta.update({'duration': '120'})
                elif i['duration'] == '0':
                    meta.update({'duration': '120'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except Exception:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], 'en')})
                except Exception:
                    pass

                poster = [i[x] for x in ['poster3', 'poster', 'poster2'] if i.get(x, '0') != '0']
                poster = poster[0] if poster else addonPoster
                meta.update({'poster': poster})

                sysmeta = urllib.quote_plus(json.dumps(meta))

                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)

                cm = []

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except Exception:
                    pass

                if traktCredentials is True:
                    cm.append(
                        (traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' %
                         (sysaddon, sysname, imdb)))

                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                if isOld is True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))

                cm.append(
                    (addToLibrary, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' %
                     (sysaddon, sysname, systitle, year, imdb, tmdb)))

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
                elif addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='Video', infoLabels=meta)

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except Exception:
                pass

        try:
            url = items[0]['next']
            if url == '':
                raise Exception()

            icon = control.addonNext()
            url = '%s?action=moviePage&url=%s' % (sysaddon, urllib.quote_plus(url))

            item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if addonFanart is not None:
                item.setProperty('Fanart_Image', addonFanart)

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except Exception:
            pass

        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('movies', {'skin.estuary': 55, 'skin.confluence': 500})

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []

        queueMenu = control.lang(32065).encode('utf-8')

        if queue is True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, cache=True, contentType='addons', sortMethod=control.xDirSort.NoSort, category=None):
        control.content(syshandle, contentType)
        if category is not None:
            control.category(syshandle, category)
        if sortMethod is not control.xDirSort.NoSort:
            control.sortMethod(syshandle, sortMethod)
        control.directory(syshandle, cacheToDisc=cache)

    def addDirectory(self, items, queue=False, isFolder=True):
        if items is None or len(items) is 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif artPath is not None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                item = control.item(label=name)

                if isFolder:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % urllib.quote_plus(i['url'])
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'false')
                else:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % i['url']
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'true')
                    item.setInfo("mediatype", "video")
                    item.setInfo("audio", '')

                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except Exception:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
