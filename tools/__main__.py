#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import logging.config

from service import timeit, timeit_property

from tools.obj.containers import ToolContainer
from tools.logger_settings import config

logging.config.dictConfig(config)


def main():
    container = ToolContainer()

    catalog = container.catalog()
    print(catalog.classes)

    lister = container.lister()
    create = lister.by_marking
    tools = timeit("Время запроса инструмента по обозначению : {}")(create)(marking="2210-0061")
    print(list(tools))

    # timeit_property("Время запроса всех инструментов: {}")(lister)("all")

    creator = container.creator()
    tools = creator.default()
    print(tools)

    tools = creator.default(group="Резец")
    print(tools)




if __name__ == '__main__':
    main()
