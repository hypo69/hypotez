# Модуль ArtifactExporter

## Обзор

Модуль `artifact_exporter.py` предоставляет класс `ArtifactExporter`, который отвечает за экспорт артефактов из элементов TinyTroupe. Артефакты представляют собой данные, которые могут быть извлечены из модели TinyTroupe и экспортированы для дальнейшего использования. 

## Классы

### `ArtifactExporter`

**Описание**: Класс `ArtifactExporter` предназначен для экспорта артефактов из элементов TinyTroupe в различные форматы. 

**Наследует**: 
   - `JsonSerializableRegistry` из `tinytroupe.utils`

**Атрибуты**:

  - `base_output_folder (str)`: Базовая папка, в которую будут экспортироваться артефакты.

**Методы**:

  - `export(artifact_name:str, artifact_data:Union[dict, str], content_type:str, content_format:str=None, target_format:str="txt", verbose:bool=False)`: Экспортирует указанные данные артефакта в файл.
  - `_export_as_txt(artifact_file_path:str, artifact_data:Union[dict, str], content_type:str, verbose:bool=False)`: Экспортирует указанные данные артефакта в текстовый файл.
  - `_export_as_json(artifact_file_path:str, artifact_data:Union[dict, str], content_type:str, verbose:bool=False)`: Экспортирует указанные данные артефакта в файл JSON.
  - `_export_as_docx(artifact_file_path:str, artifact_data:Union[dict, str], content_original_format:str, verbose:bool=False)`: Экспортирует указанные данные артефакта в файл DOCX.
  - `_compose_filepath(self, artifact_data:Union[dict, str], artifact_name:str, content_type:str, target_format:str=None, verbose:bool=False)`: Составляет путь к файлу для экспорта артефакта.

## Функции

### `export`

**Назначение**: Экспортирует указанные данные артефакта в файл.

**Параметры**:

  - `artifact_name (str)`: Имя артефакта.
  - `artifact_data (Union[dict, str])`: Данные, которые нужно экспортировать. Если задан словарь, он будет сохранен как JSON. Если задана строка, она будет сохранена как есть.
  - `content_type (str)`: Тип содержимого в артефакте.
  - `content_format (str, optional)`: Формат содержимого в артефакте (например, md, csv и т. д.). По умолчанию `None`.
  - `target_format (str)`: Формат, в который нужно экспортировать артефакт (например, json, txt, docx и т. д.).
  - `verbose (bool, optional)`: Выводить ли отладочные сообщения. По умолчанию `False`.

**Возвращает**:
  - `None`

**Вызывает исключения**:
  - `ValueError`: Если формат данных артефакта не является строкой или словарем.

**Как работает функция**:

  - Функция `export` обрабатывает данные артефакта, преобразуя их в нужный формат и сохраняя в файл с соответствующим именем и расширением. 
  - Для определения формата файла функция использует параметр `target_format`.
  - Если `target_format` равен `json`, то данные будут сохранены в файл JSON.
  - Если `target_format` равен `txt`, `text`, `md` или `markdown`, то данные будут сохранены в текстовый файл.
  - Если `target_format` равен `docx`, то данные будут сохранены в файл DOCX.
  - Функция также обрабатывает невалидные символы в имени файла, заменяя их тире.

**Примеры**:

```python
# Экспорт данных в JSON-формат
exporter.export(artifact_name='my_artifact', artifact_data={'content': 'Some data'}, content_type='data', target_format='json')

# Экспорт данных в текстовый формат
exporter.export(artifact_name='my_artifact', artifact_data='Some data', content_type='data', target_format='txt')

# Экспорт данных в DOCX-формат
exporter.export(artifact_name='my_artifact', artifact_data={'content': 'Some data in Markdown'}, content_type='data', content_format='md', target_format='docx')
```

### `_export_as_txt`

**Назначение**: Экспортирует указанные данные артефакта в текстовый файл.

**Параметры**:

  - `artifact_file_path (str)`: Путь к файлу, в который нужно экспортировать данные.
  - `artifact_data (Union[dict, str])`: Данные, которые нужно экспортировать.
  - `content_type (str)`: Тип содержимого в артефакте.
  - `verbose (bool, optional)`: Выводить ли отладочные сообщения. По умолчанию `False`.

**Возвращает**:
  - `None`

**Вызывает исключения**:
  - `None`

**Как работает функция**:

  - Функция `_export_as_txt` открывает файл с указанным путем в режиме записи (`'w'`) и записывает данные артефакта в файл. 
  - Если `artifact_data` является словарем, то функция записывает значение ключа `content` в файл.
  - Если `artifact_data` является строкой, то функция записывает ее в файл.

**Примеры**:

```python
# Экспорт данных в текстовый файл
exporter._export_as_txt(artifact_file_path='my_artifact.txt', artifact_data='Some data', content_type='data')
```

### `_export_as_json`

**Назначение**: Экспортирует указанные данные артефакта в файл JSON.

**Параметры**:

  - `artifact_file_path (str)`: Путь к файлу, в который нужно экспортировать данные.
  - `artifact_data (Union[dict, str])`: Данные, которые нужно экспортировать.
  - `content_type (str)`: Тип содержимого в артефакте.
  - `verbose (bool, optional)`: Выводить ли отладочные сообщения. По умолчанию `False`.

**Возвращает**:
  - `None`

**Вызывает исключения**:
  - `ValueError`: Если данные артефакта не являются словарем.

**Как работает функция**:

  - Функция `_export_as_json` открывает файл с указанным путем в режиме записи (`'w'`) и записывает данные артефакта в файл JSON с использованием функции `json.dump`.
  - Если `artifact_data` является словарем, то функция записывает его в файл JSON.
  - Если `artifact_data` не является словарем, то функция выдает исключение `ValueError`.

**Примеры**:

```python
# Экспорт данных в файл JSON
exporter._export_as_json(artifact_file_path='my_artifact.json', artifact_data={'content': 'Some data'}, content_type='data')
```

### `_export_as_docx`

**Назначение**: Экспортирует указанные данные артефакта в файл DOCX.

**Параметры**:

  - `artifact_file_path (str)`: Путь к файлу, в который нужно экспортировать данные.
  - `artifact_data (Union[dict, str])`: Данные, которые нужно экспортировать.
  - `content_original_format (str)`: Оригинальный формат данных (например, 'text' или 'markdown').
  - `verbose (bool, optional)`: Выводить ли отладочные сообщения. По умолчанию `False`.

**Возвращает**:
  - `None`

**Вызывает исключения**:
  - `ValueError`: Если оригинальный формат данных не является 'text', 'txt', 'markdown' или 'md'.

**Как работает функция**:

  - Функция `_export_as_docx` преобразует данные артефакта из текстового формата в HTML, а затем в DOCX с использованием библиотеки `pypandoc`.
  - Функция проверяет, является ли `content_original_format` 'text', 'txt', 'markdown' или 'md'.
  - Если да, то функция нормализует значение `content_original_format` к 'markdown'.
  - Затем, функция преобразует данные в HTML с использованием функции `markdown.markdown`. 
  - После этого, функция `pypandoc.convert_text` преобразует HTML-контент в DOCX, сохраняя файл с указанным именем.

**Примеры**:

```python
# Экспорт данных в файл DOCX
exporter._export_as_docx(artifact_file_path='my_artifact.docx', artifact_data={'content': 'Some data in Markdown'}, content_original_format='md')
```

### `_compose_filepath`

**Назначение**: Составляет путь к файлу для экспорта артефакта.

**Параметры**:

  - `artifact_data (Union[dict, str])`: Данные, которые нужно экспортировать.
  - `artifact_name (str)`: Имя артефакта.
  - `content_type (str)`: Тип содержимого в артефакте.
  - `target_format (str, optional)`: Формат, в который нужно экспортировать артефакт (например, json, txt, docx и т. д.). По умолчанию `None`.
  - `verbose (bool, optional)`: Выводить ли отладочные сообщения. По умолчанию `False`.

**Возвращает**:
  - `str`: Путь к файлу для экспорта артефакта.

**Вызывает исключения**:
  - `None`

**Как работает функция**:

  - Функция `_compose_filepath` строит путь к файлу для экспорта артефакта. 
  - Путь к файлу определяется на основе базовой папки, типа содержимого, имени артефакта и расширения файла.
  - Функция создает промежуточные папки, если они не существуют. 

**Примеры**:

```python
# Составление пути к файлу
file_path = exporter._compose_filepath(artifact_data={'content': 'Some data'}, artifact_name='my_artifact', content_type='data', target_format='json')

# Вывод пути к файлу
print(file_path)
```

## Принцип работы класса `ArtifactExporter`

Класс `ArtifactExporter` предоставляет удобный интерфейс для экспорта данных артефактов в различных форматах. 
Экспортируемые артефакты могут быть представлены как строками, так и словарями. В случае словаря, данные 
хранятся под ключом `content`.

Экспорт данных артефактов в файл осуществляется с использованием различных методов:
- `_export_as_txt` - для текстовых файлов;
- `_export_as_json` - для файлов JSON;
- `_export_as_docx` - для файлов DOCX.

Для определения пути к файлу используется метод `_compose_filepath`. Метод принимает на вход данные 
артефакта, имя артефакта, тип содержимого, формат экспорта и уровень отладки. 
В основе метода лежит логика составления пути к файлу, которая учитывает базовую папку, тип содержимого,
имя артефакта и расширение файла.

## Примеры

```python
# Создание экземпляра класса ArtifactExporter
exporter = ArtifactExporter(base_output_folder='/path/to/output/folder')

# Экспорт данных в JSON-формат
exporter.export(artifact_name='my_artifact', artifact_data={'content': 'Some data'}, content_type='data', target_format='json')

# Экспорт данных в текстовый формат
exporter.export(artifact_name='my_artifact', artifact_data='Some data', content_type='data', target_format='txt')

# Экспорт данных в DOCX-формат
exporter.export(artifact_name='my_artifact', artifact_data={'content': 'Some data in Markdown'}, content_type='data', content_format='md', target_format='docx')
```