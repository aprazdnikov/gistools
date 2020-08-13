# -*- coding: utf-8 -*-
import os
import datetime
import zipfile
import settings

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsMessageLog, Qgis


_MSG_LVL = {
    'info': Qgis.Info,
    'warning': Qgis.Warning,
    'critical': Qgis.Critical,
    'success': Qgis.Success,
    'none': None,
}


class Sender(object):
    """ Object for sending messages to log """

    def __init__(self, parent):
        self.__logs_path = settings.PATH_LOGS
        if not os.path.exists(self.__logs_path):
            os.makedirs(self.__logs_path)

        self.__log_file_name = 'log.txt'

    def send_message(self, message: str, module_name: str,
                     console_view: bool = True,
                     file_view: bool = False, level='info') -> None:
        """ Output message to console and file

        :param message: String
        :param module_name: String
        :param console_view: Boolean
        :param file_view: Boolean - Record to file
        :param level: Level message
        :return: None
        """
        date_now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M")
        message = f'{module_name}: {message};'

        # Send message to console
        if console_view:
            self.__send_console_message(message, level)

        # Record to file
        if file_view:
            self.__send_file_message(f'{date_now} | {message}', module_name)

    def __send_console_message(self, message: str, level='info') -> None:
        """ Output message to console

        :param message: String
        :param level: String
        :return: None
        """
        QgsMessageLog.logMessage(
            message, self.tr("Gis Tools"), level=_MSG_LVL[level]
        )

    def __send_file_message(self, message: str, module_name: str) -> None:
        """ Output message to file

        :param message: String
        :param module_name: String
        :return: None
        """

        log_dir_name = os.path.join(self.__logs_path, module_name)
        log_file_name = os.path.join(log_dir_name, self.__log_file_name)

        if not os.path.exists(log_file_name):
            with open(log_file_name, 'w', encoding='utf-8') as file:
                file.write(message + '\n')
        else:
            with open(log_file_name, 'rb') as file:
                lines_count = len(file.readlines())

            # Archiving and destruction of the log file when the number of
            # lines in it is exceeded
            if lines_count > 10:
                # Compilation of the name of the archive
                with open(log_file_name, "r") as file:
                    lines = file.readlines()
                    first = lines[0]
                    last = lines[lines_count-1]

                first_dt = first.split("|")[0]
                last_dt = last.split("|")[0]

                log_archive_name = f'{first_dt}{last_dt}'

                zf = zipfile.ZipFile(os.path.join(log_dir_name,
                                                  'archive.zip'), 'a')
                zf.write(log_file_name, log_archive_name + ".txt")
                zf.close()
                # Removing an obsolete log file
                os.remove(log_file_name)

            # Outputting logs to a file with its creation
            with open(log_file_name, 'a', encoding='utf-8') as file:
                file.write(message + '\n')

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
