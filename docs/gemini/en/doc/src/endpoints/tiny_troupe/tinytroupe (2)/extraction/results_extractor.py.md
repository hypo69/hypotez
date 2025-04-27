# Модуль ResultsExtractor

## Обзор

Модуль `results_extractor.py` содержит класс `ResultsExtractor`, который используется для извлечения результатов из истории взаимодействий агентов (`TinyPerson`) и миров (`TinyWorld`) в `TinyTroupe` среде. Класс использует `OpenAI` API для обработки запросов на извлечение.

## Детали

`ResultsExtractor` предоставляет методы для извлечения результатов из отдельных агентов (`TinyPerson`) или всего мира (`TinyWorld`). Он использует шаблоны для генерации запросов к `OpenAI` API, и может извлекать информацию, используя подсказки для определения имен полей. Результаты кэшируются для ускорения последующих запросов.

## Классы

### `ResultsExtractor`

**Описание**: Класс для извлечения результатов из истории взаимодействий агентов и миров.

**Атрибуты**:

- `_extraction_prompt_template_path (str)`: Путь к шаблону запроса для извлечения.
- `default_extraction_objective (str)`:  Стандартная цель извлечения.
- `default_situation (str)`: Стандартная ситуация.
- `default_fields (List[str])`:  Стандартные имена полей для извлечения.
- `default_fields_hints (dict)`:  Стандартные подсказки для полей для извлечения.
- `default_verbose (bool)`:  Флаг для вывода отладочных сообщений.
- `agent_extraction (dict)`:  Кэш результатов извлечения для агентов.
- `world_extraction (dict)`:  Кэш результатов извлечения для миров.

**Методы**:

- `extract_results_from_agents(agents: List[TinyPerson], extraction_objective: str = None, situation: str = None, fields: list = None, fields_hints: dict = None, verbose: bool = None)`: Извлекает результаты из списка агентов `TinyPerson`.
- `extract_results_from_agent(tinyperson: TinyPerson, extraction_objective: str = "The main points present in the agent's interactions history.", situation: str = "", fields: list = None, fields_hints: dict = None, verbose: bool = None)`: Извлекает результаты из одного агента `TinyPerson`.
- `extract_results_from_world(tinyworld: TinyWorld, extraction_objective: str = "The main points that can be derived from the agents conversations and actions.", situation: str = "", fields: list = None, fields_hints: dict = None, verbose: bool = None)`: Извлекает результаты из мира `TinyWorld`.
- `save_as_json(filename: str, verbose: bool = False)`:  Сохраняет результаты последнего извлечения в формате JSON.
- `_get_default_values_if_necessary(extraction_objective: str, situation: str, fields: List[str], fields_hints: dict, verbose: bool)`:  Получает стандартные значения параметров, если они не были заданы.


## Функции

### `extract_results_from_agents`

**Цель**:  Извлекает результаты из списка агентов `TinyPerson`.

**Параметры**:

- `agents (List[TinyPerson])`: Список агентов, из которых необходимо извлечь результаты.
- `extraction_objective (str)`:  Цель извлечения.
- `situation (str)`: Ситуация, которую нужно учитывать.
- `fields (list)`: Список полей для извлечения. Если не задано, экстрактор сам определяет имена.
- `fields_hints (dict)`: Подсказки для полей, которые нужно извлечь. 
- `verbose (bool)`:  Флаг для вывода отладочных сообщений.


**Возвращает**:

- `List[dict]`: Список словарей с извлеченными результатами для каждого агента.


**Пример**:

```python
from tinytroupe.extraction.results_extractor import ResultsExtractor
from tinytroupe.agent import TinyPerson

# Создаем экземпляр класса ResultsExtractor
results_extractor = ResultsExtractor()

# Создаем список агентов TinyPerson
agents = [TinyPerson(name='Agent1'), TinyPerson(name='Agent2')]

# Извлекаем результаты из агентов
extracted_results = results_extractor.extract_results_from_agents(agents)

# Выводим результаты
print(extracted_results)
```


### `extract_results_from_agent`

**Цель**: Извлекает результаты из одного агента `TinyPerson`.

**Параметры**:

- `tinyperson (TinyPerson)`:  Экземпляр агента, из которого необходимо извлечь результаты.
- `extraction_objective (str)`: Цель извлечения.
- `situation (str)`: Ситуация, которую нужно учитывать.
- `fields (list)`: Список полей для извлечения. Если не задано, экстрактор сам определяет имена.
- `fields_hints (dict)`: Подсказки для полей, которые нужно извлечь. 
- `verbose (bool)`:  Флаг для вывода отладочных сообщений.


**Возвращает**:

- `dict`: Словарь с извлеченными результатами.


**Пример**:

```python
from tinytroupe.extraction.results_extractor import ResultsExtractor
from tinytroupe.agent import TinyPerson

# Создаем экземпляр класса ResultsExtractor
results_extractor = ResultsExtractor()

# Создаем экземпляр агента TinyPerson
agent = TinyPerson(name='Agent1')

# Извлекаем результаты из агента
extracted_results = results_extractor.extract_results_from_agent(agent)

# Выводим результаты
print(extracted_results)
```


### `extract_results_from_world`

**Цель**: Извлекает результаты из мира `TinyWorld`.

**Параметры**:

- `tinyworld (TinyWorld)`:  Экземпляр мира, из которого необходимо извлечь результаты.
- `extraction_objective (str)`: Цель извлечения.
- `situation (str)`: Ситуация, которую нужно учитывать.
- `fields (list)`: Список полей для извлечения. Если не задано, экстрактор сам определяет имена.
- `fields_hints (dict)`: Подсказки для полей, которые нужно извлечь. 
- `verbose (bool)`:  Флаг для вывода отладочных сообщений.


**Возвращает**:

- `dict`: Словарь с извлеченными результатами.


**Пример**:

```python
from tinytroupe.extraction.results_extractor import ResultsExtractor
from tinytroupe.environment import TinyWorld

# Создаем экземпляр класса ResultsExtractor
results_extractor = ResultsExtractor()

# Создаем экземпляр мира TinyWorld
world = TinyWorld(name='World1')

# Извлекаем результаты из мира
extracted_results = results_extractor.extract_results_from_world(world)

# Выводим результаты
print(extracted_results)
```


### `save_as_json`

**Цель**: Сохраняет результаты последнего извлечения в формате JSON.

**Параметры**:

- `filename (str)`: Имя файла, в который нужно сохранить результаты.
- `verbose (bool)`:  Флаг для вывода отладочных сообщений.


**Возвращает**:

- `None`


**Пример**:

```python
from tinytroupe.extraction.results_extractor import ResultsExtractor

# Создаем экземпляр класса ResultsExtractor
results_extractor = ResultsExtractor()

# Извлекаем результаты из агентов или мира (не показано в этом примере)

# Сохраняем результаты в файл results.json
results_extractor.save_as_json('results.json')
```


### `_get_default_values_if_necessary`

**Цель**: Получает стандартные значения параметров, если они не были заданы.

**Параметры**:

- `extraction_objective (str)`: Цель извлечения.
- `situation (str)`: Ситуация, которую нужно учитывать.
- `fields (List[str])`: Список полей для извлечения. 
- `fields_hints (dict)`: Подсказки для полей, которые нужно извлечь. 
- `verbose (bool)`:  Флаг для вывода отладочных сообщений.


**Возвращает**:

- `tuple`: Кортеж из пяти значений: `extraction_objective`, `situation`, `fields`, `fields_hints`, `verbose`, 
    используя стандартные значения по умолчанию, если соответствующие аргументы `None`.



**Как работает функция**:

1. Проверяет, являются ли входные параметры `None`.
2. Если параметр `None`, присваивает стандартное значение из соответствующего атрибута экземпляра `ResultsExtractor`.
3. Возвращает кортеж из пяти значений, используя переданные параметры или стандартные значения по умолчанию.

**Примеры**:

```python
from tinytroupe.extraction.results_extractor import ResultsExtractor

# Создаем экземпляр класса ResultsExtractor
results_extractor = ResultsExtractor()

# Передаем значения параметров
extraction_objective = "Новая цель извлечения"
situation = "Новая ситуация"
fields = ["поле1", "поле2"]
fields_hints = {"поле1": "Подсказка для поля1", "поле2": "Подсказка для поля2"}
verbose = True

# Получаем стандартные значения, если значения None
extraction_objective, situation, fields, fields_hints, verbose = results_extractor._get_default_values_if_necessary(
    extraction_objective, situation, fields, fields_hints, verbose
)

# Выводим полученные значения
print(f"extraction_objective: {extraction_objective}")
print(f"situation: {situation}")
print(f"fields: {fields}")
print(f"fields_hints: {fields_hints}")
print(f"verbose: {verbose}")
```

## Примеры

```python
from tinytroupe.extraction.results_extractor import ResultsExtractor
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

# Создаем экземпляр класса ResultsExtractor
results_extractor = ResultsExtractor()

# Создаем экземпляр агента TinyPerson
agent = TinyPerson(name='Agent1')

# Извлекаем результаты из агента
extracted_results = results_extractor.extract_results_from_agent(agent, extraction_objective="Каковы основные выводы из взаимодействия агента?", situation="Агент взаимодействует с пользователем.")

# Выводим результаты
print(extracted_results)

# Создаем экземпляр мира TinyWorld
world = TinyWorld(name='World1')

# Извлекаем результаты из мира
extracted_results = results_extractor.extract_results_from_world(world, fields=["Выводы", "Рекомендации"], verbose=True)

# Выводим результаты
print(extracted_results)

# Сохраняем результаты в файл results.json
results_extractor.save_as_json('results.json', verbose=True)
```