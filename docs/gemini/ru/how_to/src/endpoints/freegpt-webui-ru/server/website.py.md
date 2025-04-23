### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода определяет класс `Website`, который отвечает за настройку маршрутов веб-приложения Flask и обработку запросов к различным страницам, таким как главная страница, страница чата и статические ресурсы. Он также включает функции для редиректов и обработки ошибок, связанных с поиском файлов.

Шаги выполнения
-------------------------
1. **Инициализация класса `Website`**:
   - При создании экземпляра класса `Website` передается объект приложения Flask.
   - Определяется словарь `routes`, который связывает URL-пути с соответствующими функциями и HTTP-методами.

2. **Определение маршрута `/`**:
   - При обращении к корневому URL `/` происходит перенаправление на страницу `/chat`.
   - Используются методы `GET` и `POST`.

3. **Определение маршрута `/chat/`**:
   - При обращении к URL `/chat/` вызывается метод `_index`, который отображает шаблон `index.html` с автоматически сгенерированным `chat_id`.
   - Используются методы `GET` и `POST`.

4. **Определение маршрута `/chat/<conversation_id>`**:
   - При обращении к URL `/chat/<conversation_id>` вызывается метод `_chat`, который отображает шаблон `index.html` с переданным `conversation_id`.
   - Если `conversation_id` не содержит дефис, происходит перенаправление на страницу `/chat`.
   - Используются методы `GET` и `POST`.

5. **Определение маршрута `/assets/<folder>/<file>`**:
   - При обращении к URL `/assets/<folder>/<file>` вызывается метод `_assets`, который возвращает запрошенный статический файл из соответствующей папки.
   - Если файл не найден, возвращается сообщение об ошибке "File not found" с кодом 404.
   - Используются методы `GET` и `POST`.

6. **Метод `_chat`**:
   - Проверяет, содержит ли `conversation_id` дефис. Если нет, происходит перенаправление на `/chat`.
   - Отображает шаблон `index.html` с переданным `chat_id`.

7. **Метод `_index`**:
   - Генерирует уникальный `chat_id`, используя `urandom` и текущее время.
   - Отображает шаблон `index.html` с сгенерированным `chat_id`.

8. **Метод `_assets`**:
   - Функция выполняет попытку отправить запрошенный файл из папки `/../client/{folder}/{file}`.
   - Функция возвращает файл как вложение (`as_attachment=False`).
   - Функция возвращает ошибку 404, если файл не найден.

Пример использования
-------------------------

```python
from flask import Flask, render_template, send_file, redirect
from time import time
from os import urandom

app = Flask(__name__)

class Website:
    def __init__(self, app) -> None:
        self.app = app
        self.routes = {
            '/': {
                'function': lambda: redirect('/chat'),
                'methods': ['GET', 'POST']
            },
            '/chat/': {
                'function': self._index,
                'methods': ['GET', 'POST']
            },
            '/chat/<conversation_id>': {
                'function': self._chat,
                'methods': ['GET', 'POST']
            },
            '/assets/<folder>/<file>': {
                'function': self._assets,
                'methods': ['GET', 'POST']
            }
        }

    def _chat(self, conversation_id):
        if '-' not in conversation_id:
            return redirect('/chat')

        return render_template('index.html', chat_id=conversation_id)

    def _index(self):
        return render_template('index.html', chat_id=f'{urandom(4).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{hex(int(time() * 1000))[2:]}')

    def _assets(self, folder: str, file: str):
        try:
            return send_file(f"./../client/{folder}/{file}", as_attachment=False)
        except:
            return "File not found", 404

website = Website(app)

# Пример использования маршрута /chat/
# website._index()  # Отобразит шаблон index.html с сгенерированным chat_id

# Пример использования маршрута /assets/css/style.css
# website._assets('css', 'style.css')  # Попытка отправить файл style.css из папки /../client/css/