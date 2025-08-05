# Модуль извлечения результатов (`hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/extraction/results_extractor.py`)

## Обзор

Этот модуль содержит класс `ResultsExtractor`, который используется для извлечения результатов из модели `TinyTroupe`,
а именно из истории взаимодействия агентов и среды. 

## Подробности

Класс `ResultsExtractor` обеспечивает функциональность для извлечения ключевых моментов из истории взаимодействия агентов и среды. Он использует модель `TinyTroupe` для анализа истории и получения результатов, соответствующих заданному объекту и ситуации. 

## Классы

### `ResultsExtractor`

**Описание**: Класс, ответственный за извлечение результатов из истории взаимодействий агентов и среды.
**Наследует**: Нет

**Атрибуты**:

- `_extraction_prompt_template_path` (str): Путь к шаблону подсказки для извлечения результатов.
- `default_extraction_objective` (str): Объект извлечения по умолчанию.
- `default_situation` (str): Ситуация по умолчанию.
- `default_fields` (List[str]): Поля для извлечения по умолчанию.
- `default_fields_hints` (dict): Намеки для полей для извлечения по умолчанию.
- `default_verbose` (bool): Устанавливает режим verbose (вывод отладочной информации).
- `agent_extraction` (dict): Словарь для кеширования результатов извлечения для каждого агента.
- `world_extraction` (dict): Словарь для кеширования результатов извлечения для среды.

**Методы**:

- `extract_results_from_agents(agents:List[TinyPerson], extraction_objective:str=None, situation:str =None, fields:list=None, fields_hints:dict=None, verbose:bool=None)`: Извлекает результаты из списка объектов `TinyPerson`.
    - **Параметры**: 
        - `agents` (List[TinyPerson]): Список агентов, из которых нужно извлечь результаты.
        - `extraction_objective` (str): Объект извлечения.
        - `situation` (str): Ситуация, которую нужно учитывать.
        - `fields` (list): Список полей для извлечения. Если None, экстрактор самостоятельно определит имена. 
        - `fields_hints` (dict): Намеки для полей для извлечения. Сопоставляет имена полей с подсказками в виде строк.
        - `verbose` (bool): Устанавливает режим verbose.
    - **Возвращает**: `List[dict]`: Список словарей, содержащих результаты извлечения для каждого агента. 

- `extract_results_from_agent(tinyperson:TinyPerson, extraction_objective:str="The main points present in the agent's interactions history.", situation:str = "", fields:list=None, fields_hints:dict=None, verbose:bool=None)`: Извлекает результаты из объекта `TinyPerson`.
    - **Параметры**: 
        - `tinyperson` (TinyPerson): Объект `TinyPerson`, из которого нужно извлечь результаты.
        - `extraction_objective` (str): Объект извлечения.
        - `situation` (str): Ситуация, которую нужно учитывать.
        - `fields` (list): Список полей для извлечения. Если None, экстрактор самостоятельно определит имена. 
        - `fields_hints` (dict): Намеки для полей для извлечения. Сопоставляет имена полей с подсказками в виде строк.
        - `verbose` (bool): Устанавливает режим verbose.
    - **Возвращает**: `dict`: Словарь, содержащий результаты извлечения для агента.

- `extract_results_from_world(tinyworld:TinyWorld, extraction_objective:str="The main points that can be derived from the agents conversations and actions.", situation:str="", fields:list=None, fields_hints:dict=None, verbose:bool=None)`: Извлекает результаты из объекта `TinyWorld`.
    - **Параметры**: 
        - `tinyworld` (TinyWorld): Объект `TinyWorld`, из которого нужно извлечь результаты.
        - `extraction_objective` (str): Объект извлечения.
        - `situation` (str): Ситуация, которую нужно учитывать.
        - `fields` (list): Список полей для извлечения. Если None, экстрактор самостоятельно определит имена. 
        - `fields_hints` (dict): Намеки для полей для извлечения. Сопоставляет имена полей с подсказками в виде строк.
        - `verbose` (bool): Устанавливает режим verbose.
    - **Возвращает**: `dict`: Словарь, содержащий результаты извлечения для среды.

- `save_as_json(filename:str, verbose:bool=False)`: Сохраняет результаты последнего извлечения в JSON-файл.
    - **Параметры**: 
        - `filename` (str): Имя файла для сохранения JSON.
        - `verbose` (bool): Устанавливает режим verbose.
    - **Возвращает**: `None`

- `_get_default_values_if_necessary(extraction_objective:str, situation:str, fields:List[str], fields_hints:dict, verbose:bool)`: Возвращает значения по умолчанию, если переданы None.
    - **Параметры**: 
        - `extraction_objective` (str): Объект извлечения.
        - `situation` (str): Ситуация, которую нужно учитывать.
        - `fields` (list): Список полей для извлечения.
        - `fields_hints` (dict): Намеки для полей для извлечения.
        - `verbose` (bool): Устанавливает режим verbose.
    - **Возвращает**: `tuple`: Кортеж, содержащий значения по умолчанию для объекта, ситуации, полей, намеков и режима verbose.

**Принцип работы**:

Класс `ResultsExtractor` использует шаблон подсказки для извлечения результатов. Шаблон подсказки задает конфигурацию модели, которая будет использоваться для анализа истории. 
Класс предоставляет методы для извлечения результатов как из отдельных агентов, так и из всей среды.  

Внутри функций `extract_results_from_agents`, `extract_results_from_agent` и `extract_results_from_world` происходит следующее:

1. **Формирование запроса**: Формируется запрос к модели с использованием шаблона подсказки, истории взаимодействия агентов и среды, а также заданного объекта и ситуации.
2. **Отправка запроса**: Запрос отправляется в модель `TinyTroupe` с использованием библиотеки `openai_utils`.
3. **Обработка ответа**: Модель возвращает ответ, который преобразуется в JSON-формат с помощью функции `utils.extract_json`.
4. **Сохранение результата**: Результаты сохраняются в кэш для дальнейшего использования.

**Примеры**:

```python
from tinytroupe.extraction import ResultsExtractor
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

# Создание экземпляра класса ResultsExtractor
extractor = ResultsExtractor()

# Создание агента и среды
agent = TinyPerson(name='Alice')
world = TinyWorld(name='My World')

# Извлечение результатов из агента
result = extractor.extract_results_from_agent(agent, extraction_objective='What are the main points Alice discussed?', situation='Alice is having a conversation about a new product.')
print(result)

# Извлечение результатов из среды
result = extractor.extract_results_from_world(world, extraction_objective='What are the key findings from the agents\' interactions?', situation='The agents are discussing a business plan.')
print(result)

# Сохранение результатов в файл
extractor.save_as_json('results.json')
```
## Внутренние функции

- `_get_default_values_if_necessary(extraction_objective:str, situation:str, fields:List[str], fields_hints:dict, verbose:bool)`: Функция, которая возвращает значения по умолчанию, если переданы None. 

**Параметры**: 

- `extraction_objective` (str): Объект извлечения.
- `situation` (str): Ситуация, которую нужно учитывать.
- `fields` (list): Список полей для извлечения.
- `fields_hints` (dict): Намеки для полей для извлечения.
- `verbose` (bool): Устанавливает режим verbose.

**Возвращает**: `tuple`: Кортеж, содержащий значения по умолчанию для объекта, ситуации, полей, намеков и режима verbose.

**Принцип работы**:

Функция проверяет, переданы ли в качестве параметров None. Если да, то функция использует значения по умолчанию из атрибутов класса `ResultsExtractor`.