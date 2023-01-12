#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
from abc import ABC, abstractmethod





class StandartTool(ABC):
    """ Абстрактный класс, базовый для """
    @abstractmethod
    def log(self, obj, message, path):
        return path