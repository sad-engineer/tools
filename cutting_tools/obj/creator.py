#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import re
from ast import literal_eval

from cutting_tools.obj.finder import Finder
from cutting_tools.obj.data_preparer import DataPreparer
from cutting_tools.obj.cataloger import Cataloger


class CreatorFromLogLine:
    """ Создает объект из лога """
    def __init__(self, finder: Finder, catalog: Cataloger, preparer: DataPreparer):
        self._finder = finder
        self._catalog = catalog
        self._preparer = preparer

        self._class_name: str = ""
        self._dict_params_from_log: dict = {}
        self._dict_params_from_bd: dict = {}
        self._prepare_dict_params: dict = {}

    def _read_line(self, text_line: str) -> None:
        objects = re.split("[\(\)]", text_line)
        self._class_name = objects[0]
        self._dict_params_from_log = literal_eval(objects[1])

    def _find(self):
        params = self._dict_params_from_log
        dict_params_from_bd = self._finder.find_by_marking_and_stand(params["marking"], params["standard"])
        self._dict_params_from_bd = dict_params_from_bd.loc[0].to_dict()
        self._preparer._raw_data = self._dict_params_from_bd
        self._prepare_dict_params = self._preparer.get_params

    def create(self, log_line: str):
        if not isinstance(log_line, type(None)):
            if isinstance(log_line, str):
                self._read_line(log_line)
                self._find()
                return self._catalog.get_class_by_name(self._class_name)(**self._prepare_dict_params)
