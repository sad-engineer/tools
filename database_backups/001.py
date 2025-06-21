import csv
import sqlite3

# Подключение к базе
conn = sqlite3.connect('E:\\Documents\\Программирование\\tools\\tools_old\\data\\tools.db')
cursor = conn.cursor()

# Запрос к нужной таблице
cursor.execute("SELECT * FROM tools")
rows = cursor.fetchall()

# Получение названий столбцов
columns = [description[0] for description in cursor.description]

# Сохранение в CSV
with open('tools_old.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(columns)  # заголовки
    writer.writerows(rows)

conn.close()
