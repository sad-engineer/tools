#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import sqlite3
from dependency_injector import containers, providers

from tools.obj import cutters, finders, creators, listers, data_preparers
from tools.obj.constants import DEFAULT_SETTINGS_FOR_TOOL as DS
from tools.obj.constants import PATH_DB_FOR_TOOLS as DB_PATH
from tools.obj.constants import REQUESTER_TYPE as DB_type
from tools.obj.
from service import Requester

TOOLS_CLASSES_BY_TYPE = {"Инструмент": "Tool",
                         "Резец": "TurningCutter",
                         "Фреза": "MillingCutter",
                         "Сверло": "DrillingCutter",
                         "Зенкер": "CountersinkingCutter",
                         "Развертка": "DeploymentCutter",
                         "Протяжка": "BroachingCutter",
                         }


@containers.copy(Requester)
class RequesterContainer(Requester):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'}
    )
    Requester.config.from_dict(default_settings())

    requester_tools = providers.Factory(
        Requester.requester,
        tablename="tools",
        )




class Container(containers.DeclarativeContainer):
    default_settings = providers.Object({
        'tools': {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'pandas_table'},
    })
    config = providers.Configuration()
    config.from_dict(default_settings())

    requester_container = providers.Container(
        RequesterContainer,
        config=config.tools,
    )

    # В record_requester положил созданный класс запросов, т.к. Finder использует методы record_requester а не создает класс запросов
    finder = providers.Factory(
        finders.Finder,
        record_requester=requester_container.requester_tools,
    )

    catalog = providers.Factory(
        Cataloger,
        module_name="tools.obj.cutters",
        dict_types=TOOLS_CLASSES_BY_TYPE
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

    broaching_cutter = providers.Factory(
        cutters.BroachingCutter,
        marking="специальная",
        standard="",
        angle_of_inclination=DS[cutters.BroachingCutter.CUTTER_NAME]["angle_of_inclination"],
        pitch_of_teeth=DS[cutters.BroachingCutter.CUTTER_NAME]["pitch_of_teeth"],
        number_teeth_section=DS[cutters.BroachingCutter.CUTTER_NAME]["number_teeth_section"],
        difference=DS[cutters.BroachingCutter.CUTTER_NAME]["difference"],
        length_of_working_part=DS[cutters.BroachingCutter.CUTTER_NAME]["length_of_working_part"],
    )

