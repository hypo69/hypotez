# Модуль веб-сайта для GPT4Free
===============================================================

Модуль содержит класс :class:`Website`, который отвечает за маршрутизацию и обработку запросов к веб-сайту GPT4Free. 

## Обзор

Класс `Website` определяет маршруты веб-приложения и связанные с ними функции-обработчики. 
Он использует Flask для создания веб-приложения и обработки запросов.

## Классы

### `Website`
**Описание**: Класс `Website` создает объект веб-приложения GPT4Free.

**Атрибуты**:

- `app`: Объект Flask, представляющий веб-приложение.
- `routes`: Словарь, содержащий описание маршрутов веб-приложения, включая функции-обработчики и методы HTTP.

**Методы**:

- `__init__(self, app) -> None`: Инициализирует объект `Website` с помощью объекта Flask `app` и задает маршруты приложения.
- `_chat(self, conversation_id) -> str`: Обрабатывает запрос к странице чата. 
- `_share_id(self, share_id, conversation_id: str = "") -> str`: Обрабатывает запрос к странице, связанной с URL-адресом для совместного использования.
- `_index(self) -> str`: Обрабатывает запрос к главной странице.
- `_settings(self) -> str`: Обрабатывает запрос к странице настроек.
- `_background(self) -> str`: Обрабатывает запрос к странице фоновых изображений.

## Функции

### `redirect_home()`

**Назначение**: Перенаправляет пользователя на главную страницу.

**Параметры**: Нет

**Возвращает**: Объект Flask, представляющий перенаправление.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.gui.server.website import redirect_home
redirect_home()
```

## Примеры

```python
# Пример создания объекта Website и обработки запроса
from hypotez.src.endpoints.gpt4free.g4f.gui.server.website import Website
from flask import Flask

app = Flask(__name__)
website = Website(app)

# Пример обработки запроса к странице чата
@app.route('/chat/<conversation_id>')
def chat(conversation_id):
    return website._chat(conversation_id)
```

```python
# Пример обработки запроса к странице совместного доступа
@app.route('/chat/<share_id>/<conversation_id>')
def share_id(share_id, conversation_id):
    return website._share_id(share_id, conversation_id)
```
```markdown