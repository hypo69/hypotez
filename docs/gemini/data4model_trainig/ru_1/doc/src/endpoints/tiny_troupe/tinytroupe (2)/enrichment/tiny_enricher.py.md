# Модуль tiny_enricher

## Обзор

Модуль `tiny_enricher.py` предназначен для обогащения контента с использованием OpenAI моделей. Он содержит класс `TinyEnricher`, который позволяет обогащать текстовый контент на основе заданных требований и контекстной информации. Модуль использует шаблоны Mustache для формирования запросов к языковой модели и извлекает результат из ответа модели.

## Подробней

Модуль предоставляет функциональность для обогащения контента, например, добавление дополнительной информации или изменение стиля текста, с использованием возможностей языковых моделей. `TinyEnricher` использует кэш контекста для улучшения качества обогащения при последовательных запросах. Он также обеспечивает гибкую настройку параметров запроса к модели OpenAI.

## Классы

### `TinyEnricher`

**Описание**: Класс предназначен для обогащения текстового контента с использованием моделей OpenAI.

**Наследует**:
- `JsonSerializableRegistry`: Класс наследуется от `JsonSerializableRegistry`, что позволяет сохранять и восстанавливать состояние объекта в формате JSON.

**Атрибуты**:
- `use_past_results_in_context` (bool): Определяет, следует ли использовать предыдущие результаты в контексте для обогащения контента. По умолчанию `False`.
- `context_cache` (list): Список, используемый для хранения контекстной информации между запросами.

**Методы**:
- `__init__(self, use_past_results_in_context=False)`: Инициализирует экземпляр класса `TinyEnricher`.
- `enrich_content(self, requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False)`: Обогащает контент на основе заданных требований и контекстной информации.

#### `__init__`

```python
def __init__(self, use_past_results_in_context=False) -> None:
    """
    Инициализирует экземпляр класса TinyEnricher.

    Args:
        use_past_results_in_context (bool): Флаг, указывающий, следует ли использовать предыдущие результаты в контексте. По умолчанию False.

    Returns:
        None
    """
    ...
```

#### `enrich_content`

```python
def enrich_content(self, requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False):
    """
    Обогащает контент на основе заданных требований и контекстной информации.

    Args:
        requirements (str): Требования к обогащению контента.
        content (str): Контент, который необходимо обогатить.
        content_type (str, optional): Тип контента. По умолчанию None.
        context_info (str, optional): Контекстная информация. По умолчанию "".
        context_cache (list, optional): Кэш контекста. По умолчанию None.
        verbose (bool, optional): Флаг для вывода отладочной информации. По умолчанию False.

    Returns:
        str | None: Обогащенный контент или None в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при взаимодействии с моделью OpenAI.

    **Как работает функция**:
    - Функция принимает требования, контент и контекстную информацию.
    - Формирует словарь `rendering_configs`, содержащий все необходимые данные для шаблонов.
    - Использует функцию `compose_initial_LLM_messages_with_templates` для создания сообщений для языковой модели на основе шаблонов Mustache.
    - Отправляет сообщение в OpenAI и получает ответ.
    - Извлекает блок кода из ответа.
    - Возвращает обогащенный контент.

    **Внутренние функции**:
    - Отсутствуют

    **Примеры**:
    ```python
    enricher = TinyEnricher()
    requirements = "Добавить описание продукта"
    content = "Продукт: Яблоко"
    enriched_content = enricher.enrich_content(requirements, content, verbose=True)
    if enriched_content:
        print(f"Обогащенный контент: {enriched_content}")
    ```
    """
    ...
```

## Параметры класса

- `use_past_results_in_context` (bool): Определяет, следует ли использовать предыдущие результаты в контексте для обогащения контента. По умолчанию `False`.
- `context_cache` (list): Список, используемый для хранения контекстной информации между запросами.

## Методы класса

### `enrich_content`

```python
def enrich_content(self, requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False):
    """
    Обогащает контент на основе заданных требований и контекстной информации.

    Args:
        requirements (str): Требования к обогащению контента.
        content (str): Контент, который необходимо обогатить.
        content_type (str, optional): Тип контента. По умолчанию None.
        context_info (str, optional): Контекстная информация. По умолчанию "".
        context_cache (list, optional): Кэш контекста. По умолчанию None.
        verbose (bool, optional): Флаг для вывода отладочной информации. По умолчанию False.

    Returns:
        str | None: Обогащенный контент или None в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при взаимодействии с моделью OpenAI.
    """
    ...
```

**Параметры**:
- `requirements` (str): Требования к обогащению контента.
- `content` (str): Контент, который необходимо обогатить.
- `content_type` (Optional[str], optional): Тип контента. По умолчанию `None`.
- `context_info` (str, optional): Контекстная информация. По умолчанию `""`.
- `context_cache` (Optional[list], optional): Кэш контекста. По умолчанию `None`.
- `verbose` (bool, optional): Флаг для вывода отладочной информации. По умолчанию `False`.

**Примеры**:

```python
enricher = TinyEnricher()
requirements = "Добавить описание продукта"
content = "Продукт: Яблоко"
enriched_content = enricher.enrich_content(requirements, content, verbose=True)
if enriched_content:
    print(f"Обогащенный контент: {enriched_content}")
```
```python
enricher = TinyEnricher()
requirements = "Перефразировать текст"
content = "Это просто текст."
enriched_content = enricher.enrich_content(requirements, content, verbose=True)
if enriched_content:
    print(f"Обогащенный контент: {enriched_content}")
```