# Модуль `post_event.py`

## Обзор

Модуль предназначен для автоматизации процесса публикации календарных событий в группах Facebook с использованием Selenium WebDriver. Он предоставляет функции для ввода заголовка, даты, времени и описания события, а также для отправки события.

## Подробней

Модуль содержит функции, автоматизирующие ввод данных о событии (заголовок, дата, время, описание) и отправку этого события в Facebook. Используется для автоматизации маркетинговых кампаний и упрощения процесса публикации событий. Он использует `j_loads_ns` для загрузки локаторов элементов веб-страницы из JSON-файла, что облегчает поддержку и изменение структуры страницы.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `post_title`

```python
def post_title(d: Driver, title: str) -> bool:
    """ Sends the title of event.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        event (SimpleNamespace): The event containing the title, data of event and description to be sent.

    Returns:
        bool: `True` if the title and description were sent successfully, otherwise `None`.

    Examples:
        >>> driver = Driver(...)
        >>> event = SimpleNamespace(title="Campaign Title", description="Event Description")
        >>> post_title(driver, event)
        True
    """
    ...
```

**Назначение**: Отправляет заголовок события на веб-страницу.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `title` (str): Заголовок события, который необходимо отправить.

**Возвращает**:

-   `bool`: `True`, если заголовок был успешно отправлен, иначе `None`.

**Как работает функция**:

1.  Пытается отправить заголовок события, используя локатор `locator.event_title` и метод `execute_locator` драйвера `d`.
2.  Если отправка не удалась, регистрирует ошибку с помощью `logger.error` и возвращает `None`.
3.  В случае успешной отправки возвращает `True`.

**ASCII Flowchart**:

```
A[Отправка заголовка события]
|
B[Проверка результата отправки]
|
C[Успешно: True, Неуспешно: Ошибка, None]
```

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Пример использования функции post_title
driver = Driver()  # Предполагается, что драйвер инициализирован
event_title = "Заголовок события"
result = post_title(driver, event_title)
print(f"Результат отправки заголовка: {result}")
```

### `post_date`

```python
def post_date(d: Driver, date: str) -> bool:
    """ Sends the title of event.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        event (SimpleNamespace): The event containing the title, data of event and description to be sent.

    Returns:
        bool: `True` if the title and description were sent successfully, otherwise `None`.

    Examples:
        >>> driver = Driver(...)
        >>> event = SimpleNamespace(title="Campaign Title", description="Event Description")
        >>> post_title(driver, event)
        True
    """
    ...
```

**Назначение**: Отправляет дату события на веб-страницу.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `date` (str): Дата события, которую необходимо отправить.

**Возвращает**:

-   `bool`: `True`, если дата была успешно отправлена, иначе `None`.

**Как работает функция**:

1.  Пытается отправить дату события, используя локатор `locator.start_date` и метод `execute_locator` драйвера `d`.
2.  Если отправка не удалась, регистрирует ошибку с помощью `logger.error` и возвращает `None`.
3.  В случае успешной отправки возвращает `True`.

**ASCII Flowchart**:

```
A[Отправка даты события]
|
B[Проверка результата отправки]
|
C[Успешно: True, Неуспешно: Ошибка, None]
```

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Пример использования функции post_date
driver = Driver()  # Предполагается, что драйвер инициализирован
event_date = "2024-01-01"
result = post_date(driver, event_date)
print(f"Результат отправки даты: {result}")
```

### `post_time`

```python
def post_time(d: Driver, time: str) -> bool:
    """ Sends the title of event.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        event (SimpleNamespace): The event containing the title, data of event and description to be sent.

    Returns:
        bool: `True` if the title and description were sent successfully, otherwise `None`.

    Examples:
        >>> driver = Driver(...)
        >>> event = SimpleNamespace(title="Campaign Title", description="Event Description")
        >>> post_title(driver, event)
        True
    """
    ...
```

**Назначение**: Отправляет время события на веб-страницу.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `time` (str): Время события, которое необходимо отправить.

**Возвращает**:

-   `bool`: `True`, если время было успешно отправлено, иначе `None`.

**Как работает функция**:

1.  Пытается отправить время события, используя локатор `locator.start_time` и метод `execute_locator` драйвера `d`.
2.  Если отправка не удалась, регистрирует ошибку с помощью `logger.error` и возвращает `None`.
3.  В случае успешной отправки возвращает `True`.

**ASCII Flowchart**:

```
A[Отправка времени события]
|
B[Проверка результата отправки]
|
C[Успешно: True, Неуспешно: Ошибка, None]
```

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Пример использования функции post_time
driver = Driver()  # Предполагается, что драйвер инициализирован
event_time = "12:00"
result = post_time(driver, event_time)
print(f"Результат отправки времени: {result}")
```

### `post_description`

```python
def post_description(d: Driver, description: str) -> bool:
    """ Sends the title of event.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        event (SimpleNamespace): The event containing the title, data of event and description to be sent.

    Returns:
        bool: `True` if the title and description were sent successfully, otherwise `None`.

    Examples:
        >>> driver = Driver(...)
        >>> event = SimpleNamespace(title="Campaign Title", description="Event Description")
        >>> post_title(driver, event)
        True
    """
    ...
```

**Назначение**: Отправляет описание события на веб-страницу.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `description` (str): Описание события, которое необходимо отправить.

**Возвращает**:

-   `bool`: `True`, если описание было успешно отправлено, иначе `None`.

**Как работает функция**:

1.  Выполняет скролл страницы вниз на 300 пикселей.
2.  Пытается отправить описание события, используя локатор `locator.event_description` и метод `execute_locator` драйвера `d`.
3.  Если отправка не удалась, регистрирует ошибку с помощью `logger.error` и возвращает `None`.
4.  В случае успешной отправки возвращает `True`.

**ASCII Flowchart**:

```
A[Скролл страницы вниз]
|
B[Отправка описания события]
|
C[Проверка результата отправки]
|
D[Успешно: True, Неуспешно: Ошибка, None]
```

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Пример использования функции post_description
driver = Driver()  # Предполагается, что драйвер инициализирован
event_description = "Описание события"
result = post_description(driver, event_description)
print(f"Результат отправки описания: {result}")
```

### `post_event`

```python
def post_event(d: Driver, event: SimpleNamespace) -> bool:
    """ Manages the process of promoting a post with a title, description, and media files.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        category (SimpleNamespace): The category details used for the post title and description.
        products (List[SimpleNamespace]): List of products containing media and details to be posted.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> products = [SimpleNamespace(local_image_path=\'path/to/image.jpg\', ...)]
        >>> promote_post(driver, category, products)
    """
    ...
```

**Назначение**: Управляет процессом публикации события, отправляя заголовок, дату, время и описание.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `event` (SimpleNamespace): Объект, содержащий данные события (заголовок, дату, время, описание и ссылку).

**Возвращает**:

-   `bool`: `True`, если все данные были успешно отправлены и событие опубликовано, иначе `None`.

**Как работает функция**:

1.  Отправляет заголовок события, вызывая функцию `post_title`. Если отправка не удалась, возвращает `None`.
2.  Разделяет дату и время из атрибута `event.start`.
3.  Отправляет дату события, вызывая функцию `post_date`. Если отправка не удалась, возвращает `None`.
4.  Отправляет время события, вызывая функцию `post_time`. Если отправка не удалась, возвращает `None`.
5.  Отправляет описание события и ссылку, вызывая функцию `post_description`. Если отправка не удалась, возвращает `None`.
6.  Кликает на элемент отправки события, используя локатор `locator.event_send` и метод `execute_locator` драйвера `d`.  Если клик не удался, возвращает `None`.
7.  Делает паузу в 30 секунд и возвращает `True`.

**ASCII Flowchart**:

```
A[Отправка заголовка]
|
B[Отправка даты]
|
C[Отправка времени]
|
D[Отправка описания]
|
E[Клик на отправку события]
|
F[Ожидание 30 сек]
|
G[Успешно: True]
```

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace
import time

# Пример использования функции post_event
driver = Driver()  # Предполагается, что драйвер инициализирован
event_data = SimpleNamespace(
    title="Заголовок события",
    start="2024-01-01 12:00",
    description="Описание события",
    promotional_link="http://example.com"
)
result = post_event(driver, event_data)
print(f"Результат публикации события: {result}")