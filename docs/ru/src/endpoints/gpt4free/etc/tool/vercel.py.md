# Модуль для получения и обработки информации о моделях Vercel AI SDK

## Обзор

Модуль предназначен для получения информации о моделях, доступных в Vercel AI SDK, преобразования этой информации в удобный формат и генерации кода для использования этих моделей в проекте `hypotez`. Модуль извлекает данные о моделях из JavaScript-файлов, используя регулярные выражения и QuickJS для разбора JSON-строк.

## Подробней

Этот модуль выполняет следующие задачи:

1.  Получает HTML-код главной страницы Vercel AI SDK.
2.  Извлекает пути к JavaScript-файлам, содержащим информацию о моделях.
3.  Загружает содержимое этих JavaScript-файлов.
4.  Извлекает JSON-строки, описывающие модели, используя регулярные выражения.
5.  Преобразует JSON-строки в Python-словари с использованием QuickJS.
6.  Преобразует информацию о моделях в формат, используемый в проекте `hypotez`.
7.  Генерирует код для определения моделей и их параметров.

Модуль использует библиотеки `curl_cffi`, `quickjs`, `re` и `json` для выполнения этих задач.

## Функции

### `get_model_info`

```python
def get_model_info() -> dict[str, Any]:
    """
    Получает информацию о моделях из Vercel AI SDK.

    Args:
        None

    Returns:
        dict[str, Any]: Словарь, содержащий информацию о моделях.

    Raises:
        None

    Как работает функция:
    1.  Извлекает HTML-код главной страницы Vercel AI SDK.
    2.  Извлекает пути к JavaScript-файлам, содержащим информацию о моделях.
    3.  Загружает содержимое этих JavaScript-файлов.
    4.  Извлекает JSON-строки, описывающие модели, используя регулярные выражения.
    5.  Преобразует JSON-строки в Python-словари с использованием QuickJS.

    ASCII flowchart:

    Get HTML
    ↓
    Extract paths → Load scripts
    ↓
    Find models
    ↓
    Evaluate JSON
    ↓
    Return models

    Примеры:
        >>> model_info = get_model_info()
        >>> print(model_info.keys())
        dict_keys(['cohere:command', 'openai:gpt-3.5-turbo', ...])
    """
    ...
```

### `convert_model_info`

```python
def convert_model_info(models: dict[str, Any]) -> dict[str, Any]:
    """
    Преобразует информацию о моделях в формат, используемый в проекте `hypotez`.

    Args:
        models (dict[str, Any]): Словарь, содержащий информацию о моделях.

    Returns:
        dict[str, Any]: Словарь, содержащий преобразованную информацию о моделях.

    Raises:
        None

    Как работает функция:
    1.  Итерируется по моделям в словаре `models`.
    2.  Извлекает параметры моделей и преобразует их в параметры по умолчанию.
    3.  Создает новый словарь, содержащий идентификаторы моделей и параметры по умолчанию.

    ASCII flowchart:

    Models
    ↓
    Iterate models → Extract params
    ↓
    Convert params
    ↓
    Create model info
    ↓
    Return model info

    Примеры:
        >>> models = {'cohere:command': {'id': 'cohere:command', 'parameters': {'temperature': {'value': 0.75}}}}
        >>> converted_models = convert_model_info(models)
        >>> print(converted_models)
        {'cohere:command': {'id': 'cohere:command', 'default_params': {'temperature': 0.75}}}
    """
    ...
```

### `params_to_default_params`

```python
def params_to_default_params(parameters: dict[str, Any]):
    """
    Преобразует параметры моделей в параметры по умолчанию.

    Args:
        parameters (dict[str, Any]): Словарь, содержащий параметры моделей.

    Returns:
        dict[str, Any]: Словарь, содержащий параметры по умолчанию.

    Raises:
        None

    Как работает функция:
    1.  Итерируется по параметрам в словаре `parameters`.
    2.  Если ключ параметра равен "maximumLength", он заменяется на "maxTokens".
    3.  Извлекает значение параметра и сохраняет его в словаре параметров по умолчанию.

    ASCII flowchart:

    Parameters
    ↓
    Iterate params → Check key
    ↓
    Replace key (if needed)
    ↓
    Extract value
    ↓
    Return defaults

    Примеры:
        >>> parameters = {'temperature': {'value': 0.75}, 'maximumLength': {'value': 1024}}
        >>> default_params = params_to_default_params(parameters)
        >>> print(default_params)
        {'temperature': 0.75, 'maxTokens': 1024}
    """
    ...
```

### `get_model_names`

```python
def get_model_names(model_info: dict[str, Any]):
    """
    Получает список имен моделей из информации о моделях.

    Args:
        model_info (dict[str, Any]): Словарь, содержащий информацию о моделях.

    Returns:
        list[str]: Список имен моделей.

    Raises:
        None

    Как работает функция:
    1.  Извлекает имена моделей из словаря `model_info`.
    2.  Исключает модели "openai:gpt-4" и "openai:gpt-3.5-turbo".
    3.  Сортирует список имен моделей.

    ASCII flowchart:

    Model info
    ↓
    Extract names → Exclude models
    ↓
    Sort names
    ↓
    Return names

    Примеры:
        >>> model_info = {'cohere:command': {'id': 'cohere:command'}, 'openai:gpt-4': {'id': 'openai:gpt-4'}}
        >>> model_names = get_model_names(model_info)
        >>> print(model_names)
        ['cohere:command']
    """
    ...
```

### `print_providers`

```python
def print_providers(model_names: list[str]):
    """
    Генерирует код для определения моделей и их параметров.

    Args:
        model_names (list[str]): Список имен моделей.

    Returns:
        None

    Raises:
        None

    Как работает функция:
    1.  Итерируется по именам моделей в списке `model_names`.
    2.  Разделяет имя модели на части, используя ":" и "/".
    3.  Форматирует имя модели и создает строку кода для определения модели.
    4.  Выводит строку кода.

    ASCII flowchart:

    Model names
    ↓
    Iterate names → Split name
    ↓
    Format name
    ↓
    Print line

    Примеры:
        >>> model_names = ['cohere:command', 'openai:gpt-3.5-turbo-instruct']
        >>> print_providers(model_names)
        command = Model(name="cohere:command", base_provider="cohere", best_provider=Vercel,)
        gpt_35_turbo_instruct = Model(name="openai:gpt-3.5-turbo-instruct", base_provider="openai", best_provider=Vercel,)
    """
    ...
```

### `print_convert`

```python
def print_convert(model_names: list[str]):
    """
    Генерирует код для преобразования имен моделей в переменные.

    Args:
        model_names (list[str]): Список имен моделей.

    Returns:
        None

    Raises:
        None

    Как работает функция:
    1.  Итерируется по именам моделей в списке `model_names`.
    2.  Разделяет имя модели на части, используя ":" и "/".
    3.  Извлекает последнюю часть имени модели.
    4.  Форматирует имя модели и создает строку кода для преобразования имени модели в переменную.
    5.  Выводит строку кода.

    ASCII flowchart:

    Model names
    ↓
    Iterate names → Split name
    ↓
    Extract key
    ↓
    Format name
    ↓
    Print line

    Примеры:
        >>> model_names = ['cohere:command', 'openai:gpt-3.5-turbo-instruct']
        >>> print_convert(model_names)
                "command": command,
                "gpt_35_turbo_instruct": gpt_35_turbo_instruct,
    """
    ...
```

### `main`

```python
def main():
    """
    Основная функция модуля.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Как работает функция:
    1.  Получает информацию о моделях.
    2.  Преобразует информацию о моделях.
    3.  Выводит информацию о моделях в формате JSON.
    4.  Получает список имен моделей.
    5.  Генерирует код для определения моделей и их параметров.
    6.  Генерирует код для преобразования имен моделей в переменные.

    ASCII flowchart:

    Get model info
    ↓
    Convert model info
    ↓
    Print JSON
    ↓
    Get model names
    ↓
    Print providers
    ↓
    Print convert
    """
    ...