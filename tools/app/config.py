#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import logging
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Настройка логирования
logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """Возвращает корневую директорию проекта.

    Ищет директорию, содержащую файл pyproject.toml, начиная с текущей директории
    и поднимаясь вверх по дереву директорий.

    Returns:
        Path: Путь к корневой директории проекта

    Raises:
        FileNotFoundError: Если не удается найти корневую директорию проекта
    """
    current = Path(__file__).resolve()
    while current.parent != current:  # Пока не достигли корня файловой системы
        if (current / 'pyproject.toml').exists():
            logger.info(f"Найдена корневая директория проекта: {current}")
            return current
        current = current.parent

    # Если не нашли pyproject.toml, возвращаем директорию с текущим файлом
    fallback_path = Path(__file__).parent.parent.parent
    logger.warning(f"pyproject.toml не найден, используем fallback путь: {fallback_path}")
    return fallback_path


# Определяем пути к конфигурационным файлам
PROJECT_ROOT = get_project_root()
CONFIG_DIR = PROJECT_ROOT / "settings"
ENV_FILE = CONFIG_DIR / "tools.env"

# Создаем директорию config, если её нет
try:
    CONFIG_DIR.mkdir(exist_ok=True)
    logger.info(f"Директория настроек создана/проверена: {CONFIG_DIR}")
except PermissionError as e:
    logger.error(f"Ошибка доступа при создании директории {CONFIG_DIR}: {e}")
    raise


def create_env_file() -> None:
    """Создать файл tools.env с шаблоном настроек.

    Создает файл с переменными окружения по умолчанию, если он не существует.

    Raises:
        PermissionError: Если нет прав на создание файла
        OSError: При других ошибках файловой системы
    """
    if not ENV_FILE.exists():
        template = """# Настройки базы данных
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=tools

# Настройки приложения
APP_NAME=Tools
DEBUG=True
API_V1_STR=/api/v1
"""
        try:
            ENV_FILE.write_text(template, encoding='utf-8')
            logger.info(f"Создан файл настроек: {ENV_FILE}")
        except (PermissionError, OSError) as e:
            logger.error(f"Ошибка при создании файла {ENV_FILE}: {e}")
            raise


# Загружаем переменные окружения
try:
    if not ENV_FILE.exists():
        create_env_file()

    # Проверяем наличие тестовых настроек
    TEST_ENV = os.environ.get("TOOLS_ENV")
    if TEST_ENV and Path(TEST_ENV).exists():
        load_dotenv(TEST_ENV, override=True)
        logger.info(f"Загружены тестовые настройки из: {TEST_ENV}")
    else:
        load_dotenv(ENV_FILE)
        logger.info(f"Загружены настройки из: {ENV_FILE}")
except Exception as e:
    logger.error(f"Ошибка при загрузке переменных окружения: {e}")
    raise


TABLE_NAMES: list = [
    "tools",
    "geometry_countersinking_cutter",
    "geometry_deployment_cutter",
    "geometry_drilling_cutter",
    "geometry_milling_cutters",
    "geometry_turning_cutters",
]


class Settings(BaseSettings):
    """Основные настройки приложения.

    Класс для управления настройками приложения, включая настройки базы данных
    и основные параметры приложения.

    Parameters:
    POSTGRES_USER : (str) : имя пользователя PostgreSQL.
    POSTGRES_PASSWORD : (str) : пароль пользователя PostgreSQL.
    POSTGRES_HOST : (str) : хост базы данных PostgreSQL.
    POSTGRES_PORT : (int) : порт базы данных PostgreSQL.
    POSTGRES_DB : (str) : имя базы данных PostgreSQL.
    APP_NAME : (str) : название приложения.
    DEBUG : (bool) : режим отладки.
    API_V1_STR : (str) : префикс API версии 1.
    TABLE_NAMES : (list) : список названий таблиц в базе данных.

    Properties:
    DATABASE_URL : (str) : полный URL для подключения к базе данных.

    Methods:
    model_dump : (dict) : возвращает словарь с настройками.
    """

    # Настройки базы данных
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # Настройки приложения
    APP_NAME: str
    DEBUG: bool
    API_V1_STR: str

    # Список таблиц
    TABLE_NAMES: list = TABLE_NAMES

    class Config:
        env_file = str(TEST_ENV if TEST_ENV and Path(TEST_ENV).exists() else ENV_FILE)
        case_sensitive = True

    @property
    def DATABASE_URL(self) -> str:
        """Получить полный URL для подключения к базе данных.

        Returns:
            str: URL в формате postgresql://user:password@host:port/database
        """
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def to_dict(self) -> dict:
        """Получить настройки в виде словаря.

        Returns:
            dict: Словарь с настройками приложения
        """
        return self.model_dump()

    def validate_database_settings(self) -> bool:
        """Проверить корректность настроек базы данных.

        Returns:
            bool: True если настройки корректны, False в противном случае
        """
        required_fields = [self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_DB]

        if not all(required_fields):
            logger.error("Не все обязательные поля базы данных заполнены")
            return False

        if not isinstance(self.POSTGRES_PORT, int) or self.POSTGRES_PORT <= 0:
            logger.error(f"Некорректный порт базы данных: {self.POSTGRES_PORT}")
            return False

        return True


@lru_cache()
def get_settings() -> Settings:
    """Получить настройки приложения.

    Использует кэширование для оптимизации производительности.
    При первом вызове загружает настройки из файла или переменных окружения.

    Returns:
        Settings: Объект с настройками приложения

    Raises:
        ValidationError: Если настройки некорректны
        FileNotFoundError: Если не найден файл настроек
    """
    try:
        settings = Settings()

        # Валидируем настройки базы данных
        if not settings.validate_database_settings():
            raise ValueError("Некорректные настройки базы данных")

        logger.info("Настройки приложения успешно загружены")
        return settings

    except Exception as e:
        logger.error(f"Ошибка при загрузке настроек: {e}")
        raise


if __name__ == "__main__":
    # Настройка логирования для тестирования
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
        settings = get_settings()
        print("✅ Настройки успешно загружены")
        print(f"📊 База данных: {settings.DATABASE_URL}")
        print(f"📱 Приложение: {settings.APP_NAME}")
        print(f"🐛 Режим отладки: {settings.DEBUG}")
        print(f"🔗 API версия: {settings.API_V1_STR}")
        print(f"📋 Список таблиц: {settings.TABLE_NAMES}")

        # Тестируем метод to_dict
        settings_dict = settings.to_dict()
        print(f"📋 Настройки в виде словаря: {settings_dict}")

        # Тестируем валидацию
        is_valid = settings.validate_database_settings()
        print(f"✅ Валидация настроек БД: {'Успешно' if is_valid else 'Ошибка'}")

    except Exception as e:
        print(f"❌ Ошибка при загрузке настроек: {e}")
        exit(1)
