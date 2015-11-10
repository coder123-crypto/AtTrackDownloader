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

import sys
from PyQt5.QtWidgets import QApplication
from qtgui import AtdWindow
from autotravel import Autotravel

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AtdWindow()
    window.show()
    sys.exit(app.exec_())