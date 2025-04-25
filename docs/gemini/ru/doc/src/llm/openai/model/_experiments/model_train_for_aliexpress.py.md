# Модуль для обучения моделей на данных с AliExpress

## Обзор

Модуль `src/ai/openai/model/_experiments/model_train_for_aliexpress.py` предназначен для обучения моделей машинного обучения на данных с AliExpress. Модуль использует модели OpenAI и Google Gemini для генерации описаний продуктов.

## Подробнее

Модуль считывает названия продуктов из файлов `product_titles.txt`, расположенных в каталоге `aliexpress/campaigns` на Google Drive. Затем он использует модели OpenAI и Google Gemini для генерации описаний продуктов на основе этих названий. 

## Функции

### `recursively_get_filenames`

**Описание**: 
Функция извлекает имена файлов в каталоге, рекурсивно обходя все подкаталоги.
**Параметры**:
- `path` (Path): Путь к каталогу.
- `filename_pattern` (str, optional): Шаблон имени файла. По умолчанию `None`.
**Возвращает**:
- `list`: Список найденных файлов.
**Пример**:
```python
>>> from pathlib import Path
>>> from src.utils.file import recursively_get_filenames
>>> path = Path('/home/user/documents')
>>> files = recursively_get_filenames(path, filename_pattern='*.txt')
>>> print(files)
['/home/user/documents/file1.txt', '/home/user/documents/subdir/file2.txt']
```

### `read_text_file`

**Описание**: 
Функция считывает текст из файла.
**Параметры**:
- `file_path` (str | Path): Путь к файлу.
- `as_list` (bool): Если `True`, возвращает список строк. По умолчанию `False`.
- `extensions` (Optional[List[str]]): Список расширений файлов для чтения из каталога.
- `chunk_size` (int): Размер чанков для чтения файла в байтах.
**Возвращает**:
- `Generator[str, None, None] | str | None`: Генератор строк, объединенная строка или `None` в случае ошибки.
**Пример**:
```python
>>> from pathlib import Path
>>> from src.utils.file import read_text_file
>>> file_path = Path('example.txt')
>>> content = read_text_file(file_path)
>>> if content:
...    print(f'File content: {content[:100]}...')
File content: Example text...
```

### `csv2json_csv2dict`

**Описание**: 
Функция преобразует CSV-файл в JSON-формат.
**Параметры**:
- `file_path` (str | Path): Путь к CSV-файлу.
- `sep` (str, optional): Разделитель в CSV-файле. По умолчанию ',' (запятая).
- `header_row` (int, optional): Номер строки с заголовками. По умолчанию 0.
**Возвращает**:
- `list | dict | None`: Список словарей, словарь или `None` в случае ошибки.
**Пример**:
```python
>>> from src.utils.convertors import csv2json_csv2dict
>>> file_path = 'data.csv'
>>> data = csv2json_csv2dict(file_path)
>>> print(data)
[{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
```

### `pprint`

**Описание**: 
Функция выводит данные на консоль в читаемом формате.
**Параметры**:
- `print_data` (Any, optional): Данные для вывода. По умолчанию `None`.
- `text_color` (str, optional): Цвет текста. По умолчанию 'white'.
- `bg_color` (str, optional): Цвет фона. По умолчанию ''.
- `font_style` (str, optional): Стиль шрифта. По умолчанию ''.
**Возвращает**:
- `None`
**Пример**:
```python
>>> from src.utils.printer import pprint
>>> data = {'name': 'Alice', 'age': 30}
>>> pprint(data, text_color='green')
{'name': 'Alice', 'age': 30}
```

## Классы

### `OpenAIModel`

**Описание**: 
Класс для взаимодействия с моделью OpenAI.
**Атрибуты**:
- `system_instruction` (str): Системная инструкция для модели.
**Методы**:
- `ask` (str): Отправляет запрос в модель OpenAI.
**Пример**:
```python
>>> from src.llm import OpenAIModel
>>> model = OpenAIModel(system_instruction='This is a system instruction.')
>>> response = model.ask('What is the capital of France?')
>>> print(response)
Paris
```

### `GoogleGenerativeAi`

**Описание**: 
Класс для взаимодействия с моделью Google Gemini.
**Атрибуты**:
- `system_instruction` (str): Системная инструкция для модели.
**Методы**:
- `ask` (str): Отправляет запрос в модель Google Gemini.
**Пример**:
```python
>>> from src.llm import GoogleGenerativeAi
>>> model = GoogleGenerativeAi(system_instruction='This is a system instruction.')
>>> response = model.ask('What is the capital of France?')
>>> print(response)
Paris
```

## Примеры

```python
from src import gs
from src.llm import OpenAIModel, GoogleGenerativeAi
from src.utils.file import recursively_get_filenames, read_text_file
from src.utils.convertors import csv2json_csv2dict
from src.utils.printer import pprint

product_titles_files:list = recursively_get_filenames(gs.path.google_drive / 'aliexpress' / 'campaigns', 'product_titles.txt')
system_instruction_path = gs.path.src / 'ai' / 'prompts' / 'aliexpress_campaign' / 'system_instruction.txt'
system_instruction: str = read_text_file(system_instruction_path)
openai = OpenAIModel(system_instruction = system_instruction)
gemini = GoogleGenerativeAi(system_instruction = system_instruction)

for file in product_titles_files:
    product_titles = read_text_file(file)
    response_openai = openai.ask(product_titles)
    response_gemini = gemini.ask(product_titles)