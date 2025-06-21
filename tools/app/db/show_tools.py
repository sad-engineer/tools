#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from sqlalchemy import text

from tools.app.db.session_manager import session_manager


def show_tools():
    """Показывает все инструменты в базе данных"""
    with session_manager.engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM tools ORDER BY id"))
        columns = result.keys()
        print(" | ".join(columns))
        print("-" * 80)
        for row in result:
            print(" | ".join(str(value) for value in row))


if __name__ == "__main__":
    show_tools()
