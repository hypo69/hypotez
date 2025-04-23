# Модуль `extraction.py`

## Обзор

Модуль содержит классы и функции для извлечения данных из симуляций TinyTroupe, приведения их к более компактному виду и экспорта артефактов. Он позволяет извлекать основные моменты из истории взаимодействий агентов, генерировать синтетические данные и преобразовывать данные в машиночитаемые форматы, такие как JSON или CSV.

## Подробнее

Этот модуль предоставляет инструменты для извлечения данных из элементов TinyTroupe, таких как агенты и миры. Он также предоставляет механизм для уменьшения объема извлеченных данных и экспорта артефактов. Это демонстрирует одно из различий между симуляциями агентов и AI-ассистентами, поскольку последние не предназначены для интроспекции.

## Классы

### `ResultsExtractor`

**Описание**: Класс для извлечения результатов из экземпляров `TinyPerson` (агентов) и `TinyWorld` (миров).

**Атрибуты**:
- `_extraction_prompt_template_path` (str): Путь к шаблону запроса для извлечения результатов.
- `agent_extraction` (dict): Кэш последних результатов извлечения для агентов.
- `world_extraction` (dict): Кэш последних результатов извлечения для миров.

**Методы**:
- `extract_results_from_agent`: Извлекает результаты из экземпляра `TinyPerson`.
- `extract_results_from_world`: Извлекает результаты из экземпляра `TinyWorld`.
- `save_as_json`: Сохраняет последние результаты извлечения в формате JSON.

**Принцип работы**:
Класс `ResultsExtractor` инициализируется с путем к шаблону запроса, который используется для взаимодействия с OpenAI API. Он также содержит кэш для хранения последних результатов извлечения как для агентов, так и для миров. Методы `extract_results_from_agent` и `extract_results_from_world` используют этот шаблон для формирования запросов к OpenAI API, чтобы извлечь полезную информацию из истории взаимодействий агентов или миров. Метод `save_as_json` используется для сохранения извлеченных данных в файл JSON.

### `ResultsReducer`

**Описание**: Класс для сведения результатов извлечения к более компактному виду.

**Атрибуты**:
- `results` (dict): Словарь для хранения результатов сведения.
- `rules` (dict): Словарь, содержащий правила сведения для разных типов сообщений.

**Методы**:
- `add_reduction_rule`: Добавляет правило сведения для указанного триггера.
- `reduce_agent`: Сводит историю взаимодействий агента к списку извлеченных данных.
- `reduce_agent_to_dataframe`: Сводит историю взаимодействий агента к DataFrame.

**Принцип работы**:
Класс `ResultsReducer` позволяет применять различные правила для сведения истории взаимодействий агентов к более компактному виду. Он использует словарь `rules` для хранения функций, которые определяют, как обрабатывать различные типы сообщений. Методы `reduce_agent` и `reduce_agent_to_dataframe` применяют эти правила для сведения истории взаимодействий агента и преобразования результатов в DataFrame.

### `ArtifactExporter`

**Описание**: Класс для экспорта артефактов из элементов TinyTroupe в различные форматы файлов.

**Наследует**:
- `JsonSerializableRegistry`: Класс для регистрации и сериализации объектов в JSON.

**Атрибуты**:
- `base_output_folder` (str): Базовая папка для сохранения экспортированных артефактов.

**Методы**:
- `export`: Экспортирует артефакт в указанный файл.
- `_export_as_txt`: Экспортирует артефакт в текстовый файл.
- `_export_as_json`: Экспортирует артефакт в файл JSON.
- `_export_as_docx`: Экспортирует артефакт в файл DOCX.
- `_compose_filepath`: Формирует путь к файлу для экспортируемого артефакта.

**Принцип работы**:
Класс `ArtifactExporter` отвечает за экспорт артефактов из элементов TinyTroupe в различные форматы файлов, такие как JSON, TXT и DOCX. Он использует метод `export` для определения формата экспорта и вызова соответствующего метода экспорта. Методы `_export_as_txt`, `_export_as_json` и `_export_as_docx` выполняют фактический экспорт данных в указанный формат. Метод `_compose_filepath` используется для формирования пути к файлу, в который будет сохранен артефакт.

### `Normalizer`

**Описание**: Класс для нормализации текстовых элементов, таких как пассажи и концепции.

**Атрибуты**:
- `elements` (List[str]): Список элементов для нормализации.
- `n` (int): Количество нормализованных элементов для вывода.
- `verbose` (bool): Флаг для отображения отладочных сообщений.
- `normalized_elements` (dict): JSON-структура, где каждый выходной элемент является ключом к списку входных элементов, которые были объединены в него.
- `normalizing_map` (dict): Словарь, который отображает каждый входной элемент на его нормализованный вывод. Используется как кэш.

**Методы**:
- `__init__`: Инициализирует класс `Normalizer`.
- `normalize`: Нормализует указанный элемент или элементы.

**Принцип работы**:
Класс `Normalizer` используется для нормализации текстовых элементов. При инициализации он принимает список элементов для нормализации и количество нормализованных элементов для вывода. Он использует OpenAI API для нормализации элементов и кэширует результаты в словаре `normalizing_map`. Метод `normalize` используется для нормализации одного или нескольких элементов и возвращает нормализованные элементы.

## Функции

### `ResultsExtractor.extract_results_from_agent`

```python
def extract_results_from_agent(
    self,
    tinyperson: TinyPerson,
    extraction_objective: str = "The main points present in the agent's interactions history.",
    situation: str = "",
    fields: list = None,
    fields_hints: dict = None,
    verbose: bool = False,
) -> dict | None:
    """
    Извлекает результаты из экземпляра `TinyPerson`.

    Args:
        tinyperson (TinyPerson): Экземпляр `TinyPerson`, из которого нужно извлечь результаты.
        extraction_objective (str): Цель извлечения. По умолчанию "The main points present in the agent's interactions history.".
        situation (str): Описание ситуации, которую следует учитывать при извлечении. По умолчанию "".
        fields (list, optional): Список полей для извлечения. Если `None`, экстрактор сам решает, какие имена использовать. По умолчанию `None`.
        fields_hints (dict, optional): Словарь с подсказками для полей. По умолчанию `None`.
        verbose (bool, optional): Флаг для отображения отладочных сообщений. По умолчанию `False`.

    Returns:
        dict | None: Результат извлечения в виде словаря или `None`, если извлечение не удалось.

    """
```

**Назначение**: Извлечение результатов из объекта `TinyPerson` (агента).

**Параметры**:
- `tinyperson` (TinyPerson): Объект агента, из которого извлекаются данные.
- `extraction_objective` (str): Цель извлечения данных. По умолчанию - основные моменты из истории взаимодействий агента.
- `situation` (str): Контекст или ситуация, в которой находится агент. По умолчанию - пустая строка.
- `fields` (list, optional): Список полей, которые нужно извлечь. Если не указан, экстрактор выбирает поля автоматически. По умолчанию `None`.
- `fields_hints` (dict, optional): Подсказки для экстрактора о том, как интерпретировать поля. По умолчанию `None`.
- `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Возвращает**:
- `dict | None`: Результат извлечения данных в формате словаря, либо `None`, если произошла ошибка.

**Как работает функция**:
Функция формирует запрос к OpenAI API, используя историю взаимодействий агента и цель извлечения. Запрос отправляется OpenAI API, и результат извлечения сохраняется в кэше `agent_extraction`.

**Примеры**:

```python
extractor = ResultsExtractor()
agent = TinyPerson(name="Alice")
result = extractor.extract_results_from_agent(agent, extraction_objective="Summary of interactions")
if result:
    print(result)
```

### `ResultsExtractor.extract_results_from_world`

```python
def extract_results_from_world(
    self,
    tinyworld: TinyWorld,
    extraction_objective: str = "The main points that can be derived from the agents conversations and actions.",
    situation: str = "",
    fields: list = None,
    fields_hints: dict = None,
    verbose: bool = False,
) -> dict | None:
    """
    Извлекает результаты из экземпляра `TinyWorld`.

    Args:
        tinyworld (TinyWorld): Экземпляр `TinyWorld`, из которого нужно извлечь результаты.
        extraction_objective (str): Цель извлечения. По умолчанию "The main points that can be derived from the agents conversations and actions.".
        situation (str): Описание ситуации, которую следует учитывать при извлечении. По умолчанию "".
        fields (list, optional): Список полей для извлечения. Если `None`, экстрактор сам решает, какие имена использовать. По умолчанию `None`.
        fields_hints (dict, optional): Словарь с подсказками для полей. По умолчанию `None`.
        verbose (bool, optional): Флаг для отображения отладочных сообщений. По умолчанию `False`.

    Returns:
        dict | None: Результат извлечения в виде словаря или `None`, если извлечение не удалось.

    """
```

**Назначение**: Извлечение результатов из объекта `TinyWorld` (мира).

**Параметры**:
- `tinyworld` (TinyWorld): Объект мира, из которого извлекаются данные.
- `extraction_objective` (str): Цель извлечения данных. По умолчанию - основные моменты, полученные из разговоров и действий агентов.
- `situation` (str): Контекст или ситуация, в которой находится мир. По умолчанию - пустая строка.
- `fields` (list, optional): Список полей, которые нужно извлечь. Если не указан, экстрактор выбирает поля автоматически. По умолчанию `None`.
- `fields_hints` (dict, optional): Подсказки для экстрактора о том, как интерпретировать поля. По умолчанию `None`.
- `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Возвращает**:
- `dict | None`: Результат извлечения данных в формате словаря, либо `None`, если произошла ошибка.

**Как работает функция**:
Функция формирует запрос к OpenAI API, используя историю взаимодействий агентов в мире и цель извлечения. Запрос отправляется OpenAI API, и результат извлечения сохраняется в кэше `world_extraction`.

**Примеры**:

```python
extractor = ResultsExtractor()
world = TinyWorld(name="Wonderland")
result = extractor.extract_results_from_world(world, extraction_objective="Summary of world events")
if result:
    print(result)
```

### `ResultsExtractor.save_as_json`

```python
def save_as_json(self, filename: str, verbose: bool = False) -> None:
    """
    Сохраняет последние результаты извлечения в формате JSON.

    Args:
        filename (str): Имя файла для сохранения JSON.
        verbose (bool, optional): Флаг для отображения отладочных сообщений. По умолчанию `False`.

    """
```

**Назначение**: Сохранение результатов извлечения агентов и миров в JSON файл.

**Параметры**:
- `filename` (str): Имя файла, в который будут сохранены результаты.
- `verbose` (bool, optional): Флаг для отображения отладочных сообщений. По умолчанию `False`.

**Как работает функция**:
Функция сохраняет данные из `self.agent_extraction` и `self.world_extraction` в файл JSON с указанным именем.

**Примеры**:

```python
extractor = ResultsExtractor()
extractor.save_as_json("extraction_results.json", verbose=True)
```

### `ResultsReducer.add_reduction_rule`

```python
def add_reduction_rule(self, trigger: str, func: callable) -> None:
    """
    Добавляет правило сведения для указанного триггера.

    Args:
        trigger (str): Триггер, для которого добавляется правило.
        func (callable): Функция, которая будет вызываться при срабатывании триггера.

    Raises:
        Exception: Если правило для указанного триггера уже существует.

    """
```

**Назначение**: Добавление правила сведения.

**Параметры**:
- `trigger` (str): Тип сообщения или события, которое активирует правило сведения.
- `func` (callable): Функция, которая будет выполнять сведение.

**Вызывает исключения**:
- `Exception`: Если правило для указанного триггера уже существует.

**Как работает функция**:
Функция добавляет новую функцию сведения в словарь `self.rules`, связывая ее с определенным триггером.

**Примеры**:

```python
reducer = ResultsReducer()
def my_reduction_rule(focus_agent=None, source_agent=None, target_agent=None, kind='', event='', content='', timestamp=None):
    return {"event": event, "content": content}
reducer.add_reduction_rule("chat", my_reduction_rule)
```

### `ResultsReducer.reduce_agent`

```python
def reduce_agent(self, agent: TinyPerson) -> list:
    """
    Сводит историю взаимодействий агента к списку извлеченных данных.

    Args:
        agent (TinyPerson): Агент, историю взаимодействий которого нужно свести.

    Returns:
        list: Список извлеченных данных.

    """
```

**Назначение**: Сведение истории взаимодействий агента.

**Параметры**:
- `agent` (TinyPerson): Объект агента, историю взаимодействий которого необходимо свести.

**Возвращает**:
- `list`: Список извлеченных данных из истории взаимодействий агента.

**Как работает функция**:
Функция перебирает все сообщения в эпизодической памяти агента и применяет правила сведения, определенные в `self.rules`, к каждому сообщению.

**Примеры**:

```python
reducer = ResultsReducer()
# Добавьте правила сведения перед вызовом reduce_agent
reduction = reducer.reduce_agent(agent)
```

### `ResultsReducer.reduce_agent_to_dataframe`

```python
def reduce_agent_to_dataframe(self, agent: TinyPerson, column_names: list = None) -> pd.DataFrame:
    """
    Сводит историю взаимодействий агента к DataFrame.

    Args:
        agent (TinyPerson): Агент, историю взаимодействий которого нужно свести.
        column_names (list, optional): Список названий столбцов для DataFrame. По умолчанию `None`.

    Returns:
        pd.DataFrame: DataFrame с извлеченными данными.

    """
```

**Назначение**: Сведение истории взаимодействий агента в DataFrame.

**Параметры**:
- `agent` (TinyPerson): Объект агента, историю взаимодействий которого необходимо свести.
- `column_names` (list, optional): Список названий столбцов для DataFrame. Если не указан, будут использованы названия столбцов по умолчанию. По умолчанию `None`.

**Возвращает**:
- `pd.DataFrame`: DataFrame, содержащий сведенные данные из истории взаимодействий агента.

**Как работает функция**:
Функция вызывает `self.reduce_agent` для получения списка сведенных данных, а затем преобразует этот список в DataFrame.

**Примеры**:

```python
reducer = ResultsReducer()
df = reducer.reduce_agent_to_dataframe(agent, column_names=["event", "content"])
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
        artifact_data (Union[dict, str]): Данные для экспорта. Если передан словарь, он будет сохранен как JSON.
            Если передана строка, она будет сохранена как есть.
        content_type (str): Тип содержимого в артефакте.
        content_format (str, optional): Формат содержимого в артефакте (например, md, csv и т. д.). По умолчанию `None`.
        target_format (str): Формат для экспорта артефакта (например, json, txt, docx и т. д.).
        verbose (bool, optional): Флаг для отображения отладочных сообщений. По умолчанию `False`.

    Raises:
        ValueError: Если данные артефакта не являются строкой или словарем.
        ValueError: Если указан неподдерживаемый формат экспорта.

    """
```

**Назначение**: Экспорт данных в файл.

**Параметры**:
- `artifact_name` (str): Имя артефакта (имя файла).
- `artifact_data` (Union[dict, str]): Данные для экспорта. Могут быть словарем (будут экспортированы как JSON) или строкой.
- `content_type` (str): Тип контента (например, "текст", "данные"). Используется для организации файлов по подпапкам.
- `content_format` (str, optional): Формат контента (например, "md", "csv").  По умолчанию `None`.
- `target_format` (str, optional): Целевой формат экспорта (например, "json", "txt", "docx"). По умолчанию `"txt"`.
- `verbose` (bool, optional): Включает/выключает отладочные сообщения. По умолчанию `False`.

**Вызывает исключения**:
- `ValueError`: Если `artifact_data` не является строкой или словарем.
- `ValueError`: Если `target_format` не поддерживается.

**Как работает функция**:

1.  Проверяет тип `artifact_data`.
2.  Очищает имя артефакта от недопустимых символов.
3.  Формирует путь к файлу с помощью `_compose_filepath`.
4.  Вызывает соответствующий метод экспорта в зависимости от `target_format` (`_export_as_json`, `_export_as_txt`, `_export_as_docx`).

**Примеры**:

```python
exporter = ArtifactExporter("output")
exporter.export("my_artifact", {"key": "value"}, "data", target_format="json")
exporter.export("my_text", "Hello, world!", "text", target_format="txt")
```

### `ArtifactExporter._export_as_txt`

```python
def _export_as_txt(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False) -> None:
    """
    Экспортирует указанные данные артефакта в текстовый файл.
    """
```

**Назначение**: Экспорт данных в текстовый файл.

**Параметры**:
- `artifact_file_path` (str): Полный путь к файлу, в который будут записаны данные.
- `artifact_data` (Union[dict, str]): Данные для экспорта. Если это словарь, то экспортируется значение ключа 'content'.
- `content_type` (str): Тип контента (не используется в этой функции, но передается для совместимости).
- `verbose` (bool, optional): Включает/выключает отладочные сообщения. По умолчанию `False`.

**Как работает функция**:
Функция открывает файл по указанному пути, извлекает контент из `artifact_data` (если это словарь, то берется значение по ключу `content`, иначе используется сама `artifact_data` как контент) и записывает его в файл.

**Примеры**:

```python
exporter = ArtifactExporter("output")
exporter._export_as_txt("output/text/my_text.txt", "Hello, world!", "text")
exporter._export_as_txt("output/data/my_data.txt", {"content": "Some data"}, "data")
```

### `ArtifactExporter._export_as_json`

```python
def _export_as_json(self, artifact_file_path: str, artifact_data: Union[dict, str], content_type: str, verbose: bool = False) -> None:
    """
    Экспортирует указанные данные артефакта в файл JSON.
    """
```

**Назначение**: Экспорт данных в JSON файл.

**Параметры**:
- `artifact_file_path` (str): Полный путь к файлу, в который будут записаны данные.
- `artifact_data` (Union[dict, str]): Данные для экспорта. Должны быть словарем.
- `content_type` (str): Тип контента (не используется в этой функции, но передается для совместимости).
- `verbose` (bool, optional): Включает/выключает отладочные сообщения. По умолчанию `False`.

**Вызывает исключения**:
- `ValueError`: Если `artifact_data` не является словарем.

**Как работает функция**:
Функция открывает файл по указанному пути и записывает `artifact_data` в файл в формате JSON с отступами.

**Примеры**:

```python
exporter = ArtifactExporter("output")
exporter._export_as_json("output/data/my_data.json", {"key": "value"}, "data")
```

### `ArtifactExporter._export_as_docx`

```python
def _export_as_docx(self, artifact_file_path: str, artifact_data: Union[dict, str], content_original_format: str, verbose: bool = False) -> None:
    """
    Экспортирует указанные данные артефакта в файл DOCX.
    """
```

**Назначение**: Экспорт данных в файл DOCX.

**Параметры**:
- `artifact_file_path` (str): Полный путь к файлу, в который будут записаны данные.
- `artifact_data` (Union[dict, str]): Данные для экспорта. Если это словарь, то экспортируется значение ключа 'content'.
- `content_original_format` (str): Исходный формат контента ("text", "txt", "markdown", "md").
- `verbose` (bool, optional): Включает/выключает отладочные сообщения. По умолчанию `False`.

**Вызывает исключения**:
- `ValueError`: Если `content_original_format` не поддерживается.

**Как работает функция**:

1.  Проверяет `content_original_format`.
2.  Извлекает контент из `artifact_data`.
3.  Конвертирует контент в HTML с помощью `markdown.markdown`.
4.  Конвертирует HTML в DOCX с помощью `pypandoc.convert_text`.

**Примеры**:

```python
exporter = ArtifactExporter("output")
exporter._export_as_docx("output/text/my_text.docx", "Hello, world!", "text")
exporter._export_as_docx("output/markdown/my_markdown.docx", "# Title", "markdown")
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
        content_type (str): Тип содержимого в артефакте.
        target_format (str, optional): Формат для экспорта артефакта (например, json, txt, docx и т. д.).
        verbose (bool, optional): Флаг для отображения отладочных сообщений.

    Returns:
        str: Полный путь к файлу.

    """
```

**Назначение**: Формирование полного пути к файлу для сохранения артефакта.

**Параметры**:
- `artifact_data` (Union[dict, str]): Данные артефакта (словарь или строка).
- `artifact_name` (str): Имя артефакта.
- `content_type` (str): Тип контента. Используется как имя подпапки.
- `target_format` (str, optional): Формат целевого файла (например, "json", "txt"). По умолчанию `None`.
- `verbose` (bool, optional): Флаг для отображения отладочных сообщений. По умолчанию `False`.

**Возвращает**:
- `str`: Сформированный путь к файлу.

**Как работает функция**:

1.  Определяет расширение файла на основе `target_format` или типа `artifact_data`.
2.  Определяет имя подпапки на основе `content_type`.
3.  Соединяет базовую папку, подпапку и имя файла с расширением.
4.  Создает промежуточные директории, если они не существуют.

**Примеры**:

```python
exporter = ArtifactExporter("output")
file_path = exporter._compose_filepath({"key": "value"}, "my_data", "data", target_format="json")
print(file_path)  # output/data/my_data.json

file_path = exporter._compose_filepath("Hello, world!", "my_text", "text")
print(file_path)  # output/text/my_text.txt
```

### `Normalizer.__init__`

```python
def __init__(self, elements: List[str], n: int, verbose: bool = False) -> None:
    """
    Нормализует указанные элементы.

    Args:
        elements (list): Элементы для нормализации.
        n (int): Количество нормализованных элементов для вывода.
        verbose (bool, optional): Флаг для отображения отладочных сообщений. По умолчанию `False`.

    """
```

**Назначение**: Инициализация экземпляра класса `Normalizer`.

**Параметры**:
- `elements` (List[str]): Список строк, которые нужно нормализовать.
- `n` (int): Количество нормализованных элементов, которые должны быть получены в результате.
- `verbose` (bool, optional):  Флаг для отображения отладочных сообщений. По умолчанию `False`.

**Как работает функция**:

1.  Удаляет дубликаты из списка `elements`.
2.  Сохраняет параметры `n` и `verbose`.
3.  Компонует начальные сообщения для LLM (Language Model) с использованием шаблонов "normalizer.system.mustache" и "normalizer.user.mustache".
4.  Отправляет сообщения в LLM для нормализации элементов.
5.  Извлекает результат нормализации из ответа LLM.
6.  Сохраняет результат в `self.normalized_elements`.

**Примеры**:

```python
normalizer = Normalizer(["apple", "banana", "apple", "orange"], 2, verbose=True)
print(normalizer.normalized_elements)
```

### `Normalizer.normalize`

```python
def normalize(self, element_or_elements: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Нормализует указанный элемент или элементы.

    Этот метод использует механизм кэширования для повышения производительности. Если элемент был нормализован ранее,
    его нормализованная форма хранится в кэше (self.normalizing_map). Когда тот же элемент нужно
    нормализовать снова, метод сначала проверит кэш и использует сохраненную нормализованную форму, если она доступна,
    вместо повторной нормализации элемента.

    Порядок элементов в выходных данных будет таким же, как и во входных. Это обеспечивается обработкой
    элементов в том порядке, в котором они появляются на входе, и добавлением нормализованных элементов к выходу
    список в том же порядке.

    Args:
        element_or_elements (Union[str, List[str]]): Элемент или элементы для нормализации.

    Returns:
        str: Нормализованный элемент, если вход был строкой.
        list: Нормализованные элементы, если вход был списком, с сохранением порядка элементов на входе.

    """
```

**Назначение**: Нормализация одного или нескольких элементов.

**Параметры**:
- `element_or_elements` (Union[str, List[str]]): Элемент (строка) или список элементов (строк), которые необходимо нормализовать.

**Возвращает**:
- `Union[str, List[str]]`: Нормализованный элемент (строка) или список нормализованных элементов (строк), в зависимости от типа входных данных.

**Как работает функция**:

1.  Проверяет тип входных данных (`element_or_elements`). Если это строка, она преобразуется в список из одного элемента.
2.  Создает пустой список `normalized_elements` для хранения нормализованных элементов.
3.  Создает пустой список `elements_to_normalize` для хранения элементов, которые еще не были нормализованы и отсутствуют в кэше `self.normalizing_map`.
4.  Перебирает входные элементы и проверяет, есть ли они в кэше `self.normalizing_map`. Если элемент отсутствует в кэше, он добавляется в `elements_to_normalize`.
5.  Если `elements_to_normalize` не пуст, функция отправляет запрос в LLM для нормализации этих элементов.
6.  Извлекает нормализованные элементы из ответа LLM.
7.  Обновляет кэш `self.normalizing_map` нормализованными элементами.
8.  Перебирает входные элементы и добавляет соответствующие нормализованные элементы из кэша `self.normalizing_map` в список `normalized_elements`.
9.  Возвращает нормализованные элементы.

**Примеры**:

```python
normalizer = Normalizer(["apple", "banana", "orange"], 2)
normalized_element = normalizer.normalize("apple")
print(normalized_element)

normalized_elements = normalizer.normalize(["apple", "banana", "orange"])
print(normalized_elements)
```