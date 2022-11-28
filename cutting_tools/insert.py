#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from typing import Optional, Union
from cutting_tools.find import full_table
from cutting_tools.fun import save_table


def ask_path() -> tuple:
    """ Запрашивает место расположение таблицы *.xlsx, содержащей параметры инструмента."""
    root = Tk()
    root.withdraw()
    filenames = askopenfilenames(title="Выберете файл детали", filetypes=[('MS Exel', '*.xlsx')])
    if filenames == "":
        root.destroy()
    return filenames


def insert(paths: Optional[Union[tuple, list, str]] = None) -> None:
    """ Запускает процесс загрузки таблицы для каждого файла в paths."""
    if isinstance(paths, type(None)):
        paths = ask_path()
    if isinstance(paths, (tuple, list)):
        for path in paths:
            insert_in_table(path)
    elif isinstance(paths, str):
        insert_in_table(paths)


def insert_in_table(path: str) -> None:
    """ Загрузка таблицы из эксель файла из листа1."""
    ct = full_table()
    loc_table = get_loc_table(path)
    ct = pd.concat([ct, loc_table], axis=0)
    ct = ct.sort_values(by='Обозначение')
    ct = ct.reset_index(drop=True)
    save_table(name="cutting_tools", table=ct)


def get_loc_table(path: str) -> pd.DataFrame:
    """ Получает DataFrame таблицу из файла эксель-файла."""
    loc_table = pd.read_excel(path, sheet_name='Лист1')
    cols = loc_table.columns.to_list()
    for col in cols:
        if col == 'Тип хвостовика':
            loc_table = loc_table.rename(columns={'Тип хвостовика': 'Тип_хвостовика', })
        if col == 'Тип инструмента':
            loc_table = loc_table.rename(columns={'Тип инструмента': 'Тип_инструмента', })
        if col == 'Конус Морзе':
            loc_table = loc_table.rename(columns={'Конус Морзе': 'Конус_Морзе', })
        if col == 'Конус метрический':
            loc_table = loc_table.rename(columns={'Конус метрический': 'Конус_метрический', })
        if col == 'Метрический хвостовик':
            loc_table = loc_table.rename(columns={'Метрический хвостовик': 'Метрический_хвостовик', })

        if col in ['a_откл.', 'd_1_доп.', 'd_2', 'd_2_доп.', 'l_0', 'l_1', 'l_2', 'l_3', 'l_3_доп.',
                   'r_откл.', 'r.', 'm', 'l', 'h', 'f', 'd', 'd_1', 'c', 'a', 'L_доп._', 'omega',
                   'Обозначения', ' ', 'D_', 'D_доп._', 'L_', 'a', 'f', 'omega', 'r',
                   'P_', 'a_откл.', 'd', 'd_1 _', 'd_1 _доп._', 'd_1 доп._', 'd_2 доп._', 'l_3 доп._',
                   'K_', 'L _откл.', 'fi_.1', 'type_of_cutting_part_.1', "D_1_", 'd_2 _доп._']:
            print(f"{path} -- {col}")
        if col in ['Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17',
                   'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23',
                   'Unnamed: 24', 'Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27', 'Unnamed: 28', 'Unnamed: 29',
                   'Unnamed: 30', 'Unnamed: 31', 'Unnamed: 32', 'Unnamed: 33', 'Unnamed: 34', 'Unnamed: 35',
                   'Unnamed: 36', 'Unnamed: 37', 'Unnamed: 38', 'Unnamed: 39', 'Unnamed: 40', 'Unnamed: 41',
                   'Unnamed: 42', 'Unnamed: 43', 'Unnamed: 44', 'Unnamed: 45', 'Unnamed: 46', 'Unnamed: 9',
                   'Unnamed: 14', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8']:
            loc_table = loc_table.drop(columns=col)
        if col in ['Конус Моpзе', 'Конус Морзе', ]:
            if col != "Конус Морзе":
                print(f"{path} -- Конус Морзе")
        if col == "index":
            print(f"{path} -- Конус Морзе")
    return loc_table


if __name__ == "__main__":
    table = full_table()
    print(table)
