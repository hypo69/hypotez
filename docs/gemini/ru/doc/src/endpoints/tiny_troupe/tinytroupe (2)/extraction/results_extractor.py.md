# Модуль для извлечения результатов из взаимодействий агентов и окружения
## Обзор

Модуль `results_extractor.py` предназначен для извлечения информации из истории взаимодействий агентов (`TinyPerson`) в виртуальном мире (`TinyWorld`). Он использует шаблоны для формирования запросов к моделям OpenAI, анализирует ответы и сохраняет результаты в формате JSON.

## Подробнее

Модуль содержит класс `ResultsExtractor`, который инициализируется с путем к шаблону промпта, целью извлечения, ситуацией, полями для извлечения и их подсказками. Он предоставляет методы для извлечения результатов как из отдельных агентов, так и из всего виртуального мира.

## Классы

### `ResultsExtractor`
Описание: Класс предназначен для извлечения результатов из взаимодействий агентов и окружения.

**Атрибуты**:
- `_extraction_prompt_template_path` (str): Путь к шаблону промпта для извлечения информации.
- `default_extraction_objective` (str): Цель извлечения по умолчанию.
- `default_situation` (str): Ситуация по умолчанию.
- `default_fields` (List[str]): Список полей для извлечения по умолчанию.
- `default_fields_hints` (dict): Подсказки для полей извлечения по умолчанию.
- `default_verbose` (bool): Флаг для отображения отладочных сообщений по умолчанию.
- `agent_extraction` (dict): Кэш последних извлечений для агентов.
- `world_extraction` (dict): Кэш последних извлечений для виртуального мира.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `ResultsExtractor`.
- `extract_results_from_agents`: Извлекает результаты из списка агентов.
- `extract_results_from_agent`: Извлекает результаты из отдельного агента.
- `extract_results_from_world`: Извлекает результаты из виртуального мира.
- `save_as_json`: Сохраняет последние результаты извлечения в файл JSON.
- `_get_default_values_if_necessary`: Возвращает значения по умолчанию, если аргументы не переданы.

### `__init__`
```python
def __init__(self, 
             extraction_prompt_template_path:str = os.path.join(os.path.dirname(__file__), './prompts/interaction_results_extractor.mustache'),
             extraction_objective:str = "The main points present in the agents\' interactions history.",
             situation:str = "",
             fields:List[str] = None,
             fields_hints:dict = None,
             verbose:bool = False):
    """
    Initializes the ResultsExtractor with default parameters.

    Args:
        extraction_prompt_template_path (str): The path to the extraction prompt template.
        extraction_objective (str): The default extraction objective.
        situation (str): The default situation to consider.
        fields (List[str], optional): The default fields to extract. Defaults to None.
        fields_hints (dict, optional): The default hints for the fields to extract. Defaults to None.
        verbose (bool, optional): Whether to print debug messages by default. Defaults to False.
    """
    ...
```
**Назначение**: Инициализирует объект `ResultsExtractor`, устанавливая путь к шаблону промпта, цель извлечения, ситуацию, поля и подсказки для извлечения, а также флаг verbose.

**Параметры**:
- `extraction_prompt_template_path` (str): Путь к файлу шаблона mustache, используемому для генерации запросов. По умолчанию указывает на `interaction_results_extractor.mustache` в подкаталоге `prompts`.
- `extraction_objective` (str): Цель извлечения, описывающая, какую информацию нужно извлечь из истории взаимодействий. По умолчанию - "The main points present in the agents' interactions history."
- `situation` (str): Описание ситуации, контекст, в котором происходит извлечение. По умолчанию пустая строка.
- `fields` (List[str], optional): Список полей, которые необходимо извлечь. Если не указан, экстрактор сам решает, какие поля использовать. По умолчанию `None`.
- `fields_hints` (dict, optional): Словарь с подсказками для полей, где ключи - это имена полей, а значения - строки с подсказками. По умолчанию `None`.
- `verbose` (bool, optional): Флаг, определяющий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:

Функция инициализирует класс `ResultsExtractor`, сохраняя переданные параметры в соответствующие атрибуты экземпляра класса. Также инициализирует атрибуты `agent_extraction` и `world_extraction` пустыми словарями, которые будут использоваться для кэширования результатов извлечения.

**Примеры**:

```python
extractor = ResultsExtractor(
    extraction_prompt_template_path='./prompts/custom_extractor.mustache',
    extraction_objective='Extract key decisions made by agents',
    situation='Analyzing a negotiation scenario',
    fields=['decision', 'rationale'],
    fields_hints={'decision': 'The final decision made', 'rationale': 'The reason behind the decision'},
    verbose=True
)
```

### `extract_results_from_agents`
```python
def extract_results_from_agents(self,
                                    agents:List[TinyPerson],
                                    extraction_objective:str=None,
                                    situation:str =None,
                                    fields:list=None,
                                    fields_hints:dict=None,
                                    verbose:bool=None):
    """
    Extracts results from a list of TinyPerson instances.

    Args:
        agents (List[TinyPerson]): The list of TinyPerson instances to extract results from.
        extraction_objective (str): The extraction objective.
        situation (str): The situation to consider.
        fields (list, optional): The fields to extract. If None, the extractor will decide what names to use. 
            Defaults to None.
        fields_hints (dict, optional): Hints for the fields to extract. Maps field names to strings with the hints. Defaults to None.
        verbose (bool, optional): Whether to print debug messages. Defaults to False.

    
    """
    ...
```

**Назначение**: Извлекает результаты из списка экземпляров `TinyPerson`.

**Параметры**:
- `agents` (List[TinyPerson]): Список экземпляров `TinyPerson`, из которых нужно извлечь результаты.
- `extraction_objective` (str, optional): Цель извлечения. Если не указана, будет использована цель по умолчанию.
- `situation` (str, optional): Ситуация, которую следует учитывать. Если не указана, будет использована ситуация по умолчанию.
- `fields` (list, optional): Список полей для извлечения. Если не указан, экстрактор определит, какие имена использовать. По умолчанию `None`.
- `fields_hints` (dict, optional): Подсказки для полей для извлечения. Сопоставляет имена полей со строками с подсказками. По умолчанию `None`.
- `verbose` (bool, optional): Флаг, указывающий, нужно ли печатать отладочные сообщения. По умолчанию `False`.

**Как работает функция**:
Функция перебирает список агентов и вызывает `extract_results_from_agent` для каждого агента, собирая результаты в список.

**Примеры**:
```python
agents = [TinyPerson(...), TinyPerson(...)]
results = extractor.extract_results_from_agents(agents, extraction_objective="Find key decisions")
```

### `extract_results_from_agent`
```python
def extract_results_from_agent(self, 
                    tinyperson:TinyPerson, 
                    extraction_objective:str="The main points present in the agent\'s interactions history.", 
                    situation:str = "", 
                    fields:list=None,
                    fields_hints:dict=None,
                    verbose:bool=None):
    """
    Extracts results from a TinyPerson instance.

    Args:
        tinyperson (TinyPerson): The TinyPerson instance to extract results from.
        extraction_objective (str): The extraction objective.
        situation (str): The situation to consider.
        fields (list, optional): The fields to extract. If None, the extractor will decide what names to use. 
            Defaults to None.
        fields_hints (dict, optional): Hints for the fields to extract. Maps field names to strings with the hints. Defaults to None.
        verbose (bool, optional): Whether to print debug messages. Defaults to False.
    """
    ...
```

**Назначение**: Извлекает результаты из экземпляра `TinyPerson`.

**Параметры**:
- `tinyperson` (TinyPerson): Экземпляр `TinyPerson`, из которого нужно извлечь результаты.
- `extraction_objective` (str, optional): Цель извлечения. По умолчанию "The main points present in the agent's interactions history.".
- `situation` (str, optional): Ситуация, которую следует учитывать. По умолчанию "".
- `fields` (list, optional): Список полей для извлечения. Если `None`, экстрактор сам решает, какие имена использовать. По умолчанию `None`.
- `fields_hints` (dict, optional): Подсказки для полей извлечения. Сопоставляет имена полей со строками с подсказками. По умолчанию `None`.
- `verbose` (bool, optional): Флаг, определяющий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:

1.  **Получение значений по умолчанию**: Использует метод `_get_default_values_if_necessary` для получения значений параметров, если они не были переданы явно.
2.  **Формирование сообщений**:
    *   Создает список `messages` для взаимодействия с моделью OpenAI.
    *   Формирует словарь `rendering_configs` для передачи в шаблон. Если указаны поля `fields` и/или `fields_hints`, они добавляются в `rendering_configs`.
    *   Добавляет системное сообщение с использованием шаблона, прочитанного из `self._extraction_prompt_template_path` и отрендеренного с помощью `chevron.render`.
3.  **Подготовка истории взаимодействий**:
    *   Получает историю взаимодействий агента с помощью `tinyperson.pretty_current_interactions(max_content_length=None)`.
4.  **Формирование запроса на извлечение**:
    *   Создает строку `extraction_request_prompt`, содержащую цель извлечения, ситуацию и историю взаимодействий агента.
5.  **Отправка запроса в OpenAI**:
    *   Добавляет сообщение пользователя с запросом на извлечение в список `messages`.
    *   Отправляет запрос в OpenAI с помощью `openai_utils.client().send_message`, устанавливая температуру на 0.0.
6.  **Обработка результата**:
    *   Извлекает JSON из ответа OpenAI с помощью `utils.extract_json`.
    *   Кэширует результат в `self.agent_extraction[tinyperson.name]`.
7.  **Возврат результата**: Возвращает извлеченный результат.

**Примеры**:

```python
agent = TinyPerson(...)
result = extractor.extract_results_from_agent(agent, extraction_objective="Find the agent's final decision")
```

### `extract_results_from_world`
```python
def extract_results_from_world(self, 
                                   tinyworld:TinyWorld, 
                                   extraction_objective:str="The main points that can be derived from the agents conversations and actions.", 
                                   situation:str="", 
                                   fields:list=None,
                                   fields_hints:dict=None,
                                   verbose:bool=None):
    """
    Extracts results from a TinyWorld instance.

    Args:
        tinyworld (TinyWorld): The TinyWorld instance to extract results from.
        extraction_objective (str): The extraction objective.
        situation (str): The situation to consider.
        fields (list, optional): The fields to extract. If None, the extractor will decide what names to use. 
            Defaults to None.
        verbose (bool, optional): Whether to print debug messages. Defaults to False.
    """
    ...
```

**Назначение**: Извлекает результаты из экземпляра `TinyWorld`.

**Параметры**:
- `tinyworld` (TinyWorld): Экземпляр `TinyWorld`, из которого нужно извлечь результаты.
- `extraction_objective` (str, optional): Цель извлечения. По умолчанию "The main points that can be derived from the agents conversations and actions.".
- `situation` (str, optional): Ситуация, которую следует учитывать. По умолчанию "".
- `fields` (list, optional): Список полей для извлечения. Если `None`, экстрактор сам решает, какие имена использовать. По умолчанию `None`.
- `fields_hints` (dict, optional):  Словарь с подсказками для полей, где ключи - это имена полей, а значения - строки с подсказками. По умолчанию `None`.
- `verbose` (bool, optional): Флаг, определяющий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:

1.  **Получение значений по умолчанию**: Использует метод `_get_default_values_if_necessary` для получения значений параметров, если они не были переданы явно.
2.  **Формирование сообщений**:
    *   Создает список `messages` для взаимодействия с моделью OpenAI.
    *   Формирует словарь `rendering_configs` для передачи в шаблон. Если указаны поля `fields` и/или `fields_hints`, они добавляются в `rendering_configs`.
    *   Добавляет системное сообщение с использованием шаблона, прочитанного из `self._extraction_prompt_template_path` и отрендеренного с помощью `chevron.render`.
3.  **Подготовка истории взаимодействий**:
    *   Получает историю взаимодействий агентов в мире с помощью `tinyworld.pretty_current_interactions(max_content_length=None)`.
4.  **Формирование запроса на извлечение**:
    *   Создает строку `extraction_request_prompt`, содержащую цель извлечения, ситуацию и историю взаимодействий агентов в мире.
5.  **Отправка запроса в OpenAI**:
    *   Добавляет сообщение пользователя с запросом на извлечение в список `messages`.
    *   Отправляет запрос в OpenAI с помощью `openai_utils.client().send_message`, устанавливая температуру на 0.0.
6.  **Обработка результата**:
    *   Извлекает JSON из ответа OpenAI с помощью `utils.extract_json`.
    *   Кэширует результат в `self.world_extraction[tinyworld.name]`.
7.  **Возврат результата**: Возвращает извлеченный результат.

**Примеры**:

```python
world = TinyWorld(...)
result = extractor.extract_results_from_world(world, extraction_objective="Find the overall outcome of the simulation")
```

### `save_as_json`
```python
def save_as_json(self, filename:str, verbose:bool=False):
    """
    Saves the last extraction results as JSON.

    Args:
        filename (str): The filename to save the JSON to.
        verbose (bool, optional): Whether to print debug messages. Defaults to False.
    """
    ...
```

**Назначение**: Сохраняет последние результаты извлечения в формате JSON в указанный файл.

**Параметры**:
- `filename` (str): Имя файла для сохранения JSON.
- `verbose` (bool, optional): Флаг, определяющий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:

1.  Открывает файл с указанным именем в режиме записи (`'w'`).
2.  Записывает в файл JSON, содержащий два ключа:
    *   `"agent_extractions"`: Значение - словарь `self.agent_extraction`.
    *   `"world_extraction"`: Значение - словарь `self.world_extraction`.
    JSON форматируется с отступами (`indent=4`) для удобства чтения.

**Примеры**:

```python
extractor.save_as_json('extraction_results.json', verbose=True)
```

### `_get_default_values_if_necessary`
```python
def _get_default_values_if_necessary(self,
                        extraction_objective:str,
                        situation:str,
                        fields:List[str],
                        fields_hints:dict,
                        verbose:bool):
    
    if extraction_objective is None:
        extraction_objective = self.default_extraction_objective

    if situation is None:
        situation = self.default_situation

    if fields is None:
        fields = self.default_fields

    if fields_hints is None:
        fields_hints = self.default_fields_hints

    if verbose is None:
        verbose = self.default_verbose

    return extraction_objective, situation, fields, fields_hints, verbose
```

**Назначение**: Возвращает значения параметров, заменяя `None` значениями по умолчанию, если необходимо.

**Параметры**:
- `extraction_objective` (str): Цель извлечения.
- `situation` (str): Ситуация.
- `fields` (List[str]): Список полей.
- `fields_hints` (dict): Словарь подсказок для полей.
- `verbose` (bool): Флаг verbose.

**Как работает функция**:

Функция проверяет, является ли каждый из входных параметров `None`. Если параметр равен `None`, он заменяется соответствующим значением по умолчанию из атрибутов экземпляра класса (`self.default_extraction_objective`, `self.default_situation`, `self.default_fields`, `self.default_fields_hints`, `self.default_verbose`).
В конце функция возвращает кортеж, содержащий (возможно, обновленные) значения всех пяти параметров.

**Примеры**:

```python
extraction_objective, situation, fields, fields_hints, verbose = extractor._get_default_values_if_necessary(
    None, "Some situation", None, {}, None
)
```
В этом примере `extraction_objective` будет заменена на `self.default_extraction_objective`, `fields` на `self.default_fields`, `verbose` на `self.default_verbose`. `situation` останется "Some situation", a `fields_hints` останется {}.