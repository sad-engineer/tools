#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import logging.config
from typing import List

from service_for_my_projects.obj.exceptions import InvalidValue

from tools.obj.entities import Tool
from tools.logger_settings import config

import os.path
if not os.path.exists("logs/"):
    os.makedirs("logs/")

logging.config.dictConfig(config)


def output_error_message(attr_names: List[str]):
    """Логирует ошибку корректировки наименования инструмента"""
    def decorator(func):
        def wrapper(tool):
            for name in attr_names:
                if isinstance(getattr(tool, name, None), type(None)):
                    log = logging.getLogger("tool_names")
                    log.error(f"Поле {name} класса {tool.__class__.__name__} ({tool.name}) не определено.")
            return func(tool)
        return wrapper
    return decorator


def output_info_message():
    """Логирует информационное сообщение при ошибке корректировки наименования инструмента"""
    def decorator(func):
        def wrapper(tool):
            try:
                return func(tool)
            except TypeError:
                log = logging.getLogger("tool_names")
                log.info(f"Наименование инструмента {tool.name} принято по умолчанию")
        return wrapper
    return decorator


def get_name(tool: Tool) -> None:
    """ Определяет наименование инструмента в зависимости от ГОСТа

    tool : Tool : Класс инструмента.
    """
    name_getters = {
        # Сверла
        'ГОСТ 886-77': get_name_tool_with_accuracy,
        'ГОСТ 2092-77': get_name_tool_with_accuracy,
        'ГОСТ 4010-77': get_name_tool_with_accuracy,
        'ГОСТ 8034-76': None,
        'ГОСТ 10902-77': get_name_tool_with_accuracy,
        'ГОСТ 10903-77': get_name_tool_with_accuracy,
        'ГОСТ 12121-77': get_name_tool_with_accuracy,
        'ГОСТ 12122-77': get_name_tool_with_accuracy,
        'ГОСТ 14952-75': None,
        'ГОСТ 17273-71': get_name_tool_with_material,
        'ГОСТ 17274-71': get_name_tool_with_material,  # TODO: Т в наименовании
        'ГОСТ 17275-71': get_name_tool_with_material,  # TODO: Т в наименовании
        'ГОСТ 17276-71': get_name_tool_with_material,  # TODO: Т в наименовании
        'ГОСТ 19543-74': None,
        'ГОСТ 19544-74': None,
        'ГОСТ 19545-74': None,
        'ГОСТ 19546-74': None,
        'ГОСТ 19547-74': None,
        'ГОСТ 20694-75': None,
        'ГОСТ 20695-75': None,
        'ГОСТ 20696-75': None,
        'ГОСТ 20697-75': None,
        'ГОСТ 22735-77': get_name_tool_with_accuracy,
        'ГОСТ 22736-77': get_name_tool_with_accuracy,
        'ГОСТ 28319-89': None,
        'ГОСТ 28320-89': None,
        # Зенкеры
        'ГОСТ 12489-71': get_name_tool_with_accuracy,
        'ГОСТ 21584-76': None,
        # Фрезы
        'ГОСТ 1336-77': get_name_tool_with_accuracy,
        'ГОСТ 3964-69': get_name_tool_with_accuracy,
        'ГОСТ 5348-69': get_name_tool_with_material,
        'ГОСТ 6396-78': get_name_tool_with_accuracy,
        'ГОСТ 6469-69': get_name_tool_with_material,
        'ГОСТ 6637-80': get_name_tool_with_accuracy_class_and_module,
        'ГОСТ 7063-72': None,
        'ГОСТ 8027-86': get_name_tool_with_accuracy_class,
        'ГОСТ 8543-71': get_name_tool_with_accuracy,
        'ГОСТ 9140-78': get_name_tool_with_accuracy,
        'ГОСТ 9304-69': None,
        'ГОСТ 9305-93': None,
        'ГОСТ 9324-80': get_name_tool_with_accuracy_class,
        'ГОСТ 9473-80': get_name_tool_with_material,
        'ГОСТ 10331-81': get_name_tool_with_accuracy_class,
        'ГОСТ 10673-75': None,
        'ГОСТ 13838-68': get_name_tool_with_number,
        'ГОСТ 15086-69': None,
        'ГОСТ 15127-83': get_name_tool_with_accuracy_class,
        'ГОСТ 16222-81': None,
        'ГОСТ 16223-81': None,
        'ГОСТ 16225-81': None,
        'ГОСТ 16226-81': None,
        'ГОСТ 16227-81': get_name_tool_with_accuracy,
        'ГОСТ 16228-81': None,
        'ГОСТ 16229-81': None,
        'ГОСТ 16230-81': None,
        'ГОСТ 16231-81': None,
        'ГОСТ 16463-80': get_name_tool_with_accuracy,
        'ГОСТ 18372-73': get_name_tool_with_material,
        'ГОСТ 17026-71': None,
        'ГОСТ 20533-75': None,
        'ГОСТ 20534-75': None,
        'ГОСТ 20535-75': None,
        'ГОСТ 20538-75': None,
        'ГОСТ 22088-76': None,
        'ГОСТ 23248-78': None,
        'ГОСТ 24359-80': None,
        'ГОСТ 24637-81': None,
        'ГОСТ 28527-90': get_name_tool_with_accuracy,
        'ГОСТ 28709-90': None,
        'ГОСТ 28719-90': None,
        'ГОСТ Р 50181-92': None,
        # Развертки
        'ГОСТ 7722-77': get_name_tool_with_accuracy,
        'ГОСТ 11179-71': None,
        'ГОСТ 11180-71': None,
        'ГОСТ 28321-89': None,
        'ГОСТ 883-80': get_name_tool_with_accuracy,
        # Резцы
        'ГОСТ 10046-72': None,
        'ГОСТ 18871-73': None,
        'ГОСТ 18878-73': get_name_tool_with_material,
        }
    if tool.standard not in name_getters:
        raise InvalidValue(f"Необходимо добавить вариант определения наименования инструмента для инструмента "
                           f"{tool.group} {tool.standard}")
    name_getter = name_getters[tool.standard]
    if not isinstance(name_getter, type(None)):
        name_getter(tool)


@output_info_message()
@output_error_message(["tolerance"])
def get_name_tool_with_accuracy(tool: Tool) -> None:
    """ Наименование состоит из наименования, обозначения, точности(опционально) и стандарта."""
    tool.name = " ".join([tool.group, tool.marking, tool.tolerance, tool.standard])


@output_info_message()
@output_error_message(["accuracy_class"])
def get_name_tool_with_accuracy_class(tool: Tool) -> None:
    """ Наименование состоит из наименования, обозначения, точности(опционально) и стандарта."""
    tool.name = " ".join([tool.group, tool.marking, tool.accuracy_class, tool.standard])


@output_info_message()
@output_error_message(["mat_of_cutting_part"])
def get_name_tool_with_material(tool: Tool) -> None:
    """ Наименование состоит из наименования, обозначения, материала режущей части и стандарта. """
    tool.name = " ".join([tool.group, tool.marking, tool.mat_of_cutting_part, tool.standard])


@output_info_message()
@output_error_message(["cutter_number"])
def get_name_tool_with_number(tool: Tool) -> None:
    """ Наименование состоит из наименования, обозначения, материала режущей части и стандарта. """
    tool.name = " ".join([tool.group, tool.marking, tool.cutter_number, tool.standard])


@output_info_message()
@output_error_message(["module", "accuracy_class"])
def get_name_tool_with_accuracy_class_and_module(tool: Tool) -> None:
    """ Наименование состоит из наименования, обозначения, точности(опционально) и стандарта."""
    tool.name = " ".join([tool.group, tool.marking, tool.module, tool.accuracy_class, tool.standard])
