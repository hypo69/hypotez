# Модуль extraction

## Обзор

Модуль предоставляет утилиты для извлечения данных из элементов TinyTroupe, таких как агенты и миры. Он также предоставляет механизм для сокращения извлеченных данных до более сжатой формы и для экспорта артефактов из элементов TinyTroupe.

## Подробнее

Этот модуль содержит классы и функции, предназначенные для извлечения, обработки и экспорта данных, полученных в результате симуляций TinyTroupe. Он позволяет извлекать ключевую информацию из истории взаимодействий агентов, генерировать синтетические данные и преобразовывать данные в машиночитаемые форматы, такие как JSON и CSV.

## Классы

### `ResultsExtractor`

**Описание**: Класс `ResultsExtractor` предназначен для извлечения результатов из экземпляров `TinyPerson` (агентов) и `TinyWorld`. Он использует предопределенные шаблоны для формирования запросов к OpenAI API, чтобы получить структурированные данные на основе истории взаимодействий агентов.

**Атрибуты**:

-   `_extraction_prompt_template_path` (str): Путь к шаблону mustache, используемому для формирования запросов к OpenAI API.
-   `agent_extraction` (dict): Кэш последних результатов извлечения для агентов.
-   `world_extraction` (dict): Кэш последних результатов извлечения для миров.

**Методы**:

-   `extract_results_from_agent()`: Извлекает результаты из экземпляра `TinyPerson`.
-   `extract_results_from_world()`: Извлекает результаты из экземпляра `TinyWorld`.
-   `save_as_json()`: Сохраняет последние результаты извлечения в формате JSON.

**Принцип работы**:

Класс `ResultsExtractor` использует шаблоны mustache для динамического формирования запросов к OpenAI API. Запросы включают в себя цель извлечения, текущую ситуацию и историю взаимодействий агентов. Результаты, полученные от OpenAI API, кэшируются для дальнейшего использования.

### `ResultsReducer`

**Описание**: Класс `ResultsReducer` предназначен для сокращения данных, извлеченных из агентов. Он применяет набор правил к истории взаимодействий агента, чтобы извлечь наиболее важную информацию.

**Атрибуты**:

-   `results` (dict): Словарь для хранения результатов сокращения.
-   `rules` (dict): Словарь, содержащий правила сокращения, где ключ - это триггер, а значение - функция для обработки данных.

**Методы**:

-   `add_reduction_rule()`: Добавляет правило сокращения.
-   `reduce_agent()`: Сокращает данные агента на основе заданных правил.
-   `reduce_agent_to_dataframe()`: Преобразует сокращенные данные агента в DataFrame pandas.

**Принцип работы**:

Класс `ResultsReducer` применяет правила, определенные пользователем, к истории взаимодействий агента. Каждое правило связано с определенным типом события (стимул или действие) и определяет, как извлечь информацию из этого события. Результаты сокращения сохраняются в виде списка словарей, который может быть преобразован в DataFrame pandas.

### `ArtifactExporter`

**Описание**: Класс `ArtifactExporter` отвечает за экспорт артефактов из элементов TinyTroupe в различные форматы файлов, такие как JSON, TXT и DOCX.

**Наследует**:

-   `JsonSerializableRegistry`: Класс, обеспечивающий сериализацию и десериализацию в формат JSON.

**Атрибуты**:

-   `base_output_folder` (str): Базовая папка для сохранения экспортированных артефактов.

**Методы**:

-   `export()`: Экспортирует артефакт в указанный файл.
-   `_export_as_txt()`: Экспортирует данные в текстовый файл.
-   `_export_as_json()`: Экспортирует данные в JSON-файл.
-   `_export_as_docx()`: Экспортирует данные в DOCX-файл.
-   `_compose_filepath()`: Составляет путь к файлу для экспортируемого артефакта.

**Принцип работы**:

Класс `ArtifactExporter` принимает данные и метаданные артефакта, такие как имя, тип содержимого и формат, и сохраняет их в файл в указанном формате. Он поддерживает экспорт в форматы JSON, TXT и DOCX. Для экспорта в формат DOCX используется библиотека `pypandoc` для преобразования контента из Markdown в HTML, а затем в DOCX.

### `Normalizer`

**Описание**: Класс `Normalizer` предназначен для нормализации текстовых элементов, таких как пассажи и концепции. Он использует OpenAI API для объединения похожих элементов в общие категории.

**Атрибуты**:

-   `elements` (List[str]): Список элементов для нормализации.
-   `n` (int): Количество нормализованных элементов для вывода.
-   `verbose` (bool): Флаг, указывающий, нужно ли выводить отладочные сообщения.
-   `normalized_elements` (dict): JSON-структура, где каждый выходной элемент является ключом к списку входных элементов, которые были объединены в него.
-   `normalizing_map` (dict): Словарь, который отображает каждый входной элемент на его нормализованный вывод.

**Методы**:

-   `__init__()`: Инициализирует экземпляр класса `Normalizer`.
-   `normalize()`: Нормализует указанный элемент или элементы.

**Принцип работы**:

Класс `Normalizer` использует OpenAI API для нормализации списка текстовых элементов. Он отправляет запрос к API, содержащий список элементов и количество нормализованных элементов, которые необходимо получить. Результаты, полученные от API, используются для создания карты нормализации, которая отображает каждый входной элемент на его нормализованный эквивалент.

## Функции

### `ResultsExtractor.extract_results_from_agent`

```python
def extract_results_from_agent(
    tinyperson: TinyPerson,
    extraction_objective: str = "The main points present in the agent's interactions history.",
    situation: str = "",
    fields: list = None,
    fields_hints: dict = None,
    verbose: bool = False,
) -> dict | None:
    """
    Извлекает результаты из экземпляра TinyPerson.

    Args:
        tinyperson (TinyPerson): Экземпляр TinyPerson, из которого извлекаются результаты.
        extraction_objective (str): Цель извлечения. По умолчанию "The main points present in the agent's interactions history.".
        situation (str): Ситуация, которую следует учитывать. По умолчанию "".
        fields (list, optional): Поля для извлечения. Если None, извлекатель сам решает, какие имена использовать. По умолчанию None.
        fields_hints (dict, optional): Подсказки для полей. По умолчанию None.
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию False.

    Returns:
        dict | None: Результаты извлечения в формате JSON или None в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при отправке сообщения в OpenAI API.

    """
    ...
```

**Назначение**: Извлекает результаты из экземпляра `TinyPerson` (агента) на основе заданной цели извлечения и ситуации.

**Параметры**:

-   `tinyperson` (TinyPerson): Экземпляр `TinyPerson`, из которого извлекаются результаты.
-   `extraction_objective` (str): Цель извлечения.  Определяет, какую информацию необходимо извлечь из истории взаимодействий агента. По умолчанию "The main points present in the agent's interactions history.".
-   `situation` (str):  Контекст или ситуация, которую следует учитывать при извлечении данных. По умолчанию "".
-   `fields` (list, optional): Список полей для извлечения. Если `None`, то извлекатель сам определяет, какие имена использовать. По умолчанию `None`.
-   `fields_hints` (dict, optional): Словарь с подсказками для полей, которые необходимо извлечь. По умолчанию `None`.
-   `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Возвращает**:

-   `dict | None`: Результаты извлечения в формате JSON или `None` в случае ошибки.

**Как работает функция**:

Функция формирует запрос к OpenAI API, используя цель извлечения, ситуацию и историю взаимодействий агента. Запрос отправляется в OpenAI API, и результаты извлечения возвращаются в формате JSON. Результаты также кэшируются для последующего использования.
- Если указаны `fields` и `fields_hints`, они используются для формирования запроса к OpenAI.
- История взаимодействий агента получается с помощью метода `tinyperson.pretty_current_interactions()`.
- Результаты извлечения сохраняются в `self.agent_extraction` для последующего использования.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Пример использования функции extract_results_from_agent
agent = TinyPerson(name="Alice")
extractor = ResultsExtractor()
results = extractor.extract_results_from_agent(agent, extraction_objective="Main goals")
if results:
    print(results)
```

### `ResultsExtractor.extract_results_from_world`

```python
def extract_results_from_world(
    tinyworld: TinyWorld,
    extraction_objective: str = "The main points that can be derived from the agents conversations and actions.",
    situation: str = "",
    fields: list = None,
    fields_hints: dict = None,
    verbose: bool = False,
) -> dict | None:
    """
    Извлекает результаты из экземпляра TinyWorld.

    Args:
        tinyworld (TinyWorld): Экземпляр TinyWorld, из которого извлекаются результаты.
        extraction_objective (str): Цель извлечения. По умолчанию "The main points that can be derived from the agents conversations and actions.".
        situation (str): Ситуация, которую следует учитывать. По умолчанию "".
        fields (list, optional): Поля для извлечения. Если None, извлекатель сам решает, какие имена использовать. По умолчанию None.
        fields_hints (dict, optional): Подсказки для полей. По умолчанию None.
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию False.

    Returns:
        dict | None: Результаты извлечения в формате JSON или None в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при отправке сообщения в OpenAI API.
    """
    ...
```

**Назначение**: Извлекает результаты из экземпляра `TinyWorld` на основе заданной цели извлечения и ситуации.

**Параметры**:

-   `tinyworld` (TinyWorld): Экземпляр `TinyWorld`, из которого извлекаются результаты.
-   `extraction_objective` (str): Цель извлечения. Определяет, какую информацию необходимо извлечь из истории взаимодействий агентов в мире. По умолчанию "The main points that can be derived from the agents conversations and actions.".
-   `situation` (str): Контекст или ситуация, которую следует учитывать при извлечении данных. По умолчанию "".
-   `fields` (list, optional): Список полей для извлечения. Если `None`, то извлекатель сам определяет, какие имена использовать. По умолчанию `None`.
-   `fields_hints` (dict, optional): Словарь с подсказками для полей, которые необходимо извлечь. По умолчанию `None`.
-   `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Возвращает**:

-   `dict | None`: Результаты извлечения в формате JSON или `None` в случае ошибки.

**Как работает функция**:

Функция формирует запрос к OpenAI API, используя цель извлечения, ситуацию и историю взаимодействий агентов в мире. Запрос отправляется в OpenAI API, и результаты извлечения возвращаются в формате JSON. Результаты также кэшируются для последующего использования.
- Если указаны `fields` и `fields_hints`, они используются для формирования запроса к OpenAI.
- История взаимодействий агентов получается с помощью метода `tinyworld.pretty_current_interactions()`.
- Результаты извлечения сохраняются в `self.world_extraction` для последующего использования.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Пример использования функции extract_results_from_world
world = TinyWorld(name="Wonderland")
extractor = ResultsExtractor()
results = extractor.extract_results_from_world(world, extraction_objective="Summary of events")
if results:
    print(results)
```

### `ResultsExtractor.save_as_json`

```python
def save_as_json(filename: str, verbose: bool = False) -> None:
    """
    Сохраняет последние результаты извлечения в формате JSON.

    Args:
        filename (str): Имя файла для сохранения JSON.
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию False.
    """
    ...
```

**Назначение**: Сохраняет последние результаты извлечения агентов и миров в файл в формате JSON.

**Параметры**:

-   `filename` (str): Имя файла, в который будут сохранены результаты извлечения.
-   `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:

Функция сохраняет содержимое атрибутов `agent_extraction` и `world_extraction` в файл с указанным именем в формате JSON. Она использует модуль `json` для сериализации данных в формат JSON и записи их в файл.

**Примеры**:

```python
# Пример использования функции save_as_json
extractor = ResultsExtractor()
extractor.save_as_json("extraction_results.json", verbose=True)
```

### `ResultsReducer.add_reduction_rule`

```python
def add_reduction_rule(self, trigger: str, func: callable) -> None:
    """
    Добавляет правило сокращения.

    Args:
        trigger (str): Триггер для правила.
        func (callable): Функция для обработки данных.

    Raises:
        Exception: Если правило для указанного триггера уже существует.
    """
    ...
```

**Назначение**: Добавляет правило сокращения в словарь `self.rules`.

**Параметры**:

-   `trigger` (str): Триггер, который определяет, когда применять данное правило.
-   `func` (callable): Функция, которая будет вызываться при срабатывании триггера.

**Вызывает исключения**:

-   `Exception`: Если правило для указанного триггера уже существует.

**Как работает функция**:

Функция добавляет новое правило сокращения в словарь `self.rules`. Ключом в словаре является триггер, а значением - функция, которая будет вызываться при срабатывании этого триггера. Если правило для указанного триггера уже существует, функция вызывает исключение.

**Примеры**:

```python
# Пример использования функции add_reduction_rule
reducer = ResultsReducer()

def my_reduction_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
    return {"event": event, "content": content}

reducer.add_reduction_rule("my_event", my_reduction_rule)
```

### `ResultsReducer.reduce_agent`

```python
def reduce_agent(self, agent: TinyPerson) -> list:
    """
    Сокращает данные агента на основе заданных правил.

    Args:
        agent (TinyPerson): Агент, данные которого необходимо сократить.

    Returns:
        list: Список сокращенных данных.
    """
    ...
```

**Назначение**: Сокращает историю взаимодействий агента, применяя правила, хранящиеся в `self.rules`.

**Параметры**:

-   `agent` (TinyPerson): Агент, данные которого необходимо сократить.

**Возвращает**:

-   `list`: Список сокращенных данных.

**Как работает функция**:

Функция перебирает сообщения в `episodic_memory` агента.
- Если роль сообщения `system`, то ничего не происходит.
- Если роль сообщения `user`, то извлекается информация о стимуле, и если тип стимула есть в `self.rules`, то вызывается соответствующая функция.
- Если роль сообщения `assistant`, то извлекается информация о действии, и если тип действия есть в `self.rules`, то вызывается соответствующая функция.
Результаты сокращения добавляются в список `reduction`, который возвращается в конце функции.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Пример использования функции reduce_agent
reducer = ResultsReducer()

def my_reduction_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
    return {"event": event, "content": content}

reducer.add_reduction_rule("my_event", my_reduction_rule)

agent = TinyPerson(name="Bob")
reduction = reducer.reduce_agent(agent)
print(reduction)
```

### `ResultsReducer.reduce_agent_to_dataframe`

```python
def reduce_agent_to_dataframe(self, agent: TinyPerson, column_names: list = None) -> pd.DataFrame:
    """
    Преобразует сокращенные данные агента в DataFrame pandas.

    Args:
        agent (TinyPerson): Агент, данные которого необходимо сократить и преобразовать в DataFrame.
        column_names (list, optional): Список имен столбцов для DataFrame. По умолчанию None.

    Returns:
        pd.DataFrame: DataFrame, содержащий сокращенные данные агента.
    """
    ...
```

**Назначение**: Преобразует результаты сокращения данных агента в DataFrame pandas.

**Параметры**:

-   `agent` (TinyPerson): Агент, данные которого необходимо сократить и преобразовать в DataFrame.
-   `column_names` (list, optional): Список имен столбцов для DataFrame. Если `None`, используются имена столбцов по умолчанию. По умолчанию `None`.

**Возвращает**:

-   `pd.DataFrame`: DataFrame, содержащий сокращенные данные агента.

**Как работает функция**:

Функция сначала вызывает метод `reduce_agent` для сокращения данных агента. Затем она преобразует список сокращенных данных в DataFrame pandas, используя указанные имена столбцов.

**Примеры**:

```python
import pandas as pd
from tinytroupe.agent import TinyPerson

# Пример использования функции reduce_agent_to_dataframe
reducer = ResultsReducer()

def my_reduction_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
    return {"event": event, "content": content}

reducer.add_reduction_rule("my_event", my_reduction_rule)

agent = TinyPerson(name="Charlie")
df = reducer.reduce_agent_to_dataframe(agent, column_names=["event", "content"])
print(df)
```

### `ArtifactExporter.export`

```python
def export(
    self,
    artifact_name: str,
    artifact_data: Union[dict, str],
    content_type: str,
    content_format: str = None,
    target_format: str = "txt",
    verbose: bool = False,
) -> None:
    """
    Экспортирует указанные данные артефакта в файл.

    Args:
        artifact_name (str): Имя артефакта.
        artifact_data (Union[dict, str]): Данные для экспорта. Если передан словарь, он будет сохранен в формате JSON.
            Если передана строка, она будет сохранена как есть.
        content_type (str): Тип содержимого артефакта.
        content_format (str, optional): Формат содержимого артефакта (например, md, csv и т. д.). По умолчанию None.
        target_format (str): Формат для экспорта артефакта (например, json, txt, docx и т. д.).
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию False.
    """
    ...
```

**Назначение**: Экспортирует данные артефакта в файл в указанном формате.

**Параметры**:

-   `artifact_name` (str): Имя артефакта. Используется для формирования имени файла.
-   `artifact_data` (Union[dict, str]): Данные для экспорта. Могут быть словарем (JSON) или строкой.
-   `content_type` (str): Тип содержимого артефакта. Используется для определения подпапки для сохранения файла.
-   `content_format` (str, optional): Формат содержимого артефакта (например, md, csv и т. д.). По умолчанию `None`.
-   `target_format` (str): Формат для экспорта артефакта (например, json, txt, docx и т. д.). По умолчанию `"txt"`.
-   `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:

Функция выполняет следующие действия:
1. Удаляет отступы из входных данных.
2. Очищает имя артефакта от недопустимых символов.
3. Определяет путь к файлу с помощью метода `_compose_filepath`.
4. Вызывает соответствующий метод для экспорта данных в указанном формате (`_export_as_json`, `_export_as_txt`, `_export_as_docx`).

**Примеры**:

```python
# Пример использования функции export
exporter = ArtifactExporter(base_output_folder="output")
exporter.export(
    artifact_name="my_artifact",
    artifact_data={"content": "This is a test."},
    content_type="text",
    target_format="json",
    verbose=True,
)
```

### `ArtifactExporter._export_as_txt`

```python
def _export_as_txt(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False) -> None:
    """
    Экспортирует указанные данные артефакта в текстовый файл.
    """
    ...
```

**Назначение**: Экспортирует данные артефакта в текстовый файл.

**Параметры**:

-   `artifact_file_path` (str): Путь к файлу для сохранения артефакта.
-   `artifact_data` (Union[dict, str]): Данные для экспорта. Могут быть словарем или строкой.
-   `content_type` (str): Тип содержимого артефакта.
-   `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:

Функция записывает данные артефакта в текстовый файл. Если `artifact_data` является словарем, то извлекается значение ключа `'content'`. Если `artifact_data` является строкой, то она записывается в файл как есть.

**Примеры**:

```python
# Пример использования функции _export_as_txt
exporter = ArtifactExporter(base_output_folder="output")
exporter._export_as_txt(
    artifact_file_path="output/text/my_artifact.txt",
    artifact_data="This is a test.",
    content_type="text",
    verbose=True,
)
```

### `ArtifactExporter._export_as_json`

```python
def _export_as_json(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False) -> None:
    """
    Экспортирует указанные данные артефакта в JSON-файл.
    """
    ...
```

**Назначение**: Экспортирует данные артефакта в JSON-файл.

**Параметры**:

-   `artifact_file_path` (str): Путь к файлу для сохранения артефакта.
-   `artifact_data` (Union[dict, str]): Данные для экспорта. Должны быть словарем.
-   `content_type` (str): Тип содержимого артефакта.
-   `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Вызывает исключения**:

-   `ValueError`: Если `artifact_data` не является словарем.

**Как работает функция**:

Функция записывает данные артефакта в JSON-файл. Если `artifact_data` является словарем, то он сериализуется в JSON-формат и записывается в файл. Если `artifact_data` не является словарем, то вызывается исключение `ValueError`.

**Примеры**:

```python
# Пример использования функции _export_as_json
exporter = ArtifactExporter(base_output_folder="output")
exporter._export_as_json(
    artifact_file_path="output/json/my_artifact.json",
    artifact_data={"content": "This is a test."},
    content_type="text",
    verbose=True,
)
```

### `ArtifactExporter._export_as_docx`

```python
def _export_as_docx(self, artifact_file_path: str, artifact_data: Union[dict, str], content_original_format: str, verbose: bool = False) -> None:
    """
    Экспортирует указанные данные артефакта в DOCX-файл.
    """
    ...
```

**Назначение**: Экспортирует данные артефакта в DOCX-файл.

**Параметры**:

-   `artifact_file_path` (str): Путь к файлу для сохранения артефакта.
-   `artifact_data` (Union[dict, str]): Данные для экспорта. Могут быть словарем или строкой.
-   `content_original_format` (str): Исходный формат содержимого артефакта (например, 'text', 'markdown').
-   `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Вызывает исключения**:

-   `ValueError`: Если `content_original_format` не является 'text', 'txt', 'markdown' или 'md'.

**Как работает функция**:

Функция экспортирует данные артефакта в DOCX-файл. Сначала проверяется, что `content_original_format` имеет допустимое значение. Затем данные преобразуются в HTML с помощью библиотеки `markdown`. Наконец, HTML-контент преобразуется в DOCX-файл с помощью библиотеки `pypandoc`.

**Примеры**:

```python
# Пример использования функции _export_as_docx
exporter = ArtifactExporter(base_output_folder="output")
exporter._export_as_docx(
    artifact_file_path="output/docx/my_artifact.docx",
    artifact_data={"content": "This is a test."},
    content_original_format="markdown",
    verbose=True,
)
```

### `ArtifactExporter._compose_filepath`

```python
def _compose_filepath(
    self,
    artifact_data: Union[dict, str],
    artifact_name: str,
    content_type: str,
    target_format: str = None,
    verbose: bool = False,
) -> str:
    """
    Составляет путь к файлу для экспортируемого артефакта.

    Args:
        artifact_data (Union[dict, str]): Данные для экспорта.
        artifact_name (str): Имя артефакта.
        content_type (str): Тип содержимого артефакта.
        content_format (str, optional): Формат содержимого артефакта (например, md, csv и т. д.). По умолчанию None.
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию False.
    """
    ...
```

**Назначение**: Составляет путь к файлу для экспортируемого артефакта на основе заданных параметров.

**Параметры**:

-   `artifact_data` (Union[dict, str]): Данные для экспорта. Используется для определения расширения файла.
-   `artifact_name` (str): Имя артефакта. Используется для формирования имени файла.
-   `content_type` (str): Тип содержимого артефакта. Используется для определения подпапки для сохранения файла.
-   `target_format` (str, optional): Формат для экспорта артефакта (например, json, txt, docx и т. д.). По умолчанию `None`.
-   `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:

Функция формирует путь к файлу на основе следующих правил:
1. Определяется расширение файла на основе `target_format` и типа данных `artifact_data`.
2. Определяется подпапка на основе `content_type`.
3. Составляется полный путь к файлу с использованием `base_output_folder`, подпапки и имени файла.
4. Создаются промежуточные каталоги, если они не существуют.

**Примеры**:

```python
# Пример использования функции _compose_filepath
exporter = ArtifactExporter(base_output_folder="output")
file_path = exporter._compose_filepath(
    artifact_data={"content": "This is a test."},
    artifact_name="my_artifact",
    content_type="text",
    target_format="json",
    verbose=True,
)
print(file_path)  # Output: output/text/my_artifact.json
```

### `Normalizer.__init__`

```python
def __init__(self, elements: List[str], n: int, verbose: bool = False) -> None:
    """
    Нормализует указанные элементы.

    Args:
        elements (list): Элементы для нормализации.
        n (int): Количество нормализованных элементов для вывода.
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию False.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `Normalizer` и выполняет нормализацию указанных элементов.

**Параметры**:

-   `elements` (List[str]): Список элементов для нормализации.
-   `n` (int): Количество нормализованных элементов для вывода.
-   `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Как работает функция**:

Функция выполняет следующие действия:
1. Удаляет дубликаты из списка элементов.
2. Сохраняет параметры `n` и `verbose`.
3. Формирует запрос к OpenAI API, используя шаблоны `normalizer.system.mustache` и `normalizer.user.mustache`.
4. Отправляет запрос в OpenAI API и получает результаты нормализации.
5. Сохраняет результаты нормализации в атрибуте `normalized_elements`.

**Примеры**:

```python
# Пример использования функции __init__
normalizer = Normalizer(elements=["apple", "banana", "apple"], n=2, verbose=True)
```

### `Normalizer.normalize`

```python
def normalize(self, element_or_elements: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Нормализует указанный элемент или элементы.

    Этот метод использует механизм кэширования для повышения производительности. Если элемент был нормализован ранее,
    его нормализованная форма хранится в кэше (self.normalizing_map). Когда один и тот же элемент необходимо
    нормализовать снова, метод сначала проверит кэш и использует сохраненную нормализованную форму, если она доступна,
    вместо повторной нормализации элемента.

    Порядок элементов на выходе будет таким же, как и на входе. Это обеспечивается обработкой
    элементов в том порядке, в котором они появляются на входе, и добавлением нормализованных элементов к выходу
    список в том же порядке.

    Args:
        element_or_elements (Union[str, List[str]]): Элемент или элементы для нормализации.

    Returns:
        str: Нормализованный элемент, если входные данные были строкой.
        list: Нормализованные элементы, если входные данные были списком, с сохранением порядка элементов на входе.
    """
    ...
```

**Назначение**: Нормализует указанный элемент или элементы, используя кэширование для повышения производительности.

**Параметры**:

-   `element_or_elements` (Union[str, List[str]]): Элемент или элементы для нормализации.

**Возвращает**:

-   `str`: Нормализованный элемент, если входные данные были строкой.
-   `list`: Нормализованные элементы, если входные данные были списком, с сохранением порядка элементов на входе.

**Как работает функция**:

Функция выполняет следующие действия:
1. Проверяет, является ли входной параметр строкой или списком.
2. Если входной параметр является строкой, то он преобразуется в список.
3. Перебирает элементы списка и проверяет, есть ли они в кэше `self.normalizing_map`.
4. Если элемент отсутствует в кэше, то он добавляется в список `elements_to_normalize`.
5. Если список `elements_to_normalize` не пуст, то формируется запрос к OpenAI API, используя шаблоны `normalizer.applier.system.mustache` и `normalizer.applier.user.mustache`.
6. Отправляется запрос в OpenAI API и получаются результаты нормализации.
7. Сохраняются результаты нормализации в кэше `self.normalizing_map`.
8. Формируется список нормализованных элементов, используя кэш `self.normalizing_map`.
9. Возвращается нормализованный элемент или список нормализованных элементов.

**Примеры**:

```python
# Пример использования функции normalize
normalizer = Normalizer(elements=["apple", "banana", "orange"], n=2, verbose=True)
normalized_elements = normalizer.normalize(element_or_elements=["apple", "banana", "grape"])
print(normalized_elements)
```

## Параметры класса

-   `base_output_folder` (str): Базовая папка, в которой будут сохранены результаты экспорта.
-   `artifact_name` (str): Имя артефакта, используемое при формировании имени файла.
-   `artifact_data` (Union[dict, str]): Дан