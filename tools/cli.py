#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import click

from tools.app.db import (
    clear_database_with_options,
    export_table_to_csv_with_options,
    get_status,
    init_database,
    remove_database_with_options,
    restore_database_with_options,
    show_database,
)


@click.group()
@click.version_option(version='1.0.0', prog_name='tools')
def tool():
    """
    🛠️ Tools CLI - управление базой данных инструментов

    Основные команды:

    🔧 Операции с БД:
      init                  Инициализация базы данных
      clear                 Очистка данных с подтверждением
      clear --quiet         "Тихая" очистка данных (без подтверждения)
      restore               Восстановление БД (создание + загрузка)
      restore --quiet       "Тихое" восстановление БД (без подтверждения)
      remove                Удаление БД с подтверждением
      remove --quiet        "Тихое" удаление БД (без подтверждения)

    📊 Информация:
      status                Проверка статуса БД
      show                  Информация о БД

    📤 Экспорт данных:
      export                Интерактивный экспорт (по умолчанию)
      export --all          Экспорт всех таблиц (тихий режим)

    Примеры использования:
      tool clear --quiet     # "Тихая" очистка данных (без подтверждения)
      tool restore --quiet   # "Тихое" восстановление БД (без подтверждения)
      tool remove --quiet    # "Тихое" удаление БД (без подтверждения)
    """
    pass


@tool.command()
@click.help_option('-h', '--help')
def init():
    """
    Инициализирует базу данных.

    Создает таблицы и загружает начальные данные.
    Используйте после создания базы данных.

    Пример: tool init
    """
    init_database()


@tool.command()
@click.option('--quiet', '-q', is_flag=True, help='Тихая очистка без подтверждения')
@click.help_option('-h', '--help')
def clear(quiet):
    """
    Очищает все данные в базе данных.

    Удаляет все записи из всех таблиц, но оставляет структуру.

    Примеры:
      tool clear          # Очистка с подтверждением
      tool clear --quiet  # 'Тихая' очистка без подтверждения
    """
    clear_database_with_options(quiet=quiet)


@tool.command()
@click.option('--quiet', '-q', is_flag=True, help='Тихое восстановление без подтверждения')
@click.help_option('-h', '--help')
def restore(quiet):
    """
    Восстанавливает базу данных (создает таблицы и загружает данные).

    Полное восстановление: создание таблиц + загрузка данных из CSV.
    Используйте для полной переинициализации БД.

    Примеры:
      tool restore          # Восстановление с подтверждением
      tool restore --quiet  # 'Тихое' восстановление без подтверждения
    """
    restore_database_with_options(quiet=quiet)


@tool.command()
@click.option('--quiet', '-q', is_flag=True, help='Тихое удаление без подтверждения')
@click.help_option('-h', '--help')
def remove(quiet):
    """
    Удаляет базу данных полностью.

    Полное удаление базы данных и всех таблиц.

    Примеры:
      tool remove          # Удаление с подтверждением
      tool remove --quiet  # 'Тихое' удаление без подтверждения
    """
    remove_database_with_options(quiet=quiet)


@tool.command()
@click.help_option('-h', '--help')
def status():
    """
    Показывает статус базы данных.

    Проверяет доступность БД и выводит список таблиц.
    Используйте для диагностики подключения.

    Пример: tool status
    """
    get_status()


@tool.command()
@click.help_option('-h', '--help')
def show():
    """
    Показывает информацию о базе данных.

    Выводит детальную информацию о структуре БД,
    количестве записей в таблицах.

    Пример: tool show
    """
    click.echo("📊 Информация о базе данных...")
    show_database()


@tool.command()
@click.option('--all', '-a', is_flag=True, help='Экспорт всех таблиц (тихий режим)')
@click.help_option('-h', '--help')
def export(all):
    """
    Экспортирует данные из базы данных в CSV файлы.

    Примеры:
      tool export                           # Интерактивный экспорт (по умолчанию)
      tool export --all                     # Экспорт всех таблиц (тихий режим)
    """
    export_table_to_csv_with_options(all_tables=all)


if __name__ == "__main__":
    tool()
