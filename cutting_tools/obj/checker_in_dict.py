#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from cutting_tools.obj.exceptions import InvalidValue


class CheckerInDictionary:
    """ Класс реализует проверку наличия значения в словаре однотипных ключей/значений"""

    @staticmethod
    def _in_dict(index, value, dict):
        if isinstance(index, type(list(dict.keys())[0])):
            return index in dict
        if isinstance(value, type(list(dict.values())[0])):
            return index in dict
        return False

    def check_in_dict(self, index, value, dict, err_message):
        if self._in_dict(index, value, dict):
            return index, value
        else:
            raise InvalidValue(err_message)

    def check_index_in_dict(self, index, dict, err_message):
        if self._in_dict(index, None, dict):
            return index
        else:
            raise InvalidValue(err_message)

    def check_value_in_dict(self, value, dict, err_message):
        if self._in_dict(None, value, dict):
            return value
        else:
            raise InvalidValue(err_message)
