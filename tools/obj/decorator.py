#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
def output_debug_message_for_init_method():
    """ Выводит в лог сообщение о созданном классе и зависимостях в нем"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.debug("Создан {0} со следующими зависимостями: {1}".format(
                self.__class__.__name__,  '; '.join([f'{k}: {v}' for k, v in kwargs.items()])))
            return result
        return wrapper
    return decorator
