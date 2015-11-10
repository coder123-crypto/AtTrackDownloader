#!/usr/bin/env python
# coding: utf8

"""
Copyright (C) 2015 Eremin V. Leonid (leremin@outlook.com)

This file is part of ATTrackDownloder.

ATTrackDownloder is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ATTrackDownloder is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ATTrackDownloder.  If not, see <http://www.gnu.org/licenses/>.
"""

from collections import defaultdict
import re
import urllib
import urllib.parse
import pickle
from bs4 import BeautifulSoup
import urllib.request as urllib2

AutoTravelHttp = 'http://www.autotravel.ru'

class Autotravel:
    def __init__(self):
        try:
            with open('attd.cache', 'rb') as f:
                self.__all_towns = pickle.load(f)
        except FileNotFoundError:
            self.__all_towns = list(self.__load_all_towns())
            self.__save_to_cache(self.__all_towns)

    def get_towns_track_links(self, href):
        req = urllib2.Request(href)
        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response.read().decode('utf-8'), 'html.parser')
    
        r = {}
        for link in soup.findAll('a', {'class' : 'travell5m'}):
            if link.get_text() == 'GPX':
                r['gpx'] = AutoTravelHttp + link.get('href')
            elif link.get_text() == 'KML':
                r['kml'] = AutoTravelHttp + link.get('href')
            elif link.get_text() == 'WPT':
                r['wpt'] = AutoTravelHttp + link.get('href')

        return r

    def get_town_link(self, area, town):
        for it in self.__all_towns:
            if it['town'] == town and it['area'] == area:
                return AutoTravelHttp + it['href']
        return ''  

    def get_towns_list(self, area):
        return map(lambda t : t['town'], filter(lambda t : t['area'] == area, self.__all_towns))

    def get_areas_list(self):
        return set(map(lambda t : t['area'], self.__all_towns))

    def __load_all_towns(self):
        for letter in range(1, 31):
            for town in self.__load_towns('a' + str(letter).zfill(2)):
                yield town
    
    def __load_towns(self, letter):
        html_src = self.__load_towns_page(letter)
        return self.__load_towns_from_url(html_src)

    def __load_towns_page(self, letter):
        url = AutoTravelHttp + '/towns.php'
        params = {'l' : letter.encode('cp1251')}
        req = urllib2.Request(url, urllib.parse.urlencode(params).encode('cp1251'))
        response = urllib2.urlopen(req)
        return response.read().decode('utf-8')

    def __load_towns_from_url(self, html_src):
        for line in html_src.splitlines():
            soup = BeautifulSoup(line, 'html.parser')
            area = soup.find('font', {'class' : 'travell0'})
            town= soup.find('a', {'class', 'travell5'})
        
            if town == None:
                town = soup.find('a', {'class', 'travell5c'})
            
            if town == None:
                continue
            
            town_name = town.get_text().strip()
            area_name = area.get_text().strip()[1:-1]
            town_href = town.get('href')
            yield {'area' : area_name, 'town' : town_name, 'href' : town_href}
            
    def __save_to_cache(self, data):
        with open('attd.cache', 'wb') as f:
            pickle.dump(data, f)