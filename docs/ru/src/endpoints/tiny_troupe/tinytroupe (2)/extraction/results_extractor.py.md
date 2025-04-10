# Модуль для извлечения результатов из взаимодействий агентов и окружения TinyTroupe
## Обзор

Модуль `results_extractor.py` предназначен для извлечения информации из истории взаимодействий агентов (`TinyPerson`) и окружения (`TinyWorld`) в рамках проекта `hypotez`. Он использует шаблоны для формирования запросов к OpenAI и извлекает структурированные данные в формате JSON.

## Подробней

Основная задача модуля - анализ истории взаимодействий агентов и выделение ключевых моментов. Это достигается путем формирования запросов на естественном языке с использованием шаблонов и отправки их в OpenAI для получения структурированных результатов. Результаты могут быть сохранены в формате JSON для дальнейшего анализа и использования.

## Классы

### `ResultsExtractor`

**Описание**: Класс `ResultsExtractor` предназначен для извлечения результатов из взаимодействий агентов и окружения. Он использует OpenAI для анализа текста и извлечения структурированных данных.

**Атрибуты**:
- `_extraction_prompt_template_path` (str): Путь к шаблону запроса для извлечения информации.
- `default_extraction_objective` (str): Цель извлечения информации по умолчанию.
- `default_situation` (str): Описание ситуации по умолчанию.
- `default_fields` (List[str] | None): Список полей для извлечения по умолчанию.
- `default_fields_hints` (dict | None): Подсказки для полей извлечения по умолчанию.
- `default_verbose` (bool): Флаг verbose-режима по умолчанию.
- `agent_extraction` (dict): Кэш последних результатов извлечения для агентов.
- `world_extraction` (dict): Кэш последних результатов извлечения для окружения.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `ResultsExtractor`.
- `extract_results_from_agents`: Извлекает результаты из списка агентов.
- `extract_results_from_agent`: Извлекает результаты из одного агента.
- `extract_results_from_world`: Извлекает результаты из окружения.
- `save_as_json`: Сохраняет последние результаты извлечения в файл JSON.
- `_get_default_values_if_necessary`: Возвращает значения по умолчанию, если аргументы не переданы.

## Методы класса

### `__init__`

```python
def __init__(self, 
             extraction_prompt_template_path: str = os.path.join(os.path.dirname(__file__), './prompts/interaction_results_extractor.mustache'),
             extraction_objective: str = "The main points present in the agents\' interactions history.",
             situation: str = "",
             fields: List[str] | None = None,
             fields_hints: dict | None = None,
             verbose: bool = False):
    """
    Инициализирует ResultsExtractor с параметрами по умолчанию.

    Args:
        extraction_prompt_template_path (str): Путь к шаблону запроса для извлечения. По умолчанию указывает на `./prompts/interaction_results_extractor.mustache`.
        extraction_objective (str): Цель извлечения по умолчанию. По умолчанию: "The main points present in the agents' interactions history.".
        situation (str): Ситуация для анализа по умолчанию. По умолчанию пустая строка.
        fields (List[str] | None, optional): Список полей для извлечения. По умолчанию `None`.
        fields_hints (dict | None, optional): Подсказки для полей извлечения. По умолчанию `None`.
        verbose (bool, optional): Флаг verbose-режима. Если `True`, будут выводиться отладочные сообщения. По умолчанию `False`.
    """
    ...
```

**Назначение**: Инициализирует объект `ResultsExtractor`, задавая пути к шаблонам, цели извлечения, ситуацию, поля и прочие параметры.

**Параметры**:
- `extraction_prompt_template_path` (str): Путь к шаблону запроса для извлечения.
- `extraction_objective` (str): Цель извлечения по умолчанию.
- `situation` (str): Описание ситуации по умолчанию.
- `fields` (List[str] | None): Список полей для извлечения по умолчанию.
- `fields_hints` (dict | None): Подсказки для полей извлечения по умолчанию.
- `verbose` (bool): Флаг verbose-режима по умолчанию.

**Примеры**:

```python
extractor = ResultsExtractor(verbose=True)
```

### `extract_results_from_agents`

```python
def extract_results_from_agents(self,
                                agents: List[TinyPerson],
                                extraction_objective: str | None = None,
                                situation: str | None = None,
                                fields: list | None = None,
                                fields_hints: dict | None = None,
                                verbose: bool | None = None) -> list:
    """
    Извлекает результаты из списка экземпляров TinyPerson.

    Args:
        agents (List[TinyPerson]): Список экземпляров TinyPerson, из которых нужно извлечь результаты.
        extraction_objective (str | None, optional): Цель извлечения.
        situation (str | None, optional): Ситуация для анализа.
        fields (list | None, optional): Список полей для извлечения.
        fields_hints (dict | None, optional): Подсказки для полей извлечения.
        verbose (bool | None, optional): Флаг verbose-режима.

    Returns:
        list: Список извлеченных результатов.
    """
    ...
```

**Назначение**: Извлекает результаты из списка агентов `TinyPerson`, используя заданные параметры извлечения или параметры по умолчанию.

**Параметры**:
- `agents` (List[TinyPerson]): Список агентов для извлечения результатов.
- `extraction_objective` (str | None): Цель извлечения (если не указана, используется значение по умолчанию).
- `situation` (str | None): Контекст ситуации для извлечения (если не указан, используется значение по умолчанию).
- `fields` (list | None): Список полей для извлечения (если не указан, используется значение по умолчанию).
- `fields_hints` (dict | None): Словарь подсказок для извлечения полей (если не указан, используется значение по умолчанию).
- `verbose` (bool | None): Флаг, определяющий, выводить ли отладочные сообщения (если не указан, используется значение по умолчанию).

**Как работает функция**:
- Функция итерируется по списку агентов `agents`.
- Для каждого агента вызывается метод `extract_results_from_agent`, чтобы извлечь результаты.
- Результаты добавляются в список `results`.
- В конце функция возвращает список `results`.

**Примеры**:
```python
from tinytroupe.agent import TinyPerson
from tinytroupe.extraction.results_extractor import ResultsExtractor

# Пример использования extract_results_from_agents
agent1 = TinyPerson(name='Alice')
agent2 = TinyPerson(name='Bob')
agents = [agent1, agent2]
extractor = ResultsExtractor()
results = extractor.extract_results_from_agents(agents, extraction_objective='Find main points')
print(results)
```

### `extract_results_from_agent`

```python
def extract_results_from_agent(self, 
                    tinyperson: TinyPerson, 
                    extraction_objective: str = "The main points present in the agent\'s interactions history.", 
                    situation: str = "", 
                    fields: list | None = None,
                    fields_hints: dict | None = None,
                    verbose: bool | None = None) -> dict | None:
    """
    Извлекает результаты из экземпляра TinyPerson.

    Args:
        tinyperson (TinyPerson): Экземпляр TinyPerson, из которого нужно извлечь результаты.
        extraction_objective (str, optional): Цель извлечения. По умолчанию: "The main points present in the agent's interactions history.".
        situation (str, optional): Ситуация для анализа. По умолчанию пустая строка.
        fields (list | None, optional): Список полей для извлечения.
        fields_hints (dict | None, optional): Подсказки для полей извлечения.
        verbose (bool | None, optional): Флаг verbose-режима.

    Returns:
        dict | None: Извлеченные результаты в виде словаря или None в случае ошибки.
    """
    ...
```

**Назначение**: Извлекает результаты из объекта `TinyPerson` на основе истории его взаимодействий.

**Параметры**:
- `tinyperson` (TinyPerson): Объект `TinyPerson`, из которого извлекаются результаты.
- `extraction_objective` (str): Цель извлечения (если не указана, используется значение по умолчанию).
- `situation` (str): Контекст ситуации для извлечения (если не указан, используется значение по умолчанию).
- `fields` (list | None): Список полей для извлечения (если не указан, используется значение по умолчанию).
- `fields_hints` (dict | None): Словарь подсказок для извлечения полей (если не указан, используется значение по умолчанию).
- `verbose` (bool | None): Флаг, определяющий, выводить ли отладочные сообщения (если не указан, используется значение по умолчанию).

**Как работает функция**:
- Функция сначала получает значения параметров, используя `_get_default_values_if_necessary`.
- Формирует сообщения для отправки в OpenAI, используя предоставленный шаблон (`_extraction_prompt_template_path`).
- Извлекает историю взаимодействий агента.
- Отправляет запрос в OpenAI и получает ответ.
- Извлекает JSON из ответа и кэширует результат.
- Возвращает извлеченный результат.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.extraction.results_extractor import ResultsExtractor

# Пример использования extract_results_from_agent
agent = TinyPerson(name='Alice')
extractor = ResultsExtractor()
result = extractor.extract_results_from_agent(agent, extraction_objective='Find main points')
print(result)
```

### `extract_results_from_world`

```python
def extract_results_from_world(self, 
                               tinyworld: TinyWorld, 
                               extraction_objective: str = "The main points that can be derived from the agents conversations and actions.", 
                               situation: str = "", 
                               fields: list | None = None,
                               fields_hints: dict | None = None,
                               verbose: bool | None = None) -> dict | None:
    """
    Извлекает результаты из экземпляра TinyWorld.

    Args:
        tinyworld (TinyWorld): Экземпляр TinyWorld, из которого нужно извлечь результаты.
        extraction_objective (str, optional): Цель извлечения. По умолчанию: "The main points that can be derived from the agents conversations and actions.".
        situation (str, optional): Ситуация для анализа. По умолчанию пустая строка.
        fields (list | None, optional): Список полей для извлечения.
        fields_hints (dict | None, optional): Подсказки для полей извлечения.
        verbose (bool | None, optional): Флаг verbose-режима.

    Returns:
        dict | None: Извлеченные результаты в виде словаря или None в случае ошибки.
    """
    ...
```

**Назначение**: Извлекает результаты из объекта `TinyWorld` на основе истории взаимодействий агентов в этом мире.

**Параметры**:
- `tinyworld` (TinyWorld): Объект `TinyWorld`, из которого извлекаются результаты.
- `extraction_objective` (str): Цель извлечения (если не указана, используется значение по умолчанию).
- `situation` (str): Контекст ситуации для извлечения (если не указан, используется значение по умолчанию).
- `fields` (list | None): Список полей для извлечения (если не указан, используется значение по умолчанию).
- `fields_hints` (dict | None): Словарь подсказок для извлечения полей (если не указан, используется значение по умолчанию).
- `verbose` (bool | None): Флаг, определяющий, выводить ли отладочные сообщения (если не указан, используется значение по умолчанию).

**Как работает функция**:
- Функция сначала получает значения параметров, используя `_get_default_values_if_necessary`.
- Формирует сообщения для отправки в OpenAI, используя предоставленный шаблон (`_extraction_prompt_template_path`).
- Извлекает историю взаимодействий в мире.
- Отправляет запрос в OpenAI и получает ответ.
- Извлекает JSON из ответа и кэширует результат.
- Возвращает извлеченный результат.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.extraction.results_extractor import ResultsExtractor

# Пример использования extract_results_from_world
world = TinyWorld(name='MyWorld')
extractor = ResultsExtractor()
result = extractor.extract_results_from_world(world, extraction_objective='Find main points')
print(result)
```

### `save_as_json`

```python
def save_as_json(self, filename: str, verbose: bool = False) -> None:
    """
    Сохраняет последние результаты извлечения в формате JSON.

    Args:
        filename (str): Имя файла для сохранения JSON.
        verbose (bool, optional): Флаг verbose-режима. Defaults to False.
    """
    ...
```

**Назначение**: Сохраняет последние результаты извлечения агентов и окружения в формате JSON в указанный файл.

**Параметры**:
- `filename` (str): Имя файла, в который нужно сохранить результаты.
- `verbose` (bool): Флаг, определяющий, выводить ли отладочные сообщения.

**Как работает функция**:
- Открывает файл с указанным именем в режиме записи.
- Сохраняет в файл JSON-представление словаря, содержащего результаты извлечения для агентов (`agent_extraction`) и окружения (`world_extraction`).
- Если включен режим verbose, выводит сообщение о том, в какой файл были сохранены результаты.

**Примеры**:

```python
from tinytroupe.extraction.results_extractor import ResultsExtractor

# Пример использования save_as_json
extractor = ResultsExtractor()
extractor.save_as_json('results.json', verbose=True)
```

### `_get_default_values_if_necessary`

```python
def _get_default_values_if_necessary(self,
                        extraction_objective: str | None,
                        situation: str | None,
                        fields: List[str] | None,
                        fields_hints: dict | None,
                        verbose: bool | None) -> tuple[str, str, List[str] | None, dict | None, bool]:

    """
    Возвращает значения по умолчанию, если аргументы не переданы.

    Args:
        extraction_objective (str | None): Цель извлечения.
        situation (str | None): Ситуация для анализа.
        fields (List[str] | None): Список полей для извлечения.
        fields_hints (dict | None): Подсказки для полей извлечения.
        verbose (bool | None): Флаг verbose-режима.

    Returns:
        tuple[str, str, List[str] | None, dict | None, bool]: Кортеж значений:
            - extraction_objective (str): Цель извлечения.
            - situation (str): Ситуация для анализа.
            - fields (List[str] | None): Список полей для извлечения.
            - fields_hints (dict | None): Подсказки для полей извлечения.
            - verbose (bool): Флаг verbose-режима.
    """
    ...
```

**Назначение**: Проверяет, были ли переданы значения для параметров `extraction_objective`, `situation`, `fields`, `fields_hints` и `verbose`. Если какое-либо из значений не было передано (то есть равно `None`), функция возвращает значение по умолчанию, хранящееся в атрибутах экземпляра класса `ResultsExtractor`.

**Параметры**:
- `extraction_objective` (str | None): Цель извлечения.
- `situation` (str | None): Ситуация для анализа.
- `fields` (List[str] | None): Список полей для извлечения.
- `fields_hints` (dict | None): Подсказки для полей извлечения.
- `verbose` (bool | None): Флаг verbose-режима.

**Как работает функция**:
- Если `extraction_objective` равно `None`, присваивает ему значение `self.default_extraction_objective`.
- Если `situation` равно `None`, присваивает ему значение `self.default_situation`.
- Если `fields` равно `None`, присваивает ему значение `self.default_fields`.
- Если `fields_hints` равно `None`, присваивает ему значение `self.default_fields_hints`.
- Если `verbose` равно `None`, присваивает ему значение `self.default_verbose`.
- Возвращает кортеж измененных (или исходных, если они не были `None`) значений.

**Примеры**:

```python
from tinytroupe.extraction.results_extractor import ResultsExtractor

# Пример использования _get_default_values_if_necessary
extractor = ResultsExtractor(default_extraction_objective='Default objective')
objective, _, _, _, _ = extractor._get_default_values_if_necessary(None, None, None, None, None)
print(objective)  # Выведет: Default objective
```
```python
extractor = ResultsExtractor(default_extraction_objective='Default objective')
objective, _, _, _, _ = extractor._get_default_values_if_necessary("New objective", None, None, None, None)
print(objective)
```
## Параметры класса

- `_extraction_prompt_template_path` (str): Путь к mustache-шаблону, используемому для формирования запросов к OpenAI.
- `default_extraction_objective` (str): Цель извлечения по умолчанию.
- `default_situation` (str): Контекст ситуации по умолчанию.
- `default_fields` (List[str] | None): Список полей для извлечения по умолчанию.
- `default_fields_hints` (dict | None): Подсказки для полей извлечения по умолчанию.
- `default_verbose` (bool): Флаг, определяющий, выводить ли отладочные сообщения по умолчанию.
- `agent_extraction` (dict): Словарь для кэширования результатов извлечения для агентов.
- `world_extraction` (dict): Словарь для кэширования результатов извлечения для окружения.