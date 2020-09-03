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


class OUTPUT:

    class MAPINFO:
        TYPE = 'MapInfo TAB'

    class SHP:
        TYPE = 'SHP File'

    class KML:
        TYPE = 'KML File'

    DRIVER = {
        'MapInfo TAB': 'MapInfo File',
        'SHP File': 'ESRI Shapefile',
        'KML File': 'KML'
    }
