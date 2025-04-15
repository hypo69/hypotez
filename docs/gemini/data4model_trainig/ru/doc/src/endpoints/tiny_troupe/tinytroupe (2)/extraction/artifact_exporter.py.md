# Модуль экспорта артефактов
## Обзор

Модуль `artifact_exporter.py` предоставляет класс `ArtifactExporter`, который отвечает за экспорт артефактов из элементов TinyTroupe. Например, он может быть использован для создания синтетических файлов данных из симуляций. Класс позволяет сохранять данные в различных форматах, таких как JSON, TXT и DOCX.

## Подробнее

Класс `ArtifactExporter` предоставляет функциональность для экспорта артефактов, созданных в процессе работы TinyTroupe. Он обеспечивает гибкость в выборе формата вывода, поддерживая JSON, TXT и DOCX. Кроме того, класс обрабатывает некорректные символы в именах файлов, заменяя их на дефисы, чтобы избежать ошибок при сохранении.

## Классы

### `ArtifactExporter`

**Описание**: Класс `ArtifactExporter` предназначен для экспорта артефактов из TinyTroupe элементов.

**Атрибуты**:

- `base_output_folder` (str): Базовая папка для сохранения экспортированных артефактов.

**Методы**:

- `__init__(self, base_output_folder: str) -> None`: Инициализирует экземпляр класса `ArtifactExporter`.
- `export(self, artifact_name: str, artifact_data: Union[dict, str], content_type: str, content_format: str = None, target_format: str = "txt", verbose: bool = False)`: Экспортирует артефакт в файл.
- `_export_as_txt(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False)`: Экспортирует артефакт в текстовый файл.
- `_export_as_json(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False)`: Экспортирует артефакт в JSON файл.
- `_export_as_docx(self, artifact_file_path: str, artifact_data: Union[dict, str], content_original_format: str, verbose: bool = False)`: Экспортирует артефакт в файл DOCX.
- `_compose_filepath(self, artifact_data: Union[dict, str], artifact_name: str, content_type: str, target_format: str = None, verbose: bool = False)`: Формирует путь к файлу для экспортируемого артефакта.

### `__init__`

```python
def __init__(self, base_output_folder: str) -> None
```

**Назначение**: Инициализирует экземпляр класса `ArtifactExporter` с указанной базовой папкой для вывода.

**Параметры**:

- `base_output_folder` (str): Базовая папка, в которой будут сохраняться экспортированные артефакты.

**Пример**:

```python
exporter = ArtifactExporter(base_output_folder="output")
```

### `export`

```python
def export(self, artifact_name: str, artifact_data: Union[dict, str], content_type: str, content_format: str = None, target_format: str = "txt", verbose: bool = False)
```

**Назначение**: Экспортирует указанные данные артефакта в файл.

**Параметры**:

- `artifact_name` (str): Имя артефакта.
- `artifact_data` (Union[dict, str]): Данные для экспорта. Если это словарь, он будет сохранен как JSON. Если строка, она будет сохранена как есть.
- `content_type` (str): Тип содержимого в артефакте.
- `content_format` (str, optional): Формат содержимого в артефакте (например, md, csv и т.д.). По умолчанию `None`.
- `target_format` (str): Формат экспорта артефакта (например, json, txt, docx и т.д.).
- `verbose` (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `ValueError`: Если `artifact_data` не является строкой или словарем.
- `ValueError`: Если указанный `target_format` не поддерживается.

**Как работает функция**:

1.  Удаляет лишние отступы из входных данных. Если `artifact_data` является строкой, удаляются отступы из строки. Если это словарь, удаляются отступы из значения ключа 'content'.
2.  Очищает имя артефакта от недопустимых символов, заменяя их на дефисы.
3.  Формирует путь к файлу с помощью метода `_compose_filepath`.
4.  В зависимости от `target_format` вызывает соответствующий метод экспорта (`_export_as_json`, `_export_as_txt`, `_export_as_docx`).
5.  Если `target_format` не поддерживается, вызывает исключение `ValueError`.

**Примеры**:

```python
exporter = ArtifactExporter(base_output_folder="output")
data = {"content": "Example text"}
exporter.export(artifact_name="example", artifact_data=data, content_type="text", target_format="txt")

data = {"key": "value"}
exporter.export(artifact_name="data", artifact_data=data, content_type="json", target_format="json")
```

### `_export_as_txt`

```python
def _export_as_txt(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False)
```

**Назначение**: Экспортирует указанные данные артефакта в текстовый файл.

**Параметры**:

- `artifact_file_path` (str): Путь к файлу, в который будет экспортирован артефакт.
- `artifact_data` (Union[dict, str]): Данные для экспорта. Если это словарь, будет использовано значение ключа 'content'.
- `content_type` (str): Тип содержимого в артефакте.
- `verbose` (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.

**Как работает функция**:

1.  Открывает файл по указанному пути в режиме записи с кодировкой UTF-8.
2.  Если `artifact_data` является словарем, извлекает содержимое из ключа 'content'. В противном случае использует `artifact_data` напрямую.
3.  Записывает содержимое в файл.

**Пример**:

```python
exporter = ArtifactExporter(base_output_folder="output")
data = {"content": "Example text"}
exporter._export_as_txt(artifact_file_path="output/example.txt", artifact_data=data, content_type="text")
```

### `_export_as_json`

```python
def _export_as_json(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False)
```

**Назначение**: Экспортирует указанные данные артефакта в JSON файл.

**Параметры**:

- `artifact_file_path` (str): Путь к файлу, в который будет экспортирован артефакт.
- `artifact_data` (Union[dict, str]): Данные для экспорта. Должны быть словарем.
- `content_type` (str): Тип содержимого в артефакте.
- `verbose` (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.

**Вызывает исключения**:

- `ValueError`: Если `artifact_data` не является словарем.

**Как работает функция**:

1.  Открывает файл по указанному пути в режиме записи с кодировкой UTF-8.
2.  Проверяет, является ли `artifact_data` словарем. Если нет, вызывает исключение `ValueError`.
3.  Записывает содержимое `artifact_data` в файл в формате JSON с отступами равными 4.

**Пример**:

```python
exporter = ArtifactExporter(base_output_folder="output")
data = {"key": "value"}
exporter._export_as_json(artifact_file_path="output/data.json", artifact_data=data, content_type="json")
```

### `_export_as_docx`

```python
def _export_as_docx(self, artifact_file_path: str, artifact_data: Union[dict, str], content_original_format: str, verbose: bool = False)
```

**Назначение**: Экспортирует указанные данные артефакта в файл DOCX.

**Параметры**:

- `artifact_file_path` (str): Путь к файлу, в который будет экспортирован артефакт.
- `artifact_data` (Union[dict, str]): Данные для экспорта. Если это словарь, будет использовано значение ключа 'content'.
- `content_original_format` (str): Исходный формат содержимого артефакта (например, 'text', 'markdown').
- `verbose` (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.

**Вызывает исключения**:

- `ValueError`: Если `content_original_format` не является 'text', 'txt', 'markdown' или 'md'.

**Как работает функция**:

1.  Проверяет, является ли `content_original_format` одним из поддерживаемых значений ('text', 'txt', 'markdown', 'md'). Если нет, вызывает исключение `ValueError`.
2.  Нормализует значение `content_original_format`, заменяя 'md' на 'markdown'.
3.  Если `artifact_data` является словарем, извлекает содержимое из ключа 'content'. В противном случае использует `artifact_data` напрямую.
4.  Преобразует содержимое в HTML с помощью библиотеки `markdown`.
5.  Преобразует HTML в DOCX с помощью библиотеки `pypandoc`.

**Пример**:

```python
exporter = ArtifactExporter(base_output_folder="output")
data = {"content": "# Header\nExample text"}
exporter._export_as_docx(artifact_file_path="output/example.docx", artifact_data=data, content_original_format="markdown")
```

### `_compose_filepath`

```python
def _compose_filepath(self, artifact_data: Union[dict, str], artifact_name: str, content_type: str, target_format: str = None, verbose: bool = False)
```

**Назначение**: Формирует путь к файлу для экспортируемого артефакта.

**Параметры**:

- `artifact_data` (Union[dict, str]): Данные для экспорта.
- `artifact_name` (str): Имя артефакта.
- `content_type` (str): Тип содержимого в артефакте.
- `target_format` (str, optional): Формат экспорта артефакта (например, json, txt, docx и т.д.).
- `verbose` (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.

**Как работает функция**:

1.  Определяет расширение файла в зависимости от `target_format` и типа `artifact_data`. Если `target_format` указан, используется он. Если `artifact_data` является строкой и `target_format` не указан, используется расширение "txt".
2.  Определяет подпапку в зависимости от `content_type`. Если `content_type` не указан, подпапка остается пустой.
3.  Формирует полный путь к файлу, объединяя базовую папку, подпапку и имя файла с расширением.
4.  Создает промежуточные директории, если они не существуют.
5.  Возвращает сформированный путь к файлу.

**Пример**:

```python
exporter = ArtifactExporter(base_output_folder="output")
data = {"content": "Example text"}
file_path = exporter._compose_filepath(artifact_data=data, artifact_name="example", content_type="text", target_format="txt")
print(file_path)  # output/text/example.txt