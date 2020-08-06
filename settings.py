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


DEBUG = True

PATH_PYDEVD = {
    'win32': os.environ.get('PYDEVD'),
    'darwin': '/Applications/PyCharm.app/Contents/plugins/python/helpers'
              '/pydev',
    'linux': os.environ.get('PYDEVD')
}

CONFIG_PYDEVD = {
    'server': 'localhost',
    'port': 7575,
    'suspend': False,
    'stdout': True,
    'stderr': True
}

PATH_LOCAL_DIR = os.path.expanduser("~")
PATH_LOCAL_DIR_PLUGIN = f'{PATH_LOCAL_DIR}/.gistools'

PATH_PLUGIN = os.path.abspath(os.path.join(__file__, '../'))

SYS_PATH = (
    PATH_PLUGIN,
    f'{PATH_PLUGIN}/gui',
    f'{PATH_PLUGIN}/apps',
)

ICON = f'{PATH_PLUGIN}/icon.png'
