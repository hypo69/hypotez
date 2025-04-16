# Модуль для обогащения контента с использованием AI-моделей
=============================================================

Модуль содержит класс :class:`TinyEnricher`, который используется для обогащения текстового контента на основе заданных требований с использованием AI-моделей.

Пример использования
----------------------

>>>enricher = TinyEnricher()
>>>enriched_content = enricher.enrich_content(requirements="Добавь больше деталей", content="Текст для обогащения", content_type="Описание продукта")
>>>print(enriched_content)

## Обзор

Модуль `enrichment.py` предоставляет функциональность для обогащения текстового контента с использованием моделей обработки естественного языка. Он включает класс `TinyEnricher`, который позволяет динамически улучшать контент на основе заданных требований и контекстной информации.

## Подробнее

Модуль предназначен для улучшения качества контента, такого как описания продуктов, статьи или любой другой текст, путем добавления деталей, исправления ошибок или адаптации к определенному стилю. Он использует шаблоны Mustache для динамической генерации запросов к AI-моделям и извлекает результаты из ответов модели.

## Классы

### `TinyEnricher`

**Описание**: Класс для обогащения контента с использованием AI-моделей.

**Атрибуты**:
- `use_past_results_in_context` (bool): Указывает, следует ли использовать предыдущие результаты в контексте для обогащения. По умолчанию `False`.
- `context_cache` (list): Список для хранения контекстной информации.

**Методы**:
- `enrich_content()`: Обогащает предоставленный контент на основе заданных требований и контекста.

**Принцип работы**:
Класс `TinyEnricher` инициализируется с возможностью использования предыдущих результатов в контексте. Метод `enrich_content` принимает требования, контент, тип контента и контекстную информацию, формирует запросы к AI-модели, отправляет их и извлекает обогащенный контент из ответа модели.

## Методы класса

### `__init__`

```python
def __init__(self, use_past_results_in_context=False) -> None:
    """Инициализирует экземпляр класса TinyEnricher.

    Args:
        use_past_results_in_context (bool): Указывает, следует ли использовать предыдущие результаты в контексте для обогащения. По умолчанию `False`.

    Returns:
        None

    """
```

**Назначение**: Инициализирует экземпляр класса `TinyEnricher`.

**Параметры**:
- `use_past_results_in_context` (bool): Указывает, следует ли использовать предыдущие результаты в контексте для обогащения. По умолчанию `False`.

**Примеры**:
```python
enricher = TinyEnricher()
enricher_with_context = TinyEnricher(use_past_results_in_context=True)
```

### `enrich_content`

```python
def enrich_content(self, requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False):
    """Обогащает предоставленный контент на основе заданных требований и контекста.

    Args:
        requirements (str): Требования к обогащению контента.
        content (str): Контент, который необходимо обогатить.
        content_type (str, optional): Тип контента. По умолчанию `None`.
        context_info (str, optional): Контекстная информация. По умолчанию "".
        context_cache (list, optional): Список для хранения контекстной информации. По умолчанию `None`.
        verbose (bool, optional): Флаг для вывода отладочной информации. По умолчанию `False`.

    Returns:
        str | None: Обогащенный контент или `None`, если обогащение не удалось.

    Raises:
        Exception: Если возникает ошибка при взаимодействии с AI-моделью.

    """
```

**Назначение**: Обогащает предоставленный контент на основе заданных требований и контекста.

**Параметры**:
- `requirements` (str): Требования к обогащению контента.
- `content` (str): Контент, который необходимо обогатить.
- `content_type` (str, optional): Тип контента. По умолчанию `None`.
- `context_info` (str, optional): Контекстная информация. По умолчанию "".
- `context_cache` (list, optional): Список для хранения контекстной информации. По умолчанию `None`.
- `verbose` (bool, optional): Флаг для вывода отладочной информации. По умолчанию `False`.

**Как работает функция**:
1. Формирует словарь `rendering_configs` с параметрами для шаблонов Mustache.
2. Использует функцию `utils.compose_initial_LLM_messages_with_templates` для создания сообщений для AI-модели на основе шаблонов "enricher.system.mustache" и "enricher.user.mustache".
3. Отправляет сообщения в AI-модель с помощью `openai_utils.client().send_message` и получает ответ.
4. Извлекает обогащенный контент из ответа модели с помощью `utils.extract_code_block`.
5. Возвращает обогащенный контент.

**Примеры**:
```python
enricher = TinyEnricher()
enriched_content = enricher.enrich_content(
    requirements="Добавь больше деталей",
    content="Текст для обогащения",
    content_type="Описание продукта",
    context_info="Информация о продукте",
    verbose=True
)
if enriched_content:
    print(f"Обогащенный контент: {enriched_content}")
else:
    print("Обогащение не удалось.")
```
```python
enricher = TinyEnricher()
enriched_content = enricher.enrich_content(
    requirements="Сделай более формальным",
    content="Текст для обогащения"
)
if enriched_content:
    print(f"Обогащенный контент: {enriched_content}")
else:
    print("Обогащение не удалось.")
```
```python
enricher = TinyEnricher()
enriched_content = enricher.enrich_content(
    requirements="Добавь юмора",
    content="Текст для обогащения",
    verbose=True
)
if enriched_content:
    print(f"Обогащенный контент: {enriched_content}")
else:
    print("Обогащение не удалось.")
```
```python
enricher = TinyEnricher()
enriched_content = enricher.enrich_content(
    requirements="Перефразируй",
    content="Текст для обогащения",
    verbose=True
)
if enriched_content:
    print(f"Обогащенный контент: {enriched_content}")
else:
    print("Обогащение не удалось.")
```

## Параметры класса

- `use_past_results_in_context` (bool): Указывает, следует ли использовать предыдущие результаты в контексте для обогащения. По умолчанию `False`.
- `context_cache` (list): Список для хранения контекстной информации.