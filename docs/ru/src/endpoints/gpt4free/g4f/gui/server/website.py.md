# Модуль для настройки веб-сайта G4F

## Обзор

Этот модуль содержит класс `Website`, который отвечает за настройку маршрутов веб-сайта и обработку запросов к различным страницам, таким как чат, настройки и фоновые изображения. Он использует Flask для обработки запросов и отображения HTML-шаблонов.

## Подробнее

Модуль определяет маршруты для различных URL-адресов, связывая их с соответствующими функциями класса `Website`. Это позволяет пользователям переходить между различными разделами веб-сайта, такими как чат с определенным `conversation_id`, страница настроек и другие.

## Классы

### `Website`

**Описание**: Класс `Website` отвечает за настройку маршрутов веб-сайта и обработку запросов к различным страницам.

**Принцип работы**:
Класс инициализируется с Flask-приложением, и создает словарь маршрутов, связывающих URL-адреса с функциями класса. Каждый маршрут определяет, какая функция будет вызвана для обработки запроса по этому URL-адресу, а также HTTP-методы, которые разрешены для этого маршрута.

**Атрибуты**:
- `app`: Flask-приложение, используемое для обработки запросов.
- `routes`: Словарь, связывающий URL-адреса с функциями класса и HTTP-методами.

**Методы**:
- `__init__(self, app)`: Инициализирует класс `Website`, сохраняя Flask-приложение и определяя маршруты.
- `_chat(self, conversation_id)`: Отображает страницу чата с указанным `conversation_id`.
- `_share_id(self, share_id, conversation_id: str = "")`: Отображает страницу общего доступа с указанными `share_id` и `conversation_id`.
- `_index(self)`: Отображает главную страницу чата, генерируя новый `conversation_id`.
- `_settings(self)`: Отображает страницу настроек, генерируя новый `conversation_id`.
- `_background(self)`: Отображает страницу с фоном.

## Функции

### `redirect_home`

```python
def redirect_home():
    return redirect('/chat')
```

**Назначение**: Перенаправляет пользователя на главную страницу чата (`/chat`).

**Параметры**:
- Нет

**Возвращает**:
- `flask.Response`: Объект перенаправления Flask.

**Как работает функция**:

1. Функция `redirect_home` вызывает функцию `redirect` из библиотеки Flask, передавая ей URL-адрес `/chat`.
2. Функция `redirect` возвращает объект `flask.Response`, который содержит информацию о перенаправлении.

**Примеры**:
```python
from flask import Flask, redirect
app = Flask(__name__)

@app.route('/menu/')
def redirect_to_chat():
    return redirect_home()

if __name__ == '__main__':
    app.run(debug=True)
```

ASCII flowchart:

```
Начало --> Перенаправление на /chat --> Конец
```

### `Website.__init__`

```python
def __init__(self, app) -> None:
    self.app = app
    self.routes = {
        '/chat/': {
            'function': self._index,
            'methods': ['GET', 'POST']
        },
        '/chat/<conversation_id>': {
            'function': self._chat,
            'methods': ['GET', 'POST']
        },
        '/chat/<share_id>/': {
            'function': self._share_id,
            'methods': ['GET', 'POST']
        },
        '/chat/<share_id>/<conversation_id>': {
            'function': self._share_id,
            'methods': ['GET', 'POST']
        },
        '/chat/menu/': {
            'function': redirect_home,
            'methods': ['GET', 'POST']
        },
        '/chat/settings/': {
            'function': self._settings,
            'methods': ['GET', 'POST']
        },
        '/images/': {
            'function': redirect_home,
            'methods': ['GET', 'POST']
        },
        '/background': {
            'function': self._background,
            'methods': ['GET']
        },
    }
```

**Назначение**: Инициализирует экземпляр класса `Website`, настраивая Flask-приложение и определяя маршруты для различных URL-адресов.

**Параметры**:
- `app`: Flask-приложение, которое будет использоваться для обработки запросов.

**Возвращает**:
- `None`

**Как работает функция**:

1.  Сохраняет Flask-приложение в атрибуте `app` экземпляра класса.
2.  Определяет словарь `routes`, который связывает URL-адреса с соответствующими функциями класса и HTTP-методами.

    *   Для каждого URL-адреса указывается функция, которая будет вызвана для обработки запроса, а также список HTTP-методов (например, `GET`, `POST`), которые разрешены для этого маршрута.

**Примеры**:

```python
from flask import Flask
from src.endpoints.gpt4free.g4f.gui.server.website import Website

app = Flask(__name__)
website = Website(app)
```

ASCII flowchart:

```
Начало --> Сохранение Flask-приложения --> Определение маршрутов --> Конец
```

### `Website._chat`

```python
def _chat(self, conversation_id):
    if conversation_id == "share":
        return render_template('index.html', conversation_id=str(uuid.uuid4()))
    return render_template('index.html', conversation_id=conversation_id)
```

**Назначение**: Отображает страницу чата с указанным `conversation_id`. Если `conversation_id` равен "share", генерируется новый UUID.

**Параметры**:
- `conversation_id`: Идентификатор беседы (conversation).

**Возвращает**:
- `flask.Response`: HTML-страница, отображаемая пользователю.

**Как работает функция**:

1.  Проверяет, равен ли `conversation_id` значению "share".
2.  Если `conversation_id` равен "share", генерируется новый UUID с помощью `uuid.uuid4()` и преобразуется в строку.
3.  Вызывает функцию `render_template` из библиотеки Flask, передавая ей имя шаблона `index.html` и `conversation_id`.
4.  Функция `render_template` загружает шаблон `index.html` и подставляет в него значение `conversation_id`.
5.  Возвращает HTML-страницу, сгенерированную функцией `render_template`.

**Примеры**:

```python
from flask import Flask
from src.endpoints.gpt4free.g4f.gui.server.website import Website
import uuid

app = Flask(__name__)
website = Website(app)

@app.route('/chat/<conversation_id>')
def chat(conversation_id):
    return website._chat(conversation_id)

if __name__ == '__main__':
    app.run(debug=True)
```

ASCII flowchart:

```
Начало --> Проверка conversation_id == "share" --> Генерация нового UUID (если да) --> Отображение index.html с conversation_id --> Конец
```

### `Website._share_id`

```python
def _share_id(self, share_id, conversation_id: str = ""):
    share_url = os.environ.get("G4F_SHARE_URL", "")
    conversation_id = conversation_id if conversation_id else str(uuid.uuid4())
    return render_template('index.html', share_url=share_url, share_id=share_id, conversation_id=conversation_id)
```

**Назначение**: Отображает страницу общего доступа с указанными `share_id` и `conversation_id`. Если `conversation_id` не указан, генерируется новый UUID.

**Параметры**:
- `share_id`: Идентификатор общего доступа.
- `conversation_id`: Идентификатор беседы (необязательный, по умолчанию "").

**Возвращает**:
- `flask.Response`: HTML-страница, отображаемая пользователю.

**Как работает функция**:

1.  Получает URL-адрес общего доступа из переменной окружения `G4F_SHARE_URL`.
2.  Если `conversation_id` не указан, генерируется новый UUID с помощью `uuid.uuid4()` и преобразуется в строку.
3.  Вызывает функцию `render_template` из библиотеки Flask, передавая ей имя шаблона `index.html`, `share_url`, `share_id` и `conversation_id`.
4.  Функция `render_template` загружает шаблон `index.html` и подставляет в него значения `share_url`, `share_id` и `conversation_id`.
5.  Возвращает HTML-страницу, сгенерированную функцией `render_template`.

**Примеры**:

```python
from flask import Flask
from src.endpoints.gpt4free.g4f.gui.server.website import Website
import uuid
import os

app = Flask(__name__)
website = Website(app)

# Set the environment variable for testing
os.environ["G4F_SHARE_URL"] = "http://example.com/share"

@app.route('/share/<share_id>/<conversation_id>')
def share(share_id, conversation_id):
    return website._share_id(share_id, conversation_id)

if __name__ == '__main__':
    app.run(debug=True)
```

ASCII flowchart:

```
Начало --> Получение share_url из переменной окружения --> Генерация нового UUID (если conversation_id не указан) --> Отображение index.html с share_url, share_id и conversation_id --> Конец
```

### `Website._index`

```python
def _index(self):
    return render_template('index.html', conversation_id=str(uuid.uuid4()))
```

**Назначение**: Отображает главную страницу чата, генерируя новый `conversation_id`.

**Параметры**:
- Нет

**Возвращает**:
- `flask.Response`: HTML-страница, отображаемая пользователю.

**Как работает функция**:

1.  Генерирует новый UUID с помощью `uuid.uuid4()` и преобразуется в строку.
2.  Вызывает функцию `render_template` из библиотеки Flask, передавая ей имя шаблона `index.html` и `conversation_id`.
3.  Функция `render_template` загружает шаблон `index.html` и подставляет в него значение `conversation_id`.
4.  Возвращает HTML-страницу, сгенерированную функцией `render_template`.

**Примеры**:

```python
from flask import Flask
from src.endpoints.gpt4free.g4f.gui.server.website import Website
import uuid

app = Flask(__name__)
website = Website(app)

@app.route('/')
def index():
    return website._index()

if __name__ == '__main__':
    app.run(debug=True)
```

ASCII flowchart:

```
Начало --> Генерация нового UUID --> Отображение index.html с conversation_id --> Конец
```

### `Website._settings`

```python
def _settings(self):
    return render_template('index.html', conversation_id=str(uuid.uuid4()))
```

**Назначение**: Отображает страницу настроек, генерируя новый `conversation_id`.

**Параметры**:
- Нет

**Возвращает**:
- `flask.Response`: HTML-страница, отображаемая пользователю.

**Как работает функция**:

1.  Генерирует новый UUID с помощью `uuid.uuid4()` и преобразуется в строку.
2.  Вызывает функцию `render_template` из библиотеки Flask, передавая ей имя шаблона `index.html` и `conversation_id`.
3.  Функция `render_template` загружает шаблон `index.html` и подставляет в него значение `conversation_id`.
4.  Возвращает HTML-страницу, сгенерированную функцией `render_template`.

**Примеры**:

```python
from flask import Flask
from src.endpoints.gpt4free.g4f.gui.server.website import Website
import uuid

app = Flask(__name__)
website = Website(app)

@app.route('/settings')
def settings():
    return website._settings()

if __name__ == '__main__':
    app.run(debug=True)
```

ASCII flowchart:

```
Начало --> Генерация нового UUID --> Отображение index.html с conversation_id --> Конец
```

### `Website._background`

```python
def _background(self):
    return render_template('background.html')
```

**Назначение**: Отображает страницу с фоном.

**Параметры**:
- Нет

**Возвращает**:
- `flask.Response`: HTML-страница, отображаемая пользователю.

**Как работает функция**:

1.  Вызывает функцию `render_template` из библиотеки Flask, передавая ей имя шаблона `background.html`.
2.  Функция `render_template` загружает шаблон `background.html`.
3.  Возвращает HTML-страницу, сгенерированную функцией `render_template`.

**Примеры**:

```python
from flask import Flask
from src.endpoints.gpt4free.g4f.gui.server.website import Website

app = Flask(__name__)
website = Website(app)

@app.route('/background')
def background():
    return website._background()

if __name__ == '__main__':
    app.run(debug=True)
```

ASCII flowchart:

```
Начало --> Отображение background.html --> Конец