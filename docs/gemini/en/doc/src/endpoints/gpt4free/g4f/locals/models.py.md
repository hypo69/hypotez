# Модуль models

## Обзор

Модуль `models.py` отвечает за управление и хранение моделей, используемых в проекте `hypotez`. Он содержит набор функций для загрузки, формата, чтения, сохранения и получения моделей. Модуль взаимодействует с API GPT4All.io, чтобы получить список доступных моделей и их информацию.

## Детали

Модуль взаимодействует с файлом `models.json`, который хранит информацию о моделях, доступных в проекте. Он использует следующие методы:

- `load_models()`: Загружает список доступных моделей из API GPT4All.io.
- `get_model_name()`: Извлекает имя модели из имени файла.
- `format_models()`: Преобразует данные о моделях в удобный формат.
- `read_models()`: Чтение данных о моделях из файла `models.json`.
- `save_models()`: Сохраняет данные о моделях в файл `models.json`.
- `get_model_dir()`: Возвращает путь к каталогу, где хранятся модели.
- `get_models()`: Получает список доступных моделей, загружая их из API GPT4All.io или из файла `models.json`.

## Классы

###  `None`

**Description**: Данный модуль не содержит собственных классов.

## Функции

### `load_models()`

**Purpose**: Загружает список доступных моделей из API GPT4All.io.

**Parameters**: 
- `None`

**Returns**: 
- `dict`: Возвращает словарь с информацией о моделях, полученной из API GPT4All.io.

**Raises Exceptions**:
- `requests.exceptions.RequestException`: Если возникает ошибка при выполнении запроса к API GPT4All.io.
- `src.endpoints.gpt4free.g4f.locals.requests.raise_for_status.HTTPError`: Если получен ответ с ошибкой от API GPT4All.io.

**How the Function Works**:
- Делает GET-запрос к API GPT4All.io, чтобы получить список доступных моделей.
- Вызывает `raise_for_status()` для обработки ошибок в запросе.
- Возвращает данные о моделях в формате словаря.

**Examples**:
```python
>>> models = load_models()
>>> print(models)
{'gpt4all-lora-quantized-12b': {'path': 'gpt4all-lora-quantized-12b.bin', 'ram': 10, 'prompt': 'Prompt: {input}', 'system': 'System prompt: {system}'}, ...}
```

### `get_model_name()`

**Purpose**: Извлекает имя модели из имени файла.

**Parameters**: 
- `filename (str)`: Имя файла модели.

**Returns**: 
- `str`: Возвращает имя модели.

**Raises Exceptions**:
- `None`

**How the Function Works**:
- Разбивает имя файла по точке, чтобы получить только часть до расширения.
- Заменяет все нежелательные суффиксы в имени файла, чтобы получить только имя модели.
- Возвращает имя модели.

**Examples**:
```python
>>> get_model_name("gpt4all-lora-quantized-12b.bin")
'gpt4all-lora-quantized-12b'
```

### `format_models()`

**Purpose**: Преобразует данные о моделях в удобный формат.

**Parameters**: 
- `models (list)`: Список данных о моделях, полученный из API GPT4All.io.

**Returns**: 
- `dict`: Возвращает словарь с информацией о моделях в удобном формате.

**Raises Exceptions**:
- `None`

**How the Function Works**:
- Использует функцию `get_model_name()` для извлечения имени модели из имени файла.
- Создает словарь, где ключом является имя модели, а значением - словарь с информацией о модели:
    - `path`: Путь к файлу модели.
    - `ram`: Требуемый объем оперативной памяти.
    - `prompt`: Шаблон для подсказки.
    - `system`: Системная подсказка.
- Возвращает словарь с информацией о моделях.

**Examples**:
```python
>>> models = [{'filename': 'gpt4all-lora-quantized-12b.bin', 'ramrequired': 10, 'promptTemplate': 'Prompt: {input}', 'systemPrompt': 'System prompt: {system}'}, ...]
>>> formatted_models = format_models(models)
>>> print(formatted_models)
{'gpt4all-lora-quantized-12b': {'path': 'gpt4all-lora-quantized-12b.bin', 'ram': 10, 'prompt': 'Prompt: {input}', 'system': 'System prompt: {system}'}, ...}
```

### `read_models()`

**Purpose**: Чтение данных о моделях из файла `models.json`.

**Parameters**: 
- `file_path (str)`: Путь к файлу `models.json`.

**Returns**: 
- `dict`: Возвращает словарь с данными о моделях, прочитанными из файла.

**Raises Exceptions**:
- `IOError`: Если файл `models.json` не найден.
- `json.decoder.JSONDecodeError`: Если файл `models.json` некорректный.

**How the Function Works**:
- Открывает файл `models.json` в режиме чтения.
- Вызывает `json.load()` для чтения данных из файла.
- Возвращает словарь с данными о моделях.

**Examples**:
```python
>>> models = read_models("models.json")
>>> print(models)
{'gpt4all-lora-quantized-12b': {'path': 'gpt4all-lora-quantized-12b.bin', 'ram': 10, 'prompt': 'Prompt: {input}', 'system': 'System prompt: {system}'}, ...}
```

### `save_models()`

**Purpose**: Сохраняет данные о моделях в файл `models.json`.

**Parameters**: 
- `file_path (str)`: Путь к файлу `models.json`.
- `data`: Данные о моделях в формате словаря.

**Returns**: 
- `None`

**Raises Exceptions**:
- `IOError`: Если файл `models.json` не может быть открыт для записи.

**How the Function Works**:
- Открывает файл `models.json` в режиме записи.
- Вызывает `json.dump()` для записи данных в файл.

**Examples**:
```python
>>> models = {'gpt4all-lora-quantized-12b': {'path': 'gpt4all-lora-quantized-12b.bin', 'ram': 10, 'prompt': 'Prompt: {input}', 'system': 'System prompt: {system}'}, ...}
>>> save_models("models.json", models)
```

### `get_model_dir()`

**Purpose**: Возвращает путь к каталогу, где хранятся модели.

**Parameters**: 
- `None`

**Returns**: 
- `str`: Путь к каталогу с моделями.

**Raises Exceptions**:
- `None`

**How the Function Works**:
- Получает текущий каталог.
- Находит каталог проекта `hypotez`.
- Создает каталог `models` в каталоге проекта, если он не существует.
- Возвращает путь к каталогу с моделями.

**Examples**:
```python
>>> model_dir = get_model_dir()
>>> print(model_dir)
/path/to/hypotez/models
```

### `get_models()`

**Purpose**: Получает список доступных моделей, загружая их из API GPT4All.io или из файла `models.json`.

**Parameters**: 
- `None`

**Returns**: 
- `dict`: Возвращает словарь с информацией о моделях.

**Raises Exceptions**:
- `None`

**How the Function Works**:
- Получает путь к каталогу с моделями.
- Проверяет наличие файла `models.json` в каталоге.
    - Если файл найден, то читает данные из него с помощью `read_models()`.
    - Если файл не найден, то загружает данные о моделях из API GPT4All.io с помощью `load_models()`.
- Сохраняет данные о моделях в файл `models.json` с помощью `save_models()`.
- Возвращает словарь с информацией о моделях.

**Examples**:
```python
>>> models = get_models()
>>> print(models)
{'gpt4all-lora-quantized-12b': {'path': 'gpt4all-lora-quantized-12b.bin', 'ram': 10, 'prompt': 'Prompt: {input}', 'system': 'System prompt: {system}'}, ...}
```