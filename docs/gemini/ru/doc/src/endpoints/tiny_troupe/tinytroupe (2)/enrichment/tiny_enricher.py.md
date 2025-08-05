# Модуль TinyEnricher

## Обзор

Модуль `tiny_enricher.py` содержит класс `TinyEnricher`, который используется для обогащения контента с помощью AI-модели OpenAI.  

## Подробнее

Класс `TinyEnricher` наследует класс `JsonSerializableRegistry` и предоставляет функциональность для обогащения контента с использованием API OpenAI. 

## Классы

### `TinyEnricher`

**Описание**: Класс `TinyEnricher` используется для обогащения контента (текста, кода) с помощью AI-модели OpenAI.

**Наследует**: `JsonSerializableRegistry`

**Атрибуты**:

- `use_past_results_in_context` (bool): Флаг, указывающий, нужно ли использовать прошлые результаты в контексте. 
- `context_cache` (list): Список, хранящий предыдущие результаты. 

**Методы**:

- `enrich_content(requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False) -> str | None`: Метод, обогащающий контент с помощью модели OpenAI.

## Функции

### `enrich_content`

**Назначение**: Обогащает контент с помощью модели OpenAI.

**Параметры**:

- `requirements` (str): Требования к обогащению контента.
- `content` (str): Контент, который необходимо обогатить.
- `content_type` (str, optional): Тип контента (например, "text", "code"). По умолчанию `None`.
- `context_info` (str, optional): Информация о контексте обогащения. По умолчанию пустая строка.
- `context_cache` (list, optional): Список с предыдущими результатами для использования в контексте. По умолчанию `None`.
- `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочную информацию. По умолчанию `False`.

**Возвращает**:

- `str | None`: Обогащенный контент или `None`, если произошла ошибка.

**Вызывает исключения**:

- `Exception`: Если произошла ошибка при работе с моделью OpenAI.

**Как работает функция**:

1. Функция `enrich_content` собирает информацию о контексте, контенте и требованиях.
2. Она формирует сообщения для модели OpenAI, используя шаблоны из файлов `enricher.system.mustache` и `enricher.user.mustache`.
3. Используя API OpenAI, функция отправляет сообщения в модель и получает ответ.
4. Функция извлекает код из ответа модели, если он присутствует, и возвращает его.
5. Если ответ модели не содержит код, функция возвращает `None`.

**Примеры**:

```python
# Пример использования с текстовым контентом
requirements = "Сделай текст более интересным и захватывающим"
content = "Это обычный текст."
enriched_content = enricher.enrich_content(requirements, content)

# Пример использования с кодом
requirements = "Добавь комментарии к коду"
content = "def my_function():\n    print('Hello world')"
enriched_content = enricher.enrich_content(requirements, content, content_type="code")
```

## Параметры класса

- `use_past_results_in_context` (bool): Флаг, указывающий, нужно ли использовать прошлые результаты в контексте. 
- `context_cache` (list): Список, хранящий предыдущие результаты. 

## Примеры

```python
# Создание инстанса класса TinyEnricher
enricher = TinyEnricher()

# Обогащение текстового контента
requirements = "Сделай текст более интересным и захватывающим"
content = "Это обычный текст."
enriched_content = enricher.enrich_content(requirements, content)

# Обогащение кода
requirements = "Добавь комментарии к коду"
content = "def my_function():\n    print('Hello world')"
enriched_content = enricher.enrich_content(requirements, content, content_type="code")
```