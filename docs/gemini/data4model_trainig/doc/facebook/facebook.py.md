## \\file /src/endpoints/advertisement/facebook/facebook.py

# Модуль рекламы на фейсбук

```rst
.. module:: src.endpoints.advertisement.facebook
    :platform: Windows, Unix
    :synopsis: Модуль рекламы на фейсбук

 сценарии:
    - login: логин на фейсбук
    - post_message: отправка текствого сообщения в форму
    - upload_media: Загрузка файла или списка файлов

```

## Обзор

Модуль предназначен для автоматизации задач, связанных с рекламой в Facebook. Он предоставляет набор сценариев для выполнения различных действий, таких как вход в систему, отправка сообщений и загрузка медиафайлов.

## Подробней

Модуль предоставляет класс `Facebook`, который использует веб-драйвер для взаимодействия с Facebook.

## Классы

### Facebook

**Описание**: Класс для взаимодействия с Facebook через веб-драйвер.

**Атрибуты**:

*   `d` (Driver): Экземпляр веб-драйвера.
*   `start_page` (str): URL начальной страницы (значение: `'https://www.facebook.com/hypotez.promocodes'`).
*   `promoter` (str): Имя пользователя, осуществляющего продвижение.

**Методы**:

*   `__init__(self, driver: 'Driver', promoter: str, group_file_paths: list[str], *args, **kwards)`: Инициализирует объект `Facebook`.
*   `login(self) -> bool`: Выполняет вход в Facebook.
*   `promote_post(self, item: SimpleNamespace) -> bool`: Отправляет текст в форму сообщения.
*   `promote_event(self, event: SimpleNamespace)`: Пример функции для продвижения события.

## Методы класса `Facebook`

### `__init__`

```python
def __init__(self, driver: 'Driver', promoter: str, group_file_paths: list[str], *args, **kwards):
```

**Назначение**: Инициализирует объект `Facebook`.

**Параметры**:

*   `driver` (Driver): Экземпляр веб-драйвера.
*   `promoter` (str): Имя пользователя, осуществляющего продвижение.
*   `group_file_paths` (list[str]): Список путей к файлам групп.
*   `*args`: Произвольные аргументы.
*   `**kwards`: Произвольные именованные аргументы.

**Как работает функция**:

1.  Присваивает переданные значения атрибутам `d` (драйвер), `promoter` (имя пользователя) и выполняет дополнительные настройки, связанные с путями к файлам групп.

### `login`

```python
def login(self) -> bool:
```

**Назначение**: Выполняет вход в Facebook.

**Возвращает**:

*   `bool`: `True`, если вход выполнен успешно, `False` в противном случае.

**Как работает функция**:

1.  Вызывает функцию `login` из модуля `src.endpoints.advertisement.facebook.scenarios.login` для выполнения сценария входа в Facebook.

### `promote_post`

```python
def promote_post(self, item: SimpleNamespace) -> bool:
```

**Назначение**: Отправляет текст в форму сообщения.

**Параметры**:

*   `item` (SimpleNamespace): Объект, содержащий текст сообщения.

**Возвращает**:

*   `bool`: `True`, если сообщение отправлено успешно, `False` в противном случае.

**Как работает функция**:

1.  Вызывает функцию `promote_post` из модуля `src.endpoints.advertisement.facebook.scenarios.promote_post` для отправки сообщения в Facebook.

### `promote_event`

```python
def promote_event(self, event: SimpleNamespace):
```

**Назначение**: Пример функции для продвижения события.

**Параметры**:

*   `event` (SimpleNamespace): Объект, содержащий информацию о событии.

**Как работает функция**:

1.  В коде присутствует только заглушка `...`, что означает, что функция не имеет реализации.