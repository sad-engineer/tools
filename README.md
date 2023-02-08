# `cutting_tools`

`cutting_tools` - модуль работы с базой данных инструментов.
---
---
Поддерживаемые константы:

    Словарь параметров инструментов по умолчанию (key - тип инструмента, например: "Резец"):
        tools.DEFAULT_SETTINGS_FOR_TOOL[any_type_tool]

    Словарь индексов материалов режущей части:
        tools.MATERIALS_OF_CUTTING_PART
    
    Словарь наименований группы инструмента
        tools.GROUPS_TOOL

    Типы стандартов инструмента
        tools.TYPES_STANDARD

    Типы фрез:
        tools.TYPES_OF_MILLING_CUTTER

    Типы режущей части фрезы:
        tools.TYPES_OF_CUTTING_PART_OF_MILLING_CUTTER

    Типы частоты шага:
        tools.TYPES_OF_LARGE_TOOTH
    
    Типы установки резца:
        tools.TYPES_OF_TOOL_HOLDER

    Типы нагрузок на резец:
        tools.TYPES_OF_LOADS 

    Квалитеты точности обработки:
        tools.ACCURACY_STANDARDS

    Поля допусков:
        tools.TOLERANCE_FIELDS

    Классы точности инструмента:
        tools.ACCURACY_CLASS_STANDARDS

    Описание переменных классов:
        tools.DECODING
---
Поддерживаемые классы (основные):	
    
    Контейнер поддерживаемых классов:
        container = tools.ToolContainer()
    
    Класс "Фреза":
        из контейнера (с настройками по умолчанию):
            cutter = container.milling_cutter()
        из пакета (необходимо задать начальные настройки):
            cutter = tools.MillingCutter(marking = any_marking, standard = any_standard, dia_mm = any_dia,
                length_mm = any_length, mat_of_cutting_part = any_mat_of_cutting_part, 
                main_angle_grad = any_main_angle_grad, front_angle_grad = any_front_angle_grad, 
                inclination_of_main_blade_grad = any_inclination_of_main_blade_grad, tolerance = any_tolerance, 
                type_cutter = any_type_cutter, type_of_cutting_part = any_type_of_cutting_part, 
                num_of_cutting_blades = any_num_of_cutting_blades, 
                radius_of_cutting_vertex = any_radius_of_cutting_vertex, large_tooth = any_large_tooth, 
                quantity = any_quantity, accuracy_class = any_accuracy_class, number = any_number, 
                module = any_module)
        
    Класс "Резец":
        из контейнера (с настройками по умолчанию):
            cutter = container.turning_cutter()
        из пакета (необходимо задать начальные настройки):
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
        из контейнера (с настройками по умолчанию):
            cutter = container.drilling_cutter()
        из пакета (необходимо задать начальные настройки):
            cutter = cutting_tools.DrillingCutter(marking = any_marking, standard = any_standard, dia_mm = any_dia,
                length_mm = any_length, mat_of_cutting_part = any_mat_of_cutting_part, 
                main_angle_grad = any_main_angle_grad, front_angle_grad = any_front_angle_grad, 
                inclination_of_main_blade_grad = any_inclination_of_main_blade_grad, tolerance = any_tolerance, 
                type_cutter = any_type_cutter, type_of_cutting_part = any_type_of_cutting_part, 
                num_of_cutting_blades = any_num_of_cutting_blades, 
                radius_of_cutting_vertex = any_radius_of_cutting_vertex, quantity = any_quantity)

    Класс "Зенкер":
        из контейнера (с настройками по умолчанию):
            cutter = container.countersinking_cutter()
        из пакета (необходимо задать начальные настройки):
            cutter = cutting_tools.CountersinkingCutter(marking = any_marking, standard = any_standard, dia_mm = any_dia,
                length_mm = any_length, mat_of_cutting_part = any_mat_of_cutting_part, 
                main_angle_grad = any_main_angle_grad, front_angle_grad = any_front_angle_grad, 
                inclination_of_main_blade_grad = any_inclination_of_main_blade_grad, tolerance = any_tolerance, 
                type_cutter = any_type_cutter, type_of_cutting_part = any_type_of_cutting_part, 
                num_of_cutting_blades = any_num_of_cutting_blades, 
                radius_of_cutting_vertex = any_radius_of_cutting_vertex, quantity = any_quantity)

    Класс "Развертка":
        из контейнера (с настройками по умолчанию):
            cutter = container.deployment_cutter()
        из пакета (необходимо задать начальные настройки):
            cutter = cutting_tools.DeploymentCutter(marking = any_marking, standard = any_standard, dia_mm = any_dia,
                length_mm = any_length, mat_of_cutting_part = any_mat_of_cutting_part, 
                main_angle_grad = any_main_angle_grad, front_angle_grad = any_front_angle_grad, 
                inclination_of_main_blade_grad = any_inclination_of_main_blade_grad, tolerance = any_tolerance, 
                type_cutter = any_type_cutter, type_of_cutting_part = any_type_of_cutting_part, 
                num_of_cutting_blades = any_num_of_cutting_blades, 
                radius_of_cutting_vertex = any_radius_of_cutting_vertex, quantity = any_quantity)
    
    Класс "Протяжка":
        из контейнера (с настройками по умолчанию):
            cutter = container.broaching_cutter()
        из пакета (необходимо задать начальные настройки):
            cutter = container.DeploymentCutter(marking=any_marking, standard=any_standard, angle_of_inclination=any_angle, 
            pitch_of_teeth=any_pitch, number_teeth_section=any_number, difference=any_difference, 
            length_of_working_part=any_length, 

    для основных классов досупны:
        документация:
            print(cutter.__doc__)

        словарь параметров и свойств:
            params = cutter.dict_parameters

---