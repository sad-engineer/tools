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


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    # config.path_db = PATH_DB_FOR_TOOLS

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



if __name__ == "__main__":
    ct = Container()
    ct.config.paths.path_db_for_tools.from_value(PATH_DB_FOR_TOOLS)
    ct.config.default_settings.for_cutting_tool.from_value(DEFAULT_SETTINGS_FOR_CUTTING_TOOL)
    ct.config.tool.groups.from_value(GROUPS_TOOL)

    # requester = ct.requester()
    # print(requester.filename)
    # print(requester.tablename)

    # finder = ct.finder()
    # table = finder.find_all
    # print(table)

    # cataloger = ct.cataloger()
    # print(cataloger.classes)

    creator = ct.creator_from_log_line
    with open(os.getcwd().replace('obj', 'logs\\log.txt'), mode='r', encoding="utf8") as f:
        context = f.readlines()
    for line in context:
        cutter = creator().create(log_line=line)
        print(cutter)
        print(cutter.name)

