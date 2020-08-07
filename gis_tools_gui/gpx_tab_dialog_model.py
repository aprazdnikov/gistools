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

from typing import Iterator, Tuple, Union, List
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt


class ModelFiles(QAbstractTableModel):

    def __init__(self, headers: Tuple[str, str], parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.headers = headers
        self.folder: str = ''
        self.files: List = []

    def rowCount(self, parent=QModelIndex(), *args, **kwargs) -> int:
        return len(self.files)

    def columnCount(self, parent=QModelIndex(), *args, **kwargs) -> int:
        return len(self.headers)

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = None):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]

        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return f"{section + 1}"

    def data(self, index: QModelIndex, role: int = None) -> Union[None, str]:

        if not index.isValid() or role != Qt.DisplayRole:
            return None

        if role == Qt.DisplayRole and self.files:
            return self.files[index.row()][index.column()]

        return None

    def row_data(self, index: QModelIndex) -> Union[None, List]:
        if index.isValid() and self.files:
            return self.files[index.row()]

        return None

    def rows_data(self) -> Iterator[List]:
        for row in self.files:
            yield row

    def update(self, path):
        """ Обновление модели и уведомление об этом tableView """
        self.folder = path
        self.removeRows(0, self.rowCount())
        self.__get_projects()
        self.layoutChanged.emit()

    def __get_projects(self) -> None:
        self.files = []
        for name in [f.name for f in os.scandir(self.folder)
                     if f.is_file() and '.gpx' in f.name]:
            file = f"{self.folder}/{name}"
            self.files.append([name, file])
