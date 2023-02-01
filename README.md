# `cutting_tools`

`cutting_tools` - модуль работы с базой данных инструментов.
---
---
Поддерживаемые константы:

    Список материалов по умолчанию (key - тип обработки):
        cutting_tools.DEFAULT_SETTINGS_FOR_CUTTING_TOOL[any_index]


    Словарь индексов материалов режущей части:
        cutting_tools.MATERIALS_OF_CUTTING_PART
    
    Словарь наименований группы инструмента
        cutting_tools.GROUPS_TOOL

    Типы стандартов инструмента
        cutting_tools.TYPES_STANDARD

    Типы фрез:
        cutting_tools.TYPES_OF_MILLING_CUTTER

    Типы режущей части фрезы:
        cutting_tools.TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER

    Типы частоты шага:
        cutting_tools.TYPES_OF_LARGE_TOOTH
    
    Типы установки резца:
        cutting_tools.TYPES_OF_TOOL_HOLDER

    Типы нагрузок на резец:
        cutting_tools.TYPES_OF_LOADS 

    Квалитеты точности обработки:
        cutting_tools.ACCURACY_STANDARDS

    Поля допусков:
        cutting_tools.TOLERANCE_FIELDS

    Классы точности инструмента:
        cutting_tools.ACCURACY_CLASS_STANDARDS

    Описание переменных классов:
        cutting_tools.DECODING
---
Поддерживаемые классы (основные):	
    
    Класс "Фреза":
        cutter = cutting_tools.MillingCutter(marking = any_marking, standard = any_standard, dia_mm = any_dia,
            length_mm = any_length, mat_of_cutting_part = any_mat_of_cutting_part, 
            main_angle_grad = any_main_angle_grad, front_angle_grad = any_front_angle_grad, 
            inclination_of_main_blade_grad = any_inclination_of_main_blade_grad, tolerance = any_tolerance, 
            type_cutter = any_type_cutter, type_of_cutting_part = any_type_of_cutting_part, 
            num_of_cutting_blades = any_num_of_cutting_blades, 
            radius_of_cutting_vertex = any_radius_of_cutting_vertex, large_tooth = any_large_tooth, 
            quantity = any_quantity, accuracy_class = any_accuracy_class, number = any_number, 
            module = any_module)
        
    Класс "Резец":
        cutter = cutting_tools.TurningCutter(marking = any_marking, standard = any_standard, 
            length_mm = any_length, width_mm = any_width, height_mm = any_height, 
            mat_of_cutting_part = any_mat_of_cutting_part, 
            main_angle_grad = any_main_angle_grad, front_angle_grad = any_front_angle_grad, 
            inclination_of_main_blade_grad = any_inclination_of_main_blade_grad, tolerance = any_tolerance, 
            type_cutter = any_type_cutter, type_of_cutting_part = any_type_of_cutting_part, 
            num_of_cutting_blades = any_num_of_cutting_blades, 
            radius_of_cutting_vertex = any_radius_of_cutting_vertex, large_tooth = any_large_tooth, 
            quantity = any_quantity, turret = any_turret, load = any_load, is_complex_profile = any_profile,)

    Класс "Сверло":
        cutter = cutting_tools.DrillingCutter(marking = any_marking, standard = any_standard, dia_mm = any_dia,
            length_mm = any_length, mat_of_cutting_part = any_mat_of_cutting_part, 
            main_angle_grad = any_main_angle_grad, front_angle_grad = any_front_angle_grad, 
            inclination_of_main_blade_grad = any_inclination_of_main_blade_grad, tolerance = any_tolerance, 
            type_cutter = any_type_cutter, type_of_cutting_part = any_type_of_cutting_part, 
            num_of_cutting_blades = any_num_of_cutting_blades, 
            radius_of_cutting_vertex = any_radius_of_cutting_vertex, quantity = any_quantity)

    Класс "Зенкер":
        cutter = cutting_tools.CountersinkingCutter(marking = any_marking, standard = any_standard, dia_mm = any_dia,
            length_mm = any_length, mat_of_cutting_part = any_mat_of_cutting_part, 
            main_angle_grad = any_main_angle_grad, front_angle_grad = any_front_angle_grad, 
            inclination_of_main_blade_grad = any_inclination_of_main_blade_grad, tolerance = any_tolerance, 
            type_cutter = any_type_cutter, type_of_cutting_part = any_type_of_cutting_part, 
            num_of_cutting_blades = any_num_of_cutting_blades, 
            radius_of_cutting_vertex = any_radius_of_cutting_vertex, quantity = any_quantity)

    Класс "Развертка":
        cutter = cutting_tools.DeploymentCutter(marking = any_marking, standard = any_standard, dia_mm = any_dia,
            length_mm = any_length, mat_of_cutting_part = any_mat_of_cutting_part, 
            main_angle_grad = any_main_angle_grad, front_angle_grad = any_front_angle_grad, 
            inclination_of_main_blade_grad = any_inclination_of_main_blade_grad, tolerance = any_tolerance, 
            type_cutter = any_type_cutter, type_of_cutting_part = any_type_of_cutting_part, 
            num_of_cutting_blades = any_num_of_cutting_blades, 
            radius_of_cutting_vertex = any_radius_of_cutting_vertex, quantity = any_quantity)
    
    для основных классов досупны:
        документация:
            print(cutter.__doc__)

        словарь параметров и свойств:
            params = cutter.dict_parameters

---