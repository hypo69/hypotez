# Модуль `enrichment` 

## Обзор

Модуль `enrichment` предоставляет функциональность для обогащения контента с помощью моделей ИИ.

## Подробнее

Данный модуль содержит класс `TinyEnricher`, который используется для обогащения текстового контента с помощью моделей ИИ. 

## Классы

### `TinyEnricher`

**Описание**: Класс `TinyEnricher` предоставляет методы для обогащения контента.

**Наследует**:
-  `JsonSerializableRegistry`

**Атрибуты**:
- `use_past_results_in_context` (bool): Указывает, следует ли использовать предыдущие результаты в контексте для обогащения.
- `context_cache` (list): Список предыдущих результатов для использования в контексте.

**Методы**:
- `enrich_content(requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False) -> str | None`: Обогащает контент с помощью модели ИИ.

## Методы класса

### `enrich_content`

```python
    def enrich_content(self, requirements: str, content:str, content_type:str =None, context_info:str ="", context_cache:list=None, verbose:bool=False):

        """
        Обогащает контент с помощью модели ИИ.

        Args:
            requirements (str): Требования к обогащению контента.
            content (str): Текстовый контент для обогащения.
            content_type (str, optional): Тип контента (например, "article", "product_description"). По умолчанию `None`.
            context_info (str, optional): Дополнительная информация о контексте. По умолчанию "".
            context_cache (list, optional): Список предыдущих результатов для использования в контексте. По умолчанию `None`.
            verbose (bool, optional): Флаг для включения подробного вывода. По умолчанию `False`.

        Returns:
            str | None: Обогащенный контент или `None`, если обогащение не удалось.

        Raises:
            Exception: Если возникает ошибка при обогащении контента.
        """
        rendering_configs = {"requirements": requirements,
                             "content": content,
                             "content_type": content_type, 
                             "context_info": context_info,
                             "context_cache": context_cache}

        messages = utils.compose_initial_LLM_messages_with_templates("enricher.system.mustache", "enricher.user.mustache", rendering_configs)
        next_message = openai_utils.client().send_message(messages, temperature=0.4)

        debug_msg = f"Enrichment result message: {next_message}"
        logger.debug(debug_msg)
        if verbose:
            print(debug_msg)

        if next_message is not None:
            result = utils.extract_code_block(next_message["content"])
        else:
            result = None

        return result

```

**Назначение**: Данная функция обогащает контент с помощью модели ИИ.

**Параметры**:
- `requirements` (str): Требования к обогащению контента.
- `content` (str): Текстовый контент для обогащения.
- `content_type` (str, optional): Тип контента (например, "article", "product_description"). По умолчанию `None`.
- `context_info` (str, optional): Дополнительная информация о контексте. По умолчанию "".
- `context_cache` (list, optional): Список предыдущих результатов для использования в контексте. По умолчанию `None`.
- `verbose` (bool, optional): Флаг для включения подробного вывода. По умолчанию `False`.

**Возвращает**:
- `str | None`: Обогащенный контент или `None`, если обогащение не удалось.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при обогащении контента.

**Как работает функция**:
- Функция `enrich_content` принимает требования к обогащению, контент, тип контента, информацию о контексте, список предыдущих результатов и флаг подробного вывода.
- С помощью шаблонов "enricher.system.mustache" и "enricher.user.mustache" формируются сообщения для модели ИИ.
- Используя `openai_utils.client()`, отправляется сообщение модели ИИ.
- Результат обогащения извлекается из сообщения модели ИИ с помощью `utils.extract_code_block`.
- Обогащенный контент возвращается, если обогащение успешно.

**Примеры**:
```python
from tinytroupe.enrichment import TinyEnricher

enricher = TinyEnricher()

requirements = "Добавить информацию о товаре."
content = "Это описание товара."
enriched_content = enricher.enrich_content(requirements, content)

print(f"Обогащенный контент: {enriched_content}")