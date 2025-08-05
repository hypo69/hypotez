## Как использовать функцию `json2csv`
=========================================================================================

Описание
-------------------------
Функция `json2csv` конвертирует JSON данные в формат CSV. 

Шаги выполнения
-------------------------
1. **Проверка типа входящих данных**: Функция проверяет, является ли входящий параметр `json_data` строкой, списком, словарем или путем к файлу.
2. **Загрузка JSON данных**:
    - Если `json_data` - строка, функция преобразует ее в список словарей с помощью `json.loads`.
    - Если `json_data` - список, функция принимает его как есть.
    - Если `json_data` - словарь, функция создает список из этого словаря.
    - Если `json_data` - путь к файлу, функция читает JSON данные из файла с помощью `open` и `json.load`.
3. **Сохранение в CSV**: Функция вызывает функцию `save_csv_file` для сохранения данных в CSV файл с указанным путем `csv_file_path`.

Пример использования
-------------------------

```python
from src.utils.convertors.json import json2csv

# Пример 1: JSON строка
json_data = '{"name": "John Doe", "age": 30}'
csv_file_path = 'example.csv'
success = json2csv(json_data, csv_file_path) 
print(f"CSV file created: {success}") 

# Пример 2: Список словарей
json_data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 35}
]
csv_file_path = 'people.csv'
success = json2csv(json_data, csv_file_path) 
print(f"CSV file created: {success}")

# Пример 3: Путь к JSON файлу
json_file_path = 'data.json'
csv_file_path = 'output.csv'
success = json2csv(json_file_path, csv_file_path) 
print(f"CSV file created: {success}")
```