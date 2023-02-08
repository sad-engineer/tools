#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod


class Notifier(ABC):
    """ Абстрактный класс, базовый для всех логеров или классов вывода результата"""
    @abstractmethod
    def log(self, obj, message, path): return path


class Size(ABC):
    """ Абстрактный класс для наследования классами, содержащими размеры """

    @property
    @abstractmethod
    def gabarit_volume(self): pass

    @property
    @abstractmethod
    def gabarit_str(self): pass



