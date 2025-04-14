# Модуль для реализации коннекторов заземления (Grounding)
## Обзор
Модуль `grounding.py` предоставляет инструменты для создания и управления коннекторами заземления (grounding connectors), которые позволяют агентам привязывать свои знания к внешним источникам, таким как файлы, веб-страницы и базы данных. Он содержит абстрактный класс `GroundingConnector` и его реализации для работы с семантическим поиском, локальными файлами и веб-страницами.

## Подробнее
Этот модуль является частью проекта `hypotez` и предназначен для использования в компонентах, требующих доступа к внешним знаниям для улучшения контекста и точности принимаемых решений. Он использует библиотеку `llama_index` для индексации и поиска документов на основе семантического анализа.
В модуле реализованы следующие классы:

*   `GroundingConnector`: Абстрактный класс, определяющий интерфейс для всех коннекторов заземления.
*   `BaseSemanticGroundingConnector`: Базовый класс для семантических коннекторов заземления, использующих `llama_index` для индексации и поиска документов.
*   `LocalFilesGroundingConnector`: Коннектор заземления для работы с локальными файлами.
*   `WebPagesGroundingConnector`: Коннектор заземления для работы с веб-страницами.

## Классы

### `GroundingConnector`

**Описание**: Абстрактный класс, представляющий коннектор заземления.

**Атрибуты**:

*   `name` (str): Имя коннектора.

**Методы**:

*   `__init__(self, name: str) -> None`: Инициализирует экземпляр класса `GroundingConnector`.
*   `retrieve_relevant(self, relevance_target: str, source: str, top_k=20) -> list`: Извлекает релевантные данные из источника на основе целевого запроса.
*   `retrieve_by_name(self, name: str) -> str`: Извлекает источник контента по его имени.
*   `list_sources(self) -> list`: Возвращает список доступных источников контента.

### `BaseSemanticGroundingConnector`

**Описание**: Базовый класс для семантических коннекторов заземления, использующих `llama_index` для индексации и поиска документов.

**Наследует**: `GroundingConnector`

**Атрибуты**:

*   `documents` (list): Список документов для индексации.
*   `name_to_document` (dict): Словарь, сопоставляющий имена документов с их содержимым.

**Методы**:

*   `__init__(self, name: str = "Semantic Grounding") -> None`: Инициализирует экземпляр класса `BaseSemanticGroundingConnector`.
*   `_post_init(self)`: Выполняет постобработку инициализации после `__init__`.
*   `retrieve_relevant(self, relevance_target: str, top_k=20) -> list`: Извлекает все значения из памяти, релевантные заданной цели.
*   `retrieve_by_name(self, name: str) -> list`: Извлекает источник контента по его имени.
*   `list_sources(self) -> list`: Возвращает список доступных источников контента.
*   `add_document(self, document, doc_to_name_func=None) -> None`: Индексирует один документ для семантического поиска.
*   `add_documents(self, new_documents, doc_to_name_func=None) -> list`: Индексирует несколько документов для семантического поиска.

### `LocalFilesGroundingConnector`

**Описание**: Коннектор заземления для работы с локальными файлами.

**Наследует**: `BaseSemanticGroundingConnector`

**Атрибуты**:

*   `folders_paths` (list): Список путей к папкам с файлами для заземления.
*    `loaded_folders_paths` (list): Список путей к уже загруженным папкам.

**Методы**:

*   `__init__(self, name: str = "Local Files", folders_paths: list = None) -> None`: Инициализирует экземпляр класса `LocalFilesGroundingConnector`.
*   `_post_init(self)`: Выполняет постобработку инициализации после `__init__`.
*   `add_folders(self, folders_paths: list) -> None`: Добавляет пути к папкам с файлами, используемыми для заземления.
*   `add_folder(self, folder_path: str) -> None`: Добавляет путь к папке с файлами, используемыми для заземления.
*   `add_file_path(self, file_path: str) -> None`: Добавляет путь к файлу, используемому для заземления.
*   `_mark_folder_as_loaded(self, folder_path: str) -> None`: Помечает папку как загруженную.

### `WebPagesGroundingConnector`

**Описание**: Коннектор заземления для работы с веб-страницами.

**Наследует**: `BaseSemanticGroundingConnector`

**Атрибуты**:

*   `web_urls` (list): Список URL-адресов веб-страниц для заземления.
*   `loaded_web_urls` (list): Список URL-адресов уже загруженных веб-страниц.

**Методы**:

*   `__init__(self, name: str = "Web Pages", web_urls: list = None) -> None`: Инициализирует экземпляр класса `WebPagesGroundingConnector`.
*   `_post_init(self)`: Выполняет постобработку инициализации после `__init__`.
*   `add_web_urls(self, web_urls: list) -> None`: Добавляет данные, полученные с указанных URL-адресов, для заземления.
*   `add_web_url(self, web_url: str) -> None`: Добавляет данные, полученные с указанного URL-адреса, для заземления.
*   `_mark_web_url_as_loaded(self, web_url: str) -> None`: Помечает веб-страницу как загруженную.

## Методы класса

### `GroundingConnector`

#### `__init__`

```python
def __init__(self, name: str) -> None:
    """
    Args:
        name (str): Имя коннектора.
    """
```

#### `retrieve_relevant`

```python
def retrieve_relevant(self, relevance_target: str, source: str, top_k=20) -> list:
    """
    Args:
        relevance_target (str): Целевой запрос для определения релевантности.
        source (str): Источник данных для поиска.
        top_k (int): Количество наиболее релевантных результатов для возврата.

    Returns:
        list: Список релевантных данных.

    Raises:
        NotImplementedError: Если метод не реализован в подклассе.
    """
```

#### `retrieve_by_name`

```python
def retrieve_by_name(self, name: str) -> str:
    """
    Args:
        name (str): Имя источника контента для извлечения.

    Returns:
        str: Источник контента.

    Raises:
        NotImplementedError: Если метод не реализован в подклассе.
    """
```

#### `list_sources`

```python
def list_sources(self) -> list:
    """
    Returns:
        list: Список доступных источников контента.

    Raises:
        NotImplementedError: Если метод не реализован в подклассе.
    """
```

### `BaseSemanticGroundingConnector`

#### `__init__`

```python
def __init__(self, name: str = "Semantic Grounding") -> None:
    """
    Args:
        name (str): Имя коннектора заземления. По умолчанию "Semantic Grounding".
    """
```

#### `_post_init`

```python
def _post_init(self):
    """
    Выполняет постобработку инициализации после `__init__`.

    Эта функция вызывается декоратором `@utils.post_init` после выполнения метода `__init__`.
    Она инициализирует индекс и структуры данных, необходимые для семантического поиска.
    """
```

#### `retrieve_relevant`

```python
def retrieve_relevant(self, relevance_target: str, top_k=20) -> list:
    """
    Извлекает все значения из памяти, релевантные заданной цели.

    Args:
        relevance_target (str): Целевой запрос для определения релевантности.
        top_k (int): Количество наиболее релевантных результатов для возврата.

    Returns:
        list: Список релевантных данных.
    """
```

#### `retrieve_by_name`

```python
def retrieve_by_name(self, name: str) -> list:
    """
    Извлекает источник контента по его имени.

    Args:
        name (str): Имя источника контента для извлечения.

    Returns:
        list: Список, содержащий извлеченный контент.
    """
```

#### `list_sources`

```python
def list_sources(self) -> list:
    """
    Возвращает список доступных источников контента.

    Returns:
        list: Список имен доступных источников контента.
    """
```

#### `add_document`

```python
def add_document(self, document, doc_to_name_func=None) -> None:
    """
    Индексирует один документ для семантического поиска.

    Args:
        document (Document): Документ для индексации.
        doc_to_name_func (callable): Функция для извлечения имени из документа.
    """
```

#### `add_documents`

```python
def add_documents(self, new_documents, doc_to_name_func=None) -> list:
    """
    Индексирует несколько документов для семантического поиска.

    Args:
        new_documents (list): Список документов для индексации.
        doc_to_name_func (callable): Функция для извлечения имени из документа.

    Returns:
        list: Список добавленных документов.
    """
```

### `LocalFilesGroundingConnector`

#### `__init__`

```python
def __init__(self, name: str = "Local Files", folders_paths: list = None) -> None:
    """
    Args:
        name (str): Имя коннектора заземления. По умолчанию "Local Files".
        folders_paths (list): Список путей к папкам с файлами для заземления. По умолчанию `None`.
    """
```

#### `_post_init`

```python
def _post_init(self):
    """
    Выполняет постобработку инициализации после `__init__`.

    Эта функция вызывается декоратором `@utils.post_init` после выполнения метода `__init__`.
    Она загружает пути к папкам, указанные в `self.folders_paths`.
    """
```

#### `add_folders`

```python
def add_folders(self, folders_paths: list) -> None:
    """
    Добавляет пути к папкам с файлами, используемыми для заземления.

    Args:
        folders_paths (list): Список путей к папкам для добавления.
    """
```

#### `add_folder`

```python
def add_folder(self, folder_path: str) -> None:
    """
    Добавляет путь к папке с файлами, используемыми для заземления.

    Args:
        folder_path (str): Путь к папке для добавления.
    """
```

#### `add_file_path`

```python
def add_file_path(self, file_path: str) -> None:
    """
    Добавляет путь к файлу, используемому для заземления.

    Args:
        file_path (str): Путь к файлу для добавления.
    """
```

#### `_mark_folder_as_loaded`

```python
def _mark_folder_as_loaded(self, folder_path: str) -> None:
    """
    Помечает папку как загруженную.

    Args:
        folder_path (str): Путь к папке для пометки.
    """
```

### `WebPagesGroundingConnector`

#### `__init__`

```python
def __init__(self, name: str = "Web Pages", web_urls: list = None) -> None:
    """
    Args:
        name (str): Имя коннектора заземления. По умолчанию "Web Pages".
        web_urls (list): Список URL-адресов веб-страниц для заземления. По умолчанию `None`.
    """
```

#### `_post_init`

```python
def _post_init(self):
    """
    Выполняет постобработку инициализации после `__init__`.

    Эта функция вызывается декоратором `@utils.post_init` после выполнения метода `__init__`.
    Она загружает веб-страницы, указанные в `self.web_urls`.
    """
```

#### `add_web_urls`

```python
def add_web_urls(self, web_urls: list) -> None:
    """
    Добавляет данные, полученные с указанных URL-адресов, для заземления.

    Args:
        web_urls (list): Список URL-адресов веб-страниц для добавления.
    """
```

#### `add_web_url`

```python
def add_web_url(self, web_url: str) -> None:
    """
    Добавляет данные, полученные с указанного URL-адреса, для заземления.

    Args:
        web_url (str): URL-адрес веб-страницы для добавления.
    """
```

#### `_mark_web_url_as_loaded`

```python
def _mark_web_url_as_loaded(self, web_url: str) -> None:
    """
    Помечает веб-страницу как загруженную.

    Args:
        web_url (str): URL-адрес веб-страницы для пометки.
    """
```