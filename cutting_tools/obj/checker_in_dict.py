#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.exceptions import InvalidValue


def is_correct_dict_values(dict):
    """ Проверяем типы значений (типы всех значений должны быть одинаковы)"""
    try:
        first_key_type = type(next(iter(dict.values())))
    except StopIteration:
        raise InvalidValue("Словарь пуст.")
    return all(map(lambda x: type(x) == first_key_type, dict.values()))


def is_correct_dict_keys(dict):
    """ Проверяем типы ключей (типы всех ключей должны быть одинаковы)"""
    try:
        first_key_type = type(next(iter(dict)))
    except StopIteration:
        raise InvalidValue("Словарь пуст.")
    return all(map(lambda x: type(x) == first_key_type, dict.keys()))


class CheckerInDictionary:
    """ Класс реализует проверку наличия значения в словаре однотипных ключей/значений"""

    def _check_in_dict(self, value, dict, err_message):
        is_correct_dict_keys(dict)
        is_correct_dict_values(dict)
        if isinstance(value, type(next(iter(dict)))) and value not in dict:
            raise InvalidValue(err_message)
        if isinstance(value, type(next(iter(dict.values())))) and value not in dict.values():
            raise InvalidValue(err_message)
        if not isinstance(value, (type(next(iter(dict))), type(next(iter(dict.values()))))):
            raise InvalidValue(err_message)
        return value
