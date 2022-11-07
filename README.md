# `cutting_tools`

`cutting_tools` - модуль работы с базой данных инструментов.
---
---
Поддерждиваемые функции:
	
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

	#Загрузка инструментов из таблицы эксель.

---