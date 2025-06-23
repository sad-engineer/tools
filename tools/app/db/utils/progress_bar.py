#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
def print_progress_bar(current: int, total: int, prefix: str = "Прогресс", suffix: str = "", length: int = 50):
    """Выводит прогресс-бар в консоль.

    Args:
        current (int): Текущее количество обработанных элементов
        total (int): Общее количество элементов
        prefix (str): Префикс для прогресс-бара
        suffix (str): Суффикс для прогресс-бара
        length (int): Длина прогресс-бара в символах
    """
    percent = (current / total) * 100
    filled_length = int(length * current // total)
    bar = '█' * filled_length + '-' * (length - filled_length)

    # Очищаем строку и выводим прогресс-бар
    print(f'\r{prefix} |{bar}| {percent:.1f}% {suffix}', end='', flush=True)

    # Если прогресс завершен, переходим на новую строку
    if current == total:
        print()
