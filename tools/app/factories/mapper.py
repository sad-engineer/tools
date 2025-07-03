#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Dict, Optional

from tools.app.factories.base import BaseFactory
from tools.app.interfaces.mapper import IMapper
from tools.app.mappers import CountersinkingMapper
from tools.app.mappers import MillingMapper
from tools.app.mappers import DrillingMapper
from tools.app.mappers import TurningMapper
from tools.app.mappers import ReamerMapper
from tools.app.mappers import BroachingMapper
from tools.app.models.tools import Tool


class MapperFactory(BaseFactory[IMapper]):
    """
    Фабрика для создания и управления мапперами.
    
    Предоставляет доступ к мапперам по типу инструмента и автоматически
    регистрирует все стандартные мапперы.
    """

    def _register_defaults(self) -> None:
        """Регистрирует стандартные мапперы."""
        self.register("Зенкер", CountersinkingMapper())
        self.register("Фреза", MillingMapper())
        self.register("Сверло", DrillingMapper())
        self.register("Резец", TurningMapper())
        self.register("Развертка", ReamerMapper())
        self.register("Протяжка", BroachingMapper())


# Создаем дефолтный экземпляр фабрики
default_mapper_factory = MapperFactory()
