# `tools`

`tools` - модуль работы с базой данных инструментов.

Материал демонстрационный, показывает навыки работы.
Проект устарел, показывает предыдущий взгляд на способы решения проблемы доступа и обработки информации к БД 

## Установка
```bash
pip install git+https://github.com/sad-engineer/tools.git
```

## Клонирование проекта
```bash
git clone https://github.com/sad-engineer/tools.git
cd tools
```

## Подготовка базы данных
База данных устанавливается вместе с пакетом, и настройка не требуется. Пакет поддерживает базу данных SQLite.

## Использование

Пример использования:
```python
from tools import ToolContainer

# Создаем контейнер инструментов
container = ToolContainer()

# Создание фрезы с настройками по умолчанию
cutter = container.milling_cutter()

# Создание резца с настройками по умолчанию
cutter = container.turning_cutter()

# Создание сверла с настройками по умолчанию
cutter = container.drilling_cutter()

# Создание зенкера с настройками по умолчанию
cutter = container.countersinking_cutter()

# Создание развертки с настройками по умолчанию
cutter = container.deployment_cutter()

# Создание протяжки с настройками по умолчанию
cutter = container.broaching_cutter()
```

## Структура проекта
```
tools/
├── tools/
│ ├── __init__.py
│ ├── __main__.py
│ ├── logger_settings.py        # Настройки логирования
│ ├── data/                     # Данные проекта
│ ├── logs/                     # Логи проекта
│ ├── scr/                      # Скрипты проекта
│ └── obj/                      # Основные классы и объекты
│     ├── __init__.py
│     ├── abstract_classes.py   # Абстрактные классы
│     ├── constants.py          # Константы для классов
│     ├── containers.py         # Контейнеры инструментов
│     ├── creators.py           # Создание объектов
│     ├── data_preparers.py     # Подготовка данных
│     ├── entities.py           # Сущности предметной области
│     ├── fields_types.py       # Типы полей
│     ├── finders.py            # Поиск в базе данных
│     └── listers.py            # Списки и перечисления
├── README.md 
├── poetry.lock 
├── pyproject.toml 
└── setup.cfg 
```

## Требования

- Python 3.9 или выше
- pydantic 2.11.3+
- service-for-my-projects 
- Poetry

## Установка зависимостей

Для установки зависимостей проекта используйте Poetry:

1. Установите Poetry, если он еще не установлен:
```sh
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Linux/MacOS
curl -sSL https://install.python-poetry.org | python3 -
```

2. Установите зависимости проекта:
```sh
# Перейдите в директорию проекта
cd tools

# Установите зависимости
poetry install

# Активируйте виртуальное окружение
poetry shell
```

3. Альтернативная установка через pip:
```sh
# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

## Вклад в проект

1. Создайте форк проекта
2. Создайте ветку для ваших изменений
3. Внесите изменения
4. Отправьте pull request

Пожалуйста, убедитесь, что ваши изменения:
- Сопровождаются тестами
- Следуют существующему стилю кода
- Обновляют документацию при необходимости
