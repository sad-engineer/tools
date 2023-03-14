#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from pydantic import ValidationError

from tools.obj.entities import ErrorWithData


def debug_message_when_creating_instance_of_class():
    """Логирует создание объекта (экземпляра модели данных). При ошибке создания - логирует ошибку."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            object = func(self, *args, **kwargs)
            if not isinstance(object, ErrorWithData):
                try:
                    while True:
                        item = next(object)
                        if self._verbose == True:
                            self.debug(f"Создан экземпляр класса {item.__class__.__name__}: {item.name}.")
                        yield item
                except StopIteration:
                    pass
            else:
                if isinstance(object.err, ValueError):
                    self.error(f"Переданные данные не соответствуют ожидаемой схеме модели {object.name}."
                               f"Данные, полученные из БД: {object.raw_data}."
                               f"Данные, загружаемые в модель: {object.params}.")
                elif isinstance(object.err, TypeError):
                    self.error(f"Данные, загружаемые в модель должны быть словарем. "
                               f"Полученный тип данных: {type(object.params)}.")
                elif isinstance(object.err, ValidationError):
                    self.error(f"Входные данные содержат неверные значения для полей модели {object.name}."
                               f"Данные, полученные из БД: {object.raw_data}."
                               f"Данные, загружаемые в модель: {object.params}.")
                elif isinstance(object.err, AttributeError):
                    self.error(f"Входные данные содержат неверные значения для полей модели {object.name}."
                               f"Данные, полученные из БД: {object.raw_data}."
                               f"Данные, загружаемые в модель: {object.params}.")
                else:
                    self.error(f"Ошибка создания экземпляра класса {object.name} с параметрами {object.params}."
                               f"Данные, полученные из БД: {object.raw_data}.")
        return wrapper
    return decorator


def debugging_message_for_init_method():
    """ Выводит в лог сообщение о созданном классе и зависимостях в нем"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.debug("Создан {0} со следующими зависимостями: {1}".format(
                self.__class__.__name__,  '; '.join([f'{k}: {v}' for k, v in kwargs.items()])))
            return result
        return wrapper
    return decorator


def output_debug_message_for_function_with_parameters(message: str):
    """ Выводит в лог сообщение message"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.debug(message) if message.find("{") == -1 else self.debug(
                message.format('; '.join([f'{k}= {v}' for k, v in kwargs.items()])))
            return result
        return wrapper
    return decorator
