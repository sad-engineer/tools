#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from tools.app.models.tools import Base


class GeometryCountersinkingCutter(Base):
    """SQLAlchemy модель зенкера с геометрическими параметрами.
    
    Представляет таблицу зенкеров в базе данных. Каждый зенкер связан с инструментом
    через поле tool_id, которое является внешним ключом на таблицу tools.
    Связь: один-к-одному (один инструмент = один зенкер).
    
    Attributes:
        id (int): Первичный ключ (автоинкрементный).
        tool_id (int): Внешний ключ на таблицу tools.id.
        D (float): Диаметр зенкера в мм.
        l_ (float): Длина рабочей части в мм.
        L (float): Общая длина в мм.
        z (int): Количество зубьев.
        fi_ (float): Угол fi в градусах.
        created_at (datetime): Дата и время создания записи.
        updated_at (datetime): Дата и время последнего обновления записи.
        
    Relationships:
        tool (Tool): Связь с основным инструментом (один-к-одному).
    """

    __tablename__ = "geometry_countersinking_cutter"

    # Первичный ключ (автоинкрементный)
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Внешний ключ на таблицу tools
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False, unique=True, index=True)
    
    # Основные геометрические параметры
    D = Column(Float, nullable=True)  # D - Диаметр зенкера в мм
    l_ = Column(Float, nullable=True)  # l_ - Длина рабочей части в мм
    L = Column(Float, nullable=True)  # L - Общая длина в мм
    z = Column(Integer, nullable=True)  # z - Количество зубьев
    
    # Конусы и исполнения
    morse_taper = Column(String(50), nullable=True)  # Конус_Морзе
    execution = Column(String(100), nullable=True)  # Исполнение
    fi_ = Column(Float, nullable=True)  # fi_ - Угол fi в градусах
    
    # Группа и типы
    group = Column(String(100), nullable=True)  # Группа

    # Дополнительные размеры
    D_additional = Column(Float, nullable=True)  # D_доп. - Дополнительный диаметр D
    d_ = Column(Float, nullable=True)  # d_ - Диаметр d
    
    # Тип отверстия
    hole_type = Column(String(100), nullable=True)  # Тип_отверстия
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Связи (один-к-одному)
    tool = relationship("Tool", back_populates="geometry_countersinking_cutter", uselist=False)
