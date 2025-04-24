#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import re
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator, confloat, conint, Field
from collections import namedtuple

from service_for_my_projects import InvalidValue
from service_for_my_projects import Dictionarer
# from service_for_my_projects import logged

from tools.obj.constants import TYPES_STANDARD, HARD_ALLOYS
from tools.obj.fields_types import InGroupsTool, StringValue, MarkingForSpecialTool, InMaterialsOfCuttingPart, \
    InAccuracyStandards, InToleranceField, InTypesOfMillingCutter, InTypesOfCuttingPart, InTypesOfLargeTooth, \
    InAccuracyClassStandards
from tools.obj.abstract_classes import Size


ErrorWithData = namedtuple('ErrorWithData', ['err', 'name', 'params', 'raw_data'])   # для сохранения данных с ошибкой


class Base(BaseModel):
    """Базовый класс, содержащий настройки."""

    class Config:
        validate_assignment = True
        extra = "allow"
        arbitrary_types_allowed = True


class Tool(Base, Dictionarer):
    """Управляет полями класса 'Инструмент'.

    Parameters:
        group : (str is GROUPS_TOOL) : группа инструмента.
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
        quantity : (int >= 0) : количество одновременно работающих инструментов.

    Properties:
        name : (str) : возвращает название инструмента.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.
    """
    _name: Optional[str] = Field(default=None, description="Для сохранения кастомного имени инструмента")
    group: InGroupsTool = Field(default="Инструмент", description="Группа инструмента")
    marking: StringValue = Field(default="ХХХХ-ХХХХ", description="Обозначение инструмента")
    standard: str = Field(default="ГОСТ 1000-90", description="Стандарт инструмента")
    quantity: int = Field(default=1, ge=0, description="Количество одновременно работающих инструментов")

    @property
    def name(self) -> str:
        return " ".join([self.group, self.marking, self.standard]) if isinstance(self._name, type(None)) else self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @field_validator('standard')
    def validate_standard(cls, value):
        for substring in TYPES_STANDARD:
            if substring in value:
                return value
        raise InvalidValue(f"Ожидается строка, содержащая название стандарта инструмента (например: "
                           f"{', '.join(str(i) for i in TYPES_STANDARD)}). Получено значение: {value}")

    @field_validator('marking')
    def validate_marking(cls, value):
        if not isinstance(value, str):
            raise InvalidValue(f'Неверное обозначение инструмента. Ожидается строковое выражение. Получено: {value}')
        return value

    def _parameters(self) -> dict:
        return {"group": self.group, "marking": self.marking, "standard": self.standard, "name": self.name,
                "quantity": self.quantity}


class CustomTool(Tool):
    """ Специальный инструмент. В этом инструменте в поле marking указывается только 'специальный' а поле standard
    можно оставлять пустым."""

    marking: MarkingForSpecialTool = Field(default='специальный', description="Обозначение инструмента")

    @field_validator('standard')
    def validate_standard(cls, value):
        if value == "" or isinstance(value, type(None)):
            return ""
        for substring in TYPES_STANDARD:
            if substring in value:
                return value
        raise InvalidValue(f"Ожидается строка, содержащая название стандарта инструмента (например: "
                           f"{', '.join(str(i) for i in TYPES_STANDARD)}). Получено значение: {value}")


class AxialSizes(Base, Dictionarer, Size):
    """Диаметральные размеры инструмента.

    Parameters:
        dia_mm : (float >= 0) : диаметр инструмента.
        length_mm : (float >= 0) : длина инструмента.
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.

    Properties:
        gabarit_volume : (float) : возвращает габаритный объем.
        gabarit_str : (str) : возвращает габарит, записанный строкой.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.
    """
    dia_mm: float = Field(default=6, ge=0, description="Диаметр инструмента")
    length_mm: float = Field(default=100, ge=0, description="Длина инструмента")
    radius_of_cutting_vertex: float = Field(default=1, ge=0, description="Радиус режущей вершины")

    @property
    def gabarit_volume(self):
        return self.dia_mm * self.dia_mm * self.length_mm

    @property
    def gabarit_str(self):
        return f"øDxL: ø{self.dia_mm}x{self.length_mm} мм."

    def _parameters(self) -> dict:
        return {"dia_mm": self.dia_mm, "length_mm": self.length_mm,
                "radius_of_cutting_vertex": self.radius_of_cutting_vertex, "gabarit_volume": self.gabarit_volume,
                "gabarit_str": self.gabarit_str}


class PrismaticSizes(Base, Dictionarer, Size):
    """Размеры призматического инструмента.

    Parameters:
        length_mm : (float >= 0) : длина инструмента.
        width_mm : (float >= 0) : ширина инструмента.
        height_mm : (float >= 0) : высота инструмента.
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.

    Properties:
        gabarit_volume : (float) : возвращает габаритный объем.
        gabarit_str : (str) : возвращает габарит, записанный строкой.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.
    """

    length_mm: float = Field(default=100, ge=0, description="Длина инструмента")
    width_mm: float = Field(default=16, ge=0, description="Ширина инструмента")
    height_mm: float = Field(default=25, ge=0, description="Высота инструмента")
    radius_of_cutting_vertex: float = Field(default=1, ge=0, description="Радиус режущей вершины")

    @property
    def gabarit_volume(self):
        return self.height_mm * self.width_mm * self.length_mm

    @property
    def gabarit_str(self):
        return f"LxBxH: {self.length_mm}x{self.width_mm}x{self.height_mm} мм."

    def _parameters(self):
        return {"length_mm": self.length_mm, "width_mm": self.width_mm, "height_mm": self.height_mm,
                "radius_of_cutting_vertex": self.radius_of_cutting_vertex, "gabarit_volume": self.gabarit_volume,
                "gabarit_str": self.gabarit_str}


class BladeMaterial(Base, Dictionarer):
    """ Материал лезвия.

    Parameters:
        mat_of_cutting_part : (str, int is MATERIALS_OF_CUTTING_PART) : материал режущей пластины.

    Properties:
        type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.

    """
    mat_of_cutting_part: Optional[InMaterialsOfCuttingPart] = Field(default="Т15К6", description="Материал режущей пластины")

    @property
    def type_of_mat(self):
        return 1 if self.mat_of_cutting_part in HARD_ALLOYS else 0

    def _parameters(self):
        return {"mat_of_cutting_part": self.mat_of_cutting_part, "type_of_mat": self.type_of_mat}


class Angles(Base, Dictionarer):
    """Углы инструмента

    Parameters:
        main_angle_grad : главный угол в плане.
        front_angle_grad  : передний угол.
        inclination_of_main_blade_grad : наклон передней грани

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.
    """
    main_angle_grad: float = Field(default=0, description="Главный угол в плане")
    front_angle_grad: float = Field(default=0, description="Передний угол")
    inclination_of_main_blade_grad: float = Field(default=0, description="Наклон передней грани")

    def _parameters(self):
        return {"main_angle_grad": self.main_angle_grad, "front_angle_grad": self.front_angle_grad,
                "inclination_of_main_blade_grad": self.inclination_of_main_blade_grad, }


class Tolerance(Base, Dictionarer):
    """Допуск инструмента

    Parameters:
        accuracy : (str, int is ACCURACY_STANDARDS) : квалитет.
        tolerance_field : (str, int is TOLERANCE_FIELDS) : поле допуска.

    Properties:
        tolerance : (str, int содержит по одному из ACCURACY_STANDARDS, TOLERANCE_FIELDS) : допуск.
    """
    accuracy: InAccuracyStandards = Field(default="14", description="Квалитет")
    tolerance_field: InToleranceField = Field(default='H', description="Поле допуска")

    @property
    def tolerance(self) -> str:
        return "".join([str(self.tolerance_field), str(self.accuracy)])

    @tolerance.setter
    def tolerance(self, any_tolerance) -> None:
        self.accuracy = re.findall(r'\d+', any_tolerance)[0]
        self.tolerance_field = any_tolerance.replace(re.findall(r'\d+', any_tolerance)[0], "")

    def _parameters(self) -> dict:
        return {"accuracy": self.accuracy, "tolerance_field": self.tolerance_field, "tolerance": self.tolerance}

    def __setattr__(self, name, value):
        if name == 'tolerance':
            self.accuracy = re.findall(r'\d+', value)[0]
            self.tolerance_field = value.replace(re.findall(r'\d+', value)[0], "")
        else:
            super().__setattr__(name, value)


class DrillingCutter(Tolerance, Angles, BladeMaterial, AxialSizes, Tool):
    """ Сверло

    Parameters:
        group : (str is GROUPS_TOOL) : группа инструмента.
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
        dia_mm : (float >= 0) : диаметр инструмента.
        length_mm : (float >= 0) : длина инструмента.
        mat_of_cutting_part : (str, int is MATERIALS_OF_CUTTING_PART) : материал режущей пластины.
        main_angle_grad : (float >= 0) : главный угол в плане.
        front_angle_grad  : (float >= 0) : передний угол.
        inclination_of_main_blade_grad  : (float >= 0) : наклон передней грани.
        tolerance : (str, int содержит по одному из ACCURACY_STANDARDS, TOLERANCE_FIELDS) : допуск.
        num_of_cutting_blades : (int >= 0) : количество режущих граней.
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.
        quantity : (int >= 0) : количество одновременно работающих инструментов.

    Properties:
        name : (str) : возвращает название инструмента.
        gabarit_volume : (float) : возвращает габаритный объем.
        gabarit_str : (str) : возвращает габарит, записанный строкой.
        type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.
    """
    group: InGroupsTool = Field(default="Сверло", description="Группа инструмента")
    num_of_cutting_blades: int = Field(default=2, ge=0, description="Количество режущих граней")

    @model_validator(mode="before")
    def check_group(cls, values):
        if 'group' in values and values['group'] != "Сверло":
            raise ValueError(f"Нельзя менять группу класса '{cls.__class__.__name__}' ({cls.group}). "
                             f"Используйте соответствующий класс")
        return values

    def _parameters(self):
        tool_parameters = Tool._parameters(self)
        size_parameters = AxialSizes._parameters(self)
        blade_material_parameters = BladeMaterial._parameters(self)
        angles_parameters = Angles._parameters(self)
        tolerance_parameters = Tolerance._parameters(self)
        return tool_parameters | size_parameters | blade_material_parameters | angles_parameters | \
            tolerance_parameters | {
                "num_of_cutting_blades": self.num_of_cutting_blades,
            }


class CountersinkingCutter(DrillingCutter):
    """ Зенкер

    Parameters:
        group : (str is GROUPS_TOOL) : группа инструмента.
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
        dia_mm : (float >= 0) : диаметр инструмента.
        length_mm : (float >= 0) : длина инструмента.
        mat_of_cutting_part : (str, int is MATERIALS_OF_CUTTING_PART) : материал режущей пластины.
        main_angle_grad : (float >= 0) : главный угол в плане.
        front_angle_grad  : (float >= 0) : передний угол.
        inclination_of_main_blade_grad  : (float >= 0) : наклон передней грани.
        tolerance : (str, int содержит по одному из ACCURACY_STANDARDS, TOLERANCE_FIELDS) : допуск.
        num_of_cutting_blades : (int >= 0) : количество режущих граней.
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.
        quantity : (int >= 0) : количество одновременно работающих инструментов.

    Properties:
        name : (str) : возвращает название инструмента.
        gabarit_volume : (float) : возвращает габаритный объем.
        gabarit_str : (str) : возвращает габарит, записанный строкой.
        type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.
    """
    group: InGroupsTool = Field(default="Зенкер", description="Группа инструмента")
    num_of_cutting_blades: int = Field(default=8, ge=0, description="Количество режущих граней")

    @model_validator(mode="before")
    def check_group(cls, values):
        if 'group' in values and values['group'] != "Зенкер":
            raise ValueError(f"Нельзя менять группу класса '{cls.__class__.__name__}' ({cls.group}). "
                             f"Используйте соответствующий класс")
        return values


class DeploymentCutter(DrillingCutter):
    """ Развертка

    Parameters:
        group : (str is GROUPS_TOOL) : группа инструмента.
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
        dia_mm : (float >= 0) : диаметр инструмента.
        length_mm : (float >= 0) : длина инструмента.
        mat_of_cutting_part : (str, int is MATERIALS_OF_CUTTING_PART) : материал режущей пластины.
        main_angle_grad : (float >= 0) : главный угол в плане.
        front_angle_grad  : (float >= 0) : передний угол.
        inclination_of_main_blade_grad  : (float >= 0) : наклон передней грани.
        tolerance : (str, int содержит по одному из ACCURACY_STANDARDS, TOLERANCE_FIELDS) : допуск.
        num_of_cutting_blades : (int >= 0) : количество режущих граней.
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.
        quantity : (int >= 0) : количество одновременно работающих инструментов.

    Properties:
        name : (str) : возвращает название инструмента.
        gabarit_volume : (float) : возвращает габаритный объем.
        gabarit_str : (str) : возвращает габарит, записанный строкой.
        type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.
    """
    group: InGroupsTool = Field(default="Развертка", description="Группа инструмента")
    num_of_cutting_blades: int = Field(default=8, ge=0, description="Количество режущих граней")

    @model_validator(mode="before")
    def check_group(cls, values):
        if 'group' in values and values['group'] != "Развертка":
            raise ValueError(f"Нельзя менять группу класса '{cls.__class__.__name__}' ({cls.group}). "
                             f"Используйте соответствующий класс")
        return values


class MillingCutter(DrillingCutter):
    """ Управляет полями класса "Фреза".

    Parameters:
        group : (str is GROUPS_TOOL) : группа инструмента.
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
        dia_mm : (float >= 0) : диаметр инструмента.
        length_mm : (float >= 0) : длина инструмента.
        mat_of_cutting_part : (str, int in MATERIALS_OF_CUTTING_PART) : материал режущей пластины.
        main_angle_grad : (float >= 0) : главный угол в плане.
        front_angle_grad  : (float >= 0) : передний угол.
        inclination_of_main_blade_grad  : (float >= 0) : наклон передней грани.
        tolerance : (str, int содержит по одному из ACCURACY_STANDARDS, TOLERANCE_FIELDS) : допуск.
        type_cutter : (str, int, float in TYPES_OF_MILLING_CUTTER) : Тип инструмента:
        type_of_cutting_part : (str, int, float in TYPES_OF_CUTTING_PART) : тип режущей части.
        large_tooth : (str, int, float in TYPES_OF_LARGE_TOOTH) :  Крупный/мелкий зуб.
        num_of_cutting_blades : (int >= 0) : количество режущих граней.
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.
        quantity : (int >= 0) : количество одновременно работающих инструментов.
        accuracy_class : (str, int in ACCURACY_CLASS_STANDARDS) : класс точности инструмента.
        cutter_number : (Optional[str]) : номер фрезы ("1", "1 1/2", и т.д.).
        module : (Optional[float] >= 0) : модуль червячной фрезы.

    Properties:
        name : (str) : возвращает название инструмента.
        gabarit_volume : (float) : возвращает габаритный объем.
        gabarit_str : (str) : возвращает габарит, записанный строкой.
        type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.
    """

    group: InGroupsTool = Field(default="Фреза", description="Группа инструмента")
    type_cutter: InTypesOfMillingCutter = Field(default="Цилиндрическая", description="Тип инструмента")
    type_of_cutting_part: InTypesOfCuttingPart = Field(default="Цельная", description="Тип режущей части")
    large_tooth: InTypesOfLargeTooth = Field(default="Крупный шаг", description="Крупный/мелкий зуб")
    num_of_cutting_blades: int = Field(default=12, ge=0, description="Количество режущих граней")
    accuracy_class: Optional[InAccuracyClassStandards] = Field(default=None, description="Класс точности инструмента")
    cutter_number: Optional[StringValue] = Field(default=None, description="Номер фрезы")
    module: Optional[float] = Field(default=None, ge=0, description="Модуль червячной фрезы")

    @model_validator(mode="before")
    def check_group(cls, values):
        if 'group' in values and values['group'] != "Фреза":
            raise ValueError(f"Нельзя менять группу класса '{cls.__class__.__name__}' ({cls.group}). "
                             f"Используйте соответствующий класс")
        return values

    def _parameters(self):
        tool_parameters = Tool._parameters(self)
        size_parameters = AxialSizes._parameters(self)
        blade_material_parameters = BladeMaterial._parameters(self)
        angles_parameters = Angles._parameters(self)
        tolerance_parameters = Tolerance._parameters(self)
        return tool_parameters | size_parameters | blade_material_parameters | angles_parameters | \
            tolerance_parameters | {
               "type_cutter": self.type_cutter,
               "type_of_cutting_part": self.type_of_cutting_part,
               "large_tooth": self.large_tooth,
               "num_of_cutting_blades": self.num_of_cutting_blades,
               "accuracy_class": self.accuracy_class,
               "cutter_number": self.cutter_number,
               "module": self.module
               }


class TurningCutter(Tolerance, Angles, BladeMaterial, PrismaticSizes, Tool):
    """ Резец

    parameters:
        group : (str is GROUPS_TOOL) : группа инструмента.
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
        length_mm : (float >= 0) : длина инструмента.
        width_mm : (float >= 0) : ширина инструмента.
        height_mm : (float >= 0) : высота инструмента.
        mat_of_cutting_part : (str, int is MATERIALS_OF_CUTTING_PART) : материал режущей пластины.
        main_angle_grad : (float >= 0) : главный угол в плане.
        front_angle_grad  : (float >= 0) : передний угол.
        inclination_of_main_blade_grad  : (float >= 0) : наклон передней грани
        radius_of_cutting_vertex : (float >= 0) : радиус режущей вершины.
        quantity : (int >= 0) : количество одновременно работающих инструментов.
        turret : (int, str in TYPES_OF_TOOL_HOLDER) :  Наличие револьверной головки.
        load : (int, str in TYPES_OF_TOOL_HOLDER) : Нагрузка на резец.
        is_complex_profile : (Optional[bool]) : Показатель наличия глубокого или сложного профиля. По умолчанию: None.

    Properties:
        name : (str) : возвращает название инструмента.
        gabarit_volume : (float) : возвращает габаритный объем.
        gabarit_str : (str) : возвращает габарит, записанный строкой.
        type_of_mat  : (int) : тип материала режущей пластины: 0-быстрорез; 1-твердый сплав.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.

    """
    group: InGroupsTool = Field(default="Резец", description="Группа инструмента")

    @model_validator(mode="before")
    def check_group(cls, values):
        if 'group' in values and values['group'] != "Резец":
            raise ValueError(f"Нельзя менять группу класса '{cls.__class__.__name__}' ({cls.group}). "
                             f"Используйте соответствующий класс")
        return values

    def _parameters(self):
        tool_parameters = Tool._parameters(self)
        size_parameters = PrismaticSizes._parameters(self)
        blade_material_parameters = BladeMaterial._parameters(self)
        angles_parameters = Angles._parameters(self)
        tolerance_parameters = Tolerance._parameters(self)
        return tool_parameters | size_parameters | blade_material_parameters | angles_parameters | \
            tolerance_parameters


class BroachingCutter(CustomTool):
    """ Протяжка

    Parameters:
        group : (str is GROUPS_TOOL) : группа инструмента.
        marking : (str) : обозначение инструмента.
        standard : (str contains one of TYPES_STANDARD) : стандарт инструмента.
        angle_of_inclination: (float) : Угол наклона зубьев протяжки.
        pitch_of_teeth: (float >= 0) : Шаг зубьев протяжки.
        number_teeth_section: (int >= 0) : Число зубьев секции протяжки.
        difference: (float >= 0) : Подача на зуб протяжки (размерный перепад между соседними зубьями).
        length_of_working_part: (float >= 0) : Длина режущей части протяжки.

    Properties:
        name : (str) : возвращает название инструмента.

    Methods:
        parameters : (dict) : возвращает словарь параметров и свойств.
    """
    group: InGroupsTool = Field(default="Протяжка", description="Группа инструмента")
    marking: MarkingForSpecialTool = Field(default='специальная', description="Обозначение инструмента")
    angle_of_inclination: float = Field(default=0.0, description="Угол наклона зубьев протяжки")
    pitch_of_teeth: float = Field(default=0.0, ge=0, description="Шаг зубьев протяжки")
    number_teeth_section: int = Field(default=0, ge=0, description="Число зубьев секции протяжки")
    difference: float = Field(default=0.0, ge=0, description="Подача на зуб протяжки")
    length_of_working_part: float = Field(default=0.0, ge=0, description="Длина режущей части протяжки")

    @model_validator(mode="before")
    def check_group(cls, values):
        if 'group' in values and values['group'] != "Протяжка":
            raise ValueError(f"Нельзя менять группу класса '{cls.__class__.__name__}' ({cls.group}). "
                             f"Используйте соответствующий класс")
        return values

    def _parameters(self):
        tool_parameter = Tool._parameters(self)
        return tool_parameter | {"angle_of_inclination": self.angle_of_inclination,
                                 "pitch_of_teeth": self.pitch_of_teeth,
                                 "number_teeth_section": self.number_teeth_section,
                                 "difference": self.difference,
                                 "length_of_working_part": self.length_of_working_part
                                 }


if __name__ == '__main__':
    tool = DrillingCutter()
    # print(tool.group)
    # tool.group = 1
    #
    # tool.marking = "Специальная"
    # tool.standard = "ГОСТ ХХХ-ХХ"

    # tool.dia_mm = 100
    tool.tolerance = 'H8'

    print(tool.name)
    print(tool.parameters)
    print(tool.length_mm)
    print(tool.gabarit_str)
    print(tool.dict())
    tool.type_cutter = "Торцовая"
    print(tool.parameters)
