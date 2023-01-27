#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
import pandas as pd

class Dictionarer(ABC):
    """ Абстрактный класс, наследовать для вывода словаря параметров класса"""
    @abstractmethod
    def _dict_parameters(self) -> dict: pass
        # """ Возвращать словарь публичных параметров класса. Использовать для конструктора внитри дочерних классов
        # (при множественном наследовании) """

    @property
    def dict_parameters(self):
        return self._dict_parameters()


class Notifier(ABC):
    """ Абстрактный класс, базовый для всех логгеров или классов вывода результата"""
    @abstractmethod
    def log(self, obj, message, path): return path


class RecordRequester(ABC):
    """ Абстрактный класс, реализующий работу с какой-либо БД"""
    @abstractmethod
    def get_records(self, values_dict: dict) -> pd.DataFrame: pass
        # """ Реализация метода должна обеспечивать получение записей по словарю столбцов:значений, передаваемых в
        # values_dict """

    @property
    @abstractmethod
    def get_all_records(self) -> pd.DataFrame: pass
        # """ Возвращает DataFrame со всеми записями таблицы tablename."""


class Size(ABC):
    """ Абстрактный класс для наследования классами, содержащими размеры """

    @property
    @abstractmethod
    def gabarit_volume(self): pass

    @property
    @abstractmethod
    def gabarit_str(self): pass
