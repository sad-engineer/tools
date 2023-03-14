#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import logging.config

from service import timeit, timeit_property

from tools.obj.containers import Container
from tools.logger_settings import config

logging.config.dictConfig(config)


def main():
    container = Container()

    catalod = container.catalog()
    print(catalod.classes)

    lister = container.lister()
    create = lister.by_marking
    tools = timeit("Время запроса инструмента по обозначению : {}")(create)(marking="2210-0061")
    print(list(tools))

    timeit_property("Время запроса всех инструментов: {}")(lister)("all")


if __name__ == '__main__':
    main()


