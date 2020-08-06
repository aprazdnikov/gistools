# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GpxTabDialog
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

from qgis.PyQt import uic


FORM_CLASS, BASE = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'gpx_tab_dialog.ui'))


class GpxTabDialog(BASE, FORM_CLASS):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btnAll.setDisabled(True)
        self.btnSelect.setDisabled(True)

        self.btnFolder.clicked.connect(self._select_folder)
        self.btnAll.clicked.connect(self._processing_all)
        self.btnSelect.clicked.connect(self._processing_select)
        self.btnCancel.clicked.connect(self.accept)

        self.exec_()

    @staticmethod
    def _select_folder():
        pass

    @staticmethod
    def _processing_all():
        pass

    @staticmethod
    def _processing_select():
        pass

    def closeEvent(self, event):
        event.accept()
