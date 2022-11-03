#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        exceptions
# Purpose:     Contains local exceptions
#
# Author:      ANKorenuk
#
# Created:     20.05.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Содержит локальные исключения
# -------------------------------------------------------------------------------


class InvalidValue(Exception):
    """Исключение возникает при некорректном значении переменной.
    Например, если значение не соответствует ожидаемому типу или пустое

    Атрибуты:
        message: объяснение ошибки
    """
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class ReceivedEmptyDataFrame(Exception):
    """Выкидывать ошибку, если DataFrame пустой.
    message: объяснение ошибки
    """
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class UnexpectedDataInDataFrame(Exception):
    """Выкидывать ошибку, если данные в DataFrame не похожи на ожидаемый
    результат (Больше строк, чем предполагалось; пустой DataFrame; и т.д.)
    message: объяснение ошибки
    """
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)
