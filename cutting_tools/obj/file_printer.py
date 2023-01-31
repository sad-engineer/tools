#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import datetime
import os

from cutting_tools.obj.abstract_classes import Notifier
from cutting_tools.obj.constants import DECODING


class StandardResultFilePrinter(Notifier):
    """ Выводит результат в файл"""
    def __init__(self):
        # Настройки по умолчанию. Расположение лога определять вне класса.
        self.prefix = datetime.datetime.now().strftime('%H-%M %d-%m-%Y')
        self.folder = f"{__file__}".replace("obj\\file_printer.py", f"logs")
        self.path = self.folder + f"\\{self.prefix}_log.txt"

    def _check_folder(self, folder_path=None):
        if isinstance(folder_path, type(None)):
            folder_path = self.folder
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    def log(self, obj, message=None, path=None, full=False):
        if isinstance(path, type(None)):
            self._check_folder()
            path = self.path

        with open(path, 'a+', encoding='UTF8') as f:
            f.write(f"{message}\n")
            for key, val in obj.dict_parameters.items():
                if full:
                    f.write(f"{DECODING[key].format(obj=val)}\n") if key in DECODING else f.write(f"{key} = {val}\n")
                else:
                    f.write(f"{DECODING[key].format(obj=val)}\n") if key in DECODING else f.write(f"")
            f.write("\n")
        return path


class StandardObjectFilePrinter(StandardResultFilePrinter):
    """ Выводит результат в файл"""
    def __init__(self):
        StandardResultFilePrinter.__init__(self)

    def log(self, obj, message=None, path=None, _full=False):
        if isinstance(path, type(None)):
            self._check_folder()
            path = self.path

        with open(path, 'a+', encoding='UTF8') as f:
            f.write(f"{obj.__class__.__name__}({obj.dict_parameters})\n")
        return path
