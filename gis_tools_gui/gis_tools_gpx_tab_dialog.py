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
import typing
import settings

from PyQt5.QtWidgets import QFileDialog, QHeaderView as QHV
from PyQt5.QtCore import QCoreApplication, QSize
from qgis.PyQt import uic
from qgis.PyQt.QtGui import QIcon

from gis_tools_apps.gpx_to_tab.processing_gpx_to_tab import ProcessingGPXtoTAB
from gis_tools_gui.gpx_tab_dialog_model import ModelFiles


_FORM_CLASS, _BASE = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'gis_tools_gpx_tab_dialog.ui'))


class GpxTabDialog(_BASE, _FORM_CLASS):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(settings.ICON))

        self.btnFolder.setIcon(self._get_icon('search.png'))
        self.btnFolder.setIconSize(QSize(30, 30))
        self.btnFolder.setWhatsThis(self.tr("Select folder"))
        self.btnFolder.setStatusTip(self.tr("Select folder"))

        self.btnAll.setIcon(self._get_icon('all.png'))
        self.btnAll.setIconSize(QSize(30, 30))
        self.btnAll.setWhatsThis(self.tr("Convert all items to MapInfo TAB"))
        self.btnAll.setStatusTip(self.tr("Convert all items to MapInfo TAB"))
        self.btnAll.setDisabled(True)

        self.btnSelect.setIcon(self._get_icon('select.png'))
        self.btnSelect.setIconSize(QSize(30, 30))
        self.btnSelect.setWhatsThis(
            self.tr("Convert selected items to MapInfo TAB"))
        self.btnSelect.setStatusTip(
            self.tr("Convert selected items to MapInfo TAB"))
        self.btnSelect.setDisabled(True)

        self.btnCancel.setIcon(self._get_icon('cancel.png'))
        self.btnCancel.setIconSize(QSize(30, 30))
        self.btnCancel.setWhatsThis(self.tr("Cancel"))
        self.btnCancel.setStatusTip(self.tr("Cancel"))

        self.btnFolder.clicked.connect(self._select_folder)
        self.btnAll.clicked.connect(self._processing_all)
        self.btnSelect.clicked.connect(self._processing_select)
        self.btnCancel.clicked.connect(self.accept)

        self.model = ModelFiles((self.tr('File name'), 'path'))
        self.tableView.setModel(self.model)
        self.tableView.setColumnHidden(1, True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHV.Stretch)

        self.exec_()

    def _select_folder(self):
        path = QFileDialog.getExistingDirectory(
            self, self.tr('Select folder with files GPX format'), '.'
        )

        if path:
            self.model.update(path)
            self.btnAll.setEnabled(True)
            self.btnSelect.setEnabled(True)
            self.label.setText(
                self.tr('Select item or all items convert to MapInfo TAB')
            )

    def _processing_all(self):
        process = ProcessingGPXtoTAB()
        for data in self.model.rows_data():
            process.handle_gpx(data)

    def _processing_select(self):
        idx_list = self.tableView.selectionModel().selectedRows()

        if not len(idx_list):
            self.label.setText(
                self.tr('You must select at least one file from the list')
            )
        else:
            process = ProcessingGPXtoTAB()
            for item in list(idx_list):
                process.handle_gpx(self.model.row_data(item))

    @staticmethod
    def _get_icon(name: typing.Text) -> QIcon:
        return QIcon(settings.PATH_PLUGIN + '/resources' + '/' + name)

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

    # noinspection PyMethodMayBeStatic
    def closeEvent(self, event):
        event.accept()
