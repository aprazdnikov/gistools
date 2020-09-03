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
import os

from qgis.core import (
    QgsVectorLayer, QgsGeometry, QgsPointXY, QgsField, QgsFeature, QgsPoint,
    QgsProject, QgsVectorFileWriter, QgsMessageLog, Qgis
)
from qgis.PyQt.QtCore import QVariant, QCoreApplication

from gis_tools_libs import gpxpy
from gis_tools_libs.messages import MessageStatusBar

_TIME = 'time'
_NAME = 'name'


class ProcessingGPX:
    def __init__(self, folder: str, parent, out_type: str, driver: str):
        self.status = MessageStatusBar()
        self.status.start()

        self.log = parent.log
        self.iface = parent.iface
        self.out_type = out_type
        self.driver = driver

        self.folder = f'{folder}/output'
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        self.mi_points = QgsVectorLayer('Point', 'points', 'memory')
        self.mi_points.dataProvider().addAttributes(
            [QgsField(_NAME, QVariant.String)])
        self.mi_points.dataProvider().addAttributes(
            [QgsField(_TIME, QVariant.String)])
        self.mi_points.updateFields()

        self.mi_tracks = QgsVectorLayer('LineString', 'tracks', 'memory')
        self.mi_tracks.dataProvider().addAttributes(
            [QgsField(_NAME, QVariant.String)])
        self.mi_tracks.dataProvider().addAttributes(
            [QgsField(_TIME, QVariant.String)])
        self.mi_tracks.updateFields()

        self.mi_routes = QgsVectorLayer('LineString', 'routes', 'memory')
        self.mi_routes.dataProvider().addAttributes(
            [QgsField(_NAME, QVariant.String)])
        self.mi_routes.dataProvider().addAttributes(
            [QgsField(_TIME, QVariant.String)])
        self.mi_routes.updateFields()

    def handle_gpx(self, data):
        count = len(data)
        current = 1
        percent = round((100 / count))
        success = self.tr("complete")

        for name, gpx in self._get_gpx(data):
            msg = self.tr('Handle %s of %s')
            self.status.set_value(0, msg % (current, count))

            for waypoint in gpx.waypoints:
                self._handle_points(waypoint, name, self.mi_points)

            for track in gpx.tracks:
                self._handle_tracks_and_routes(track, name, self.mi_tracks)

            for route in gpx.routes:
                self._handle_tracks_and_routes(route, name, self.mi_routes)

            self.status.set_value(percent)
            current += 1

            self.log.send_message(
                f'{name} {success}', self.tr('Handle GPX')
            )

        self._save_to_files()

        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage(
            f'GPX -> {self.out_type}', self.tr('Handle complete'), Qgis.Success
        )

    def _handle_points(self, point, name, layer):
        features = []
        name, time, geom = self._get_geometry_waypoint(point, name)
        features = self._prepare_features(
            layer.fields(), name, time, geom, features)
        layer.dataProvider().addFeatures(features)

    def _handle_tracks_and_routes(self, part, name, layer):
        features = []
        name, time, geoms = self._get_geometry_track(part, name)
        for geom in geoms:
            features = self._prepare_features(
                layer.fields(), name, time, geom, features)
            layer.dataProvider().addFeatures(features)

    def _save_to_files(self):

        self.status.reset()
        self.status.set_value(0, self.tr('Save to file'))

        if self.mi_points.featureCount():
            self.__save(self.mi_points)

        self.status.set_value(30)

        if self.mi_tracks.featureCount():
            self.__save(self.mi_tracks)

        self.status.set_value(30)

        if self.mi_routes.featureCount():
            self.__save(self.mi_routes)

        self.status.set_value(40)

    def __save(self, layer):
        tc = QgsProject.instance().transformContext()
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = self.driver
        options.actionOnExistingFile = \
            QgsVectorFileWriter.CreateOrOverwriteFile
        options.layerName = layer.name()

        file = f'{self.folder}/{layer.name()}'

        result = QgsVectorFileWriter.writeAsVectorFormatV2(
            layer=layer, fileName=file, transformContext=tc,
            options=options
        )
        if not result[0] == QgsVectorFileWriter.NoError:
            self.log.send_message(result[1], __class__.__name__)

    @staticmethod
    def _get_geometry_waypoint(data, name):
        name = data.name if data.name else name
        time = str(data.time)
        geom = QgsGeometry.fromPointXY(
            QgsPointXY(data.longitude, data.latitude)
        )
        return name, time, geom

    @staticmethod
    def _get_geometry_track(data, name):
        name = data.name if data.name else name
        time = None
        geom = []
        for segment in data.segments:
            time = str(segment.points[0].time)
            points = [QgsPoint(point.longitude, point.latitude)
                      for point in segment.points]
            geom.append(QgsGeometry.fromPolyline(points))

        return name, time, geom

    @staticmethod
    def _prepare_features(fields, name, time, geom, features):
        feat = QgsFeature(fields)
        feat.setAttribute(_NAME, name)
        feat.setAttribute(_TIME, time)
        feat.setGeometry(geom)
        features.append(feat)
        return features

    @staticmethod
    def _get_gpx(list_data):
        for file in list_data:
            with open(file[1], 'r') as file_gpx:
                yield file[0], gpxpy.parse(file_gpx)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate(__class__.__name__, message)
