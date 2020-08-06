# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GisTools
                                 A QGIS plugin
 Gis simple tools
                             -------------------
        begin                : 2020-08-06
        copyright            : (C) 2020 by Aleksandr Prazdnikov
        email                : 79237017153@ya.ru
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
import sys
from . import settings

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GisTools class from file GisTools.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    if settings.DEBUG:

        if settings.PATH_PYDEVD.get(sys.platform) not in sys.path:
            sys.path.insert(0, settings.PATH_PYDEVD.get(sys.platform))

        try:
            import pydevd_pycharm
            pydevd_pycharm.settrace(
                settings.CONFIG_PYDEVD['server'],
                port=settings.CONFIG_PYDEVD['port'],
                stdoutToServer=settings.CONFIG_PYDEVD['stdout'],
                stderrToServer=settings.CONFIG_PYDEVD['stderr'],
                suspend=settings.CONFIG_PYDEVD['suspend']
            )
        except ImportError:
            import pydevd
            pydevd.settrace(
                settings.CONFIG_PYDEVD['server'],
                port=settings.CONFIG_PYDEVD['port'],
                stdoutToServer=settings.CONFIG_PYDEVD['stdout'],
                stderrToServer=settings.CONFIG_PYDEVD['stderr'],
                suspend=settings.CONFIG_PYDEVD['suspend']
            )

    for __ in settings.SYS_PATH:
        if __ not in sys.path:
            sys.path.insert(0, __)

    from .gistools import GisTools
    return GisTools(iface)
