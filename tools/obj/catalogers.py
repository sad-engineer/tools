#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar

from tools.obj import cutters

TOOLS_CLASSES_BY_TYPE = {"Инструмент": "Tool",
               "Резец": "TurningCutter",
               "Фреза": "MillingCutter",
               "Сверло": "DrillingCutter",
               "Зенкер": "CountersinkingCutter",
               "Развертка": "DeploymentCutter",
               # "Протяжка": "broaching",
               }


class Cataloger:
    """ Хранит ссылки на классы проекта"""
    BY_TYPE: ClassVar[str] = TOOLS_CLASSES_BY_TYPE

    def __init__(self) -> None:
        self._classes = [obj for name, obj in cutters.__dict__.items() if isinstance(obj, type)]

    @property
    def classes(self) -> list:
        return self._classes

    def by_name(self, name: str):
        return next((class_ for class_ in self._classes if name == class_.__name__), None)

    def by_type(self, type_tool: str):
        assert type_tool in self.BY_TYPE
        return self.by_name(self.BY_TYPE[type_tool])


if __name__ == "__main__":
    cataloger = Cataloger()
    print(cataloger.classes)
    print(cataloger.by_name("MillingCutter"))
    print(cataloger.by_type("Фреза"))
