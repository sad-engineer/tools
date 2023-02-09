#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import inspect
from typing import Union, Optional
from logger.obj.exceptions import InvalidValue


def get_class_names(module_names) -> list:
    """ Вернет список ссылок классов из списка пакетов/модулей 'module_names'"""
    if isinstance(module_names, str):
        return [obj for name, obj in inspect.getmembers(__import__(module_names)) if inspect.isclass(obj)]
    elif isinstance(module_names, (list, tuple)):
        return [class_name for module_name in module_names for class_name in get_class_names(module_name)]


class Cataloger:
    """ Хранит ссылки на классы проекта"""
    def __init__(self, module_names: Union[str, list, tuple] = "!cutting_tools") -> None:
        self._module_names = module_names
        self._classes: Optional[list] = None
        self._get_classes(self._module_names)

    def _get_classes(self, module_names) -> None:
        """ Вернет список ссылок классов из списка пакетов/модулей 'module_names'"""
        if isinstance(module_names, (str, list, tuple)):
            self._classes = get_class_names(module_names)
        else:
            raise InvalidValue(f"Для поиска классов передайте имя модуля или список имен модулей. Вы передали "
                               f"{self._module_names}")

    @property
    def classes(self) -> list:
        return self._classes

    def get_class_by_name(self, name: str):
        return next((class_ for class_ in self._classes if name == class_.__name__), None)


if __name__ == "__main__":
    # cataloger = Cataloger(["logger", "!cutting_tools"])
    # print(cataloger.classes)
    # print(cataloger.get_class_by_name("Logger"))

    cataloger = Cataloger("!cutting_tools")
    print(cataloger.classes)
