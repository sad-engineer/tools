#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import text

from tools.app.db.session_manager import session_manager


def show_table(table_name: str):
    """Показывает все записи в указанной таблице
    
    Args:
        table_name (str): Название таблицы для отображения
    """
    with session_manager.engine.connect() as connection:
        result = connection.execute(text(f"SELECT * FROM {table_name} ORDER BY id"))
        columns = result.keys()
        print(f"Таблица: {table_name}")
        print(" | ".join(columns))
        print("-" * 80)
        for row in result:
            print(" | ".join(str(value) for value in row))


if __name__ == "__main__":
    show_table("tools")
    # show_table("geometry_milling_cutters")

