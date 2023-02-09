#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar
from typing import Union, Optional

from tools.obj.constants import ACCURACY_STANDARDS
from tools.obj.constants import TOLERANCE_FIELDS
from tools.obj.constants import ACCURACY_CLASS_STANDARDS
from tools.obj.constants import TYPES_OF_MILLING_CUTTER
from tools.obj.constants import TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER
from tools.obj.constants import TYPES_OF_LARGE_TOOTH
from tools.obj.constants import TYPES_OF_TOOL_HOLDER
from tools.obj.constants import TYPES_OF_LOADS
from service import CheckerInDictionary
from service import InvalidValue
from service import Dictionarer


class IAccuracy(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с точностью

    Parameters:
        accuracy : (str, int) : квалитет.

    Сostants:
        ACCURACY_STANDARDS : Квалитеты точности обработки
    """
    ACCURACY_STANDARDS: ClassVar[dict] = ACCURACY_STANDARDS

    def __init__(self, accuracy: Union[str, int, float]) -> None:
        self._accuracy = None
        self.accuracy = accuracy

    @property
    def accuracy(self) -> None:
        return self._accuracy

    @accuracy.setter
    def accuracy(self, any_accuracy) -> None:
        err_message = f'Неверное значение точности инструмента. Значение должно быть из {self.ACCURACY_STANDARDS}.\n ' \
                      f'Передано {any_accuracy}.'
        any_accuracy = self._check_in_dict(any_accuracy, self.ACCURACY_STANDARDS, err_message)
        self._accuracy = any_accuracy if isinstance(any_accuracy, str) else self.ACCURACY_STANDARDS[any_accuracy]

    def _parameters(self) -> dict:
        return {"accuracy": self._accuracy}


class IAccuracyClass(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с классами точности

    Parameters:
        accuracy_class : (str, int in ACCURACY_CLASS_STANDARDS) : класс точности инструмента.

    Сostants:
        ACCURACY_CLASS_STANDARDS : Классы точности инструмента.
    """
    ACCURACY_CLASS_STANDARDS: ClassVar[dict] = ACCURACY_CLASS_STANDARDS

    def __init__(self, accuracy_class: Union[str, int, float]) -> None:
        self._accuracy_class = None
        self.accuracy_class = accuracy_class

    @property
    def accuracy_class(self) -> None:
        return self._accuracy_class

    @accuracy_class.setter
    def accuracy_class(self, any_accuracy_class) -> None:
        err_message = f'Неверное значение класса точности инструмента. Значение должно быть из ' \
                      f'{self.ACCURACY_CLASS_STANDARDS}.\n Передано {any_accuracy_class}.'
        any_accuracy_class = self._check_in_dict(any_accuracy_class, self.ACCURACY_CLASS_STANDARDS, err_message)
        self._accuracy_class = any_accuracy_class if isinstance(any_accuracy_class, str) \
            else self.ACCURACY_CLASS_STANDARDS[any_accuracy_class]

    def _parameters(self) -> dict:
        return {"accuracy_class": self._accuracy_class}


class IQuantity(Dictionarer):
    """ Интерфейс работы с количеством

    Parameters:
        quantity : (int >= 0) : количество одновременно работающих инструментов.
    """
    def __init__(self, quantity: int) -> None:
        self._quantity = None
        self.quantity = quantity

    @property
    def quantity(self) -> None:
        return self._quantity

    @quantity.setter
    def quantity(self, any_quantity) -> None:
        if not isinstance(any_quantity, int) or any_quantity < 0:
            raise InvalidValue(f'Количество должно быть целым положительным числом (передано {any_quantity})')
        self._quantity = any_quantity

    def _parameters(self) -> dict:
        return {"quantity": self._quantity}


class INumOfBlades(Dictionarer):
    """ Интерфейс работы с количеством режущих граней

    Parameters:
        num_of_cutting_blades : (int >= 0) : количество режущих граней.
    """
    def __init__(self, num_of_cutting_blades: int) -> None:
        self._num_of_cutting_blades = None
        self.num_of_cutting_blades = num_of_cutting_blades

    @property
    def num_of_cutting_blades(self):
        return self._num_of_cutting_blades

    @num_of_cutting_blades.setter
    def num_of_cutting_blades(self, any_num):
        if not isinstance(any_num, int) or any_num < 0:
            raise InvalidValue(f'Количество режущих граней должно быть целым положительным числом (передано {any_num})')
        self._num_of_cutting_blades = any_num

    def _parameters(self) -> dict:
        return {"num_of_cutting_blades": self._num_of_cutting_blades}


class IRadius(Dictionarer):
    """ Интерфейс работы с количеством режущих граней

    Parameters:
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.
    """
    def __init__(self, radius_of_cutting_vertex: float) -> None:
        self._radius_of_cutting_vertex = None
        self.radius_of_cutting_vertex = radius_of_cutting_vertex

    @property
    def radius_of_cutting_vertex(self):
        return self._radius_of_cutting_vertex

    @radius_of_cutting_vertex.setter
    def radius_of_cutting_vertex(self, any_radius):
        if not isinstance(any_radius, (int, float)) or any_radius < 0:
            raise InvalidValue(f'Радиус вершины должен быть положительным числом (передано {any_radius})')
        self._radius_of_cutting_vertex = any_radius

    def _parameters(self) -> dict:
        return {"radius_of_cutting_vertex": self._radius_of_cutting_vertex}


class IToleranceField(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с полями допусков

    Parameters:
        tolerance_field : (str, int) : поле допуска.

    Сostants:
        TOLERANCE_FIELDS : Поля допусков
    """
    TOLERANCE_FIELDS: ClassVar[dict] = TOLERANCE_FIELDS

    def __init__(self, tolerance_field: Union[str, int, float]) -> None:
        self._tolerance_field = None
        self.tolerance_field = tolerance_field

    @property
    def tolerance_field(self) -> None:
        return self._tolerance_field

    @tolerance_field.setter
    def tolerance_field(self, any_field) -> None:
        err_message = f'Неверное значение поля допуска. Значение должно быть из {self.TOLERANCE_FIELDS}.\n ' \
                      f'Передано {any_field}.'
        any_field = self._check_in_dict(any_field, self.TOLERANCE_FIELDS, err_message)
        self._tolerance_field = any_field if isinstance(any_field, str) else self.TOLERANCE_FIELDS[any_field]

    def _parameters(self) -> dict:
        return {"tolerance_field": self._tolerance_field}


class ITypeCutter(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с типом фрезы

    Parameters:
        type_cutter : (str, int, float in TYPES_OF_MILLING_CUTTER) : Тип инструмента:
            "Цилиндрическая": 0,
            "Торцовая": 1,
            "Дисковая, обработка торца": 2,
            "Дисковая, обработка паза": 3,
            "Пазовая": 3,
            "Отрезная": 4,
            "Прорезная": 4,
            "Концевая, обработка торца": 5,
            "Концевая, обработка паза": 6,
            "Угловая": 7,
            "Фасонная, с выпуклым профилем": 8,
            "Фасонная, с вогнутым профилем": 9,
            "Шпоночная": 10,
            "Резьбовая": 8,
            "Червячная": 0,

    Сostants:
        TYPES_OF_MILLING_CUTTER : Типы фрез
    """
    TYPES_OF_MILLING_CUTTER: ClassVar[dict] = TYPES_OF_MILLING_CUTTER

    def __init__(self, type_cutter: Union[str, int, float]) -> None:
        self._type_cutter = None
        self.type_cutter = type_cutter

    @property
    def type_cutter(self):
        return self._type_cutter

    @type_cutter.setter
    def type_cutter(self, any_type):
        err_message = f'Неверное значение типа фрезы.' \
                      f' Значение должно быть из {self.TYPES_OF_MILLING_CUTTER}.\n Передано {any_type}.'
        any_type = self._check_in_dict(any_type, self.TYPES_OF_MILLING_CUTTER, err_message)
        self._type_cutter = any_type if isinstance(any_type, (int, float)) else self.TYPES_OF_MILLING_CUTTER[any_type]

    def _parameters(self) -> dict:
        return {"type_cutter": self._type_cutter}


class ITypeOfCuttingPart(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с типом режущей части фрезы

    Parameters:
        type_of_cutting_part : (str, int, float in TYPES_OF_CUTTING_PART) : тип режущей части.

    Сostants:
        TYPES_OF_CUTTING_PART : Типы режущей части фрезы.
    """
    TYPES_OF_CUTTING_PART: ClassVar[dict] = TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER

    def __init__(self, type_of_cutting_part: Union[str, int, float]) -> None:
        self._type_of_cutting_part = None
        self.type_of_cutting_part = type_of_cutting_part

    @property
    def type_of_cutting_part(self):
        return self._type_of_cutting_part

    @type_of_cutting_part.setter
    def type_of_cutting_part(self, any_type):
        err_message = f'Неверное значение типа режущей части фрезы. ' \
                      f'Значение должно быть из {self.TYPES_OF_CUTTING_PART}.\n Передано {any_type}.'
        any_type = self._check_in_dict(any_type, self.TYPES_OF_CUTTING_PART, err_message)
        self._type_of_cutting_part = any_type if isinstance(any_type, (int, float)) else \
            self.TYPES_OF_CUTTING_PART[any_type]

    def _parameters(self) -> dict:
        return {"type_of_cutting_part": self._type_of_cutting_part}


class ILargeTooth(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с типом частоты режущей части

    Parameters:
        large_tooth : (str, int, float in TYPES_OF_LARGE_TOOTH) :  Крупный/мелкий зуб.

    Сostants:
        TYPES_OF_LARGE_TOOTH : Типы частоты режущей части.
    """
    TYPES_OF_LARGE_TOOTH: ClassVar[dict] = TYPES_OF_LARGE_TOOTH

    def __init__(self, large_tooth: Union[str, int, float]) -> None:
        self._large_tooth = None
        self.large_tooth = large_tooth

    @property
    def large_tooth(self):
        return self._large_tooth

    @large_tooth.setter
    def large_tooth(self, any_large_tooth):
        err_message = f'Неверное значение типа режущей части фрезы. ' \
                      f'Значение должно быть из {self.TYPES_OF_LARGE_TOOTH}.\n Передано {any_large_tooth}.'
        any_type = self._check_in_dict(any_large_tooth, self.TYPES_OF_LARGE_TOOTH, err_message)
        self._large_tooth = any_type if isinstance(any_type, (int, float)) else self.TYPES_OF_LARGE_TOOTH[any_type]

    def _parameters(self) -> dict:
        return {"large_tooth": self._large_tooth}


class ICutterNumber(Dictionarer):
    """ Интерфейс работы с номером фрезы

    Parameters:
        cutter_number : (Optional[str]) : номер фрезы ("1", "1 1/2", и т.д.).
    """
    def __init__(self, cutter_number: Optional[str]) -> None:
        self._cutter_number = None
        self.cutter_number = cutter_number

    @property
    def cutter_number(self):
        return self._cutter_number

    @cutter_number.setter
    def cutter_number(self, any_num):
        if not isinstance(any_num, type(None)):
            if not isinstance(any_num, str):
                raise InvalidValue(f'Номер фрезы должен быть задан строкой (передано {any_num})')
        self._cutter_number = any_num

    def _parameters(self) -> dict:
        return {"cutter_number": self._cutter_number}


class IModule(Dictionarer):
    """ Интерфейс работы с модулем фрезы

    Parameters:
        module : (Optional[float] >= 0) : модуль червячной фрезы.
    """
    def __init__(self, module: Optional[float]) -> None:
        self._module = None
        self.module = module

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, any_module):
        if not isinstance(any_module, type(None)):
            if not isinstance(any_module, (int, float)) or any_module < 0:
                raise InvalidValue(f'Модуль фрезы должен быть положительным числом (передано {any_module})')
        self._module = any_module

    def _parameters(self) -> dict:
        return {"module": self._module}


class ITurret(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с полем наличия револьверной головки

    Parameters:
        turret : (int, str in TYPES_OF_TOOL_HOLDER) :  Наличие револьверной головки.

    Сostants:
        TYPES_OF_TOOL_HOLDER : Типы установки резца.
    """
    TYPES_OF_TOOL_HOLDER: ClassVar[dict] = TYPES_OF_TOOL_HOLDER

    def __init__(self, turret: Union[str, int, float]) -> None:
        self._turret = None
        self.turret = turret

    @property
    def turret(self):
        return self._turret

    @turret.setter
    def turret(self, any_type):
        err_message = f'Неверное значение типа установки резца.' \
                      f' Значение должно быть из {self.TYPES_OF_TOOL_HOLDER}.\n Передано {any_type}.'
        any_type = self._check_in_dict(any_type, self.TYPES_OF_TOOL_HOLDER, err_message)
        self._type_cutter = any_type if isinstance(any_type, (int, float)) else self.TYPES_OF_TOOL_HOLDER[any_type]

    def _parameters(self) -> dict:
        return {"turret": self._turret}


class ILoad(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с полем нагрузки на резец

    Parameters:
        load : (int, str in TYPES_OF_TOOL_HOLDER) : Нагрузка на резец.

    Сostants:
        TYPES_OF_LOADS : Типы нагрузок на резец.
    """
    TYPES_OF_LOADS: ClassVar[dict] = TYPES_OF_LOADS

    def __init__(self, load: Union[str, int, float]) -> None:
        self._load = None
        self.load = load

    @property
    def load(self):
        return self._load

    @load.setter
    def load(self, any_type):
        err_message = f'Неверное значение типа нагрузки на резец.' \
                      f' Значение должно быть из {self.TYPES_OF_LOADS}.\n Передано {any_type}.'
        any_type = self._check_in_dict(any_type, self.TYPES_OF_LOADS, err_message)
        self._load = any_type if isinstance(any_type, (int, float)) else self.TYPES_OF_LOADS[any_type]

    def _parameters(self) -> dict:
        return {"load": self._load}


class IComplexProfile(CheckerInDictionary, Dictionarer):
    """ Интерфейс работы с полем наличия глубокого или сложного профиля.

    Parameters:
        is_complex_profile : (Optional[bool]) : Показатель наличия глубокого или сложного профиля. По умолчанию: None.
    """
    def __init__(self, is_complex_profile: bool) -> None:
        self._is_complex_profile = None
        self.is_complex_profile = is_complex_profile

    @property
    def is_complex_profile(self):
        return self._is_complex_profile

    @is_complex_profile.setter
    def is_complex_profile(self, any_value):
        if not isinstance(any_value, bool):
            raise InvalidValue('Передайте "True" если резец имеет глубокий и сложный профиль')
        self._is_complex_profile = any_value

    def _parameters(self) -> dict:
        return {"is_complex_profile": self._is_complex_profile}


class IAngleOfInclination(Dictionarer):
    """ Интерфейс работы с полем угол наклона зубьев протяжки.

    Parameters:
        angle_of_inclination: (float >= 0) : Угол наклона зубьев протяжки.
    """
    def __init__(self, angle_of_inclination: float) -> None:
        self._angle_of_inclination = None
        self.angle_of_inclination = angle_of_inclination

    @property
    def angle_of_inclination(self):
        return self._angle_of_inclination

    @angle_of_inclination.setter
    def angle_of_inclination(self, any_value):
        if not isinstance(any_value, (int, float)) or any_value < 0:
            raise InvalidValue(f'Угол наклона должен быть числом (передано {any_value})')
        self._angle_of_inclination = any_value

    def _parameters(self) -> dict:
        return {"angle_of_inclination": self._angle_of_inclination}


class IPitchOfTeeth(Dictionarer):
    """ Интерфейс работы с полем шаг зубьев протяжки..

    Parameters:
         pitch_of_teeth: (float >= 0) : Шаг зубьев протяжки.
    """
    def __init__(self, pitch_of_teeth: float) -> None:
        self._pitch_of_teeth = None
        self.pitch_of_teeth = pitch_of_teeth

    @property
    def pitch_of_teeth(self):
        return self._pitch_of_teeth

    @pitch_of_teeth.setter
    def pitch_of_teeth(self, any_value):
        if not isinstance(any_value, (int, float)) or any_value < 0:
            raise InvalidValue(f'Шаг зубьев должен быть положительным числом (передано {any_value})')
        self._pitch_of_teeth = any_value

    def _parameters(self) -> dict:
        return {"pitch_of_teeth": self._pitch_of_teeth}


class INumberTeethSection(Dictionarer):
    """ Интерфейс работы с полем число зубьев секции протяжки.

    Parameters:
         number_teeth_section: (float >= 0) : Число зубьев секции протяжки.
    """

    def __init__(self, number_teeth_section: float) -> None:
        self._number_teeth_section = None
        self.number_teeth_section = number_teeth_section

    @property
    def number_teeth_section(self):
        return self._number_teeth_section

    @number_teeth_section.setter
    def number_teeth_section(self, any_value):
        if not isinstance(any_value, (int, float)) or any_value < 0:
            raise InvalidValue(f'Число зубьев секции протяжки должно быть положительным числом (передано {any_value})')
        self._number_teeth_section = any_value

    def _parameters(self) -> dict:
        return {"number_teeth_section": self._number_teeth_section}


class IDifference(Dictionarer):
    """ Интерфейс работы с полем подача на зуб протяжки .

    Parameters:
         difference: (float >= 0) : Подача на зуб протяжки (размерный перепад между соседними зубьями).
    """

    def __init__(self, difference: float) -> None:
        self._difference = None
        self.difference = difference

    @property
    def difference(self):
        return self._difference

    @difference.setter
    def difference(self, any_value):
        if not isinstance(any_value, (int, float)) or any_value < 0:
            raise InvalidValue(f'Подача на зуб протяжки должно быть положительным числом (передано {any_value})')
        self._difference = any_value

    def _parameters(self) -> dict:
        return {"difference": self._difference}


class ILengthOfWorkingPart(Dictionarer):
    """ Интерфейс работы с полем длина режущей части протяжки.

    Parameters:
         length_of_working_part: (float >= 0) : Длина режущей части протяжки.
    """

    def __init__(self, length_of_working_part: float) -> None:
        self._length_of_working_part = None
        self.length_of_working_part = length_of_working_part

    @property
    def length_of_working_part(self):
        return self._length_of_working_part

    @length_of_working_part.setter
    def length_of_working_part(self, any_value):
        if not isinstance(any_value, (int, float)) or any_value < 0:
            raise InvalidValue(f'Длина режущей части должна быть положительным числом (передано {any_value})')
        self._length_of_working_part = any_value

    def _parameters(self) -> dict:
        return {"length_of_working_part": self._length_of_working_part}
