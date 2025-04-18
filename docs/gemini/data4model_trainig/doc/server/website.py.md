# Модуль веб-сайта

## Обзор

Модуль `src.endpoints.freegpt-webui-ru/server/website.py` предназначен для определения маршрутов и функций веб-сайта, используемых Flask-приложением.

## Подробней

Модуль содержит класс `Website`, который определяет маршруты для главной страницы, страницы чата и статических ресурсов.

## Классы

### `Website`

**Описание**: Класс для управления маршрутами веб-сайта.

**Атрибуты**:

*   `app` (Flask): Экземпляр Flask-приложения.
*   `routes` (dict): Словарь, содержащий маршруты и соответствующие им функции и методы.

**Методы**:

*   `__init__(self, app)`: Инициализирует объект `Website`.
*   `_chat(self, conversation_id)`: Обрабатывает маршрут для страницы чата с указанным ID разговора.
*   `_index(self)`: Обрабатывает маршрут для главной страницы.
*   `_assets(self, folder: str, file: str)`: Обрабатывает маршрут для статических ресурсов.

## Методы класса `Website`

### `__init__`

```python
def __init__(self, app):
```

**Назначение**: Инициализирует объект `Website`.

**Параметры**:

*   `app` (Flask): Экземпляр Flask-приложения.

**Как работает функция**:

1.  Сохраняет экземпляр Flask-приложения в атрибуте `app`.
2.  Определяет словарь `routes`, содержащий маршруты, функции и методы HTTP для обработки этих маршрутов.

### `_chat`

```python
def _chat(self, conversation_id):
```

**Назначение**: Обрабатывает маршрут для страницы чата с указанным ID разговора.

**Параметры**:

*   `conversation_id` (str): ID разговора.

**Как работает функция**:

1.  Проверяет, содержит ли `conversation_id` символ `'-'`.
2.  Если `conversation_id` не содержит символ `'-'`, перенаправляет на главную страницу (`/chat`).
3.  Отрисовывает шаблон `index.html` с передачей `conversation_id`.

### `_index`

```python
def _index(self):
```

**Назначение**: Обрабатывает маршрут для главной страницы.

**Как работает функция**:

1.  Генерирует случайный ID разговора.
2.  Отрисовывает шаблон `index.html` с передачей сгенерированного ID разговора.

### `_assets`

```python
def _assets(self, folder: str, file: str):
```

**Назначение**: Обрабатывает маршрут для статических ресурсов.

**Параметры**:

*   `folder` (str): Имя папки, содержащей ресурс.
*   `file` (str): Имя файла ресурса.

**Как работает функция**:

1.  Пытается отправить файл из указанной папки.
2.  В случае ошибки возвращает сообщение "File not found" с кодом состояния 404.