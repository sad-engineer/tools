#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Union, Optional, ClassVar
from pydantic import BaseModel, validator

from tools.obj.constants import GROUPS_TOOL
from service import InvalidValue, InvalidTypeValue


class StringValue:
    """Для определения полей, значение которых должны быть строго строковыми"""

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise InvalidTypeValue(f'Ожидается строковое значение. Тип полученого значение {type(value)}')
        return value

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


class ValueFromDict:
    """Для определения полей, значение которых должны быть из словаря доступных значений"""
    AVAILABLE_VALUES: ClassVar[dict] = {}

    @classmethod
    def validate(cls, value):
        if not isinstance(value, (int, str)):
            raise ValueError(f"Ожидается целое число или строка, получено: {type(value)}")
        elif isinstance(value, str):
            if value not in cls.AVAILABLE_VALUES.values():
                raise InvalidValue(f"Строковое значение должно быть из списка {list(cls.AVAILABLE_VALUES.values())}, "
                                 f"получено: {value}")
            return value
        elif isinstance(value, int):
            if value not in cls.AVAILABLE_VALUES:
                raise InvalidValue(f"Значение должно быть из списка {list(cls.AVAILABLE_VALUES.keys())}, получено: {value}")
            return cls.AVAILABLE_VALUES[value]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


class InGroupsTool(ValueFromDict):
    AVAILABLE_VALUES = GROUPS_TOOL


class MarkingForSpecialTool(ValueFromDict):
    AVAILABLE_VALUES = {0: 'специальный', 1: 'специальная', 2: 'специальное'}
