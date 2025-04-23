### **Инструкции по работе с кодом**

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот модуль предоставляет утилиты для работы с CSV и JSON файлами, включая функции для сохранения данных в CSV файлы, чтения CSV файлов, преобразования CSV в JSON и чтения CSV в различные форматы данных (список словарей, словарь).

Шаги выполнения
-------------------------
1. **Сохранение данных в CSV файл**:
   - Функция `save_csv_file` принимает список словарей, путь к файлу, режим записи (добавление или перезапись) и флаг для логирования ошибок.
   - Функция проверяет входные данные на соответствие типу (список словарей) и непустоту.
   - Функция создаёт все необходимые родительские директории для файла, если они не существуют.
   - Функция открывает файл в указанном режиме и записывает данные, используя `csv.DictWriter`. Если файл новый или открыт в режиме перезаписи, записывается заголовок.

2. **Чтение данных из CSV файла**:
   - Функция `read_csv_file` принимает путь к CSV файлу и флаг для логирования ошибок.
   - Функция открывает CSV файл и читает его содержимое, используя `csv.DictReader`, преобразуя каждую строку в словарь.
   - Функция возвращает список словарей, представляющий содержимое CSV файла.

3. **Преобразование CSV файла в JSON**:
   - Функция `read_csv_as_json` принимает пути к CSV и JSON файлам и флаг для логирования ошибок.
   - Функция читает данные из CSV файла с помощью `read_csv_file`.
   - Функция записывает прочитанные данные в JSON файл с отступами для удобочитаемости.

4. **Чтение CSV файла в словарь**:
   - Функция `read_csv_as_dict` принимает путь к CSV файлу.
   - Функция читает CSV файл, используя `csv.DictReader`, и преобразует его содержимое в словарь, где ключ `"data"` содержит список словарей.

5. **Чтение CSV файла с использованием Pandas**:
   - Функция `read_csv_as_ns` принимает путь к CSV файлу.
   - Функция использует библиотеку `pandas` для чтения CSV файла в DataFrame, а затем преобразует DataFrame в список словарей.

Пример использования
-------------------------

```python
from src.utils.csv import (
    save_csv_file,
    read_csv_file,
    read_csv_as_json,
    read_csv_as_dict,
    read_csv_as_ns,
)
from pathlib import Path

# Пример данных для записи в CSV
data = [
    {"name": "Alice", "age": "30", "city": "New York"},
    {"name": "Bob", "age": "25", "city": "Los Angeles"},
]

# Путь к CSV файлу
csv_file_path = "output.csv"

# Сохранение данных в CSV файл
if save_csv_file(data, csv_file_path, mode="w"):
    print(f"CSV file '{csv_file_path}' was successfully saved.")
else:
    print("Failed to save CSV file.")

# Чтение данных из CSV файла
read_data = read_csv_file(csv_file_path)
if read_data:
    print("Data read from CSV:", read_data)
else:
    print("Failed to read CSV file.")

# Путь к JSON файлу
json_file_path = "output.json"

# Преобразование CSV в JSON
if read_csv_as_json(csv_file_path, json_file_path):
    print(f"CSV file '{csv_file_path}' was successfully converted to JSON '{json_file_path}'.")
else:
    print("Failed to convert CSV to JSON.")

# Чтение CSV в словарь
csv_dict = read_csv_as_dict(csv_file_path)
if csv_dict:
    print("CSV as dictionary:", csv_dict)
else:
    print("Failed to read CSV as dictionary.")

# Чтение CSV с использованием Pandas
csv_ns = read_csv_as_ns(csv_file_path)
if csv_ns:
    print("CSV as list of dictionaries (Pandas):", csv_ns)
else:
    print("Failed to read CSV using Pandas.")