# Модуль для работы с коннекторами заземления (Grounding connectors)
==================================================================

Модуль содержит классы для подключения к различным источникам данных (файлы, веб-страницы) и индексации этих данных для семантического поиска.

## Обзор

Этот модуль предоставляет инструменты для "заземления" знаний агента, позволяя ему получать информацию из внешних источников, таких как локальные файлы и веб-страницы. Он включает абстрактный класс `GroundingConnector`, который определяет интерфейс для коннекторов заземления, а также конкретные реализации, такие как `BaseSemanticGroundingConnector`, `LocalFilesGroundingConnector` и `WebPagesGroundingConnector`. Эти коннекторы позволяют агенту извлекать релевантную информацию из различных источников на основе семантического поиска.

## Подробнее

Модуль предоставляет абстрактный класс `GroundingConnector`, который определяет интерфейс для коннекторов заземления.
`BaseSemanticGroundingConnector` предоставляет базовую реализацию семантического коннектора заземления, использующего `VectorStoreIndex` из библиотеки `llama_index`. `LocalFilesGroundingConnector` и `WebPagesGroundingConnector` расширяют эту базовую реализацию для работы с локальными файлами и веб-страницами соответственно.

## Классы

### `GroundingConnector`

**Описание**:
Абстрактный класс, представляющий коннектор заземления. Коннектор заземления - это компонент, который позволяет агенту "заземлять" свои знания во внешних источниках, таких как файлы, веб-страницы, базы данных и т.д.

**Атрибуты**:
- `name` (str): Имя коннектора заземления.

**Методы**:
- `retrieve_relevant(relevance_target: str, source: str, top_k: int = 20) -> list`:
    Абстрактный метод для извлечения релевантной информации из источника на основе целевой релевантности. Должен быть реализован в подклассах.
- `retrieve_by_name(name: str) -> str`:
    Абстрактный метод для извлечения источника контента по его имени. Должен быть реализован в подклассах.
- `list_sources() -> list`:
    Абстрактный метод для перечисления имен доступных источников контента. Должен быть реализован в подклассах.

### `BaseSemanticGroundingConnector`

**Описание**:
Базовый класс для семантических коннекторов заземления. Семантический коннектор заземления - это компонент, который индексирует и извлекает документы на основе так называемого "семантического поиска" (т.е. поиска на основе embeddings). Эта конкретная реализация основана на классе `VectorStoreIndex` из библиотеки `LLaMa-Index`. Здесь "документы" относятся к структуре данных `llama-index`, которая хранит единицу контента, не обязательно файл.

**Наследует**:
- `GroundingConnector`: Наследует функциональность коннектора заземления.

**Атрибуты**:
- `documents` (list): Список документов, проиндексированных для семантического поиска.
- `name_to_document` (dict): Словарь, сопоставляющий имена документов со списками документов (каждый документ может быть разбит на несколько страниц).
- `index` (VectorStoreIndex): Индекс `VectorStoreIndex` из библиотеки `llama_index`, используемый для семантического поиска.

**Методы**:

#### `__init__(name: str = "Semantic Grounding") -> None`

```python
def __init__(self, name: str = "Semantic Grounding") -> None
```

**Назначение**:
Инициализирует экземпляр класса `BaseSemanticGroundingConnector`.

**Параметры**:
- `name` (str, optional): Имя коннектора. По умолчанию "Semantic Grounding".

**Как работает функция**:
1. Вызывает конструктор базового класса `GroundingConnector` с переданным именем.
2. Инициализирует атрибуты `documents` и `name_to_document` значениями `None`.
3. Использует декоратор `@utils.post_init` для обеспечения вызова метода `_post_init` после завершения инициализации.

```
A[Инициализация GroundingConnector]
|
B[Инициализация self.documents = None]
|
C[Инициализация self.name_to_document = None]
|
D[Вызов _post_init после инициализации]
```

#### `_post_init()`

```python
def _post_init(self)
```

**Назначение**:
Выполняет дополнительную инициализацию после вызова метода `__init__`.

**Как работает функция**:
1. Устанавливает `self.index = None`.
2. Проверяет, существуют ли атрибуты `self.documents` и `self.name_to_document`, и если нет, инициализирует их пустыми списками и словарями соответственно.
3. Вызывает метод `self.add_documents(self.documents)` для добавления существующих документов в индекс.

```
A[Инициализация self.index = None]
|
B[Проверка существования self.documents]
|
C[Инициализация self.documents = [] если не существует]
|
D[Проверка существования self.name_to_document]
|
E[Инициализация self.name_to_document = {} если не существует]
|
F[Вызов self.add_documents(self.documents) для индексации документов]
```

#### `retrieve_relevant(relevance_target: str, top_k: int = 20) -> list`

```python
def retrieve_relevant(self, relevance_target: str, top_k: int = 20) -> list
```

**Назначение**:
Извлекает все значения из памяти, которые релевантны данной цели.

**Параметры**:
- `relevance_target` (str): Цель релевантности.
- `top_k` (int, optional): Количество извлекаемых наиболее релевантных узлов. По умолчанию 20.

**Возвращает**:
- `list`: Список строк, содержащих релевантный контент, информацию об источнике и оценку схожести.

**Как работает функция**:
1. Проверяет, существует ли индекс (`self.index`).
2. Если индекс существует, создает объект `retriever` с помощью метода `self.index.as_retriever(similarity_top_k=top_k)`.
3. Извлекает релевантные узлы с помощью метода `retriever.retrieve(relevance_target)`.
4. Если индекс не существует, устанавливает `nodes = []`.
5. Итерирует по узлам и формирует список строк, содержащих информацию об источнике, оценку схожести и релевантный контент.

```
A[Проверка существования self.index]
|
B[Создание retriever (self.index.as_retriever)]
|
C[Извлечение релевантных узлов (retriever.retrieve)]
|
D[Итерация по узлам]
|
E[Формирование списка строк с информацией об источнике, оценке и контенте]
```

#### `retrieve_by_name(name: str) -> list`

```python
def retrieve_by_name(self, name: str) -> list
```

**Назначение**:
Извлекает источник контента по его имени.

**Параметры**:
- `name` (str): Имя источника контента.

**Возвращает**:
- `list`: Список строк, содержащих информацию об источнике, странице и контенте.

**Как работает функция**:
1. Проверяет, существует ли `self.name_to_document` и есть ли имя в `self.name_to_document`.
2. Если да, то итерирует по документам, связанным с этим именем, и формирует список строк, содержащих информацию об источнике, странице и контенте.

```
A[Проверка существования self.name_to_document и наличия имени в нем]
|
B[Итерация по документам, связанным с именем]
|
C[Формирование списка строк с информацией об источнике, странице и контенте]
```

#### `list_sources() -> list`

```python
def list_sources(self) -> list
```

**Назначение**:
Перечисляет имена доступных источников контента.

**Возвращает**:
- `list`: Список имен источников контента.

**Как работает функция**:
1. Проверяет, существует ли `self.name_to_document`.
2. Если да, то возвращает список ключей `self.name_to_document`.
3. Если нет, возвращает пустой список.

```
A[Проверка существования self.name_to_document]
|
B[Возврат списка ключей self.name_to_document]
|
C[Возврат [] если self.name_to_document не существует]
```

#### `add_document(self, document, doc_to_name_func=None) -> None`

```python
def add_document(self, document, doc_to_name_func=None) -> None
```

**Назначение**:
Индексирует документ для семантического извлечения.

**Параметры**:
- `document`: Документ для индексации.
- `doc_to_name_func` (function, optional): Функция для извлечения имени из документа. По умолчанию `None`.

**Как работает функция**:
1. Вызывает `self.add_documents([document], doc_to_name_func)` для добавления документа в индекс.

```
A[Вызов self.add_documents([document], doc_to_name_func)]
```

#### `add_documents(self, new_documents, doc_to_name_func=None) -> list`

```python
def add_documents(self, new_documents, doc_to_name_func=None) -> list
```

**Назначение**:
Индексирует документы для семантического извлечения.

**Параметры**:
- `new_documents` (list): Список документов для индексации.
- `doc_to_name_func` (function, optional): Функция для извлечения имени из документа. По умолчанию `None`.

**Как работает функция**:
1. Проверяет, есть ли новые документы для добавления.
2. Добавляет новые документы в `self.documents`.
3. Итерирует по новым документам и добавляет их в `self.name_to_document` с использованием `doc_to_name_func` для получения имени.
4. Обновляет индекс `self.index` с использованием `VectorStoreIndex.from_documents` или `self.index.refresh`.

```
A[Проверка наличия новых документов]
|
B[Добавление новых документов в self.documents]
|
C[Итерация по новым документам]
|
D[Извлечение имени документа с помощью doc_to_name_func]
|
E[Добавление документа в self.name_to_document]
|
F[Обновление индекса self.index]
```

### `LocalFilesGroundingConnector`

**Описание**:
Класс для подключения к локальным файлам для заземления.

**Наследует**:
- `BaseSemanticGroundingConnector`: Наследует функциональность семантического коннектора заземления.

**Атрибуты**:
- `folders_paths` (list): Список путей к папкам с файлами, используемыми для заземления.
- `loaded_folders_paths` (list): Список путей к папкам, которые уже были загружены.

**Методы**:

#### `__init__(name: str = "Local Files", folders_paths: list = None) -> None`

```python
def __init__(self, name: str = "Local Files", folders_paths: list = None) -> None
```

**Назначение**:
Инициализирует экземпляр класса `LocalFilesGroundingConnector`.

**Параметры**:
- `name` (str, optional): Имя коннектора. По умолчанию "Local Files".
- `folders_paths` (list, optional): Список путей к папкам с файлами. По умолчанию `None`.

**Как работает функция**:
1. Вызывает конструктор базового класса `BaseSemanticGroundingConnector` с переданным именем.
2. Инициализирует атрибут `folders_paths`.
3. Использует декоратор `@utils.post_init` для обеспечения вызова метода `_post_init` после завершения инициализации.

```
A[Инициализация BaseSemanticGroundingConnector]
|
B[Инициализация self.folders_paths]
|
C[Вызов _post_init после инициализации]
```

#### `_post_init()`

```python
def _post_init(self)
```

**Назначение**:
Выполняет дополнительную инициализацию после вызова метода `__init__`.

**Как работает функция**:
1. Инициализирует `self.loaded_folders_paths = []`.
2. Проверяет, существует ли атрибут `self.folders_paths`, и если нет, инициализирует его пустым списком.
3. Вызывает метод `self.add_folders(self.folders_paths)` для добавления существующих папок.

```
A[Инициализация self.loaded_folders_paths = []]
|
B[Проверка существования self.folders_paths]
|
C[Инициализация self.folders_paths = [] если не существует]
|
D[Вызов self.add_folders(self.folders_paths) для добавления папок]
```

#### `add_folders(self, folders_paths: list) -> None`

```python
def add_folders(self, folders_paths: list) -> None
```

**Назначение**:
Добавляет пути к папкам с файлами, используемыми для заземления.

**Параметры**:
- `folders_paths` (list): Список путей к папкам.

**Как работает функция**:
1. Итерирует по путям к папкам в списке `folders_paths`.
2. Для каждого пути вызывает метод `self.add_folder(folder_path)` для добавления папки.
3. Обрабатывает исключения `FileNotFoundError` и `ValueError` и выводит сообщения об ошибках.

```
A[Итерация по folders_paths]
|
B[Вызов self.add_folder для каждой папки]
|
C[Обработка исключений FileNotFoundError и ValueError]
```

#### `add_folder(self, folder_path: str) -> None`

```python
def add_folder(self, folder_path: str) -> None
```

**Назначение**:
Добавляет путь к папке с файлами, используемыми для заземления.

**Параметры**:
- `folder_path` (str): Путь к папке.

**Как работает функция**:
1. Проверяет, была ли уже загружена папка.
2. Если нет, то помечает папку как загруженную с помощью метода `self._mark_folder_as_loaded(folder_path)`.
3. Загружает данные из папки с помощью `SimpleDirectoryReader(folder_path).load_data()`.
4. Добавляет документы в индекс с помощью метода `self.add_documents(new_files, lambda doc: doc.metadata["file_name"])`.

```
A[Проверка, была ли уже загружена папка]
|
B[Пометка папки как загруженной (_mark_folder_as_loaded)]
|
C[Загрузка данных из папки (SimpleDirectoryReader.load_data)]
|
D[Добавление документов в индекс (add_documents)]
```

#### `add_file_path(self, file_path: str) -> None`

```python
def add_file_path(self, file_path: str) -> None
```

**Назначение**:
Добавляет путь к файлу, используемому для заземления.

**Параметры**:
- `file_path` (str): Путь к файлу.

**Как работает функция**:
1. Создает список, содержащий путь к файлу.
2. Загружает данные из файла с помощью `SimpleDirectoryReader(input_files=[file_path]).load_data()`.
3. Добавляет документы в индекс с помощью метода `self.add_documents(new_files, lambda doc: doc.metadata["file_name"])`.

```
A[Создание списка с путем к файлу]
|
B[Загрузка данных из файла (SimpleDirectoryReader.load_data)]
|
C[Добавление документов в индекс (add_documents)]
```

#### `_mark_folder_as_loaded(self, folder_path: str) -> None`

```python
def _mark_folder_as_loaded(self, folder_path: str) -> None
```

**Назначение**:
Помечает папку как загруженную.

**Параметры**:
- `folder_path` (str): Путь к папке.

**Как работает функция**:
1. Добавляет путь к папке в список `self.loaded_folders_paths`, если его там еще нет.
2. Добавляет путь к папке в список `self.folders_paths`, если его там еще нет.

```
A[Проверка наличия folder_path в self.loaded_folders_paths]
|
B[Добавление folder_path в self.loaded_folders_paths, если отсутствует]
|
C[Проверка наличия folder_path в self.folders_paths]
|
D[Добавление folder_path в self.folders_paths, если отсутствует]
```

### `WebPagesGroundingConnector`

**Описание**:
Класс для подключения к веб-страницам для заземления.

**Наследует**:
- `BaseSemanticGroundingConnector`: Наследует функциональность семантического коннектора заземления.

**Атрибуты**:
- `web_urls` (list): Список URL-адресов веб-страниц, используемых для заземления.
- `loaded_web_urls` (list): Список URL-адресов веб-страниц, которые уже были загружены.

**Методы**:

#### `__init__(name: str = "Web Pages", web_urls: list = None) -> None`

```python
def __init__(self, name: str = "Web Pages", web_urls: list = None) -> None
```

**Назначение**:
Инициализирует экземпляр класса `WebPagesGroundingConnector`.

**Параметры**:
- `name` (str, optional): Имя коннектора. По умолчанию "Web Pages".
- `web_urls` (list, optional): Список URL-адресов веб-страниц. По умолчанию `None`.

**Как работает функция**:
1. Вызывает конструктор базового класса `BaseSemanticGroundingConnector` с переданным именем.
2. Инициализирует атрибут `web_urls`.
3. Использует декоратор `@utils.post_init` для обеспечения вызова метода `_post_init` после завершения инициализации.

```
A[Инициализация BaseSemanticGroundingConnector]
|
B[Инициализация self.web_urls]
|
C[Вызов _post_init после инициализации]
```

#### `_post_init()`

```python
def _post_init(self)
```

**Назначение**:
Выполняет дополнительную инициализацию после вызова метода `__init__`.

**Как работает функция**:
1. Инициализирует `self.loaded_web_urls = []`.
2. Проверяет, существует ли атрибут `self.web_urls`, и если нет, инициализирует его пустым списком.
3. Вызывает метод `self.add_web_urls(self.web_urls)` для добавления существующих URL-адресов.

```
A[Инициализация self.loaded_web_urls = []]
|
B[Проверка существования self.web_urls]
|
C[Инициализация self.web_urls = [] если не существует]
|
D[Вызов self.add_web_urls(self.web_urls) для добавления URL-адресов]
```

#### `add_web_urls(self, web_urls: list) -> None`

```python
def add_web_urls(self, web_urls: list) -> None
```

**Назначение**:
Добавляет данные, полученные с указанных URL-адресов, для заземления.

**Параметры**:
- `web_urls` (list): Список URL-адресов веб-страниц.

**Как работает функция**:
1. Фильтрует список `web_urls`, чтобы оставить только те URL-адреса, которые еще не были загружены.
2. Итерирует по отфильтрованным URL-адресам и вызывает метод `self._mark_web_url_as_loaded(url)` для каждого URL-адреса.
3. Загружает данные с веб-страниц с помощью `SimpleWebPageReader(html_to_text=True).load_data(filtered_web_urls)`.
4. Добавляет документы в индекс с помощью метода `self.add_documents(new_documents, lambda doc: doc.id_)`.

```
A[Фильтрация web_urls для удаления уже загруженных URL-адресов]
|
B[Итерация по отфильтрованным URL-адресам]
|
C[Пометка URL-адреса как загруженного (_mark_web_url_as_loaded)]
|
D[Загрузка данных с веб-страниц (SimpleWebPageReader.load_data)]
|
E[Добавление документов в индекс (add_documents)]
```

#### `add_web_url(self, web_url: str) -> None`

```python
def add_web_url(self, web_url: str) -> None
```

**Назначение**:
Добавляет данные, полученные с указанного URL-адреса, для заземления.

**Параметры**:
- `web_url` (str): URL-адрес веб-страницы.

**Как работает функция**:
1. Вызывает метод `self.add_web_urls([web_url])` для добавления URL-адреса.

```
A[Вызов self.add_web_urls([web_url])]
```

#### `_mark_web_url_as_loaded(self, web_url: str) -> None`

```python
def _mark_web_url_as_loaded(self, web_url: str) -> None
```

**Назначение**:
Помечает URL-адрес веб-страницы как загруженный.

**Параметры**:
- `web_url` (str): URL-адрес веб-страницы.

**Как работает функция**:
1. Добавляет URL-адрес в список `self.loaded_web_urls`, если его там еще нет.
2. Добавляет URL-адрес в список `self.web_urls`, если его там еще нет.

```
A[Проверка наличия web_url в self.loaded_web_urls]
|
B[Добавление web_url в self.loaded_web_urls, если отсутствует]
|
C[Проверка наличия web_url в self.web_urls]
|
D[Добавление web_url в self.web_urls, если отсутствует]
```