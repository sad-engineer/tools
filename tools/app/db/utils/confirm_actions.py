#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Универсальный модуль для подтверждения действий в скриптах БД.

Содержит функции для запроса подтверждения различных операций
с базой данных с настраиваемыми сообщениями.
"""

from typing import Optional

from tools.app.config import get_settings

settings = get_settings()


def confirm_action(
    action_name: str,
    action_description: str,
    database_name: Optional[str] = None,
    is_destructive: bool = True,
    custom_message: Optional[str] = None,
) -> bool:
    """
    Универсальная функция для подтверждения действий.

    Args:
        action_name (str): Название действия (например, "очистка", "удаление")
        action_description (str): Описание что будет сделано
        database_name (str, optional): Название базы данных. Если None, используется из настроек
        is_destructive (bool): Является ли действие разрушительным (показывает предупреждение)
        custom_message (str, optional): Дополнительное сообщение

    Returns:
        bool: True если пользователь подтвердил действие, False в противном случае
    """
    if database_name is None:
        database_name = settings.POSTGRES_DB

    print("\n" + "=" * 60)

    if is_destructive:
        print("⚠️  ВНИМАНИЕ! Это действие необратимо!")
        print("=" * 60)

    print(f"Вы собираетесь выполнить: {action_name}")
    print(f"База данных: {database_name}")
    print(f"Действие: {action_description}")

    if custom_message:
        print(f"Дополнительно: {custom_message}")

    print("=" * 60)

    while True:
        response = input("Вы уверены, что хотите продолжить? (да/нет): ").lower().strip()
        if response in ['да', 'yes', 'y', 'д']:
            return True
        elif response in ['нет', 'no', 'n', 'н']:
            return False
        else:
            print("Пожалуйста, введите 'да' или 'нет'")


def confirm_clear() -> bool:
    """
    Запрашивает подтверждение очистки базы данных.

    Returns:
        bool: True если пользователь подтвердил очистку, False в противном случае
    """
    return confirm_action(
        action_name="очистка базы данных",
        action_description="Удаление всех данных из всех таблиц (структура таблиц сохранится)",
        is_destructive=True,
        custom_message="Это приведет к потере всех данных, но таблицы останутся.",
    )


def confirm_removal() -> bool:
    """
    Запрашивает подтверждение удаления базы данных.

    Returns:
        bool: True если пользователь подтвердил удаление, False в противном случае
    """
    return confirm_action(
        action_name="удаление базы данных",
        action_description="Полное удаление базы данных и всех таблиц",
        is_destructive=True,
        custom_message="Это приведет к полной потере всех данных и структуры.",
    )


def confirm_restore() -> bool:
    """
    Запрашивает подтверждение восстановления базы данных.

    Returns:
        bool: True если пользователь подтвердил восстановление, False в противном случае
    """
    return confirm_action(
        action_name="восстановление базы данных",
        action_description="Создание таблиц и загрузка данных из CSV файлов",
        is_destructive=False,
        custom_message="Существующие данные будут перезаписаны.",
    )
