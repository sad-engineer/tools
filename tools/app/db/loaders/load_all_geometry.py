#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Универсальный скрипт для загрузки всех типов геометрических данных инструментов из CSV файла.

Этот скрипт загружает данные для всех типов инструментов:
- Фрезы (geometry_milling_cutters)
- Сверла (geometry_drilling_cutter)
- Зенкеры (geometry_countersinking_cutter)
- Развертки (geometry_deployment_cutter)
- Токарные резцы (geometry_turning_cutters)
"""

import logging
from pathlib import Path

from tools.app.db.loaders.base_loader import BaseGeometryLoader
from tools.app.db.loaders.load_countersinking_cutter import COUNTERSINKING_COLUMN_MAPPING
from tools.app.db.loaders.load_deployment_cutter import DEPLOYMENT_COLUMN_MAPPING
from tools.app.db.loaders.load_drilling_cutter import DRILL_COLUMN_MAPPING
from tools.app.db.loaders.load_milling_cutters import MILLING_CUTTER_COLUMN_MAPPING
from tools.app.db.loaders.load_turning_cutters import TURNING_COLUMN_MAPPING
from tools.app.models.geometry_countersinking_cutter import GeometryCountersinkingCutter
from tools.app.models.geometry_deployment_cutter import GeometryDeploymentCutter
from tools.app.models.geometry_drilling_cutter import GeometryDrillingCutter
from tools.app.models.geometry_milling_cutters import GeometryMillingCutters
from tools.app.models.geometry_turning_cutters import GeometryTurningCutters

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация загрузчиков для всех типов инструментов
LOADERS_CONFIG = {
    "Фреза": {
        "model": GeometryMillingCutters,
        "mapping": MILLING_CUTTER_COLUMN_MAPPING,
    },
    "Сверло": {
        "model": GeometryDrillingCutter,
        "mapping": DRILL_COLUMN_MAPPING,
    },
    "Зенкер": {
        "model": GeometryCountersinkingCutter,
        "mapping": COUNTERSINKING_COLUMN_MAPPING,
    },
    "Развертка": {
        "model": GeometryDeploymentCutter,
        "mapping": DEPLOYMENT_COLUMN_MAPPING,
    },
    "Резец": {
        "model": GeometryTurningCutters,
        "mapping": TURNING_COLUMN_MAPPING,
    },
}


def load_all_geometry_data(csv_file_path: str = None) -> dict:
    """
    Загружает данные для всех типов инструментов.

    Args:
        csv_file_path: Путь к CSV файлу

    Returns:
        dict: Словарь с результатами загрузки для каждого типа
    """
    if csv_file_path is None:
        project_root = Path(__file__).parent.parent.parent.parent.parent
        csv_file_path = project_root / "database_backups" / "tools_old.csv"

    results = {}

    for tool_type, config in LOADERS_CONFIG.items():
        try:
            logger.info(f"🔄 Загружаем данные для {tool_type}...")

            loader = BaseGeometryLoader(
                tool_type=tool_type, model_class=config["model"], column_mapping=config["mapping"]
            )

            loaded_count = loader.run(csv_file_path)
            results[tool_type] = loaded_count

            logger.info(f"✅ {tool_type}: загружено {loaded_count} записей")

        except Exception as e:
            logger.error(f"❌ Ошибка при загрузке {tool_type}: {e}")
            results[tool_type] = 0

    return results


def load_all_geometry():
    """Основная функция."""
    try:
        logger.info("🚀 Начинаем загрузку всех геометрических данных инструментов")

        results = load_all_geometry_data()

        # Выводим итоговую статистику
        logger.info("\n📊 ИТОГОВАЯ СТАТИСТИКА:")
        total_loaded = 0
        for tool_type, count in results.items():
            logger.info(f"  {tool_type}: {count} записей")
            total_loaded += count

        logger.info(f"\n✅ Загрузка завершена! Всего загружено: {total_loaded} записей")

    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        raise


if __name__ == "__main__":
    load_all_geometry()
