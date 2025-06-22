#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Tool(Base):
    """SQLAlchemy модель инструмента.

    Представляет таблицу инструментов в базе данных. Каждый инструмент имеет
    уникальное обозначение и может принадлежать к определенной группе.

    Attributes:
        id (int): Уникальный идентификатор инструмента (первичный ключ).
        marking (str): Обозначение инструмента (например, "2100-0001").
        group (str): Группа инструмента (например, "Резец", "Сверло").
        standard (str): Стандарт или нормативный документ (например, "ГОСТ 18878-73").
        created_at (datetime): Дата и время создания записи.
        updated_at (datetime): Дата и время последнего обновления записи.

    Relationships:
        geometry_countersinking_cutter (GeometryCountersinkingCutter): Геометрия зенкера, связанная с инструментом.
        geometry_deployment_cutter (GeometryDeploymentCutter): Геометрия развертки, связанная с инструментом.
        geometry_drilling_cutter (GeometryDrillingCutter): Геометрия сверла, связанная с инструментом.
        geometry_milling_cutters (GeometryMillingCutters): Геометрия фрезы, связанная с инструментом.
    """

    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор инструмента
    marking = Column(String)  # Обозначение инструмента (например, "2100-0001")
    group = Column(String)  # Группа станка (например, "Резец")
    standard = Column(String)  # Группа станка (например, "ГОСТ 18878-73")

    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Связи
    geometry_countersinking_cutter = relationship("GeometryCountersinkingCutter", back_populates="tool", uselist=False)
    geometry_deployment_cutter = relationship("GeometryDeploymentCutter", back_populates="tool", uselist=False)
    geometry_drilling_cutter = relationship("GeometryDrillingCutter", back_populates="tool", uselist=False)
    geometry_milling_cutters = relationship("GeometryMillingCutters", back_populates="tool", uselist=False)
