#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import os
import sqlite3

from dependency_injector import containers, providers
# from dependency_injector.wiring import Provide, inject

from cutting_tools.obj.constants import PATH_DB_FOR_TOOLS, DEFAULT_SETTINGS_FOR_TOOL, GROUPS_TOOL, DECODING

from cutting_tools.obj import finder
from cutting_tools.obj import creator
from cutting_tools.obj import data_preparer
from cutting_tools.obj import cataloger
from cutting_tools.obj import turning_cutter, milling_cutter, drilling_cutter, countersinking_cutter, deployment_cutter

from logger import Container as LoggerContainer


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    config.paths.path_db_for_tools.from_value(PATH_DB_FOR_TOOLS)
    config.default_settings.for_tool.from_value(DEFAULT_SETTINGS_FOR_TOOL)
    config.tool.groups.from_value(GROUPS_TOOL)

    # Gateways
    tools_database = providers.Singleton(
        sqlite3.connect,
        config.paths.path_db_for_tools,
    )
    
    # Services
    request_record_from_sqlyte = providers.Factory(
        LoggerContainer.request_record_from_sqlyte,
        database_client=tools_database,
        tablename="tools"
    )

    standard_result_terminal_printer = providers.Singleton(
        LoggerContainer.standard_result_terminal_printer,
        decoding=DECODING,
    )

    finder = providers.Factory(
        finder.Finder,
        record_requester=request_record_from_sqlyte,
    )

    data_preparer = providers.Factory(
        data_preparer.DataPreparer,
        default_settings=config.default_settings.for_tool,
        groups_tool=config.tool.groups,
    )

    cataloger = providers.Singleton(
        cataloger.Cataloger,
        module_names=["logger", "!cutting_tools"],
    )

    creator_from_log_line = providers.Factory(
        creator.CreatorFromLogLine,
        finder=finder,
        catalog=cataloger,
        preparer=data_preparer,
    )

    turning_cutter = providers.Singleton(
        turning_cutter.TurningCutter,
        marking=config.default_settings.for_tool["Резец"]["marking"].as_(str),
        standard=config.default_settings.for_tool["Резец"]["Стандарт"].as_(str),
        mat_of_cutting_part=config.default_settings.for_tool["Резец"]["mat_of_cutting_part"].as_(str),
        quantity=config.default_settings.for_tool["Резец"]["quantity"].as_int(),
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

    milling_cutter = providers.Singleton(
        milling_cutter.MillingCutter,
        marking=config.default_settings.for_tool["Фреза"]["marking"].as_(str),
        standard=config.default_settings.for_tool["Фреза"]["Стандарт"].as_(str),
        mat_of_cutting_part=config.default_settings.for_tool["Фреза"]["mat_of_cutting_part"].as_(str),
        quantity=config.default_settings.for_tool["Фреза"]["quantity"].as_int(),
        tolerance=config.default_settings.for_tool["Фреза"]["tolerance"].as_(str),
        dia_mm=40,
        length_mm=100,
        main_angle_grad=90,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        type_cutter=1,
        type_of_cutting_part=1,
        num_of_cutting_blades=10,
        radius_of_cutting_vertex=1,
        large_tooth=0,
        accuracy_class=None,
        number=None,
        module=None,
    )

    drilling_cutter = providers.Singleton(
        drilling_cutter.DrillingCutter,
        marking=config.default_settings.for_tool["Сверло"]["marking"].as_(str),
        standard=config.default_settings.for_tool["Сверло"]["Стандарт"].as_(str),
        mat_of_cutting_part=config.default_settings.for_tool["Сверло"]["mat_of_cutting_part"].as_(str),
        quantity=config.default_settings.for_tool["Сверло"]["quantity"].as_int(),
        tolerance=config.default_settings.for_tool["Сверло"]["tolerance"].as_(str),
        dia_mm=2.4,
        length_mm=95,
        main_angle_grad=59,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        num_of_cutting_blades=2,
        radius_of_cutting_vertex=1,
    )

    countersinking_cutter = providers.Singleton(
        countersinking_cutter.CountersinkingCutter,
        marking=config.default_settings.for_tool["Зенкер"]["marking"].as_(str),
        standard=config.default_settings.for_tool["Зенкер"]["Стандарт"].as_(str),
        mat_of_cutting_part=config.default_settings.for_tool["Зенкер"]["mat_of_cutting_part"].as_(str),
        quantity=config.default_settings.for_tool["Зенкер"]["quantity"].as_int(),
        tolerance=config.default_settings.for_tool["Зенкер"]["tolerance"].as_(str),
        dia_mm=2.4,
        length_mm=95,
        main_angle_grad=90,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        num_of_cutting_blades=2,
        radius_of_cutting_vertex=1,
    )
    deployment_cutter = providers.Singleton(
        deployment_cutter.DeploymentCutter,
        marking=config.default_settings.for_tool["Зенкер"]["marking"].as_(str),
        standard=config.default_settings.for_tool["Зенкер"]["Стандарт"].as_(str),
        mat_of_cutting_part=config.default_settings.for_tool["Зенкер"]["mat_of_cutting_part"].as_(str),
        quantity=config.default_settings.for_tool["Зенкер"]["quantity"].as_int(),
        tolerance=config.default_settings.for_tool["Зенкер"]["tolerance"].as_(str),
        dia_mm=2.4,
        length_mm=95,
        main_angle_grad=90,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        num_of_cutting_blades=2,
        radius_of_cutting_vertex=1,
    )


if __name__ == "__main__":
    from logger import Logger
    from logger import StandardResultTerminalPrinter, StandardObjectTerminalPrinter
    from logger import StandardResultFilePrinter, StandardObjectFilePrinter, StandardObjectFileSaver


    ct = Container()

    # requester = ct.request_record_from_sqlyte()
    # print(requester.tablename)
    #
    # finder = ct.finder()
    # table = finder.find_all
    # print(table)

    cataloger = ct.cataloger()
    print(cataloger.classes)

    creator = ct.creator_from_log_line()
    print(creator._catalog.classes)


    # creator = ct.creator_from_log_line
    # with open(os.getcwd().replace('obj', 'logs\\log.txt'), mode='r', encoding="utf8") as f:
    #     context = f.readlines()
    # for line in context:
    #     cutter = creator().create(log_line=line)
    #     print(cutter)
    #     print(cutter.name)
    #
    # cutter = ct.drilling_cutter()
    # print(cutter.length_mm)
    #
    # ct.drilling_cutter.reset()
    # cutter = ct.drilling_cutter(length_mm=16)
    # print(cutter.length_mm)
    #
    # ct.drilling_cutter.reset()
    # cutter = ct.drilling_cutter()
    # print(cutter.length_mm)
    #
    # cutter.length_mm = 40
    # print(cutter.length_mm)
    # print(cutter.__class__.__name__)
