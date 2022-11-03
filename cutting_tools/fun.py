#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        fun
# Purpose:     Contains local functions for working with the database
#
# Author:      ANKorenuk
#
# Created:     28.10.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Содержит локальные функции работы с БД
# -------------------------------------------------------------------------------
import sqlite3
import pandas as pd
from cutting_tools.obj.constants import PATH_DB_FOR_TOOLS as PATH_DB
from cutting_tools.obj.exceptions import InvalidValue


def connect(filename):
    """
    Создает и подключает базу данных если ее нет. Если БД есть - подключает ее

    Parameters
    ----------
    filename : str
        Имя файла БД.

    Returns
    -------
    db : TYPE
        Указатель на подключенную БД.
    cursor : TYPE
        Указатель на курсор БД.
    """
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    db.commit()
    return db, cursor


def save_table(name: str = "",
               table=None,
               path_bd: str = PATH_DB):
    """ Сохраняет таблицу DataFrame в БД. Если таблица существует - заменяет ее

    Parameters
    ----------
    name : str, optional 
        Имя таблицы в БД
    table : DataFrame, optional 
        DataFrame для сохранения в БД.
    path_bd : str, optional 
        Путь к базе данных по материаллам

    Returns
    -------
        True - если данные были записаны/перезаписаны
        InvalidValue - если на вход дали некорректное имя таблицы или таблицу, 
            тип оторой отличается от pd.DataFrame
    """
    is_correct_name = isinstance(name, str) and name not in ["", " ", "  "]
    is_correct_table = isinstance(table, pd.DataFrame)
    if is_correct_name and is_correct_table:
        db, cursor = connect(path_bd)
        cursor.execute(f"DROP TABLE IF EXISTS {name}")
        table.to_sql(name=f'{name}', con=db)
        db.commit()
        db.close()
        return True
    else:
        if not is_correct_name:
            raise InvalidValue(f"Переменная 'name' должна содержать название таблицы. Вы передали: {name}.")
        elif not is_correct_table:
            raise InvalidValue("Переменная 'table' должна содержать таблицу типа pd.DataFrame. Проверьте входные "
                               "данные.")
        return False
