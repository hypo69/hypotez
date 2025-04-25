# Модуль `grounding.py`

## Обзор

Этот модуль предоставляет классы для работы с "grounding connectors" - компонентов, которые позволяют агенту получать информацию из внешних источников, таких как файлы, веб-страницы, базы данных и т. д. Модуль содержит абстрактный класс `GroundingConnector` и несколько его реализаций, таких как `BaseSemanticGroundingConnector`, `LocalFilesGroundingConnector` и `WebPagesGroundingConnector`.

## Подробней

Модуль `grounding.py` является частью проекта `tinytroupe`, который позволяет создавать  и использовать агентов на базе больших языковых моделей (LLM). В этом модуле реализованы "grounding connectors" - компоненты, позволяющие агентам получать информацию из внешних источников, чтобы дополнить свои знания.

## Классы

### `class GroundingConnector`

**Описание**: Абстрактный класс, представляющий "grounding connector". "Grounding connector" - это компонент, который позволяет агенту получать знания из внешних источников, таких как файлы, веб-страницы, базы данных и т. д.

**Наследует**:
 - `JsonSerializableRegistry` - Этот класс обеспечивает возможность сериализации и десериализации экземпляров.

**Атрибуты**:

 - `name` (str): Имя "grounding connector".

**Методы**:

 - `retrieve_relevant(relevance_target:str, source:str, top_k=20) -> list`: Абстрактный метод, который должен быть реализован в подклассах. Метод возвращает список элементов, соответствующих заданному критерию `relevance_target` из источника `source`.
 - `retrieve_by_name(name:str) -> str`: Абстрактный метод, который должен быть реализован в подклассах. Метод возвращает текст из источника данных, соответствующего заданному имени `name`.
 - `list_sources() -> list`: Абстрактный метод, который должен быть реализован в подклассах. Метод возвращает список имен доступных источников данных.

### `class BaseSemanticGroundingConnector`

**Описание**: Базовый класс для "semantic grounding connectors". "Semantic grounding connector" - это компонент, который индексирует и извлекает документы на основе так называемого "семантического поиска" (т.е. поиска на основе эмбеддингов). Эта конкретная реализация основана на классе `VectorStoreIndex` из библиотеки LLaMa-Index. Здесь "документы" относятся к структуре данных LLaMa-Index, которая хранит единицу содержания, не обязательно файл.

**Наследует**:
 - `GroundingConnector`

**Атрибуты**:

 - `documents` (list): Список документов, которые были проиндексированы.
 - `name_to_document` (dict): Словарь, сопоставляющий имена документов (или источников данных) с их содержимым.
 - `index` (`VectorStoreIndex`): Индекс, используемый для семантического поиска.

**Методы**:

 - `_post_init()`: Этот метод выполняется после инициализации класса. Он используется для индексации документов и инициализации других атрибутов.
 - `retrieve_relevant(relevance_target:str, top_k=20) -> list`: Извлекает все значения из памяти, которые соответствуют заданной цели.
 - `retrieve_by_name(name:str) -> list`: Извлекает источник данных по его имени.
 - `list_sources() -> list`: Возвращает список имен доступных источников данных.
 - `add_document(document, doc_to_name_func=None) -> None`: Индексирует документ для семантического поиска.
 - `add_documents(new_documents, doc_to_name_func=None) -> list`: Индексирует документы для семантического поиска.


### `class LocalFilesGroundingConnector`

**Описание**: Класс для работы с "grounding connector", который индексирует документы из локальных файлов.

**Наследует**:
 - `BaseSemanticGroundingConnector`

**Атрибуты**:

 - `folders_paths` (list): Список путей к папкам, содержащим файлы, которые должны быть проиндексированы.
 - `loaded_folders_paths` (list): Список путей к папкам, которые уже были проиндексированы.

**Методы**:

 - `_post_init()`: Этот метод выполняется после инициализации класса. Он используется для индексации файлов из папок, указанных в атрибуте `folders_paths`.
 - `add_folders(folders_paths:list) -> None`: Добавляет путь к папке, содержащей файлы, используемые для "grounding".
 - `add_folder(folder_path:str) -> None`: Добавляет путь к папке, содержащей файлы, используемые для "grounding".
 - `add_file_path(file_path:str) -> None`: Добавляет путь к файлу, используемому для "grounding".
 - `_mark_folder_as_loaded(folder_path:str) -> None`: Отмечает папку как загруженную.

### `class WebPagesGroundingConnector`

**Описание**: Класс для работы с "grounding connector", который индексирует документы с веб-страниц.

**Наследует**:
 - `BaseSemanticGroundingConnector`

**Атрибуты**:

 - `web_urls` (list): Список URL-адресов веб-страниц, которые должны быть проиндексированы.
 - `loaded_web_urls` (list): Список URL-адресов веб-страниц, которые уже были проиндексированы.

**Методы**:

 - `_post_init()`: Этот метод выполняется после инициализации класса. Он используется для индексации веб-страниц, указанных в атрибуте `web_urls`.
 - `add_web_urls(web_urls:list) -> None`: Добавляет URL-адреса веб-страниц, используемые для "grounding".
 - `add_web_url(web_url:str) -> None`: Добавляет URL-адрес веб-страницы, используемой для "grounding".
 - `_mark_web_url_as_loaded(web_url:str) -> None`: Отмечает веб-страницу как загруженную.

## Параметры класса

- `name` (str): Имя "grounding connector".
- `folders_paths` (list): Список путей к папкам, содержащим файлы, которые должны быть проиндексированы.
- `web_urls` (list): Список URL-адресов веб-страниц, которые должны быть проиндексированы.

## Примеры

**Пример 1: Использование `LocalFilesGroundingConnector` для индексации документов из локальной папки:**

```python
from tinytroupe.agent.grounding import LocalFilesGroundingConnector

# Создание экземпляра "grounding connector" с указанием пути к папке
grounding_connector = LocalFilesGroundingConnector(folders_paths=["/path/to/folder"])

# Индексация документов из папки
grounding_connector.add_folders(["/path/to/folder"])

# Извлечение релевантных документов
results = grounding_connector.retrieve_relevant(relevance_target="Some query")

# Вывод результатов
print(results)
```

**Пример 2: Использование `WebPagesGroundingConnector` для индексации документов с веб-страниц:**

```python
from tinytroupe.agent.grounding import WebPagesGroundingConnector

# Создание экземпляра "grounding connector" с указанием URL-адресов
grounding_connector = WebPagesGroundingConnector(web_urls=["https://example.com", "https://another-example.com"])

# Индексация документов с веб-страниц
grounding_connector.add_web_urls(["https://example.com", "https://another-example.com"])

# Извлечение релевантных документов
results = grounding_connector.retrieve_relevant(relevance_target="Some query")

# Вывод результатов
print(results)
```

**Пример 3: Использование `BaseSemanticGroundingConnector` для добавления документов вручную:**

```python
from tinytroupe.agent.grounding import BaseSemanticGroundingConnector

# Создание экземпляра "grounding connector"
grounding_connector = BaseSemanticGroundingConnector()

# Добавление документа
document = {
    "text": "This is an example document.",
    "metadata": {
        "file_name": "example.txt"
    }
}
grounding_connector.add_document(document)

# Извлечение релевантных документов
results = grounding_connector.retrieve_relevant(relevance_target="This is an example")

# Вывод результатов
print(results)