### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода определяет класс `Website`, который отвечает за настройку маршрутов (endpoints) для веб-приложения на Flask. Он связывает URL-адреса с соответствующими функциями, которые обрабатывают HTTP-запросы и возвращают HTML-шаблоны для отображения веб-страниц.

Шаги выполнения
-------------------------
1. **Инициализация класса `Website`**:
   - При создании экземпляра класса `Website` передается объект Flask-приложения (`app`).
   - Определяются маршруты в словаре `self.routes`, где ключи - это URL-адреса, а значения - словарь с указанием функции обработчика (`function`) и разрешенных HTTP-методов (`methods`).

2. **Определение маршрутов**:
   - Маршруты включают:
     - `/chat/`: отображает главную страницу чата с новым conversation_id.
     - `/chat/<conversation_id>`: отображает страницу чата с указанным conversation_id.
     - `/chat/<share_id>/`: отображает страницу чата с возможностью шаринга, генерируя новый conversation_id.
     - `/chat/<share_id>/<conversation_id>`: отображает страницу чата с указанным share_id и conversation_id.
     - `/chat/menu/`: перенаправляет на главную страницу чата (`/chat`).
     - `/chat/settings/`: отображает страницу настроек чата с новым conversation_id.
     - `/images/`: перенаправляет на главную страницу чата (`/chat`).
     - `/background`: отображает страницу с фоном.

3. **Функции обработчики маршрутов**:
   - `_chat(self, conversation_id)`:
     - Отображает страницу чата (`index.html`) с переданным `conversation_id`. Если `conversation_id` равен "share", генерирует новый UUID.
   - `_share_id(self, share_id, conversation_id: str = "")`:
     - Отображает страницу чата (`index.html`) с параметрами для шаринга (`share_url`, `share_id`) и `conversation_id`. Если `conversation_id` не указан, генерирует новый UUID.
   - `_index(self)`:
     - Отображает главную страницу чата (`index.html`) с новым сгенерированным `conversation_id`.
   - `_settings(self)`:
     - Отображает страницу настроек (`index.html`) с новым сгенерированным `conversation_id`.
   - `_background(self)`:
     - Отображает страницу с фоном (`background.html`).
   - `redirect_home()`:
     - Выполняет перенаправление на главную страницу чата (`/chat`).

Пример использования
-------------------------

```python
from flask import Flask

app = Flask(__name__)
website = Website(app)

# Пример: Добавление маршрутов Flask из класса Website
for route, config in website.routes.items():
    app.add_url_rule(route, view_func=config['function'], methods=config['methods'])

if __name__ == '__main__':
    app.run(debug=True)