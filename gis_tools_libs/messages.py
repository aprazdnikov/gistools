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
import queue
import threading
import time

from qgis.core import Qgis
from qgis.utils import iface
from qgis.PyQt.QtWidgets import QProgressBar, QLabel


class MessageStatusBar(threading.Thread):
    def __init__(self, title="", msg="", queue_size=1):
        threading.Thread.__init__(self)
        iface.messageBar().clearWidgets()

        self.title = title
        self.msg = QLabel()
        self.msg.setText(msg)
        self.pipeline = queue.Queue(maxsize=queue_size)
        self.__create_status_bar()

    def run(self):
        while True:
            # Get data from queue
            value = self.pipeline.get()
            self.__set_value_to_progress_bar(value[0], value[1])
            # Send emit because task finished
            self.pipeline.task_done()

    def __create_status_bar(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.message = \
            iface.messageBar().createMessage(self.title)
        self.message.layout().addWidget(self.progress_bar)
        self.message.layout().addWidget(self.msg)

        iface.messageBar().pushWidget(self.message, Qgis.Info)

    def __set_value_to_progress_bar(self, value, message):
        if message:
            self.msg.setText(message)

        value = self.progress_bar.value() + value
        for _ in range(self.progress_bar.value(), value+1, 1):
            time.sleep(0.01)
            self.progress_bar.setValue(_)

    def reset(self, value=0):
        self.progress_bar.setValue(value)

    def set_value(self, value, message=None):
        self.pipeline.put((value, message))
        self.pipeline.join()

    def show_progress(self, value):
        self.__create_status_bar()
        self.pipeline.put(value)
        self.pipeline.join()
