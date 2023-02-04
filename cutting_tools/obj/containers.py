#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import os

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from cutting_tools.obj.request_record_from_sqlyte import RequestRecordFromSQLyte
from cutting_tools.obj.finder import Finder
from cutting_tools.obj.creator import CreatorFromLogLine
from cutting_tools.obj.data_preparer import DataPreparer
from cutting_tools.obj.cataloger import Cataloger
from cutting_tools.obj.constants import PATH_DB_FOR_TOOLS, DEFAULT_SETTINGS_FOR_CUTTING_TOOL, GROUPS_TOOL
from cutting_tools.obj.turning_cutter import TurningCutter


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    config.paths.path_db_for_tools.from_value(PATH_DB_FOR_TOOLS)
    config.default_settings.for_cutting_tool.from_value(DEFAULT_SETTINGS_FOR_CUTTING_TOOL)
    config.tool.groups.from_value(GROUPS_TOOL)

    requester = providers.Singleton(
        RequestRecordFromSQLyte,
        filename=config.paths.path_db_for_tools,
        tablename="cutting_tools"
    )

    finder = providers.Factory(
        Finder,
        record_requester=requester,
    )

    data_preparer = providers.Factory(
        DataPreparer,
        default_settings=config.default_settings.for_cutting_tool,
        groups_tool=config.tool.groups,
    )

    cataloger = providers.Singleton(
        Cataloger,
        module_names=["logger", "cutting_tools"],
    )

    creator_from_log_line = providers.Factory(
        CreatorFromLogLine,
        finder=finder,
        catalog=cataloger,
        preparer=data_preparer,
    )

    turning_cutter = providers.Singleton(
        TurningCutter,
        marking=config.default_settings.for_cutting_tool["Резец"]["marking"].as_(str),
        standard=config.default_settings.for_cutting_tool["Резец"]["Стандарт"].as_(str),
        mat_of_cutting_part=config.default_settings.for_cutting_tool["Резец"]["mat_of_cutting_part"].as_(str),
        quantity=config.default_settings.for_cutting_tool["Резец"]["quantity"].as_int(),
        length_mm=100,
        width_mm=25,
        height_mm=25,
        main_angle_grad=90,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        radius_of_cutting_vertex=1,
        turret=0,
        load=0,
        is_complex_profile=False,
    )


if __name__ == "__main__":
    ct = Container()


    # requester = ct.requester()
    # print(requester.filename)
    # print(requester.tablename)

    # finder = ct.finder()
    # table = finder.find_all
    # print(table)

    # cataloger = ct.cataloger()
    # print(cataloger.classes)

    # creator = ct.creator_from_log_line
    # with open(os.getcwd().replace('obj', 'logs\\log.txt'), mode='r', encoding="utf8") as f:
    #     context = f.readlines()
    # for line in context:
    #     cutter = creator().create(log_line=line)
    #     print(cutter)
    #     print(cutter.name)

    cutter = ct.turning_cutter()
    print(cutter.width_mm)

    ct.turning_cutter.reset()
    cutter = ct.turning_cutter(width_mm=16)
    print(cutter.width_mm)

    ct.turning_cutter.reset()
    cutter = ct.turning_cutter()
    print(cutter.width_mm)

    cutter.width_mm = 40
    print(cutter.width_mm)
    print(cutter.__class__.__name__)
