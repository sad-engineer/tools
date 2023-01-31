#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.abstract_classes import Notifier
from cutting_tools.obj.constants import DECODING
import sys


class StandardResultTerminalPrinter(Notifier):
    """ Выводит результат в консоль"""
    def __init__(self):
        pass

    def log(self, obj, message=None, _path=None):
        if message:
            sys.stdout.write("\n" + message + "\n")
        for key, val in obj.dict_parameters.items():
            sys.stdout.write(f"{DECODING[key].format(obj=val)}\n") if key in DECODING else None


class StandardObjectTerminalPrinter(Notifier):
    """ Выводит объект в консоль"""
    def __init__(self):
        pass

    def log(self, obj, _message=None, _path=None):
        sys.stdout.write(f"{obj.__class__.__name__}({obj.dict_parameters})\n")
