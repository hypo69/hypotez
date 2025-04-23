### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Модуль `jjson` предназначен для работы с JSON-данными: загрузки, сохранения и преобразования. Он включает функции для чтения данных из файлов, строк и объектов, а также для записи данных в файлы в различных режимах. Модуль также поддерживает преобразование данных в объекты `SimpleNamespace` для удобного доступа к ним.

Шаги выполнения
-------------------------
1. **Импорт модуля**: Импортируйте модуль `jjson` в свой проект.
2. **Использование `j_dumps`**: Используйте функцию `j_dumps` для записи JSON-данных в файл или получения их в виде словаря.
3. **Использование `j_loads`**: Используйте функцию `j_loads` для загрузки JSON-данных из файла, строки или объекта.
4. **Использование `j_loads_ns`**: Используйте функцию `j_loads_ns` для загрузки JSON-данных и преобразования их в объекты `SimpleNamespace`.

Пример использования
-------------------------

```python
    from pathlib import Path
    from types import SimpleNamespace
    from src.utils.jjson import j_dumps, j_loads, j_loads_ns

    # Пример использования j_dumps для записи данных в файл
    data = {"name": "Alice", "age": 30}
    file_path = Path("output.json")
    j_dumps(data, file_path=file_path)

    # Пример использования j_loads для чтения данных из файла
    loaded_data = j_loads(file_path)
    print(loaded_data)  # Вывод: {'name': 'Alice', 'age': 30}

    # Пример использования j_dumps для получения данных в виде словаря
    data = {"name": "Bob", "age": 25}
    json_data = j_dumps(data)
    print(json_data)  # Вывод: {'name': 'Bob', 'age': 25}

    # Пример использования j_loads_ns для преобразования данных в SimpleNamespace
    ns_data = j_loads_ns(data)
    print(ns_data.name)  # Вывод: Bob

    # Пример использования j_loads_ns для загрузки данных из файла и преобразования в SimpleNamespace
    ns_data_from_file = j_loads_ns(file_path)
    print(ns_data_from_file.name)  # Вывод: Alice