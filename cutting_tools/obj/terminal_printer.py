#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.abstract_classes import Notifier
from cutting_tools.obj.constants import DECODING
import sys


class TerminalPrinter(Notifier):
    """ Выводит результат в консоль"""
    def __init__(self):
        pass

    def log(self, obj, message=None, path=None):
        if message:
            sys.stdout.write("\n" + message + "\n")
        for key, val in obj.dict_parameters.items():
            sys.stdout.write(f"{DECODING[key].format(obj=val)}\n") if key in DECODING else None

