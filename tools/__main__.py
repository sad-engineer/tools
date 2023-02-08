#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import time

from tools.obj.containers import ToolContainer


def main():
    container = ToolContainer()
    container.config.from_yaml('config.yml')

    tool_database_client = container.tool_database_client()
    print(tool_database_client)

    requester = container.requester()
    print(requester)

    lister = container.lister()
    start_time_1 = time.time()
    cutters = lister.by_marking(marking="2210-0061")
    end_time_1 = time.time()
    time_1 = end_time_1 - start_time_1
    print("Время запроса инструмента по обозначению ", time_1)

    start_time_2 = time.time()
    cutters = lister.all
    end_time_2 = time.time()
    time_2 = end_time_2 - start_time_2
    print("Время запроса всех инструментов", time_2)

    print(f"Разница составила {time_2/time_1} раз(а).", )

    cutter = container.milling_cutter()
    print(cutter.name)
    print(cutter.CUTTER_NAME)

    cutter = container.turning_cutter()
    print(cutter.name)
    print(cutter.CUTTER_NAME)

    cutter = container.drilling_cutter()
    print(cutter.name)
    print(cutter.CUTTER_NAME)

    cutter = container.countersinking_cutter()
    print(cutter.name)
    print(cutter.CUTTER_NAME)

    cutter = container.deployment_cutter()
    print(cutter.name)
    print(cutter.CUTTER_NAME)


if __name__ == '__main__':
    main()

