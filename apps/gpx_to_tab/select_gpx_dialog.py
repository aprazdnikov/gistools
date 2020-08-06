# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GisToolsDockWidget
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
import weakref

from gui.gpx_tab_dialog import GpxTabDialog


class GpxToTab(object):
    def __init__(self, parent):
        self.parent = weakref.ref(parent)
        self.dialog = GpxTabDialog()