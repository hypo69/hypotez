# Модуль `models.py`

## Обзор

Модуль предназначен для загрузки, форматирования, сохранения и предоставления информации о моделях, используемых в проекте `hypotez`. Он обеспечивает централизованный доступ к данным о моделях, таким как их расположение, требования к оперативной памяти и шаблоны промптов.

## Подробнее

Модуль выполняет следующие основные функции:

1.  **Загрузка моделей**: Модуль загружает информацию о доступных моделях из внешнего источника (`gpt4all.io`) и форматирует её.
2.  **Локальное хранение**: Загруженные данные сохраняются локально в файле `models.json` для последующего использования.
3.  **Предоставление информации**: Модуль предоставляет функции для чтения информации о моделях из локального файла и доступа к этой информации.

## Функции

### `load_models`

```python
def load_models() -> dict:
    """
    Загружает информацию о моделях с сайта gpt4all.io.

    Returns:
        dict: Словарь, содержащий информацию о моделях.
    
    Raises:
        requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.

    Как работает функция:
    - Отправляет GET-запрос к "https://gpt4all.io/models/models3.json".
    - Вызывает функцию `raise_for_status(response)` для проверки статуса ответа.
    - Вызывает функцию `format_models(response.json())` для форматирования полученных данных.

    Примеры:
        >>> models = load_models()
        >>> print(models.keys())  # Пример: dict_keys(['mistral-7b-openorca.Q4_0.gguf', 'mistral-7b-openorca.Q4_0.gguf', ...])
    """
    ...
```

### `get_model_name`

```python
def get_model_name(filename: str) -> str:
    """
    Извлекает имя модели из имени файла, удаляя лишние суффиксы.

    Args:
        filename (str): Имя файла модели.

    Returns:
        str: Очищенное имя модели.

    Как работает функция:
    - Разделяет имя файла по первой точке.
    - Последовательно удаляет из имени модели суффиксы, такие как "-v1_5", "-v1", "-q4_0", "_v01", "-v0", "-f16", "-gguf2", "-newbpe".
    - Возвращает очищенное имя модели.

    Примеры:
        >>> get_model_name("mistral-7b-openorca-v1_5.Q4_0.gguf")
        'mistral-7b-openorca'
        >>> get_model_name("llama-2-7b-chat-newbpe.Q4_0.gguf")
        'llama-2-7b-chat'
    """
    ...
```

### `format_models`

```python
def format_models(models: list) -> dict:
    """
    Форматирует список моделей в словарь, где ключом является имя модели.

    Args:
        models (list): Список моделей, полученный из JSON.

    Returns:
        dict: Словарь, содержащий информацию о моделях, где ключ - имя модели.

    Как работает функция:
    - Преобразует список моделей в словарь, используя генератор словаря.
    - Ключом словаря является имя модели, полученное с помощью `get_model_name(model["filename"])`.
    - Значением каждого ключа является словарь с информацией о модели:
        - "path": `model["filename"]` (путь к файлу модели).
        - "ram": `model["ramrequired"]` (требования к оперативной памяти).
        - "prompt": `model["promptTemplate"]` (шаблон промта, если он есть).
        - "system": `model["systemPrompt"]` (системный промт, если он есть).

    Примеры:
        >>> models_data = [{"filename": "mistral-7b-openorca-v1_5.Q4_0.gguf", "ramrequired": "8 GB", "promptTemplate": "<prompt>", "systemPrompt": "<system>"}]
        >>> formatted_models = format_models(models_data)
        >>> print(formatted_models)
        {'mistral-7b-openorca': {'path': 'mistral-7b-openorca-v1_5.Q4_0.gguf', 'ram': '8 GB', 'prompt': '<prompt>', 'system': '<system>'}}
    """
    ...
```

### `read_models`

```python
def read_models(file_path: str) -> dict:
    """
    Считывает данные о моделях из JSON-файла.

    Args:
        file_path (str): Путь к файлу.

    Returns:
        dict: Словарь с информацией о моделях.

    Как работает функция:
    - Открывает файл по указанному пути в режиме чтения байтов ("rb").
    - Загружает JSON-данные из файла с помощью `json.load(f)`.
    - Возвращает словарь с информацией о моделях.

    Примеры:
        >>> import os
        >>> file_path = 'models.json'
        >>> # Создадим временный файл для примера
        >>> with open(file_path, 'w') as f:
        ...     json.dump({'model1': {'path': 'path1'}}, f)
        >>> models = read_models(file_path)
        >>> print(models)
        {'model1': {'path': 'path1'}}
        >>> os.remove(file_path)  # Удаляем временный файл
    """
    ...
```

### `save_models`

```python
def save_models(file_path: str, data: dict):
    """
    Сохраняет данные о моделях в JSON-файл.

    Args:
        file_path (str): Путь к файлу.
        data (dict): Данные для сохранения.

    Как работает функция:
    - Открывает файл по указанному пути в режиме записи ('w').
    - Записывает данные в файл в формате JSON с отступами равными 4 с помощью `json.dump(data, f, indent=4)`.

    Примеры:
        >>> import os
        >>> file_path = 'models.json'
        >>> data = {'model1': {'path': 'path1'}}
        >>> save_models(file_path, data)
        >>> with open(file_path, 'r') as f:
        ...     print(json.load(f))
        {'model1': {'path': 'path1'}}
        >>> os.remove(file_path)  # Удаляем временный файл
    """
    ...
```

### `get_model_dir`

```python
def get_model_dir() -> str:
    """
    Определяет и возвращает путь к каталогу для хранения моделей. Если каталог не существует, он создается.

    Returns:
        str: Путь к каталогу моделей.

    Как работает функция:
    - Определяет путь к текущему файлу (`__file__`) и извлекает родительский каталог, используя `os.path.dirname`.
    - Формирует путь к каталогу `models`, располагающемуся на уровень выше текущего файла.
    - Проверяет существование каталога `models`. Если каталог не существует, он создается с помощью `os.mkdir(model_dir)`.
    - Возвращает путь к каталогу `models`.

    Примеры:
        >>> model_dir = get_model_dir()
        >>> print(model_dir)  # Пример: /path/to/project/models
    """
    ...
```

### `get_models`

```python
def get_models() -> dict[str, dict]:
    """
    Получает данные о моделях из локального файла, если он существует; в противном случае загружает, сохраняет и возвращает их.

    Returns:
        dict[str, dict]: Словарь с информацией о моделях.

    Как работает функция:
    - Получает путь к каталогу моделей с помощью `get_model_dir()`.
    - Формирует полный путь к файлу `models.json` в каталоге моделей.
    - Проверяет существование файла `models.json`.
        - Если файл существует, читает данные из файла с помощью `read_models(file_path)` и возвращает их.
        - Если файл не существует, загружает данные о моделях с помощью `load_models()`, сохраняет их в файл с помощью `save_models(file_path, models)` и возвращает загруженные данные.

    Примеры:
        >>> models = get_models()
        >>> print(models.keys())  # Пример: dict_keys(['mistral-7b-openorca', 'llama-2-7b-chat', ...])
    """
    ...