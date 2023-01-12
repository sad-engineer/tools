#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Union
from dataclasses import dataclass
from typing import ClassVar

from cutting_tools.obj.constants import INDEXES_OF_MATERIALS_OF_CUTTING_PART
from cutting_tools.obj.constants import INDEXES_HARD_ALLOYS, INDEXES_HIGH_SPEED_STEELS


@dataclass
class BladeMaterial:
    """ДатаКласс 'Материал лезвия'.

    Parameters:
        mat_of_cutting_part : (str) : группа инструмента.
        type_of_mat  : (int) : тип материала инструмента: 0-быстрорез; 1-твердый сплав.

    Сostants:
        HARD_ALLOYS : перечень доступных твердосплавных материалов
        HIGH_SPEED_STEELS : перечень доступных быстрорежущих материалов
        MATS_OF_CUTTING_PART : перечень доступных материалов режущей части (общий)
    """
    mat_of_cutting_part: Union[str, int] = 'Т15К6'
    HARD_ALLOYS: ClassVar[dict] = INDEXES_HARD_ALLOYS
    HIGH_SPEED_STEELS: ClassVar[dict] = INDEXES_HIGH_SPEED_STEELS
    MATS_OF_CUTTING_PART: ClassVar[dict] = INDEXES_OF_MATERIALS_OF_CUTTING_PART

    def __post_init__(self):
        self.update_mat_of_cutting_part(self.mat_of_cutting_part)

    @property
    def type_of_mat(self):
        return 1 if self.mat_of_cutting_part in self.HARD_ALLOYS else 0

    @property
    def _is_correct_mat_of_cutting_part(self):
        if isinstance(self.mat_of_cutting_part, str):
            return self.mat_of_cutting_part in self.MATS_OF_CUTTING_PART
        return False

    def update_mat_of_cutting_part(self, new_mat_of_cutting_part):
        self.mat_of_cutting_part = new_mat_of_cutting_part
        if not self._is_correct_mat_of_cutting_part:
            self.mat_of_cutting_part = list(self.MATS_OF_CUTTING_PART.keys())[3]


# if __name__ == "__main__":
#     a = BladeMaterial("Р18")
#     print(a)
#     print(a.HARD_ALLOYS)
#     print(a.HIGH_SPEED_STEELS)
#     print(a.MATS_OF_CUTTING_PART)
#     print(a.type_of_mat)

