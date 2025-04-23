# Модуль для обогащения контента в Tiny Troupe
## Обзор

Модуль `tiny_enricher.py` предназначен для обогащения контента с использованием моделей машинного обучения. Он предоставляет класс `TinyEnricher`, который позволяет добавлять дополнительную информацию или улучшать существующий контент на основе заданных требований и контекста.
## Подробнее

Этот модуль является частью системы Tiny Troupe и отвечает за улучшение качества контента. Он использует OpenAI API для взаимодействия с моделями машинного обучения и библиотеку Mustache для создания шаблонов запросов.
## Классы

### `TinyEnricher`
**Описание**: Класс для обогащения контента на основе заданных требований и контекста.

**Наследует**:
- `JsonSerializableRegistry`: Класс обеспечивает функциональность для сериализации и десериализации объектов в формат JSON.

**Атрибуты**:
- `use_past_results_in_context` (bool): Флаг, указывающий, следует ли использовать предыдущие результаты в контексте. По умолчанию `False`.
- `context_cache` (list): Кэш контекстной информации для использования в процессе обогащения контента.

**Методы**:
- `__init__(self, use_past_results_in_context: bool = False) -> None`: Инициализирует экземпляр класса `TinyEnricher`.
- `enrich_content(self, requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False)`: Обогащает предоставленный контент на основе заданных требований и контекстной информации.

## Методы класса

### `__init__`

```python
    def __init__(self, use_past_results_in_context=False) -> None:
        """
        Инициализирует экземпляр класса `TinyEnricher`.

        Args:
            use_past_results_in_context (bool, optional): Указывает, следует ли использовать предыдущие результаты в контексте. По умолчанию `False`.

        Returns:
            None
        """
```

### `enrich_content`

```python
    def enrich_content(self, requirements: str, content:str, content_type:str =None, context_info:str ="", context_cache:list=None, verbose:bool=False):
        """
        Обогащает предоставленный контент на основе заданных требований и контекстной информации.

        Args:
            requirements (str): Требования к обогащению контента.
            content (str): Контент, который нужно обогатить.
            content_type (str, optional): Тип контента. По умолчанию `None`.
            context_info (str, optional): Дополнительная контекстная информация. По умолчанию пустая строка.
            context_cache (list, optional): Кэш контекстной информации. По умолчанию `None`.
            verbose (bool, optional): Флаг, указывающий, следует ли выводить отладочные сообщения. По умолчанию `False`.

        Returns:
            str | None: Обогащенный контент или `None`, если не удалось обогатить контент.
        """
```

**Как работает функция**:
- Функция `enrich_content` принимает требования, контент и контекстную информацию в качестве входных данных.
- Формирует `rendering_configs`, содержащий требования, контент, тип контента и контекстную информацию.
- Составляет сообщения для языковой модели (LLM), используя шаблоны из `enricher.system.mustache` и `enricher.user.mustache`. Шаблоны находятся в папке `enrichment`.
- Отправляет сообщение в OpenAI API для получения обогащенного контента.
- Извлекает блок кода из ответа, если он присутствует.
- Возвращает обогащенный контент или `None`, если обогащение не удалось.

**Внутренние функции**:
- `utils.compose_initial_LLM_messages_with_templates`: Cоставляет сообщения для языковой модели (LLM), используя шаблоны из `enricher.system.mustache` и `enricher.user.mustache`
- `openai_utils.client().send_message`: Отправляет сообщение в OpenAI API для получения обогащенного контента.
- `utils.extract_code_block`: Извлекает блок кода из ответа, если он присутствует.

**Примеры**:

```python
from tinytroupe.enrichment.tiny_enricher import TinyEnricher

enricher = TinyEnricher()
requirements = "Добавь в текст больше юмора"
content = "Это просто текст."
enriched_content = enricher.enrich_content(requirements, content)
if enriched_content:
    print(f"Обогащенный контент: {enriched_content}")
else:
    print("Не удалось обогатить контент.")