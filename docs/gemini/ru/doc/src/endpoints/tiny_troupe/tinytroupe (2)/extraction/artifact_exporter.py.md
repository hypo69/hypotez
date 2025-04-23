# Модуль для экспорта артефактов `artifact_exporter.py`

## Обзор

Модуль `artifact_exporter.py` предоставляет функциональность для экспорта артефактов, созданных в процессе работы с TinyTroupe. Он позволяет сохранять данные в различных форматах, таких как JSON, TXT и DOCX, обеспечивая гибкость при создании синтетических данных на основе симуляций.

## Подробнее

Этот модуль содержит класс `ArtifactExporter`, который управляет процессом экспорта артефактов. Он принимает базовую папку для вывода файлов и предоставляет метод `export` для сохранения данных в нужном формате. Модуль также включает вспомогательные методы для экспорта в конкретные форматы и для формирования пути к файлу.

## Классы

### `ArtifactExporter`

**Описание**: Класс `ArtifactExporter` отвечает за экспорт артефактов из элементов TinyTroupe.

**Атрибуты**:
- `base_output_folder` (str): Базовая папка для сохранения экспортированных артефактов.

**Методы**:
- `__init__(self, base_output_folder: str) -> None`: Конструктор класса.
- `export(self, artifact_name: str, artifact_data: Union[dict, str], content_type: str, content_format: str = None, target_format: str = "txt", verbose: bool = False)`: Экспортирует данные артефакта в файл.
- `_export_as_txt(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False)`: Экспортирует данные артефакта в текстовый файл.
- `_export_as_json(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False)`: Экспортирует данные артефакта в JSON файл.
- `_export_as_docx(self, artifact_file_path: str, artifact_data: Union[dict, str], content_original_format: str, verbose: bool = False)`: Экспортирует данные артефакта в файл DOCX.
- `_compose_filepath(self, artifact_data: Union[dict, str], artifact_name: str, content_type: str, target_format: str = None, verbose: bool = False)`: Формирует путь к файлу для экспортируемого артефакта.

### `__init__`
```python
    def __init__(self, base_output_folder:str) -> None:
        """
        Инициализирует экземпляр класса `ArtifactExporter`.

        Args:
            base_output_folder (str): Путь к базовой папке для вывода артефактов.
        """
```
### `export`

```python
    def export(self, artifact_name:str, artifact_data:Union[dict, str], content_type:str, content_format:str=None, target_format:str="txt", verbose:bool=False):
        """
        Экспортирует указанные данные артефакта в файл.

        Args:
            artifact_name (str): Имя артефакта.
            artifact_data (Union[dict, str]): Данные для экспорта. Если указан словарь, он будет сохранен как JSON.
                Если указана строка, она будет сохранена как есть.
            content_type (str): Тип контента в артефакте.
            content_format (str, optional): Формат контента в артефакте (например, md, csv и т.д.). По умолчанию `None`.
            target_format (str): Формат для экспорта артефакта (например, json, txt, docx и т.д.).
            verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.

        Raises:
            ValueError: Если `artifact_data` не является строкой или словарем.
            ValueError: Если `target_format` не поддерживается.

        Как работает функция:
        - Проверяет тип входных данных `artifact_data` и, если это строка или словарь, приводит текст к единообразному виду с помощью функции `utils.dedent()`.
        - Очищает имя артефакта `artifact_name` от недопустимых символов, заменяя их дефисами.
        - Формирует путь к файлу артефакта с помощью метода `_compose_filepath()`.
        - В зависимости от значения `target_format` вызывает соответствующий метод для экспорта данных в нужном формате: `_export_as_json()`, `_export_as_txt()` или `_export_as_docx()`.
        - Если `target_format` не поддерживается, вызывает исключение `ValueError`.

        Примеры:
            Пример экспорта в JSON:
            ```python
            exporter = ArtifactExporter("output")
            data = {"key": "value"}
            exporter.export("my_artifact", data, "config", target_format="json")
            ```

            Пример экспорта в TXT:
            ```python
            exporter = ArtifactExporter("output")
            text = "Hello, world!"
            exporter.export("my_artifact", text, "log", target_format="txt")
            ```

            Пример экспорта в DOCX:
            ```python
            exporter = ArtifactExporter("output")
            text = "# Заголовок\nПривет, мир!"
            exporter.export("my_artifact", {"content": text}, "report", content_format="md", target_format="docx")
            ```
        """
        
```

### `_export_as_txt`

```python
    def _export_as_txt(self, artifact_file_path:str, artifact_data:Union[dict, str], content_type:str, verbose:bool=False):
        """
        Экспортирует указанные данные артефакта в текстовый файл.
        
        Args:
            artifact_file_path (str): Путь к файлу для экспорта.
            artifact_data (Union[dict, str]): Данные для экспорта. Если указан словарь, берется значение ключа 'content'.
            content_type (str): Тип контента в артефакте.
            verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.
        
        Как работает функция:
        - Открывает файл по указанному пути `artifact_file_path` в режиме записи с кодировкой UTF-8.
        - Если `artifact_data` является словарем, извлекает содержимое из ключа `content`. В противном случае использует `artifact_data` как содержимое.
        - Записывает содержимое в файл.
        
        Примеры:
            Пример экспорта текста:
            ```python
            exporter = ArtifactExporter("output")
            exporter._export_as_txt("output/my_artifact.txt", "Hello, world!", "log")
            ```
            
            Пример экспорта текста из словаря:
            ```python
            exporter = ArtifactExporter("output")
            data = {"content": "Hello, world!"}
            exporter._export_as_txt("output/my_artifact.txt", data, "log")
            ```
        """
```

### `_export_as_json`

```python
    def _export_as_json(self, artifact_file_path:str, artifact_data:Union[dict, str], content_type:str, verbose:bool=False):
        """
        Экспортирует указанные данные артефакта в JSON файл.
        
        Args:
            artifact_file_path (str): Путь к файлу для экспорта.
            artifact_data (Union[dict, str]): Данные для экспорта. Должны быть словарем.
            content_type (str): Тип контента в артефакте.
            verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.
        
        Raises:
            ValueError: Если `artifact_data` не является словарем.
        
        Как работает функция:
        - Открывает файл по указанному пути `artifact_file_path` в режиме записи с кодировкой UTF-8.
        - Если `artifact_data` является словарем, преобразует его в JSON-формат с отступами и записывает в файл.
        - Если `artifact_data` не является словарем, вызывает исключение `ValueError`.
        
        Примеры:
            Пример экспорта словаря в JSON:
            ```python
            exporter = ArtifactExporter("output")
            data = {"key": "value"}
            exporter._export_as_json("output/my_artifact.json", data, "config")
            ```
            
            Пример вызова ошибки при попытке экспорта строки в JSON:
            ```python
            exporter = ArtifactExporter("output")
            try:
                exporter._export_as_json("output/my_artifact.json", "Hello, world!", "config")
            except ValueError as ex:
                print(f"Ошибка: {ex}")
            ```
        """
```

### `_export_as_docx`

```python
    def _export_as_docx(self, artifact_file_path:str, artifact_data:Union[dict, str], content_original_format:str, verbose:bool=False):
        """
        Экспортирует указанные данные артефакта в файл DOCX.
        
        Args:
            artifact_file_path (str): Путь к файлу для экспорта.
            artifact_data (Union[dict, str]): Данные для экспорта. Если указан словарь, берется значение ключа 'content'.
            content_original_format (str): Исходный формат контента (например, 'text', 'markdown').
            verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.
        
        Raises:
            ValueError: Если `content_original_format` не поддерживается.
        
        Как работает функция:
        - Проверяет, что `content_original_format` является одним из поддерживаемых форматов ('text', 'txt', 'markdown', 'md').
        - Нормализует значение `content_original_format`, приводя 'md' к 'markdown'.
        - Извлекает содержимое для экспорта: если `artifact_data` является словарем, берет значение из ключа 'content', иначе использует `artifact_data` как содержимое.
        - Преобразует содержимое в HTML с использованием библиотеки `markdown`.
        - Использует `pypandoc` для конвертации HTML-контента в DOCX-файл и сохранения по указанному пути `artifact_file_path`.
        
        Примеры:
            Пример экспорта markdown в DOCX:
            ```python
            exporter = ArtifactExporter("output")
            data = {"content": "# Заголовок\nПривет, мир!"}
            exporter._export_as_docx("output/my_artifact.docx", data, "markdown")
            ```
            
            Пример экспорта текста в DOCX:
            ```python
            exporter = ArtifactExporter("output")
            exporter._export_as_docx("output/my_artifact.docx", "Hello, world!", "text")
            ```
            
            Пример вызова ошибки при неподдерживаемом формате:
            ```python
            exporter = ArtifactExporter("output")
            try:
                exporter._export_as_docx("output/my_artifact.docx", "Hello, world!", "xml")
            except ValueError as ex:
                print(f"Ошибка: {ex}")
            ```
        """
```

### `_compose_filepath`

```python
    def _compose_filepath(self, artifact_data:Union[dict, str], artifact_name:str, content_type:str, target_format:str=None, verbose:bool=False):
        """
        Формирует путь к файлу для экспортируемого артефакта.
        
        Args:
            artifact_data (Union[dict, str]): Данные для экспорта.
            artifact_name (str): Имя артефакта.
            content_type (str): Тип контента в артефакте.
            target_format (str, optional): Формат для экспорта артефакта (например, json, txt, docx и т.д.). По умолчанию `None`.
            verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.
        
        Как работает функция:
        - Определяет расширение файла на основе `target_format`. Если `target_format` указан, используется он. Если `target_format` не указан и `artifact_data` является строкой, используется расширение "txt".
        - Определяет подпапку на основе `content_type`. Если `content_type` не указан, подпапка остается пустой.
        - Формирует полный путь к файлу, объединяя базовую папку вывода, подпапку и имя файла с расширением.
        - Создает промежуточные директории, если они не существуют.
        - Возвращает сформированный путь к файлу.
        
        Примеры:
            Пример формирования пути для JSON-файла:
            ```python
            exporter = ArtifactExporter("output")
            file_path = exporter._compose_filepath({"key": "value"}, "my_artifact", "config", target_format="json")
            print(file_path)  # output/config/my_artifact.json
            ```
            
            Пример формирования пути для TXT-файла:
            ```python
            exporter = ArtifactExporter("output")
            file_path = exporter._compose_filepath("Hello, world!", "my_artifact", "log", target_format="txt")
            print(file_path)  # output/log/my_artifact.txt
            ```
            
            Пример формирования пути без указания типа контента:
            ```python
            exporter = ArtifactExporter("output")
            file_path = exporter._compose_filepath("Hello, world!", "my_artifact", None, target_format="txt")
            print(file_path)  # output/my_artifact.txt
            ```
        """