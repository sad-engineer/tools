#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from tools.app.models.tools import Base


class GeometryDrillingCutter(Base):
    """SQLAlchemy модель сверла с геометрическими параметрами.

    Представляет таблицу сверл в базе данных. Каждое сверло связано с инструментом
    через поле tool_id, которое является внешним ключом на таблицу tools.
    Связь: один-к-одному (один инструмент = одно сверло).

    Attributes:
        id (int): Первичный ключ (автоинкрементный).
        tool_id (int): Внешний ключ на таблицу tools.id.
        D (float): Диаметр сверла в мм.
        L (float): Общая длина в мм.
        l_ (float): Длина рабочей части в мм.
        d_1_ (float): Диаметр d1 в мм.
        d_2_ (float): Диаметр d2 в мм.
        z (int): Количество зубьев.
        created_at (datetime): Дата и время создания записи.
        updated_at (datetime): Дата и время последнего обновления записи.

    Relationships:
        tool (Tool): Связь с основным инструментом (один-к-одному).
    """

    __tablename__ = "geometry_drilling_cutter"

    # Первичный ключ (автоинкрементный)
    id = Column(Integer, primary_key=True, index=True)

    # Внешний ключ на таблицу tools
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False, unique=True, index=True)

    # Основные геометрические параметры
    a_ = Column(Float, nullable=True)  # a_ - Параметр a
    D = Column(Float, nullable=True)  # D - Диаметр сверла в мм
    d_1_ = Column(Float, nullable=True)  # d_1_ - Диаметр d1 в мм
    d_2_ = Column(Float, nullable=True)  # d_2_ - Диаметр d2 в мм
    l_ = Column(Float, nullable=True)  # l_ - Длина рабочей части в мм
    L = Column(Float, nullable=True)  # L - Общая длина в мм
    f_ = Column(Float, nullable=True)  # f_ - Параметр f
    z = Column(Integer, nullable=True)  # z - Количество зубьев

    # Конусы и исполнения
    morse_taper = Column(String(50), nullable=True)  # Конус_Морзе
    execution = Column(String(100), nullable=True)  # Исполнение
    fi_ = Column(Float, nullable=True)  # fi_ - Угол fi

    # Группа и типы
    group = Column(String(100), nullable=True)  # Группа

    # Дополнительные размеры
    D_1 = Column(Float, nullable=True)  # D_1 - Диаметр D1
    P = Column(Float, nullable=True)  # P - Параметр P
    d_ = Column(Float, nullable=True)  # d_ - Диаметр d

    # Направление и параметры
    direction = Column(String(100), nullable=True)  # Направление
    B = Column(Float, nullable=True)  # B - Параметр B
    K = Column(Float, nullable=True)  # K - Параметр K

    # Точность и дополнительные параметры
    accuracy = Column(String(100), nullable=True)  # Точность
    D_2 = Column(Float, nullable=True)  # D_2 - Диаметр D2
    l_1_ = Column(Float, nullable=True)  # l_1_ - Длина l1
    series = Column(String(100), nullable=True)  # Серия
    omega_ = Column(Float, nullable=True)  # omega_ - Угол omega
    r_ = Column(Float, nullable=True)  # r_ - Радиус r

    # Номинальные размеры
    D_nominal = Column(Float, nullable=True)  # D_ном. - Номинальный диаметр D
    D_1_additional = Column(Float, nullable=True)  # D_1_доп. - Дополнительный диаметр D1
    D_2_additional = Column(Float, nullable=True)  # D_2_доп. - Дополнительный диаметр D2

    # Длины
    L_1 = Column(Float, nullable=True)  # L_1 - Длина L1
    L_2 = Column(Float, nullable=True)  # L_2 - Длина L2
    L_3 = Column(Float, nullable=True)  # L_3 - Длина L3
    L_3_additional = Column(Float, nullable=True)  # L_3_доп. - Дополнительная длина L3

    # Разряд и тип хвостовика
    rank = Column(String(100), nullable=True)  # Разряд
    shank_type = Column(String(100), nullable=True)  # Тип_хвостовика

    # Отклонения
    l_deviation = Column(Float, nullable=True)  # l_откл._ - Отклонение l
    L_deviation = Column(Float, nullable=True)  # L_откл. - Отклонение L
    r_deviation = Column(Float, nullable=True)  # r_откл._ - Отклонение r
    l_0_ = Column(Float, nullable=True)  # l_0_ - Длина l0
    k_ = Column(Float, nullable=True)  # k_ - Параметр k
    K_deviation = Column(Float, nullable=True)  # K_откл. - Отклонение K
    a_deviation = Column(Float, nullable=True)  # a_откл._ - Отклонение a

    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Связи (один-к-одному)
    tool = relationship("Tool", back_populates="geometry_drilling_cutter", uselist=False)
