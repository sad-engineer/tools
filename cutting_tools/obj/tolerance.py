#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import re
from typing import Optional, Union

from cutting_tools.obj.interfaces import IAccuracy, IToleranceField
from cutting_tools.obj.exceptions import InvalidValue


class Tolerance(IAccuracy, IToleranceField):
    """ДатаКласс 'Допуск'. Хранит поля и свойства для работы с допуском

    Parameters:
        accuracy : (str, int is ACCURACY_STANDARDS) : квалитет.
        tolerance_field : (str, int is TOLERANCE_FIELDS) : поле допуска.
        tolerance : (str, int содержит по одному из ACCURACY_STANDARDS, TOLERANCE_FIELDS) : допуск.

    Сostants:
        ACCURACY_STANDARDS : Квалитеты точности обработки.
        TOLERANCE_FIELDS : Поля допусков.
    """
    def __init__(self,
                 tolerance: Optional[str] = None,
                 accuracy: Optional[Union[str, int, float]] = None,
                 tolerance_field: Optional[str] = None,
                 ):
        if isinstance(tolerance, type(None)):
            IToleranceField.__init__(self, tolerance_field)
            IAccuracy.__init__(self, accuracy)
            self._tolerance = None
        elif not isinstance(tolerance, type(None)):
            self.tolerance = tolerance
        else:
            raise InvalidValue("Допуск не задан.")

    @property
    def tolerance(self) -> str:
        return "".join([str(self._tolerance_field), str(self._accuracy)])

    @tolerance.setter
    def tolerance(self, any_tolerance) -> None:
        self.accuracy = re.findall(r'\d+', any_tolerance)[0]
        self.tolerance_field = any_tolerance.replace(re.findall(r'\d+', any_tolerance)[0], "")

    def _dict_parameters(self) -> dict:
        itolerancefield = IToleranceField._dict_parameters(self)
        iaccuracy = IAccuracy._dict_parameters(self)
        return itolerancefield | iaccuracy | {"tolerance": self.tolerance}


if __name__ == "__main__":
    obj = Tolerance(tolerance_field="K", accuracy="10")
    print(obj.tolerance)
    print(obj.dict_parameters)
    obj = Tolerance(tolerance="h12")
    print(obj.tolerance)
    print(obj.dict_parameters)
    obj = Tolerance("H7")
    print(obj.tolerance)
    print(obj.dict_parameters)
