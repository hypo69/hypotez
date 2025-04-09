# Модуль для извлечения данных из TinyTroupe
==================================================

Модуль предоставляет утилиты для извлечения данных из элементов TinyTroupe, таких как агенты и миры. Он также предоставляет механизм для сокращения извлеченных данных до более лаконичной формы и экспорта артефактов из элементов TinyTroupe.

## Обзор

Этот модуль предназначен для извлечения, обработки и экспорта данных из симуляций TinyTroupe. Он предоставляет классы и функции для извлечения информации из агентов (TinyPerson) и миров (TinyWorld), а также для нормализации и экспорта этих данных в различные форматы, такие как JSON, TXT и DOCX.

## Подробнее

Модуль содержит классы `ResultsExtractor`, `ResultsReducer` и `ArtifactExporter`, которые используются для извлечения результатов, их сокращения и экспорта артефактов соответственно. Также присутствует класс `Normalizer` для нормализации текстовых элементов.

## Классы

### `ResultsExtractor`

**Описание**: Класс для извлечения результатов из экземпляров `TinyPerson` и `TinyWorld`.

**Принцип работы**: Класс использует шаблоны (`.mustache`) и OpenAI API для извлечения данных. Он кэширует последние результаты извлечения для каждого типа, чтобы их можно было использовать для создания отчетов или других дополнительных выходных данных.

**Методы**:

- `__init__`: Инициализирует экземпляр класса, устанавливает путь к шаблону запроса на извлечение и создает кэш для результатов извлечения агентов и миров.
- `extract_results_from_agent`: Извлекает результаты из экземпляра `TinyPerson`.
- `extract_results_from_world`: Извлекает результаты из экземпляра `TinyWorld`.
- `save_as_json`: Сохраняет последние результаты извлечения в формате JSON.

### `ResultsReducer`

**Описание**: Класс для сокращения данных, извлеченных из агентов.

**Принцип работы**: Класс применяет правила сокращения к сообщениям из эпизодической памяти агента и преобразует сокращенные данные в DataFrame.

**Методы**:

- `__init__`: Инициализирует экземпляр класса, создает словари для хранения результатов и правил сокращения.
- `add_reduction_rule`: Добавляет правило сокращения для определенного триггера.
- `reduce_agent`: Сокращает данные агента на основе установленных правил.
- `reduce_agent_to_dataframe`: Преобразует сокращенные данные агента в DataFrame.

### `ArtifactExporter`

**Описание**: Класс для экспорта артефактов из элементов TinyTroupe в различные форматы файлов.

**Принцип работы**: Класс позволяет сохранять данные в форматах JSON, TXT и DOCX, автоматически создавая необходимые подкаталоги и обрабатывая недопустимые символы в именах артефактов.

**Методы**:

- `__init__`: Инициализирует экземпляр класса, устанавливает базовую папку для вывода артефактов.
- `export`: Экспортирует данные артефакта в файл указанного формата.
- `_export_as_txt`: Экспортирует данные в текстовый файл.
- `_export_as_json`: Экспортирует данные в JSON файл.
- `_export_as_docx`: Экспортирует данные в DOCX файл.
- `_compose_filepath`: Составляет путь к файлу для экспортируемого артефакта.

### `Normalizer`

**Описание**: Класс для нормализации текстовых элементов.

**Принцип работы**: Класс использует OpenAI API для нормализации списка элементов и кэширует результаты для повышения производительности.

**Методы**:

- `__init__`: Инициализирует экземпляр класса, выполняет нормализацию элементов с использованием OpenAI API и создает карту нормализации.
- `normalize`: Нормализует указанный элемент или список элементов, используя кэш, если это возможно.

## Функции

### `ResultsExtractor.extract_results_from_agent`

```python
def extract_results_from_agent(self, 
                        tinyperson:TinyPerson, 
                        extraction_objective:str="The main points present in the agent's interactions history.", 
                        situation:str = "", 
                        fields:list=None,
                        fields_hints:dict=None,
                        verbose:bool=False) -> dict | None:
    """
    Извлекает результаты из экземпляра `TinyPerson`.

    Args:
        tinyperson (TinyPerson): Экземпляр `TinyPerson`, из которого нужно извлечь результаты.
        extraction_objective (str): Цель извлечения. Описывает, какие данные нужно извлечь из истории взаимодействий агента. По умолчанию "The main points present in the agent's interactions history.".
        situation (str): Описание ситуации, которую нужно учитывать при извлечении. По умолчанию "".
        fields (list, optional): Список полей для извлечения. Если `None`, экстрактор сам решает, какие имена использовать. По умолчанию `None`.
        fields_hints (dict, optional): Словарь с подсказками для полей. По умолчанию `None`.
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

    Returns:
        dict | None: Результат извлечения в виде словаря, или `None`, если извлечение не удалось.

    Raises:
        Exception: Если возникает ошибка при отправке сообщения в OpenAI API.

    Example:
        >>> extractor = ResultsExtractor()
        >>> agent = TinyPerson(name='Alice')
        >>> results = extractor.extract_results_from_agent(agent, extraction_objective='Summarize the agent\'s goals.')
        >>> if results:
        ...     print(results)
        {'goals': 'Agent Alice wants to make friends.'}
    """
    ...
```

**Назначение**: Извлечение результатов из истории взаимодействий агента `TinyPerson` с использованием OpenAI API.

**Параметры**:
- `tinyperson` (TinyPerson): Экземпляр агента, из которого извлекаются данные.
- `extraction_objective` (str): Цель извлечения, определяет, какие данные должны быть извлечены из истории взаимодействий агента.
- `situation` (str): Описание ситуации, которую следует учитывать при извлечении данных.
- `fields` (list, optional): Список полей для извлечения. Если не указан, экстрактор сам определяет, какие поля извлекать.
- `fields_hints` (dict, optional): Словарь с подсказками для полей извлечения.
- `verbose` (bool, optional): Флаг, указывающий, следует ли выводить отладочные сообщения.

**Возвращает**:
- `dict | None`: Результат извлечения в виде словаря или `None` в случае ошибки.

**Как работает функция**:
1. Формирует сообщение для OpenAI API, используя шаблон `interaction_results_extractor.mustache` и переданные параметры.
2. Добавляет историю взаимодействий агента в запрос.
3. Отправляет запрос в OpenAI API и получает ответ.
4. Извлекает JSON из ответа и кэширует результат.
5. Возвращает извлеченный JSON.

```
Начало
  │
  ├── Формирование сообщения для OpenAI API
  │   │
  │   └── Добавление истории взаимодействий агента
  │       │
  │       └── Отправка запроса в OpenAI API
  │           │
  │           └── Извлечение JSON из ответа
  │               │
  │               └── Кэширование результата
  │                   │
  │                   └── Возврат извлеченного JSON
  │
Конец
```

**Примеры**:

```python
extractor = ResultsExtractor()
agent = TinyPerson(name='Alice')
results = extractor.extract_results_from_agent(agent, extraction_objective='Summarize the agent\'s goals.')
if results:
    print(results)
```

### `ResultsExtractor.extract_results_from_world`

```python
def extract_results_from_world(self, 
                                   tinyworld:TinyWorld, 
                                   extraction_objective:str="The main points that can be derived from the agents conversations and actions.", 
                                   situation:str="", 
                                   fields:list=None,
                                   fields_hints:dict=None,
                                   verbose:bool=False) -> dict | None:
    """
    Извлекает результаты из экземпляра `TinyWorld`.

    Args:
        tinyworld (TinyWorld): Экземпляр `TinyWorld`, из которого нужно извлечь результаты.
        extraction_objective (str): Цель извлечения. Описывает, какие данные нужно извлечь из истории взаимодействий агентов в мире. По умолчанию "The main points that can be derived from the agents conversations and actions.".
        situation (str): Описание ситуации, которую нужно учитывать при извлечении. По умолчанию "".
        fields (list, optional): Список полей для извлечения. Если `None`, экстрактор сам решает, какие имена использовать. По умолчанию `None`.
        fields_hints (dict, optional): Словарь с подсказками для полей. По умолчанию `None`.
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

    Returns:
        dict | None: Результат извлечения в виде словаря, или `None`, если извлечение не удалось.

    Raises:
        Exception: Если возникает ошибка при отправке сообщения в OpenAI API.

    Example:
        >>> extractor = ResultsExtractor()
        >>> world = TinyWorld(name='Wonderland')
        >>> results = extractor.extract_results_from_world(world, extraction_objective='Summarize the main events in the world.')
        >>> if results:
        ...     print(results)
        {'events': 'Alice met the Mad Hatter.'}
    """
    ...
```

**Назначение**: Извлечение результатов из истории взаимодействий агентов в мире `TinyWorld` с использованием OpenAI API.

**Параметры**:
- `tinyworld` (TinyWorld): Экземпляр мира, из которого извлекаются данные.
- `extraction_objective` (str): Цель извлечения, определяет, какие данные должны быть извлечены из истории взаимодействий агентов в мире.
- `situation` (str): Описание ситуации, которую следует учитывать при извлечении данных.
- `fields` (list, optional): Список полей для извлечения. Если не указан, экстрактор сам определяет, какие поля извлекать.
- `fields_hints` (dict, optional): Словарь с подсказками для полей извлечения.
- `verbose` (bool, optional): Флаг, указывающий, следует ли выводить отладочные сообщения.

**Возвращает**:
- `dict | None`: Результат извлечения в виде словаря или `None` в случае ошибки.

**Как работает функция**:
1. Формирует сообщение для OpenAI API, используя шаблон `interaction_results_extractor.mustache` и переданные параметры.
2. Добавляет историю взаимодействий агентов в мире в запрос.
3. Отправляет запрос в OpenAI API и получает ответ.
4. Извлекает JSON из ответа и кэширует результат.
5. Возвращает извлеченный JSON.

```
Начало
  │
  ├── Формирование сообщения для OpenAI API
  │   │
  │   └── Добавление истории взаимодействий агентов в мире
  │       │
  │       └── Отправка запроса в OpenAI API
  │           │
  │           └── Извлечение JSON из ответа
  │               │
  │               └── Кэширование результата
  │                   │
  │                   └── Возврат извлеченного JSON
  │
Конец
```

**Примеры**:

```python
extractor = ResultsExtractor()
world = TinyWorld(name='Wonderland')
results = extractor.extract_results_from_world(world, extraction_objective='Summarize the main events in the world.')
if results:
    print(results)
```

### `ResultsExtractor.save_as_json`

```python
def save_as_json(self, filename:str, verbose:bool=False) -> None:
    """
    Сохраняет последние результаты извлечения в формате JSON.

    Args:
        filename (str): Имя файла для сохранения JSON.
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

    Raises:
        Exception: Если возникает ошибка при записи в файл.

    Example:
        >>> extractor = ResultsExtractor()
        >>> extractor.save_as_json('extraction_results.json', verbose=True)
        Saved extraction results to extraction_results.json
    """
    ...
```

**Назначение**: Сохранение последних извлеченных результатов (агентов и миров) в файл в формате JSON.

**Параметры**:
- `filename` (str): Имя файла, в который будут сохранены результаты.
- `verbose` (bool, optional): Флаг для включения/выключения отладочных сообщений.

**Как работает функция**:
1. Открывает файл с указанным именем для записи.
2. Записывает в файл JSON, содержащий результаты извлечения для агентов и миров.
3. Выводит отладочное сообщение, если `verbose` установлен в `True`.

```
Начало
  │
  ├── Открытие файла для записи
  │   │
  │   └── Запись JSON в файл
  │       │
  │       └── Вывод отладочного сообщения (если verbose=True)
  │
Конец
```

**Примеры**:

```python
extractor = ResultsExtractor()
extractor.save_as_json('extraction_results.json', verbose=True)
```

### `ResultsReducer.add_reduction_rule`

```python
def add_reduction_rule(self, trigger: str, func: callable) -> None:
    """
    Добавляет правило сокращения для определенного триггера.

    Args:
        trigger (str): Триггер, для которого добавляется правило.
        func (callable): Функция, которая будет вызвана при срабатывании триггера.

    Raises:
        Exception: Если правило для указанного триггера уже существует.

    Example:
        >>> reducer = ResultsReducer()
        >>> def my_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        ...     return {'event': event, 'content': content}
        >>> reducer.add_reduction_rule('stimulus_type', my_rule)
    """
    ...
```

**Назначение**: Добавление правила сокращения в класс `ResultsReducer`.

**Параметры**:
- `trigger` (str): Строка, представляющая триггер, при котором должно применяться правило.
- `func` (callable): Функция, которая будет вызываться для сокращения данных при срабатывании триггера.

**Как работает функция**:
1. Проверяет, существует ли уже правило для указанного триггера.
2. Если правило уже существует, вызывает исключение.
3. Если правило не существует, добавляет функцию `func` в словарь `self.rules` под ключом `trigger`.

```
Начало
  │
  ├── Проверка существования правила для триггера
  │   │
  │   ├── Правило существует: Вызов исключения
  │   │
  │   └── Правило не существует: Добавление функции в словарь self.rules
  │
Конец
```

**Примеры**:

```python
reducer = ResultsReducer()
def my_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
    return {'event': event, 'content': content}
reducer.add_reduction_rule('stimulus_type', my_rule)
```

### `ResultsReducer.reduce_agent`

```python
def reduce_agent(self, agent: TinyPerson) -> list:
    """
    Сокращает данные агента на основе установленных правил.

    Args:
        agent (TinyPerson): Агент, данные которого нужно сократить.

    Returns:
        list: Список сокращенных данных.

    Raises:
        Exception: Если возникает ошибка при применении правил сокращения.

    Example:
        >>> reducer = ResultsReducer()
        >>> def my_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        ...     return {'event': event, 'content': content}
        >>> reducer.add_reduction_rule('stimulus_type', my_rule)
        >>> agent = TinyPerson(name='Alice')
        >>> reduction = reducer.reduce_agent(agent)
    """
    ...
```

**Назначение**: Сокращение данных агента `TinyPerson` на основе установленных правил.

**Параметры**:
- `agent` (TinyPerson): Агент, чьи данные нужно сократить.

**Возвращает**:
- `list`: Список сокращенных данных.

**Как работает функция**:
1. Итерируется по всем сообщениям в эпизодической памяти агента.
2. Пропускает сообщения с ролью `system`.
3. Для сообщений с ролью `user` извлекает тип, контент и источник стимула, а также временную метку.
4. Если для типа стимула существует правило сокращения, применяет его и добавляет результат в список сокращений.
5. Для сообщений с ролью `assistant` извлекает тип, контент и цель действия, а также временную метку.
6. Если для типа действия существует правило сокращения, применяет его и добавляет результат в список сокращений.
7. Возвращает список сокращенных данных.

```
Начало
  │
  ├── Итерация по сообщениям в эпизодической памяти агента
  │   │
  │   ├── Пропуск сообщений с ролью `system`
  │   │
  │   ├── Сообщение с ролью `user`: Извлечение типа, контента и источника стимула
  │   │   │
  │   │   └── Применение правила сокращения (если существует)
  │   │
  │   └── Сообщение с ролью `assistant`: Извлечение типа, контента и цели действия
  │       │
  │       └── Применение правила сокращения (если существует)
  │
Конец
```

**Примеры**:

```python
reducer = ResultsReducer()
def my_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
    return {'event': event, 'content': content}
reducer.add_reduction_rule('stimulus_type', my_rule)
agent = TinyPerson(name='Alice')
reduction = reducer.reduce_agent(agent)
```

### `ResultsReducer.reduce_agent_to_dataframe`

```python
def reduce_agent_to_dataframe(self, agent: TinyPerson, column_names: list=None) -> pd.DataFrame:
    """
    Преобразует сокращенные данные агента в DataFrame.

    Args:
        agent (TinyPerson): Агент, данные которого нужно сократить и преобразовать в DataFrame.
        column_names (list, optional): Список имен столбцов для DataFrame. Если `None`, используются имена столбцов по умолчанию. По умолчанию `None`.

    Returns:
        pd.DataFrame: DataFrame с сокращенными данными агента.

    Raises:
        Exception: Если возникает ошибка при создании DataFrame.

    Example:
        >>> reducer = ResultsReducer()
        >>> def my_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        ...     return {'event': event, 'content': content}
        >>> reducer.add_reduction_rule('stimulus_type', my_rule)
        >>> agent = TinyPerson(name='Alice')
        >>> df = reducer.reduce_agent_to_dataframe(agent, column_names=['event', 'content'])
    """
    ...
```

**Назначение**: Преобразование сокращенных данных агента в объект `pd.DataFrame`.

**Параметры**:
- `agent` (TinyPerson): Агент, чьи данные будут сокращены и преобразованы в DataFrame.
- `column_names` (list, optional): Список имен столбцов для DataFrame. Если не указан, используются имена столбцов по умолчанию.

**Возвращает**:
- `pd.DataFrame`: DataFrame, содержащий сокращенные данные агента.

**Как работает функция**:
1. Вызывает метод `reduce_agent` для сокращения данных агента.
2. Создает DataFrame из списка сокращенных данных, используя указанные имена столбцов (если они предоставлены).
3. Возвращает созданный DataFrame.

```
Начало
  │
  ├── Вызов метода `reduce_agent`
  │   │
  │   └── Создание DataFrame из сокращенных данных
  │       │
  │       └── Возврат DataFrame
  │
Конец
```

**Примеры**:

```python
reducer = ResultsReducer()
def my_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
    return {'event': event, 'content': content}
reducer.add_reduction_rule('stimulus_type', my_rule)
agent = TinyPerson(name='Alice')
df = reducer.reduce_agent_to_dataframe(agent, column_names=['event', 'content'])
```

### `ArtifactExporter.export`

```python
def export(self, artifact_name:str, artifact_data:Union[dict, str], content_type:str, content_format:str=None, target_format:str="txt", verbose:bool=False) -> None:
    """
    Экспортирует указанные данные артефакта в файл.

    Args:
        artifact_name (str): Имя артефакта.
        artifact_data (Union[dict, str]): Данные для экспорта. Если передан словарь, он будет сохранен в формате JSON. Если передана строка, она будет сохранена как есть.
        content_type (str): Тип контента внутри артефакта.
        content_format (str, optional): Формат контента внутри артефакта (например, md, csv и т.д.). По умолчанию `None`.
        target_format (str): Формат для экспорта артефакта (например, json, txt, docx и т.д.).
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

    Raises:
        ValueError: Если `artifact_data` не является строкой или словарем.
        ValueError: Если `target_format` не поддерживается.

    Example:
        >>> exporter = ArtifactExporter('output')
        >>> exporter.export('agent_data', {'name': 'Alice', 'age': 30}, 'agent', target_format='json', verbose=True)
        Saved extraction results to output/agent/agent_data.json
    """
    ...
```

**Назначение**: Экспорт данных артефакта в файл заданного формата.

**Параметры**:
- `artifact_name` (str): Имя артефакта (имя файла без расширения).
- `artifact_data` (Union[dict, str]): Данные для экспорта. Могут быть строкой или словарем.
- `content_type` (str): Тип контента (имя подкаталога, в котором будет сохранен файл).
- `content_format` (str, optional): Формат контента (например, 'md', 'csv'). Используется для формирования имени файла. По умолчанию `None`.
- `target_format` (str): Целевой формат файла (например, 'json', 'txt', 'docx'). По умолчанию 'txt'.
- `verbose` (bool, optional): Флаг для включения/выключения отладочных сообщений.

**Как работает функция**:
1. Удаляет лишние отступы из данных артефакта, если это строка или словарь.
2. Очищает имя артефакта от недопустимых символов.
3. Составляет путь к файлу, используя метод `_compose_filepath`.
4. В зависимости от `target_format` вызывает соответствующие методы экспорта (`_export_as_json`, `_export_as_txt`, `_export_as_docx`).

```
Начало
  │
  ├── Удаление отступов из данных артефакта
  │   │
  │   ├── Очистка имени артефакта от недопустимых символов
  │   │   │
  │   │   └── Составление пути к файлу
  │   │       │
  │   │       └── Вызов метода экспорта в зависимости от target_format
  │   │
  │   └── Конец
  │
Конец
```

**Примеры**:

```python
exporter = ArtifactExporter('output')
exporter.export('agent_data', {'name': 'Alice', 'age': 30}, 'agent', target_format='json', verbose=True)
```

### `ArtifactExporter._export_as_txt`

```python
def _export_as_txt(self, artifact_file_path:str, artifact_data:Union[dict, str], content_type:str, verbose:bool=False) -> None:
    """
    Экспортирует указанные данные артефакта в текстовый файл.
    """
    ...
```

**Назначение**: Экспорт данных артефакта в текстовый файл.

**Параметры**:
- `artifact_file_path` (str): Путь к файлу, в который будут записаны данные.
- `artifact_data` (Union[dict, str]): Данные для экспорта. Если это словарь, то извлекается значение по ключу `content`.
- `content_type` (str): Тип контента (не используется в этой функции, но необходим для соответствия интерфейсу).
- `verbose` (bool, optional): Флаг для включения/выключения отладочных сообщений (не используется в этой функции).

**Как работает функция**:
1. Открывает файл по указанному пути для записи в кодировке UTF-8.
2. Если `artifact_data` является словарем, извлекает значение по ключу `'content'`.
3. Записывает содержимое в файл.

```
Начало
  │
  ├── Открытие файла для записи
  │   │
  │   ├── Извлечение контента из словаря (если artifact_data - словарь)
  │   │   │
  │   │   └── Запись контента в файл
  │   │
  │   └── Конец
  │
Конец
```

### `ArtifactExporter._export_as_json`

```python
def _export_as_json(self, artifact_file_path:str, artifact_data:Union[dict, str], content_type:str, verbose:bool=False) -> None:
    """
    Экспортирует указанные данные артефакта в JSON файл.
    """
    ...
```

**Назначение**: Экспорт данных артефакта в JSON файл.

**Параметры**:
- `artifact_file_path` (str): Путь к файлу, в который будут записаны данные.
- `artifact_data` (Union[dict, str]): Данные для экспорта. Должны быть словарем.
- `content_type` (str): Тип контента (не используется в этой функции, но необходим для соответствия интерфейсу).
- `verbose` (bool, optional): Флаг для включения/выключения отладочных сообщений (не используется в этой функции).

**Вызывает исключения**:
- `ValueError`: Если `artifact_data` не является словарем.

**Как работает функция**:
1. Открывает файл по указанному пути для записи в кодировке UTF-8.
2. Проверяет, является ли `artifact_data` словарем. Если нет, вызывает исключение `ValueError`.
3. Записывает словарь в файл в формате JSON с отступами.

```
Начало
  │
  ├── Открытие файла для записи
  │   │
  │   ├── Проверка, является ли artifact_data словарем
  │   │   │
  │   │   ├── Если не словарь: Вызов исключения ValueError
  │   │   │
  │   │   └── Если словарь: Запись в файл в формате JSON
  │   │
  │   └── Конец
  │
Конец
```

### `ArtifactExporter._export_as_docx`

```python
def _export_as_docx(self, artifact_file_path:str, artifact_data:Union[dict, str], content_original_format:str, verbose:bool=False) -> None:
    """
    Экспортирует указанные данные артефакта в DOCX файл.
    """
    ...
```

**Назначение**: Экспорт данных артефакта в файл формата DOCX.

**Параметры**:
- `artifact_file_path` (str): Путь к файлу, в который будут записаны данные.
- `artifact_data` (Union[dict, str]): Данные для экспорта. Если это словарь, то извлекается значение по ключу `content`.
- `content_original_format` (str): Исходный формат контента (например, 'text', 'markdown').
- `verbose` (bool, optional): Флаг для включения/выключения отладочных сообщений (не используется в этой функции).

**Вызывает исключения**:
- `ValueError`: Если `content_original_format` не является допустимым значением ('text', 'txt', 'markdown', 'md').

**Как работает функция**:
1. Проверяет допустимость значения `content_original_format`.
2. Извлекает контент из `artifact_data`. Если `artifact_data` является словарем, то извлекается значение по ключу `content`.
3. Преобразует контент в HTML с использованием библиотеки `markdown`.
4. Преобразует HTML в DOCX с использованием библиотеки `pypandoc`.

```
Начало
  │
  ├── Проверка допустимости content_original_format
  │   │
  │   ├── Извлечение контента из artifact_data
  │   │   │
  │   │   ├── Преобразование контента в HTML
  │   │   │
  │   │   └── Преобразование HTML в DOCX
  │   │
  │   └── Конец
  │
Конец
```

### `ArtifactExporter._compose_filepath`

```python
def _compose_filepath(self, artifact_data:Union[dict, str], artifact_name:str, content_type:str, target_format:str=None, verbose:bool=False) -> str:
    """
    Составляет путь к файлу для экспортируемого артефакта.

    Args:
        artifact_data (Union[dict, str]): Данные для экспорта.
        artifact_name (str): Имя артефакта.
        content_type (str): Тип контента внутри артефакта.
        target_format (str, optional): Формат для экспорта артефакта (например, json, txt, docx и т.д.).
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

    Returns:
        str: Сформированный путь к файлу.

    Raises:
        ValueError: Если `artifact_data` не является строкой или словарем.
        ValueError: Если `target_format` не поддерживается.

    Example:
        >>> exporter = ArtifactExporter('output')
        >>> file_path = exporter._compose_filepath({'content': 'test'}, 'my_artifact', 'test_type', target_format='json')
        >>> print(file_path)
        output/test_type/my_artifact.json
    """
    ...
```

**Назначение**: Функция составляет путь к файлу для экспортируемого артефакта, основываясь на переданных параметрах.

**Параметры**:
- `artifact_data` (Union[dict, str]): Данные для экспорта. Используется для определения расширения файла, если `target_format` не указан.
- `artifact_name` (str): Имя артефакта, которое будет использовано в имени файла.
- `content_type` (str): Тип контента, который будет использован в качестве подпапки для сохранения файла.
- `target_format` (str, optional): Целевой формат файла (например, 'json', 'txt', 'docx'). Если указан, используется для определения расширения файла. По умолчанию `None`.
- `verbose` (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.

**Возвращает**:
- `str`: Сформированный путь к файлу.

**Как работает функция**:

1.  Определяет расширение файла в зависимости от `target_format` и типа `artifact_data`.
2.  Определяет подпапку для сохранения файла на основе `content_type`.
3.  Составляет полный путь к файлу, объединяя базовую папку вывода, подпапку и имя файла с расширением.
4.  Создает промежуточные каталоги, если они не существуют.
5.  Возвращает сформированный путь к файлу.

```
Начало
  │
  ├── Определение расширения файла
  │   │
  │   ├── Определение подпапки
  │   │   │
  │   │   ├── Составление полного пути к файлу
  │   │   │   │
  │   │   │   ├── Создание промежуточных каталогов (если необходимо)
  │   │   │   │   │
  │   │   │   │   └── Возврат сформированного пути к файлу
  │   │   │   │
  │   │   │   └── Конец
  │   │   │
  │   │   └── Конец
  │   │
  │   └── Конец
  │
Конец
```

**Примеры**:

```python
exporter = ArtifactExporter('output')
file_path = exporter._compose_filepath({'content': 'test'}, 'my_artifact', 'test_type', target_format='json')
print(file_path)
```

### `Normalizer.__init__`

```python
def __init__(self, elements:List[str], n:int, verbose:bool=False) -> None:
    """
    Нормализует указанные элементы.

    Args:
        elements (list): Элементы для нормализации.
        n (int): Количество нормализованных элементов для вывода.
        verbose (bool, optional): Флаг, указывающий, нужно ли выводить отладочные сообщения. По умолчанию `False`.
    """
    ...
```

**Назначение**: Инициализация экземпляра класса `Normalizer`.

**Параметры**:
- `elements` (list): Список элементов для нормализации.
- `n` (int): Количество нормализованных элементов, которые нужно получить в результате.
- `verbose` (bool, optional): Флаг для включения/выключения отладочных сообщений.