# Модуль рекламы на Facebook

## Обзор

Модуль `facebook.py` предназначен для автоматизации работы с Facebook через веб-драйвер. Он включает в себя функции для логина, отправки сообщений, загрузки медиафайлов и продвижения постов.

## Подробней

Этот модуль является частью проекта `hypotez` и используется для автоматизации рекламных кампаний в Facebook. Он содержит классы и функции, упрощающие взаимодействие с веб-интерфейсом Facebook, такие как вход в систему, публикация контента и управление медиафайлами. Модуль использует веб-драйвер для имитации действий пользователя в браузере.

## Классы

### `Facebook`

**Описание**: Класс для взаимодействия с Facebook через веб-драйвер.

**Принцип работы**:
Класс инициализируется с драйвером веб-браузера, именем промоутера и списком путей к файлам групп. Он предоставляет методы для входа в Facebook, продвижения постов и событий.

**Атрибуты**:
- `d` (Driver): Инстанс веб-драйвера для взаимодействия с Facebook.
- `start_page` (str): URL начальной страницы Facebook (по умолчанию "https://www.facebook.com/hypotez.promocodes").
- `promoter` (str): Имя промоутера.

**Методы**:
- `__init__`: Инициализирует класс `Facebook` с драйвером, именем промоутера и списком файлов групп.
- `login`: Выполняет вход в Facebook.
- `promote_post`: Отправляет сообщение в форму для публикации поста.
- `promote_event`: Продвигает событие в Facebook.

### `__init__`

```python
 def __init__(self, driver: 'Driver', promoter: str, group_file_paths: list[str], *args, **kwards):
        """ Я могу передать уже запущенный инстанс драйвера. Например, из алиэкспресс
        @todo:
            - Добавить проверку на какой странице открылся фейсбук. Если открылась страница логина - выполнитл сценарий логина
        """
```

**Назначение**: Инициализация экземпляра класса `Facebook`.

**Параметры**:
- `driver` (Driver): Инстанс веб-драйвера для взаимодействия с Facebook.
- `promoter` (str): Имя промоутера.
- `group_file_paths` (list[str]): Список путей к файлам групп.
- `*args`: Произвольные позиционные аргументы.
- `**kwards`: Произвольные именованные аргументы.

**Как работает функция**:

1. **Инициализация драйвера**: Сохраняет переданный инстанс драйвера в атрибуте `self.d`.
2. **Инициализация промоутера**: Сохраняет имя промоутера в атрибуте `self.promoter`.

```
A: Инициализация драйвера и промоутера
|
B: Сохранение параметров в атрибуты класса
```

**Примеры**:

```python
from src.webdirver import Driver, Chrome
driver = Driver(Chrome)
fb = Facebook(driver=driver, promoter="MyPromoter", group_file_paths=[])
```

### `login`

```python
def login(self) -> bool:
    """ Функция отправляет текст в форму сообщения
    @param message: сообщение текстом. Знаки `;` будут заменеы на `SHIFT+ENTER`
    @returns `True`, если успешно, иначе `False`
    """
```

**Назначение**: Выполняет вход в Facebook.

**Возвращает**:
- `bool`: `True`, если вход выполнен успешно, иначе `False`.

**Вызывает**:
- Функцию `login` из модуля `.scenarios.login`.

**Как работает функция**:

1. **Вызов функции `login`**: Вызывает функцию `login` из модуля `.scenarios.login`, передавая текущий инстанс класса `Facebook` (self).

```
A: Вызов функции login из модуля scenarios.login
|
B: Возвращает результат выполнения функции login
```

**Примеры**:

```python
from src.webdirver import Driver, Chrome
driver = Driver(Chrome)
fb = Facebook(driver=driver, promoter="MyPromoter", group_file_paths=[])
result = fb.login()
print(f"Login successful: {result}")
```

### `promote_post`

```python
def promote_post(self, item: SimpleNamespace) -> bool:
    """ Функция отправляет текст в форму сообщения 
    @param message: сообщение текстом. Знаки `;` будут заменеы на `SHIFT+ENTER`
    @returns `True`, если успешно, иначе `False`
    """
```

**Назначение**: Отправляет сообщение в форму для публикации поста.

**Параметры**:
- `item` (SimpleNamespace): Объект, содержащий данные для публикации поста.

**Возвращает**:
- `bool`: `True`, если отправка выполнена успешно, иначе `False`.

**Вызывает**:
- Функцию `promote_post` из модуля `.scenarios`.

**Как работает функция**:

1. **Вызов функции `promote_post`**: Вызывает функцию `promote_post` из модуля `.scenarios`, передавая инстанс веб-драйвера (`self.d`) и объект `item` с данными для публикации.

```
A: Вызов функции promote_post из модуля scenarios
|
B: Возвращает результат выполнения функции promote_post
```

**Примеры**:

```python
from src.webdirver import Driver, Chrome
from types import SimpleNamespace
driver = Driver(Chrome)
fb = Facebook(driver=driver, promoter="MyPromoter", group_file_paths=[])
item = SimpleNamespace(message="Hello Facebook!")
result = fb.promote_post(item)
print(f"Post promotion successful: {result}")
```

### `promote_event`

```python
def promote_event(self, event: SimpleNamespace):
        """ Пример функции для продвижения события """
        ...
```

**Назначение**: Продвигает событие в Facebook.

**Параметры**:
- `event` (SimpleNamespace): Объект, содержащий данные о событии для продвижения.

**Как работает функция**:

Функция помечена как пример продвижения события. В текущей версии ее реализация отсутствует.

## Функции

В данном модуле функции определены внутри класса `Facebook`. Описание функций смотрите в разделе "Классы", в описании методов класса `Facebook`.