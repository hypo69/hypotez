# Модуль `website.py`

## Обзор

Модуль `website.py` содержит класс `Website`, который отвечает за настройку маршрутов веб-сайта на основе фреймворка Flask. Он обрабатывает запросы к различным страницам, таким как главная страница, страница чата и статические ресурсы (assets).

## Более детально

Этот модуль определяет структуру веб-сайта, связывая URL-адреса с соответствующими функциями обработки запросов. Класс `Website` инициализируется с экземпляром приложения Flask и определяет маршруты для перенаправления на страницу чата, отображения страницы чата с уникальным идентификатором разговора и обслуживания статических файлов.

## Классы

### `Website`

**Описание**:
Класс `Website` отвечает за настройку маршрутов и обработку запросов для веб-сайта.

**Атрибуты**:
- `app`: Экземпляр приложения Flask.
- `routes` (dict): Словарь, содержащий маршруты веб-сайта и связанные с ними функции и методы.

**Методы**:
- `__init__(self, app)`: Инициализирует экземпляр класса `Website` с заданным приложением Flask.
- `_chat(self, conversation_id)`: Обрабатывает запросы к странице чата с определенным идентификатором разговора.
- `_index(self)`: Обрабатывает запросы к главной странице, генерируя уникальный идентификатор разговора и отображая страницу чата.
- `_assets(self, folder: str, file: str)`: Обрабатывает запросы к статическим ресурсам (assets), таким как файлы JavaScript и CSS.

#### `__init__`

```python
def __init__(self, app) -> None:
    """
    Инициализирует экземпляр класса `Website` с заданным приложением Flask.

    Args:
        app: Экземпляр приложения Flask.

    Returns:
        None
    """
```

#### `_chat`

```python
def _chat(self, conversation_id):
    """
    Обрабатывает запросы к странице чата с определенным идентификатором разговора.

    Args:
        conversation_id: Идентификатор разговора.

    Returns:
        response: Ответ Flask, который либо перенаправляет на страницу чата, либо отображает шаблон `index.html` с указанным `chat_id`.
    """
```

#### `_index`

```python
def _index(self):
    """
    Обрабатывает запросы к главной странице, генерируя уникальный идентификатор разговора и отображая страницу чата.

    Returns:
        response: Ответ Flask, который отображает шаблон `index.html` с уникальным `chat_id`.
    """
```

#### `_assets`

```python
def _assets(self, folder: str, file: str):
    """
    Обрабатывает запросы к статическим ресурсам (assets), таким как файлы JavaScript и CSS.

    Args:
        folder (str): Папка, в которой находится файл.
        file (str): Имя файла.

    Returns:
        response: Ответ Flask, содержащий запрошенный файл, или сообщение об ошибке, если файл не найден.
    """
```

## Примеры

### Создание экземпляра класса `Website`

```python
from flask import Flask
from src.endpoints.freegpt_webui_ru.server.website import Website

app = Flask(__name__)
website = Website(app)
```

### Пример маршрута `/chat/<conversation_id>`

```python
from flask import Flask
from src.endpoints.freegpt_webui_ru.server.website import Website

app = Flask(__name__)
website = Website(app)

@app.route('/chat/<conversation_id>')
def chat(conversation_id):
    return website._chat(conversation_id)