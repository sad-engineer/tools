#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from tools.obj.creators import ToolCreator
from typing import Callable


class ToolLister:
    def __init__(self, tool_creator: Callable[..., ToolCreator]):
        self._tool_creator = tool_creator

    def by_marking_and_stand(self, marking: str, standard: str) -> list:
        return [tool for tool in self._tool_creator().by_marking_and_stand(marking, standard)]

    def by_marking(self, marking: str) -> list:
        return [tool for tool in self._tool_creator().by_marking(marking)]

    def by_stand(self, standard: str) -> list:
        return [tool for tool in self._tool_creator().by_stand(standard)]

    @property
    def all(self) -> list:
        return [tool for tool in self._tool_creator().all]
