### **Инструкции по использованию модуля `src.scenario`**

=========================================================================================

Описание:
-------------------------
Модуль `src.scenario` предназначен для автоматизации взаимодействия с поставщиками, используя сценарии, описанные в файлах JSON. Он оптимизирует процесс извлечения и обработки данных о товарах с веб-сайтов поставщиков и синхронизирует эту информацию с базой данных (например, PrestaShop).

Шаги выполнения:
-------------------------
1. **Чтение сценариев**: Модуль загружает сценарии из файлов JSON, содержащих информацию о товарах и URL-адреса на веб-сайте поставщика.
2. **Взаимодействие с веб-сайтами**: Обрабатывает URL-адреса из сценариев для извлечения данных о товарах.
3. **Обработка данных**: Преобразует извлеченные данные в формат, подходящий для базы данных, и сохраняет их.
4. **Логирование выполнения**: Ведет журналы с деталями выполнения сценариев и результатами для отслеживания прогресса и выявления ошибок.

Пример использования:
-------------------------

```python
from src.scenario import run_scenario_files
from src.core import Settings  # Предполагается, что Settings определен в src.core

# Создаем экземпляр настроек (пример)
settings = Settings()
settings.db_host = "localhost"
settings.db_name = "prestashop_db"
settings.db_user = "user"
settings.db_password = "password"

# Список файлов сценариев для выполнения
scenario_files = ["scenarios/scenario_file_1.json", "scenarios/scenario_file_2.json"]

# Запускаем выполнение сценариев
run_scenario_files(settings, scenario_files)
```

Как использовать `run_scenario_files(s, scenario_files_list)`
=========================================================================================

Описание
-------------------------
Функция `run_scenario_files` принимает список файлов сценариев и выполняет их последовательно, вызывая функцию `run_scenario_file` для каждого файла.

Шаги выполнения
-------------------------
1. Функция получает список файлов сценариев (`scenario_files_list`).
2. Для каждого файла в списке вызывается функция `run_scenario_file`, которая загружает и выполняет сценарии из этого файла.
3. Если файл не найден, возникает исключение `FileNotFoundError`.
4. Если файл содержит неверный JSON, возникает исключение `JSONDecodeError`.

Пример использования
-------------------------

```python
from src.scenario import run_scenario_files
from src.core import Settings  # Предполагается, что Settings определен в src.core

# Создаем экземпляр настроек (пример)
settings = Settings()
settings.db_host = "localhost"
settings.db_name = "prestashop_db"
settings.db_user = "user"
settings.db_password = "password"

# Список файлов сценариев для выполнения
scenario_files = ["scenarios/scenario_file_1.json", "scenarios/scenario_file_2.json"]

# Запускаем выполнение сценариев
run_scenario_files(settings, scenario_files)
```

Как использовать `run_scenario_file(s, scenario_file)`
=========================================================================================

Описание
-------------------------
Функция `run_scenario_file` загружает сценарии из указанного файла и вызывает `run_scenario` для каждого сценария в файле.

Шаги выполнения
-------------------------
1. Функция принимает путь к файлу сценариев (`scenario_file`).
2. Загружает сценарии из файла.
3. Для каждого сценария в файле вызывается функция `run_scenario`, которая обрабатывает отдельный сценарий.
4. Если файл не найден, возникает исключение `FileNotFoundError`.
5. Если файл содержит неверный JSON, возникает исключение `JSONDecodeError`.

Пример использования
-------------------------

```python
from src.scenario import run_scenario_file
from src.core import Settings  # Предполагается, что Settings определен в src.core

# Создаем экземпляр настроек (пример)
settings = Settings()
settings.db_host = "localhost"
settings.db_name = "prestashop_db"
settings.db_user = "user"
settings.db_password = "password"

# Путь к файлу сценариев
scenario_file = "scenarios/scenario_file_1.json"

# Запускаем выполнение сценариев из файла
run_scenario_file(settings, scenario_file)
```

Как использовать `run_scenario(s, scenario)`
=========================================================================================

Описание
-------------------------
Функция `run_scenario` обрабатывает отдельный сценарий, переходя по URL-адресу, извлекая данные о товаре и сохраняя их в базу данных.

Шаги выполнения
-------------------------
1. Функция принимает объект настроек (`s`) и словарь, содержащий сценарий (`scenario`).
2. Извлекает URL-адрес из сценария.
3. Переходит по URL-адресу.
4. Извлекает данные о товаре со страницы.
5. Сохраняет данные о товаре в базе данных.
6. Если возникают проблемы с запросом к веб-сайту, возникает исключение `requests.exceptions.RequestException`.

Пример использования
-------------------------

```python
from src.scenario import run_scenario
from src.core import Settings  # Предполагается, что Settings определен в src.core

# Создаем экземпляр настроек (пример)
settings = Settings()
settings.db_host = "localhost"
settings.db_name = "prestashop_db"
settings.db_user = "user"
settings.db_password = "password"

# Пример сценария
scenario = {
    "url": "https://example.com/product/123",
    "name": "Sample Product",
    "presta_categories": {
        "default_category": 12345,
        "additional_categories": [12346, 12347]
    }
}

# Запускаем выполнение сценария
run_scenario(settings, scenario)
```

Как использовать `dump_journal(s, journal)`
=========================================================================================

Описание
-------------------------
Функция `dump_journal` сохраняет журнал выполнения в файл для последующего анализа.

Шаги выполнения
-------------------------
1. Функция принимает объект настроек (`s`) и список записей журнала (`journal`).
2. Сохраняет журнал в файл.
3. Если возникают проблемы при записи в файл, возникает исключение `Exception`.

Пример использования
-------------------------

```python
from src.scenario import dump_journal
from src.core import Settings  # Предполагается, что Settings определен в src.core

# Создаем экземпляр настроек (пример)
settings = Settings()

# Пример журнала
journal = [
    {"scenario": "scenario_1", "status": "success", "message": "Product added"},
    {"scenario": "scenario_2", "status": "failure", "message": "Failed to add product"}
]

# Сохраняем журнал
dump_journal(settings, journal)
```

Как использовать `main()`
=========================================================================================

Описание
-------------------------
Функция `main` является основной функцией для запуска модуля.

Шаги выполнения
-------------------------
1. Функция `main` запускает модуль.
2. Обрабатывает любые критические ошибки во время выполнения.

Пример использования
-------------------------

```python
from src.scenario import main

# Запускаем модуль
if __name__ == "__main__":
    main()
```