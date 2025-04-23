# Модуль enrichment.py

## Обзор

Модуль `enrichment.py` предназначен для обогащения содержимого с использованием AI-моделей. Он содержит класс `TinyEnricher`, который позволяет улучшать контент на основе заданных требований и контекстной информации.

## Подробней

Этот модуль является частью проекта `hypotez` и отвечает за улучшение текстового содержимого. Он использует шаблоны Mustache для создания запросов к AI-моделям и извлекает результаты из ответов. Расположение файла указывает на то, что он является частью модуля `tinytroupe`.

## Классы

### `TinyEnricher`

**Описание**: Класс `TinyEnricher` предназначен для обогащения контента с использованием AI-моделей. Он позволяет улучшать содержимое на основе заданных требований и контекстной информации.

**Наследует**: `JsonSerializableRegistry`

**Атрибуты**:

- `use_past_results_in_context` (bool): Определяет, использовать ли предыдущие результаты в контексте. По умолчанию `False`.
- `context_cache` (list): Кэш контекстной информации.

**Методы**:

- `__init__(self, use_past_results_in_context=False)`: Инициализирует экземпляр класса `TinyEnricher`.
- `enrich_content(self, requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False)`: Обогащает контент на основе заданных требований и контекстной информации.

### `__init__`

```python
def __init__(self, use_past_results_in_context=False) -> None:
    """
    Инициализирует экземпляр класса `TinyEnricher`.

    Args:
        use_past_results_in_context (bool, optional): Определяет, следует ли использовать предыдущие результаты в контексте. По умолчанию `False`.

    Returns:
        None
    """
```

**Как работает функция**:
- Функция инициализирует класс `TinyEnricher`.
- Устанавливает значение атрибута `use_past_results_in_context` на основе переданного аргумента.
- Инициализирует `context_cache` как пустой список.

**Примеры**:

```python
enricher = TinyEnricher(use_past_results_in_context=True)
print(enricher.use_past_results_in_context)  # Вывод: True

enricher = TinyEnricher()
print(enricher.use_past_results_in_context)  # Вывод: False
```

### `enrich_content`

```python
def enrich_content(self, requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False) -> str | None:
    """
    Обогащает контент на основе заданных требований и контекстной информации.

    Args:
        requirements (str): Требования к обогащению контента.
        content (str): Контент для обогащения.
        content_type (str, optional): Тип контента. По умолчанию `None`.
        context_info (str, optional): Контекстная информация. По умолчанию пустая строка.
        context_cache (list, optional): Кэш контекстной информации. По умолчанию `None`.
        verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.

    Returns:
        str | None: Обогащенный контент или `None`, если обогащение не удалось.
    """
```

**Внутренние функции**:
Отсутствуют

**Как работает функция**:

1.  **Подготовка данных**:
    *   Функция принимает входные параметры, такие как `requirements` (требования к обогащению), `content` (содержимое для обогащения), `content_type` (тип содержимого), `context_info` (контекстная информация) и `context_cache` (кэш контекстной информации).
    *   Создается словарь `rendering_configs`, содержащий все входные параметры для использования в шаблонах.
2.  **Композиция сообщений для LLM**:
    *   Вызывается функция `utils.compose_initial_LLM_messages_with_templates` для создания списка сообщений, которые будут отправлены в AI-модель (LLM). Эта функция использует шаблоны Mustache (`enricher.system.mustache` и `enricher.user.mustache`) и словарь `rendering_configs` для генерации сообщений.
3.  **Отправка сообщений в AI-модель**:
    *   Используется `openai_utils.client().send_message` для отправки сгенерированных сообщений в AI-модель. Параметр `temperature` устанавливается на 0.4, что влияет на случайность и креативность ответов модели.
    *   Результат от AI-модели сохраняется в переменной `next_message`.
4.  **Обработка результата**:
    *   Включается логирование и отладочные сообщения:
        *   Создается отладочное сообщение `debug_msg`, содержащее результат обогащения.
        *   Сообщение логируется с уровнем `DEBUG` с помощью `logger.debug(debug_msg)`.
        *   Если установлен флаг `verbose`, сообщение также выводится на экран.
    *   Извлечение кода из ответа:
        *   Если `next_message` не `None`, функция пытается извлечь блок кода из содержимого сообщения с помощью `utils.extract_code_block`.
        *   Если `next_message` равен `None`, `result` устанавливается в `None`.
5.  **Возврат результата**:
    *   Функция возвращает извлеченный `result`, который содержит обогащенный контент или `None`, если обогащение не удалось.

**Примеры**:

```python
from unittest.mock import MagicMock

# Mocking necessary modules and classes
openai_utils = MagicMock()
utils = MagicMock()
logger = MagicMock()

# Creating a mock for the OpenAI client's send_message method
mock_client = MagicMock()
mock_response = {"content": "```enriched content```"}
mock_client.send_message.return_value = mock_response
openai_utils.client.return_value = mock_client

# Setting up the extract_code_block mock to return the content directly
utils.extract_code_block.return_value = "enriched content"

# Initializing TinyEnricher
enricher = TinyEnricher()

# Calling enrich_content with some dummy data
requirements = "Make it better"
content = "This is some content"
enriched_content = enricher.enrich_content(requirements, content, verbose=True)

# Assertions to verify the mocks were called correctly
openai_utils.client.assert_called_once()
mock_client.send_message.assert_called_once()
utils.extract_code_block.assert_called_once_with(mock_response["content"])

# Printing the result
print(enriched_content)
```

## Параметры класса

- `use_past_results_in_context` (bool): Указывает, следует ли использовать предыдущие результаты в контексте при обогащении контента. Это может быть полезно для сохранения последовательности и контекста в многошаговых задачах обогащения.
- `context_cache` (list): Список, используемый для хранения контекстной информации между вызовами функции `enrich_content`. Это позволяет сохранять и использовать информацию о предыдущих запросах и ответах для улучшения качества обогащения.

## Методы класса

### `enrich_content`

```python
def enrich_content(self, requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False) -> str | None:
    """
    Обогащает контент на основе заданных требований и контекстной информации.

    Args:
        requirements (str): Требования к обогащению контента.
        content (str): Контент для обогащения.
        content_type (str, optional): Тип контента. По умолчанию `None`.
        context_info (str, optional): Контекстная информация. По умолчанию пустая строка.
        context_cache (list, optional): Кэш контекстной информации. По умолчанию `None`.
        verbose (bool, optional): Флаг для вывода отладочных сообщений. По умолчанию `False`.

    Returns:
        str | None: Обогащенный контент или `None`, если обогащение не удалось.
    """
```

**Параметры**:

- `requirements` (str): Требования к обогащению контента.
- `content` (str): Контент, который необходимо обогатить.
- `content_type` (str, optional): Тип контента (например, "текст", "код"). По умолчанию `None`.
- `context_info` (str, optional): Дополнительная контекстная информация, которая может помочь AI-модели в процессе обогащения. По умолчанию пустая строка.
- `context_cache` (list, optional): Список, содержащий кэш контекстной информации. По умолчанию `None`.
- `verbose` (bool, optional): Флаг, указывающий, следует ли выводить отладочные сообщения. По умолчанию `False`.

**Примеры**:

```python
enricher = TinyEnricher()
requirements = "Улучши этот текст"
content = "Какой-то текст для улучшения"
enriched_content = enricher.enrich_content(requirements, content)
if enriched_content:
    print(f"Обогащенный контент: {enriched_content}")
else:
    print("Обогащение не удалось")
```