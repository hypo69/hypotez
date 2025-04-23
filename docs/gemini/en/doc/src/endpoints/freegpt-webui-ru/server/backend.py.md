# Документация модуля `backend.py`

## Обзор

Модуль предоставляет API для взаимодействия с языковой моделью, такой как ChatGPT, с использованием библиотеки `g4f`. Он включает в себя функциональность для создания бесед, получения результатов поиска в интернете и применения инструкций обхода ограничений (jailbreak).

## Более подробная информация

Модуль содержит класс `Backend_Api`, который обрабатывает запросы к API и генерирует ответы от языковой модели. Он также включает функции для построения сообщений, получения результатов поиска и управления обходом ограничений. В проекте `hypotez` этот код используется для предоставления интерфейса для взаимодействия с различными языковыми моделями через API.

## Содержание

1.  [Классы](#Классы)
    *   [Backend_Api](#Backend_Api)
2.  [Функции](#Функции)
    *   [build_messages](#build_messages)
    *   [fetch_search_results](#fetch_search_results)
    *   [generate_stream](#generate_stream)
    *   [response_jailbroken_success](#response_jailbroken_success)
    *   [response_jailbroken_failed](#response_jailbroken_failed)
    *   [set_response_language](#set_response_language)
    *   [isJailbreak](#isJailbreak)

## Классы

### `Backend_Api`

Класс для обработки API-запросов и взаимодействия с языковой моделью.

**Атрибуты:**

*   `app`: Экземпляр Flask-приложения.
*   `use_auto_proxy`: Флаг, указывающий на использование автоматического прокси.
*   `routes`: Словарь, содержащий маршруты API и соответствующие функции.

**Методы:**

*   `__init__(self, app, config: dict) -> None`: Инициализирует класс `Backend_Api`.
*   `_conversation(self)`: Обрабатывает запросы на создание беседы и генерирует ответы от языковой модели.

#### `__init__`

```python
    def __init__(self, app, config: dict) -> None:
        """
        Инициализирует класс `Backend_Api`.

        Args:
            app: Экземпляр Flask-приложения.
            config (dict): Словарь конфигурации.

        Returns:
            None
        """
```

#### `_conversation`

```python
    def _conversation(self):
        """
        Обрабатывает запросы на создание беседы и генерирует ответы от языковой модели.

        Returns:
            flask.Response: Ответ от Flask-приложения с потоком данных или словарь с информацией об ошибке.

        Raises:
            Exception: В случае возникновения ошибки при обработке запроса.
        """
```

## Функции

### `build_messages`

```python
def build_messages(jailbreak):
    """
    Создает список сообщений для беседы на основе данных из запроса.

    Args:
        jailbreak: Инструкции для обхода ограничений.

    Returns:
        list: Список сообщений для беседы.
    """
```

### `fetch_search_results`

```python
def fetch_search_results(query):
    """
    Выполняет поиск в интернете и возвращает результаты в виде списка сообщений.

    Args:
        query: Поисковый запрос.

    Returns:
        list: Список сообщений с результатами поиска.
    """
```

### `generate_stream`

```python
def generate_stream(response, jailbreak):
    """
    Генерирует поток данных для ответа от языковой модели.

    Args:
        response: Ответ от языковой модели.
        jailbreak: Инструкции для обхода ограничений.

    Yields:
        str: Часть ответа от языковой модели.
    """
```

### `response_jailbroken_success`

```python
def response_jailbroken_success(response: str) -> bool:
    """
    Проверяет, успешно ли применены инструкции обхода ограничений к ответу.

    Args:
        response (str): Ответ от языковой модели.

    Returns:
        bool: `True`, если инструкции успешно применены, иначе `False`.
    """
```

### `response_jailbroken_failed`

```python
def response_jailbroken_failed(response):
    """
    Проверяет, не удалось ли применить инструкции обхода ограничений к ответу.

    Args:
        response: Ответ от языковой модели.

    Returns:
        bool: `True`, если не удалось применить инструкции, иначе `False`.
    """
```

### `set_response_language`

```python
def set_response_language(prompt):
    """
    Определяет язык запроса и возвращает строку с инструкцией для языковой модели.

    Args:
        prompt: Текст запроса.

    Returns:
        str: Строка с инструкцией для языковой модели.
    """
```

### `isJailbreak`

```python
def isJailbreak(jailbreak):
    """
    Проверяет, включены ли инструкции обхода ограничений, и возвращает их.

    Args:
        jailbreak: Имя набора инструкций для обхода ограничений.

    Returns:
        list | None: Список инструкций для обхода ограничений, если они включены, иначе `None`.
    """
```