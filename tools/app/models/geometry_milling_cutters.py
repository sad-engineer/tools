#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from tools.app.models.tools import Base


class GeometryMillingCutters(Base):
    """SQLAlchemy модель фрезы с геометрическими параметрами.

    Представляет таблицу фрез в базе данных. Каждая фреза связана с инструментом
    через поле tool_id, которое является внешним ключом на таблицу tools.
    Связь: один-к-одному (один инструмент = одна фреза).

    Attributes:
        id (int): Первичный ключ (автоинкрементный).
        tool_id (int): Внешний ключ на таблицу tools.id.
        D (float): Диаметр фрезы в мм.
        L (float): Общая длина в мм.
        l (float): Длина режущей части в мм.
        d (float): Диаметр хвостовика в мм.
        z (int): Количество зубьев.
        created_at (datetime): Дата и время создания записи.
        updated_at (datetime): Дата и время последнего обновления записи.

    Relationships:
        tool (Tool): Связь с основным инструментом (один-к-одному).
    """

    __tablename__ = "geometry_milling_cutters"

    # Первичный ключ (автоинкрементный)
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Внешний ключ на таблицу tools
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False, unique=True, index=True)

    # Основные геометрические параметры
    D = Column(Float, nullable=True)  # D - Диаметр фрезы в мм
    L = Column(Float, nullable=True)  # L - Общая длина в мм
    l = Column(Float, nullable=True)  # l - Длина режущей части в мм
    d = Column(Float, nullable=True)  # d - Диаметр хвостовика в мм
    z = Column(Integer, nullable=True)  # z - Количество зубьев

    # Дополнительные геометрические параметры
    a_ = Column(Float, nullable=True)  # a_ - Параметр a
    d_1_ = Column(Float, nullable=True)  # d_1_ - Диаметр d1
    d_2_ = Column(Float, nullable=True)  # d_2_ - Диаметр d2
    l_ = Column(Float, nullable=True)  # l_ - Длина l
    L_ = Column(Float, nullable=True)  # L_ - Длина L
    f_ = Column(Float, nullable=True)  # f_ - Параметр f
    q_ = Column(Float, nullable=True)  # q_ - Параметр q

    # Конусы и исполнения
    morse_taper = Column(String(50), nullable=True)  # Конус_Морзе
    execution = Column(String(100), nullable=True)  # Исполнение
    fi_ = Column(Float, nullable=True)  # fi_ - Угол fi
    type_cutter_ = Column(String(100), nullable=True)  # type_cutter_ - Тип фрезы

    # Материалы и типы
    material = Column(String(100), nullable=True)  # mat_ - Материал
    type_of_cutting_part_ = Column(String(100), nullable=True)  # type_of_cutting_part_ - Тип режущей части
    group = Column(String(100), nullable=True)  # Группа

    # Дополнительные размеры
    D_1 = Column(Float, nullable=True)  # D_1 - Диаметр D1
    f_additional_ = Column(Float, nullable=True)  # f_доп._ - Дополнительный параметр f
    D_additional = Column(Float, nullable=True)  # D_доп._ - Дополнительный диаметр D
    P = Column(Float, nullable=True)  # P - Параметр P
    l_nominal_ = Column(Float, nullable=True)  # l_номин._ - Номинальная длина l
    d_ = Column(Float, nullable=True)  # d_ - Диаметр d
    d_additional_ = Column(Float, nullable=True)  # d_доп._ - Дополнительный диаметр d
    d_1_additional_ = Column(Float, nullable=True)  # d_1_доп._ - Дополнительный диаметр d1

    # Направление и параметры
    direction = Column(String(100), nullable=True)  # Направление
    B = Column(Float, nullable=True)  # B - Параметр B
    c_ = Column(Float, nullable=True)  # c_ - Параметр c
    c_additional_ = Column(Float, nullable=True)  # c_доп._ - Дополнительный параметр c
    h_ = Column(Float, nullable=True)  # h_ - Высота h
    R = Column(Float, nullable=True)  # R - Радиус R
    R_additional = Column(Float, nullable=True)  # R_доп._ - Дополнительный радиус R
    m_n0_ = Column(Float, nullable=True)  # m_n0_ - Параметр m_n0
    L_additional = Column(Float, nullable=True)  # L_доп._ - Дополнительная длина L
    K = Column(Float, nullable=True)  # K - Параметр K
    K_additional = Column(Float, nullable=True)  # K_доп._ - Дополнительный параметр K

    # Точность и дополнительные параметры
    accuracy = Column(String(100), nullable=True)  # Точность
    D_2 = Column(Float, nullable=True)  # D_2 - Диаметр D2
    l_1_ = Column(Float, nullable=True)  # l_1_ - Длина l1
    f_deviation_ = Column(Float, nullable=True)  # f_откл._ - Отклонение f
    g_ = Column(Float, nullable=True)  # g_ - Параметр g
    g_deviation_ = Column(Float, nullable=True)  # g_откл._ - Отклонение g
    zxd_xD = Column(String(100), nullable=True)  # zxd_xD - Параметр zxd_xD
    z_0_ = Column(Float, nullable=True)  # z_0_ - Параметр z0
    series = Column(String(100), nullable=True)  # Серия
    groove_accuracy = Column(String(100), nullable=True)  # Точность_паза
    m_0_ = Column(Float, nullable=True)  # m_0_ - Параметр m0
    subgroup = Column(String(100), nullable=True)  # Подгруппа
    h_additional_ = Column(Float, nullable=True)  # h_доп._ - Дополнительная высота h
    m_ = Column(Float, nullable=True)  # m_ - Параметр m

    # Метрические параметры
    metric_shank = Column(String(100), nullable=True)  # Метрический_хвостовик
    b_ = Column(Float, nullable=True)  # b_ - Параметр b
    S = Column(Float, nullable=True)  # S - Параметр S
    t_ = Column(Float, nullable=True)  # t_ - Параметр t
    d_0_ = Column(Float, nullable=True)  # d_0_ - Диаметр d0
    l_additional_ = Column(Float, nullable=True)  # l_доп._ - Дополнительная длина l
    omega_ = Column(Float, nullable=True)  # omega_ - Угол omega
    l_2_ = Column(Float, nullable=True)  # l_2_ - Длина l2
    r_ = Column(Float, nullable=True)  # r_ - Радиус r
    r_additional_ = Column(Float, nullable=True)  # r_доп._ - Дополнительный радиус r
    B_additional = Column(Float, nullable=True)  # B_доп._ - Дополнительный параметр B
    H = Column(Float, nullable=True)  # H - Высота H
    omega_u_ = Column(Float, nullable=True)  # omega_u_ - Угол omega_u
    D_deviation = Column(Float, nullable=True)  # D_откл._ - Отклонение D
    c_general_purpose_ = Column(Float, nullable=True)  # c_общего_назначения_ - Параметр c общего назначения
    c_keyway_ = Column(Float, nullable=True)  # c_для_шпоночных_пазов_ - Параметр c для шпоночных пазов
    metric_taper = Column(String(100), nullable=True)  # Конус_метрический
    alpha_ = Column(Float, nullable=True)  # alpha_ - Угол alpha

    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Связи (один-к-одному)
    tool = relationship("Tool", back_populates="geometry_milling_cutters", uselist=False)
