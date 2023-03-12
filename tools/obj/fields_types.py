#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar

from service import InvalidValue, InvalidTypeValue

from tools.obj.constants import GROUPS_TOOL, MATERIALS_OF_CUTTING_PART, ACCURACY_STANDARDS, TOLERANCE_FIELDS, \
    TYPES_OF_MILLING_CUTTER, TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER, TYPES_OF_LARGE_TOOTH, ACCURACY_CLASS_STANDARDS


class StringValue:
    """Для определения полей, значение которых должны быть строго строковыми"""

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise InvalidTypeValue(f'Ожидается строковое значение. Тип полученного значение {type(value)}')
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
            if value not in cls.AVAILABLE_VALUES:
                raise InvalidValue(f"Строковое значение должно быть из списка {list(cls.AVAILABLE_VALUES.keys())}, "
                                   f"получено: {value}")
            return value
        elif isinstance(value, int):
            if value not in cls.AVAILABLE_VALUES.values():
                raise InvalidValue(f"Значение должно быть из списка {list(cls.AVAILABLE_VALUES.values())}, "
                                   f"получено: {value}")
            index = list(cls.AVAILABLE_VALUES.values()).index(value)
            return list(cls.AVAILABLE_VALUES.keys())[index]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


class InGroupsTool(ValueFromDict):
    AVAILABLE_VALUES = GROUPS_TOOL


class MarkingForSpecialTool(ValueFromDict):
    AVAILABLE_VALUES = {'специальный': 0, 'специальная': 1, 'специальное': 2}


class InMaterialsOfCuttingPart(ValueFromDict):
    AVAILABLE_VALUES = MATERIALS_OF_CUTTING_PART


class InAccuracyStandards(ValueFromDict):
    AVAILABLE_VALUES = {v: k for k, v in ACCURACY_STANDARDS.items()}


class InToleranceField(ValueFromDict):
    AVAILABLE_VALUES = {v: k for k, v in TOLERANCE_FIELDS.items()}


class InTypesOfMillingCutter(ValueFromDict):
    AVAILABLE_VALUES = TYPES_OF_MILLING_CUTTER


class InTypesOfCuttingPart(ValueFromDict):
    AVAILABLE_VALUES = TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER


class InTypesOfLargeTooth(ValueFromDict):
    AVAILABLE_VALUES = TYPES_OF_LARGE_TOOTH


class InAccuracyClassStandards(ValueFromDict):
    AVAILABLE_VALUES = ACCURACY_CLASS_STANDARDS
