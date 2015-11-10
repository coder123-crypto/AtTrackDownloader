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

import re
import webbrowser
import urllib.request as urllib2
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QComboBox, QFormLayout
from autotravel import Autotravel

class AtdWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('AtTrackDownloader')
        self.setCentralWidget(QWidget(self))
        self.__create_widgets()
        
        self.__autotravel = Autotravel()
        self.__comboBoxAreas.addItems(sorted(self.__autotravel.get_areas_list()))
        
    def __update_towns(self, text):
        self.__comboBoxTowns.clear()
        self.__comboBoxTowns.addItems(self.__autotravel.get_towns_list(text))
        
    def __save_track(self, state):
        area = self.__comboBoxAreas.currentText()
        town = self.__comboBoxTowns.currentText()
        track_links = self.__autotravel.get_towns_track_links(self.__autotravel.get_town_link(area, town))
        
        filters = [e.upper() + ' треки (*.' + e + ')' for e in track_links]
        fileName, filter = QFileDialog.getSaveFileName(self, 'Save track', '', ';;'.join(filters))
        if fileName:
            ext = re.search('\\.\\w+', filter).group(0)
            track = urllib2.urlopen(track_links[ext[1:]])
            f = open(fileName if fileName.endswith(ext) else fileName + ext, 'wb')
            f.write(track.read())
            f.close()
     
    def __goto_web(self, state):
        area = self.__comboBoxAreas.currentText()
        town = self.__comboBoxTowns.currentText()
        town_link = self.__autotravel.get_town_link(area, town)
        webbrowser.open(town_link)
        
    def __center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def __create_widgets(self):
        self.__l = QFormLayout(self.centralWidget())

        self.__comboBoxAreas = QComboBox(self)
        self.__comboBoxTowns = QComboBox(self)
        self.__buttonDownload = QPushButton('Скачать трек', self)
        self.__buttonOpenWebPage = QPushButton('Открыть страницу с городом', self)
        
        self.__l.addRow('Области: ', self.__comboBoxAreas)
        self.__l.addRow('Города: ', self.__comboBoxTowns)
        self.__l.addRow(self.__buttonDownload)
        self.__l.addRow(self.__buttonOpenWebPage)
        
        self.__buttonDownload.clicked.connect(self.__save_track)
        self.__buttonOpenWebPage.clicked.connect(self.__goto_web)
        self.__comboBoxAreas.currentTextChanged.connect(self.__update_towns)
        
    def showEvent(self, event):
        super(QMainWindow, self).showEvent(event)
        self.setFixedSize(self.size())
        self.__center()