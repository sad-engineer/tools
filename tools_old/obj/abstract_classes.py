#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod


class Size(ABC):
    """Абстрактный класс для наследования классами, содержащими размеры"""

    @property
    @abstractmethod
    def gabarit_volume(self):
        pass

    @property
    @abstractmethod
    def gabarit_str(self):
        pass
