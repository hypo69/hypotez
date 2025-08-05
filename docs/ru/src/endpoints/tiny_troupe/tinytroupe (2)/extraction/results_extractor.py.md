# Модуль `results_extractor.py`

## Обзор

Модуль предназначен для извлечения результатов из взаимодействий агентов в среде `tinytroupe`. Он содержит класс `ResultsExtractor`, который использует шаблоны для формирования запросов к OpenAI и извлекает структурированные данные в формате JSON из ответов.

## Подробнее

Модуль позволяет извлекать результаты как из отдельных агентов (`TinyPerson`), так и из всей среды (`TinyWorld`). Результаты извлекаются на основе истории взаимодействий агентов, с учетом заданной цели извлечения (`extraction_objective`) и контекста (`situation`). Извлеченные результаты могут быть сохранены в формате JSON.

## Классы

### `ResultsExtractor`

**Описание**: Класс для извлечения результатов из взаимодействий агентов.

**Атрибуты**:
- `_extraction_prompt_template_path` (str): Путь к шаблону запроса для извлечения данных.
- `default_extraction_objective` (str): Цель извлечения по умолчанию.
- `default_situation` (str): Контекст по умолчанию.
- `default_fields` (List[str]): Список полей для извлечения по умолчанию.
- `default_fields_hints` (dict): Подсказки для полей извлечения по умолчанию.
- `default_verbose` (bool): Флаг для отображения отладочных сообщений по умолчанию.
- `agent_extraction` (dict): Кэш для последних результатов извлечения для агентов.
- `world_extraction` (dict): Кэш для последних результатов извлечения для среды.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `ResultsExtractor`.
- `extract_results_from_agents`: Извлекает результаты из списка агентов.
- `extract_results_from_agent`: Извлекает результаты из одного агента.
- `extract_results_from_world`: Извлекает результаты из среды.
- `save_as_json`: Сохраняет последние результаты извлечения в файл JSON.
- `_get_default_values_if_necessary`: Возвращает значения по умолчанию, если необходимые параметры не заданы.

## Методы класса

### `__init__`

```python
def __init__(self, 
             extraction_prompt_template_path: str = os.path.join(os.path.dirname(__file__), './prompts/interaction_results_extractor.mustache'),
             extraction_objective: str = "The main points present in the agents\' interactions history.",
             situation: str = "",
             fields: List[str] = None,
             fields_hints: dict = None,
             verbose: bool = False):
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

**Назначение**: Инициализирует класс `ResultsExtractor` значениями по умолчанию.

**Параметры**:
- `extraction_prompt_template_path` (str): Путь к файлу шаблона запроса для извлечения данных. По умолчанию используется файл `interaction_results_extractor.mustache`, расположенный в поддиректории `prompts`.
- `extraction_objective` (str): Основная цель извлечения информации из истории взаимодействий агентов. По умолчанию: "The main points present in the agents' interactions history."
- `situation` (str): Описание ситуации или контекста, в котором происходит взаимодействие агентов. По умолчанию пустая строка.
- `fields` (List[str], optional): Список полей, которые необходимо извлечь из истории взаимодействий. Если не указан, извлекаются все доступные поля. По умолчанию `None`.
- `fields_hints` (dict, optional): Словарь, содержащий подсказки для каждого поля извлечения. Ключи словаря - названия полей, значения - строки с подсказками. По умолчанию `None`.
- `verbose` (bool, optional): Флаг, определяющий, нужно ли выводить отладочные сообщения в процессе извлечения. По умолчанию `False`.

**Как работает функция**:
- Функция инициализирует атрибуты экземпляра класса, сохраняя переданные значения параметров.
- Устанавливает значения по умолчанию для цели извлечения, ситуации, списка полей, подсказок для полей и флага отладки.
- Инициализирует пустые словари для хранения кэша результатов извлечения для агентов (`agent_extraction`) и среды (`world_extraction`).

**Примеры**:

```python
extractor = ResultsExtractor(verbose=True)
```

```python
extractor = ResultsExtractor(extraction_objective="Extract the sentiment of each agent.")
```

### `extract_results_from_agents`

```python
def extract_results_from_agents(self,
                                agents: List[TinyPerson],
                                extraction_objective: str = None,
                                situation: str = None,
                                fields: list = None,
                                fields_hints: dict = None,
                                verbose: bool = None):
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
- `agents` (List[TinyPerson]): Список экземпляров `TinyPerson`, из которых необходимо извлечь результаты.
- `extraction_objective` (str, optional): Цель извлечения. Если не указана, используется значение по умолчанию.
- `situation` (str, optional): Ситуация для рассмотрения. Если не указана, используется значение по умолчанию.
- `fields` (list, optional): Список полей для извлечения. Если не указан, извлекаются все доступные поля. По умолчанию `None`.
- `fields_hints` (dict, optional): Подсказки для полей извлечения. Отображает имена полей в строки с подсказками. По умолчанию `None`.
- `verbose` (bool, optional): Флаг для отображения отладочных сообщений. По умолчанию `False`.

**Возвращает**:
- `list`: Список результатов извлечения, где каждый элемент соответствует результату извлечения из одного агента.

**Как работает функция**:
- Функция итерируется по списку агентов (`agents`).
- Для каждого агента вызывает метод `extract_results_from_agent` для извлечения результатов.
- Добавляет полученный результат в список `results`.
- Возвращает список `results`, содержащий результаты извлечения для каждого агента.

**Примеры**:

```python
agents = [TinyPerson(...), TinyPerson(...)]
results = extractor.extract_results_from_agents(agents, extraction_objective="...")
```

### `extract_results_from_agent`

```python
def extract_results_from_agent(self, 
                    tinyperson: TinyPerson, 
                    extraction_objective: str = "The main points present in the agent\'s interactions history.", 
                    situation: str = "", 
                    fields: list = None,
                    fields_hints: dict = None,
                    verbose: bool = None):
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
- `tinyperson` (TinyPerson): Экземпляр `TinyPerson`, из которого необходимо извлечь результаты.
- `extraction_objective` (str, optional): Цель извлечения. По умолчанию "The main points present in the agent's interactions history.".
- `situation` (str, optional): Ситуация для рассмотрения. По умолчанию пустая строка.
- `fields` (list, optional): Список полей для извлечения. Если `None`, извлекатель решает, какие имена использовать. По умолчанию `None`.
- `fields_hints` (dict, optional): Подсказки для полей для извлечения. Сопоставляет имена полей со строками с подсказками. По умолчанию `None`.
- `verbose` (bool, optional): Определяет, нужно ли печатать отладочные сообщения. По умолчанию `False`.

**Возвращает**:
- `dict | None`: Результат извлечения в формате JSON или `None`, если извлечение не удалось.

**Как работает функция**:
1.  **Получение значений по умолчанию**:
    *   Вызывает `self._get_default_values_if_necessary()` для получения значений по умолчанию для `extraction_objective`, `situation`, `fields`, `fields_hints` и `verbose`, если они не были предоставлены.
2.  **Подготовка сообщений**:
    *   Инициализирует пустой список `messages`.
    *   Инициализирует словарь `rendering_configs` для хранения конфигураций рендеринга.
    *   Если `fields` предоставлены, добавляет их в виде строки, разделенной запятыми, в `rendering_configs` под ключом `"fields"`.
    *   Если `fields_hints` предоставлены, преобразует их в список пар ключ-значение и добавляет в `rendering_configs` под ключом `"fields_hints"`.
    *   Добавляет системное сообщение в список `messages`. Это сообщение формируется с использованием шаблона, расположенного по пути `self._extraction_prompt_template_path`, и заполняется данными из `rendering_configs`.
3.  **Формирование истории взаимодействий**:
    *   Получает историю взаимодействий агента с помощью `tinyperson.pretty_current_interactions(max_content_length=None)`.
4.  **Формирование запроса на извлечение**:
    *   Создает строку `extraction_request_prompt`, содержащую цель извлечения, ситуацию и историю взаимодействий агента.
    *   Добавляет сообщение пользователя с `extraction_request_prompt` в список `messages`.
5.  **Отправка сообщения в OpenAI**:
    *   Отправляет список сообщений в OpenAI с помощью `openai_utils.client().send_message()`.
    *   Устанавливает температуру `0.0`, `frequency_penalty=0.0` и `presence_penalty=0.0` для получения более детерминированных результатов.
6.  **Обработка ответа**:
    *   Логирует и, если `verbose=True`, выводит отладочное сообщение, содержащее необработанный ответ от OpenAI.
    *   Если получен ответ от OpenAI, извлекает JSON из содержимого ответа с помощью `utils.extract_json()`.
    *   Если ответ от OpenAI не получен, устанавливает `result = None`.
7.  **Кэширование результата**:
    *   Кэширует результат в `self.agent_extraction` под ключом, соответствующим имени агента (`tinyperson.name`).
8.  **Возврат результата**:
    *   Возвращает извлеченный результат.

**Примеры**:

```python
agent = TinyPerson(...)
result = extractor.extract_results_from_agent(agent, extraction_objective="...")
```

**Внутренние функции**:
-   Внутри данной функции вызывается `self._get_default_values_if_necessary` (описание ниже).

### `extract_results_from_world`

```python
def extract_results_from_world(self, 
                                   tinyworld: TinyWorld, 
                                   extraction_objective: str = "The main points that can be derived from the agents conversations and actions.", 
                                   situation: str = "", 
                                   fields: list = None,
                                   fields_hints: dict = None,
                                   verbose: bool = None):
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
- `tinyworld` (TinyWorld): Экземпляр `TinyWorld`, из которого необходимо извлечь результаты.
- `extraction_objective` (str, optional): Цель извлечения. По умолчанию "The main points that can be derived from the agents conversations and actions.".
- `situation` (str, optional): Ситуация для рассмотрения. По умолчанию пустая строка.
- `fields` (list, optional): Список полей для извлечения. Если `None`, извлекатель решает, какие имена использовать. По умолчанию `None`.
- `fields_hints` (dict, optional): Подсказки для полей для извлечения. Сопоставляет имена полей со строками с подсказками. По умолчанию `None`.
- `verbose` (bool, optional): Определяет, нужно ли печатать отладочные сообщения. По умолчанию `False`.

**Возвращает**:
- `dict | None`: Результат извлечения в формате JSON или `None`, если извлечение не удалось.

**Как работает функция**:
1.  **Получение значений по умолчанию**:
    *   Вызывает `self._get_default_values_if_necessary()` для получения значений по умолчанию для `extraction_objective`, `situation`, `fields`, `fields_hints` и `verbose`, если они не были предоставлены.
2.  **Подготовка сообщений**:
    *   Инициализирует пустой список `messages`.
    *   Инициализирует словарь `rendering_configs` для хранения конфигураций рендеринга.
    *   Если `fields` предоставлены, добавляет их в виде строки, разделенной запятыми, в `rendering_configs` под ключом `"fields"`.
     *   Если `fields_hints` предоставлены, преобразует их в список пар ключ-значение и добавляет в `rendering_configs` под ключом `"fields_hints"`.
    *   Добавляет системное сообщение в список `messages`. Это сообщение формируется с использованием шаблона, расположенного по пути `self._extraction_prompt_template_path`, и заполняется данными из `rendering_configs`.
3.  **Формирование истории взаимодействий**:
    *   Получает историю взаимодействий агентов в мире с помощью `tinyworld.pretty_current_interactions(max_content_length=None)`.
4.  **Формирование запроса на извлечение**:
    *   Создает строку `extraction_request_prompt`, содержащую цель извлечения, ситуацию и историю взаимодействий агентов.
    *   Добавляет сообщение пользователя с `extraction_request_prompt` в список `messages`.
5.  **Отправка сообщения в OpenAI**:
    *   Отправляет список сообщений в OpenAI с помощью `openai_utils.client().send_message()`.
    *   Устанавливает температуру `0.0` для получения более детерминированных результатов.
6.  **Обработка ответа**:
    *   Логирует и, если `verbose=True`, выводит отладочное сообщение, содержащее необработанный ответ от OpenAI.
    *   Если получен ответ от OpenAI, извлекает JSON из содержимого ответа с помощью `utils.extract_json()`.
    *   Если ответ от OpenAI не получен, устанавливает `result = None`.
7.  **Кэширование результата**:
    *   Кэширует результат в `self.world_extraction` под ключом, соответствующим имени мира (`tinyworld.name`).
8.  **Возврат результата**:
    *   Возвращает извлеченный результат.

**Примеры**:

```python
world = TinyWorld(...)
result = extractor.extract_results_from_world(world, extraction_objective="...")
```

**Внутренние функции**:
*   Внутри данной функции вызывается `self._get_default_values_if_necessary` (описание ниже).

### `save_as_json`

```python
def save_as_json(self, filename: str, verbose: bool = False):
    """
    Saves the last extraction results as JSON.

    Args:
        filename (str): The filename to save the JSON to.
        verbose (bool, optional): Whether to print debug messages. Defaults to False.
    """
    ...
```

**Назначение**: Сохраняет последние результаты извлечения в файл JSON.

**Параметры**:
- `filename` (str): Имя файла для сохранения JSON.
- `verbose` (bool, optional): Определяет, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:
1.  **Открытие файла**:
    *   Открывает файл с именем `filename` в режиме записи (`'w'`).
2.  **Сохранение JSON**:
    *   Сохраняет словарь, содержащий результаты извлечений агентов (`self.agent_extraction`) и мира (`self.world_extraction`), в файл в формате JSON с отступами равными 4.
3.  **Вывод сообщения (если verbose)**:
    *   Если `verbose=True`, выводит сообщение о том, в какой файл были сохранены результаты извлечения.

**Примеры**:

```python
extractor.save_as_json("results.json", verbose=True)
```

### `_get_default_values_if_necessary`

```python
def _get_default_values_if_necessary(self,
                                        extraction_objective: str,
                                        situation: str,
                                        fields: List[str],
                                        fields_hints: dict,
                                        verbose: bool):
    """
    """
    ...
```

**Назначение**: Возвращает значения по умолчанию для параметров, если они не были переданы.

**Параметры**:
- `extraction_objective` (str): Цель извлечения.
- `situation` (str): Ситуация.
- `fields` (List[str]): Список полей.
- `fields_hints` (dict): Подсказки для полей.
- `verbose` (bool): Флаг отладки.

**Возвращает**:
- `tuple`: Кортеж, содержащий значения `extraction_objective`, `situation`, `fields`, `fields_hints` и `verbose`. Если какой-либо из параметров равен `None`, он заменяется значением по умолчанию из атрибутов класса.

**Как работает функция**:
1.  **Проверка и замена значений**:
    *   Проверяет, является ли `extraction_objective` равным `None`. Если да, заменяет его на `self.default_extraction_objective`.
    *   Аналогично проверяет и заменяет `situation`, `fields`, `fields_hints` и `verbose`, используя соответствующие атрибуты класса.
2.  **Возврат значений**:
    *   Возвращает кортеж, содержащий (возможно, обновленные) значения `extraction_objective`, `situation`, `fields`, `fields_hints` и `verbose`.

**Примеры**:

```python
extraction_objective, situation, fields, verbose = self._get_default_values_if_necessary(extraction_objective, situation, fields, verbose)
```