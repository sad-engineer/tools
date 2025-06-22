#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from tools.app.models.tools import Base


class GeometryDeploymentCutter(Base):
    """SQLAlchemy модель развертки с геометрическими параметрами.

    Представляет таблицу разверток в базе данных. Каждая развертка связана с инструментом
    через поле tool_id, которое является внешним ключом на таблицу tools.
    Связь: один-к-одному (один инструмент = одна развертка).

    Attributes:
        id (int): Первичный ключ (автоинкрементный).
        tool_id (int): Внешний ключ на таблицу tools.id.
        D (float): Диаметр развертки в мм.
        d_1_ (float): Диаметр d1 в мм.
        d_2_ (float): Диаметр d2 в мм.
        l_ (float): Длина рабочей части в мм.
        L (float): Общая длина в мм.
        z (int): Количество зубьев.
        fi_ (float): Угол fi в градусах.
        created_at (datetime): Дата и время создания записи.
        updated_at (datetime): Дата и время последнего обновления записи.

    Relationships:
        tool (Tool): Связь с основным инструментом (один-к-одному).
    """

    __tablename__ = "geometry_deployment_cutter"

    # Первичный ключ (автоинкрементный)
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Внешний ключ на таблицу tools
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False, unique=True, index=True)

    # Основные геометрические параметры
    D = Column(Float, nullable=True)  # D - Диаметр развертки в мм
    d_1_ = Column(Float, nullable=True)  # d_1_ - Диаметр d1 в мм
    d_2_ = Column(Float, nullable=True)  # d_2_ - Диаметр d2 в мм
    l_ = Column(Float, nullable=True)  # l_ - Длина рабочей части в мм
    L = Column(Float, nullable=True)  # L - Общая длина в мм
    z = Column(Integer, nullable=True)  # z - Количество зубьев

    # Конусы и исполнения
    morse_taper = Column(String(50), nullable=True)  # Конус_Морзе
    execution = Column(String(100), nullable=True)  # Исполнение
    fi_ = Column(Float, nullable=True)  # fi_ - Угол fi в градусах

    # Материал и группа
    mat_ = Column(String(100), nullable=True)  # mat_ - Материал
    group = Column(String(100), nullable=True)  # Группа

    # Дополнительные размеры
    D_1 = Column(Float, nullable=True)  # D_1 - Диаметр D1
    d_ = Column(Float, nullable=True)  # d_ - Диаметр d
    h_ = Column(Float, nullable=True)  # h_ - Высота h
    l_1_ = Column(Float, nullable=True)  # l_1_ - Длина l1
    l_2_ = Column(Float, nullable=True)  # l_2_ - Длина l2
    r_ = Column(Float, nullable=True)  # r_ - Радиус r
    l_0_ = Column(Float, nullable=True)  # l_0_ - Длина l0

    # Тип развертки и углы
    reamer_type = Column(String(100), nullable=True)  # Тип_развертки
    fi_1_ = Column(Float, nullable=True)  # fi_1_ - Угол fi1
    gamma_ = Column(Float, nullable=True)  # gamma_ - Угол gamma
    lambda_ = Column(Float, nullable=True)  # lambda_ - Угол lambda

    # Конусность и дополнительные параметры
    reamer_taper = Column(Float, nullable=True)  # Конусность_развертки
    d_2_additional = Column(Float, nullable=True)  # d_2_доп. - Дополнительный диаметр d2

    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Связи (один-к-одному)
    tool = relationship("Tool", back_populates="geometry_deployment_cutter", uselist=False)
