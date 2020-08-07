# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                 A QGIS plugin
 Gis simple tools
                             -------------------
        begin                : 2020-08-06
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Aleksandr Prazdnikov
        email                : 79237017153@ya.ru
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from gis_tools_libs.messages import MessageStatusBar


class ProcessingGPXtoTAB:
    def __init__(self):
        self.status = MessageStatusBar()
        self.l_points = ''
        self.l_polylines = ''
        self.l_polygons = ''

    def handle_gpx(self, data):
        pass
