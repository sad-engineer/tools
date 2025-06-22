#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from tools.app.models.tools import Base


class GeometryTurningCutters(Base):
    """SQLAlchemy модель токарного резца с геометрическими параметрами.
    
    Представляет таблицу токарных резцов в базе данных. Каждый резец связан с инструментом
    через поле tool_id, которое является внешним ключом на таблицу tools.
    Связь: один-к-одному (один инструмент = один резец).
    
    Attributes:
        id (int): Первичный ключ (автоинкрементный).
        tool_id (int): Внешний ключ на таблицу tools.id.
        a_ (float): Параметр a в мм.
        D (float): Диаметр резца в мм.
        l_ (float): Длина рабочей части в мм.
        L (float): Общая длина в мм.
        fi_ (float): Угол fi в градусах.
        created_at (datetime): Дата и время создания записи.
        updated_at (datetime): Дата и время последнего обновления записи.
        
    Relationships:
        tool (Tool): Связь с основным инструментом (один-к-одному).
    """

    __tablename__ = "geometry_turning_cutters"

    # Первичный ключ (автоинкрементный)
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Внешний ключ на таблицу tools
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False, unique=True, index=True)
    
    # Основные геометрические параметры
    a_ = Column(Float, nullable=True)  # a_ - Параметр a в мм
    D = Column(Float, nullable=True)  # D - Диаметр резца в мм
    l_ = Column(Float, nullable=True)  # l_ - Длина рабочей части в мм
    L = Column(Float, nullable=True)  # L - Общая длина в мм
    
    # Исполнение и углы
    execution = Column(String(100), nullable=True)  # Исполнение
    fi_ = Column(Float, nullable=True)  # fi_ - Угол fi в градусах
    
    # Материал и группа
    mat_ = Column(String(100), nullable=True)  # mat_ - Материал
    group = Column(String(100), nullable=True)  # Группа
    
    # Дополнительные размеры
    D_1 = Column(Float, nullable=True)  # D_1 - Диаметр D1
    d_ = Column(Float, nullable=True)  # d_ - Диаметр d
    
    # Направление и параметры
    direction = Column(String(100), nullable=True)  # Направление
    B = Column(Float, nullable=True)  # B - Параметр B
    h_ = Column(Float, nullable=True)  # h_ - Высота h
    l_1_ = Column(Float, nullable=True)  # l_1_ - Длина l1
    m_ = Column(Float, nullable=True)  # m_ - Параметр m
    l_2_ = Column(Float, nullable=True)  # l_2_ - Длина l2
    r_ = Column(Float, nullable=True)  # r_ - Радиус r
    H = Column(Float, nullable=True)  # H - Высота H
    
    # Углы резца
    fi_1_ = Column(Float, nullable=True)  # fi_1_ - Угол fi1
    gamma_ = Column(Float, nullable=True)  # gamma_ - Угол gamma
    lambda_ = Column(Float, nullable=True)  # lambda_ - Угол lambda
    
    # Дополнительные параметры
    n_ = Column(Float, nullable=True)  # n_ - Параметр n
    bl_ = Column(Float, nullable=True)  # bl_ - Параметр bl
    
    # Тип резца и группа
    cutter_type = Column(String(100), nullable=True)  # Тип_резца
    h_1_ = Column(Float, nullable=True)  # h_1_ - Высота h1
    cutter_group = Column(String(100), nullable=True)  # Группа_резца
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Связи (один-к-одному)
    tool = relationship("Tool", back_populates="geometry_turning_cutters", uselist=False)

