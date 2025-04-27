# Модуль ArtifactExporter
## Обзор
Модуль `artifact_exporter.py` предоставляет класс `ArtifactExporter`, который отвечает за экспорт артефактов из элементов TinyTroupe.  Артефакты могут быть экспортированы в различных форматах, таких как JSON, TXT, DOCX, MD и т. д.,  что позволяет создавать синтетические файлы данных из симуляций.

## Детали
Класс `ArtifactExporter` наследуется от `JsonSerializableRegistry`, что позволяет его использовать в качестве регистра для хранения и загрузки артефактов.

## Классы
### `class ArtifactExporter`
**Описание**: Класс `ArtifactExporter` отвечает за экспорт артефактов из элементов TinyTroupe. Артефакты могут быть экспортированы в различных форматах, таких как JSON, TXT, DOCX, MD и т. д., что позволяет создавать синтетические файлы данных из симуляций. 

**Inherits**:  `JsonSerializableRegistry`

**Attributes**:
- `base_output_folder` (str): Базовый каталог для экспорта артефактов.

**Methods**:
- `export(artifact_name:str, artifact_data:Union[dict, str], content_type:str, content_format:str=None, target_format:str="txt", verbose:bool=False)`: Экспортирует данные артефакта в файл.

### `class ArtifactExporter._export_as_txt`
**Описание**: Экспортирует данные артефакта в текстовый файл.

**Parameters**:
- `artifact_file_path` (str): Путь к файлу, в который будут экспортированы данные.
- `artifact_data` (Union[dict, str]): Данные, которые нужно экспортировать. 
- `content_type` (str): Тип контента внутри артефакта.
- `verbose` (bool, optional): Флаг для вывода отладочной информации. По умолчанию `False`. 

**Returns**: 
- `None`

### `class ArtifactExporter._export_as_json`
**Описание**: Экспортирует данные артефакта в JSON-файл.

**Parameters**:
- `artifact_file_path` (str): Путь к файлу, в который будут экспортированы данные.
- `artifact_data` (Union[dict, str]): Данные, которые нужно экспортировать. 
- `content_type` (str): Тип контента внутри артефакта.
- `verbose` (bool, optional): Флаг для вывода отладочной информации. По умолчанию `False`. 

**Returns**: 
- `None`

### `class ArtifactExporter._export_as_docx`
**Описание**: Экспортирует данные артефакта в DOCX-файл.

**Parameters**:
- `artifact_file_path` (str): Путь к файлу, в который будут экспортированы данные.
- `artifact_data` (Union[dict, str]): Данные, которые нужно экспортировать. 
- `content_original_format` (str):  Оригинальный формат контента внутри артефакта. Должен быть равен 'text', 'txt', 'markdown' или 'md'.
- `verbose` (bool, optional): Флаг для вывода отладочной информации. По умолчанию `False`. 

**Returns**: 
- `None`

### `class ArtifactExporter._compose_filepath`
**Описание**: Формирует путь к файлу для экспорта артефакта.

**Parameters**:
- `artifact_data` (Union[dict, str]): Данные, которые нужно экспортировать.
- `artifact_name` (str): Имя артефакта.
- `content_type` (str): Тип контента внутри артефакта.
- `target_format` (str, optional): Формат, в который нужно экспортировать артефакт. 
- `verbose` (bool, optional): Флаг для вывода отладочной информации. По умолчанию `False`. 

**Returns**: 
- `str`: Путь к файлу.


## Функции 
### `export(artifact_name:str, artifact_data:Union[dict, str], content_type:str, content_format:str=None, target_format:str="txt", verbose:bool=False)`
**Описание**: Экспортирует данные артефакта в файл.

**Parameters**:
- `artifact_name` (str): Имя артефакта.
- `artifact_data` (Union[dict, str]): Данные, которые нужно экспортировать. Если передается словарь, он будет сохранен в формате JSON. Если передается строка, она будет сохранена как есть.
- `content_type` (str): Тип контента внутри артефакта.
- `content_format` (str, optional): Формат контента внутри артефакта (например, md, csv и т. д.). По умолчанию `None`. 
- `target_format` (str): Формат, в который нужно экспортировать артефакт (например, json, txt, docx и т. д.).
- `verbose` (bool, optional): Флаг для вывода отладочной информации. По умолчанию `False`.

**Returns**: 
- `None`

**Raises Exceptions**:
- `ValueError`: Если `artifact_data` не является строкой или словарем.

**How the Function Works**:
- Функция `export` принимает на вход данные артефакта, его имя, тип контента, формат контента, формат экспорта и флаг для вывода отладочной информации. 
- Сначала функция очищает имя артефакта от недопустимых символов, заменяя их на дефисы. 
- Затем функция определяет путь к файлу, куда будет экспортирован артефакт, используя метод `_compose_filepath`.
- После этого функция вызывает соответствующий метод экспорта в зависимости от указанного формата экспорта: `_export_as_json`, `_export_as_txt` или `_export_as_docx`.

**Examples**:
```python
# Экспорт данных в JSON
exporter.export(artifact_name='product_data', artifact_data={'product_name': 'Товар 1', 'price': 100}, content_type='product', target_format='json', verbose=True)

# Экспорт данных в TXT
exporter.export(artifact_name='product_description', artifact_data='Описание товара 1', content_type='product', target_format='txt', verbose=False)
```

## Пример использования
```python
from tinytroupe.extraction.artifact_exporter import ArtifactExporter

# Создание экземпляра экспортера
exporter = ArtifactExporter(base_output_folder='./output')

# Экспорт данных в JSON
exporter.export(artifact_name='product_data', artifact_data={'product_name': 'Товар 1', 'price': 100}, content_type='product', target_format='json', verbose=True)

# Экспорт данных в TXT
exporter.export(artifact_name='product_description', artifact_data='Описание товара 1', content_type='product', target_format='txt', verbose=False)
```