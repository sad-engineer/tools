# `cutting_tools`

`cutting_tools` - модуль работы с базой данных инструментов.
---
---
Поддерживаемые функции:
	
	Получение таблицы инструментов по критериям отбора (в формате DataFrame()):
		table_cutting_tools = cutting_tools.by_dia_and_type(dia=any_dia)
		
		table_cutting_tools = cutting_tools.by_dia_and_type(dia_out=any_dia_out)
		
		table_cutting_tools = cutting_tools.by_dia_and_type(
								dia=any_dia,
								type_tool=any_type)
		
		table_cutting_tools = cutting_tools.by_dia_and_type(
								dia_out=any_dia_out,
								type_tool=any_type)
		
		table_cutting_tools = cutting_tools.by_dia_and_type(type_tool=any_type)

	Получение параметров инструмента по наименованию (в формате словаря):
		param = cutting_tools.by_marking(marking="any")

	Получение полной таблицы инструментов (в формате DataFrame()):
		table_cutting_tools = cutting_tools.full_table()

	Словарь наименований материалов режущей части с доступом по индексу:
		NAMES_OF_MATERIALS_OF_CUTTING_PART
    Словарь индексов материалов режущей части с доступом по наименованию:
		NAMES_OF_MATERIALS_OF_CUTTING_PART

---