# Модуль для экспорта артефактов

## Обзор

Модуль `artifact_exporter.py` предназначен для экспорта артефактов, полученных из элементов TinyTroupe, например, для создания синтетических файлов данных из симуляций. Он содержит класс `ArtifactExporter`, который управляет процессом экспорта артефактов в различные форматы, такие как JSON, TXT и DOCX.

## Подробнее

Этот модуль предоставляет функциональность для сохранения данных в различных форматах, что позволяет использовать результаты работы TinyTroupe в различных целях, например, для анализа данных или создания отчетов.

## Классы

### `ArtifactExporter`

**Описание**: Класс `ArtifactExporter` отвечает за экспорт артефактов из TinyTroupe. Он предоставляет методы для экспорта данных в различные форматы файлов, такие как JSON, TXT и DOCX.

**Атрибуты**:
- `base_output_folder` (str): Базовая папка для сохранения экспортируемых артефактов.

**Методы**:
- `__init__(self, base_output_folder: str)`: Конструктор класса, инициализирует базовую папку для вывода.
- `export(self, artifact_name: str, artifact_data: Union[dict, str], content_type: str, content_format: str = None, target_format: str = "txt", verbose: bool = False)`: Экспортирует артефакт в указанный файл.
- `_export_as_txt(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False)`: Экспортирует артефакт в текстовый файл.
- `_export_as_json(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False)`: Экспортирует артефакт в JSON файл.
- `_export_as_docx(self, artifact_file_path: str, artifact_data: Union[dict, str], content_original_format: str, verbose: bool = False)`: Экспортирует артефакт в DOCX файл.
- `_compose_filepath(self, artifact_data: Union[dict, str], artifact_name: str, content_type: str, target_format: str = None, verbose: bool = False)`: Составляет путь к файлу для экспортируемого артефакта.

#### `__init__`

```python
    def __init__(self, base_output_folder: str) -> None:
        """
        Инициализирует экземпляр класса ArtifactExporter.

        Args:
            base_output_folder (str): Базовая папка для сохранения экспортируемых артефактов.
        """
        self.base_output_folder = base_output_folder
```

#### `export`

```python
    def export(self, artifact_name: str, artifact_data: Union[dict, str], content_type: str, content_format: str = None, target_format: str = "txt", verbose: bool = False):
        """
        Экспортирует указанные данные артефакта в файл.

        Args:
            artifact_name (str): Имя артефакта.
            artifact_data (Union[dict, str]): Данные для экспорта. Если передан словарь, он будет сохранен как JSON.
                Если передана строка, она будет сохранена как есть.
            content_type (str): Тип контента в артефакте.
            content_format (str, optional): Формат контента в артефакте (например, md, csv и т.д.). По умолчанию None.
            target_format (str): Формат экспорта артефакта (например, json, txt, docx и т.д.).
            verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию False.

        Raises:
            ValueError: Если данные артефакта не являются строкой или словарем.
            ValueError: Если указанный формат экспорта не поддерживается.

        Как работает функция:
        - Проверяет тип входных данных `artifact_data`, и если это строка, удаляет начальные отступы. Если это словарь, удаляет отступы из значения ключа `'content'`. Если тип данных не строка и не словарь, выбрасывает исключение ValueError.
        - Очищает имя артефакта `artifact_name` от недопустимых символов, заменяя их на дефисы.
        - Составляет путь к файлу артефакта с помощью метода `_compose_filepath`.
        - В зависимости от значения `target_format` вызывает соответствующий метод для экспорта данных в нужный формат (_export_as_json, _export_as_txt или _export_as_docx).
        - Если `target_format` не поддерживается, выбрасывает исключение ValueError.
        """

```

#### `_export_as_txt`

```python
    def _export_as_txt(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False):
        """
        Экспортирует указанные данные артефакта в текстовый файл.

        Args:
            artifact_file_path (str): Путь к файлу для экспорта.
            artifact_data (Union[dict, str]): Данные для экспорта.
            content_type (str): Тип контента в артефакте.
            verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию False.

        Как работает функция:
        - Открывает файл по указанному пути `artifact_file_path` для записи в кодировке utf-8.
        - Проверяет тип данных `artifact_data`. Если это словарь, извлекает значение по ключу 'content'. Если это строка, использует строку как контент.
        - Записывает контент в файл.
        """
```

#### `_export_as_json`

```python
    def _export_as_json(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False):
        """
        Экспортирует указанные данные артефакта в JSON файл.

        Args:
            artifact_file_path (str): Путь к файлу для экспорта.
            artifact_data (Union[dict, str]): Данные для экспорта.
            content_type (str): Тип контента в артефакте.
            verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию False.

        Raises:
            ValueError: Если данные артефакта не являются словарем.

        Как работает функция:
        - Открывает файл по указанному пути `artifact_file_path` для записи в кодировке utf-8.
        - Проверяет тип данных `artifact_data`. Если это словарь, сериализует его в JSON-формат с отступами и записывает в файл.
        - Если `artifact_data` не является словарем, выбрасывает исключение ValueError.
        """
```

#### `_export_as_docx`

```python
    def _export_as_docx(self, artifact_file_path: str, artifact_data: Union[dict, str], content_original_format: str, verbose: bool = False):
        """
        Экспортирует указанные данные артефакта в DOCX файл.

        Args:
            artifact_file_path (str): Путь к файлу для экспорта.
            artifact_data (Union[dict, str]): Данные для экспорта.
            content_original_format (str): Исходный формат контента (например, 'text' или 'markdown').
            verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию False.

        Raises:
            ValueError: Если исходный формат контента не поддерживается.

        Как работает функция:
        - Проверяет, что `content_original_format` является одним из допустимых значений ('text', 'txt', 'markdown', 'md'). Если нет, выбрасывает исключение ValueError.
        - Нормализует значение `content_original_format`, приводя 'md' к 'markdown'.
        - Извлекает контент из `artifact_data`. Если это словарь, берет значение по ключу 'content'. Если это строка, использует строку как контент.
        - Преобразует контент в HTML с помощью markdown.markdown().
        - Конвертирует HTML-контент в формат DOCX с помощью pypandoc.convert_text().
        """
```

#### `_compose_filepath`

```python
    def _compose_filepath(self, artifact_data: Union[dict, str], artifact_name: str, content_type: str, target_format: str = None, verbose: bool = False):
        """
        Составляет путь к файлу для экспортируемого артефакта.

        Args:
            artifact_data (Union[dict, str]): Данные для экспорта.
            artifact_name (str): Имя артефакта.
            content_type (str): Тип контента в артефакте.
            target_format (str, optional): Формат экспорта артефакта (например, json, txt, docx и т.д.).
            verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию False.

        Returns:
            str: Сформированный путь к файлу артефакта.

        Как работает функция:
        - Определяет расширение файла на основе `target_format` и типа `artifact_data`.
        - Определяет подпапку на основе `content_type`.
        - Формирует полный путь к файлу, объединяя базовую папку, подпапку и имя файла с расширением.
        - Создает промежуточные директории, если они не существуют.
        - Возвращает сформированный путь к файлу.
        """