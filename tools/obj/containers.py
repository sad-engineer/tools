#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import sqlite3
from dependency_injector import containers, providers

from . import cutters, finders, creators, listers, requesters, catalogers, data_preparers
from .constants import DEFAULT_SETTINGS_FOR_TOOL as DS
from .constants import PATH_DB_FOR_TOOLS, REQUESTER_TYPE


class ToolContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    config.tool_database.path.from_value(PATH_DB_FOR_TOOLS)
    config.requester.type.from_value(REQUESTER_TYPE)

    # Gateways
    tool_database_client = providers.Singleton(
        sqlite3.connect,
        config.tool_database.path,
    )

    # Services
    csv_requester = providers.Singleton()

    sqlyte_requester = providers.Singleton(
        requesters.RequestRecordFromSQLyte,
        tablename="tools",
        database_client=tool_database_client
    )
    # Выбор класса запросов
    requester = providers.Selector(
        config.requester.type,
        csv=csv_requester,
        sqlite=sqlyte_requester,
    )

    # В record_requester положил созданный класс запросов, т.к. Finder использует методы record_requester а не создает класс запросов
    finder = providers.Factory(
        finders.Finder,
        record_requester=requester,
    )

    catalog = providers.Factory(
        catalogers.Cataloger,
    )

    data_preparer = providers.Factory(
        data_preparers.DataPreparer,
    )

    creator = providers.Factory(
        creators.ToolCreator,
        finder=finder,
        catalog=catalog,
        preparer_factory=data_preparer.provider,
    )

    lister = providers.Factory(
        listers.ToolLister,
        tool_creator=creator.provider,
    )

    milling_cutter = providers.Factory(
        cutters.MillingCutter,
        marking=DS[cutters.MillingCutter.CUTTER_NAME]["marking"],
        standard=DS[cutters.MillingCutter.CUTTER_NAME]["Стандарт"],
        dia_mm=50,
        length_mm=100,
        mat_of_cutting_part=DS[cutters.MillingCutter.CUTTER_NAME]["mat_of_cutting_part"],
        main_angle_grad=0,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        tolerance=DS[cutters.MillingCutter.CUTTER_NAME]["tolerance"],
        type_cutter=1,
        type_of_cutting_part=1,
        num_of_cutting_blades=8,
        radius_of_cutting_vertex=1,
        large_tooth=0,
        quantity=1,
        accuracy_class=None,
        number=None,
        module=None,
    )

    turning_cutter = providers.Factory(
        cutters.TurningCutter,
        marking=DS[cutters.TurningCutter.CUTTER_NAME]["marking"],
        standard=DS[cutters.TurningCutter.CUTTER_NAME]["Стандарт"],
        length_mm=100,
        width_mm=25,
        height_mm=16,
        mat_of_cutting_part=DS[cutters.TurningCutter.CUTTER_NAME]["mat_of_cutting_part"],
        main_angle_grad=45,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        radius_of_cutting_vertex=1,
        quantity=1,
        turret=0,
        load=0,
        is_complex_profile=False,
    )

    drilling_cutter = providers.Factory(
        cutters.DrillingCutter,
        marking=DS[cutters.DrillingCutter.CUTTER_NAME]["marking"],
        standard=DS[cutters.DrillingCutter.CUTTER_NAME]["Стандарт"],
        dia_mm=50,
        length_mm=100,
        mat_of_cutting_part=DS[cutters.DrillingCutter.CUTTER_NAME]["mat_of_cutting_part"],
        main_angle_grad=0,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        num_of_cutting_blades=8,
        radius_of_cutting_vertex=1,
        quantity=1,
        tolerance=DS[cutters.DrillingCutter.CUTTER_NAME]["tolerance"],
    )

    countersinking_cutter = providers.Factory(
        cutters.CountersinkingCutter,
        marking=DS[cutters.CountersinkingCutter.CUTTER_NAME]["marking"],
        standard=DS[cutters.CountersinkingCutter.CUTTER_NAME]["Стандарт"],
        dia_mm=50,
        length_mm=100,
        mat_of_cutting_part=DS[cutters.CountersinkingCutter.CUTTER_NAME]["mat_of_cutting_part"],
        main_angle_grad=0,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        num_of_cutting_blades=8,
        radius_of_cutting_vertex=1,
        quantity=1,
        tolerance=DS[cutters.CountersinkingCutter.CUTTER_NAME]["tolerance"],
    )

    deployment_cutter = providers.Factory(
        cutters.DeploymentCutter,
        marking=DS[cutters.DeploymentCutter.CUTTER_NAME]["marking"],
        standard=DS[cutters.DeploymentCutter.CUTTER_NAME]["Стандарт"],
        dia_mm=50,
        length_mm=100,
        mat_of_cutting_part=DS[cutters.DeploymentCutter.CUTTER_NAME]["mat_of_cutting_part"],
        main_angle_grad=0,
        front_angle_grad=0,
        inclination_of_main_blade_grad=0,
        num_of_cutting_blades=8,
        radius_of_cutting_vertex=1,
        quantity=1,
        tolerance=DS[cutters.DeploymentCutter.CUTTER_NAME]["tolerance"],
    )
