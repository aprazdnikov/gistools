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

import os
import weakref

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal

from gis_tools_apps import gpx_convert
from gis_tools_libs.enums import OUTPUT

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'gis_tools_dockwidget_base.ui'))


class GisToolsDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, gis_tools, parent=None):
        super(GisToolsDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.gis_tools = weakref.ref(gis_tools)

        self.gpxTab.clicked.connect(self._run_gpx_to_tab)
        self.gpxKml.clicked.connect(self._run_gpx_to_kml)
        self.gpxShp.clicked.connect(self._run_gpx_to_shp)

    def _run_gpx_to_tab(self):
        gpx_convert.show(self.gis_tools, OUTPUT.MAPINFO.TYPE)

    def _run_gpx_to_kml(self):
        gpx_convert.show(self.gis_tools, OUTPUT.KML.TYPE)

    def _run_gpx_to_shp(self):
        gpx_convert.show(self.gis_tools, OUTPUT.SHP.TYPE)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
