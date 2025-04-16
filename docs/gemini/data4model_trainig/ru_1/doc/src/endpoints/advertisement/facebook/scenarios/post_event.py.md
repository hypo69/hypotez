# Модуль `post_event`

## Обзор

Модуль `post_event` предназначен для автоматизации процесса публикации календарных событий в группах Facebook с использованием Selenium WebDriver. Он содержит функции для отправки заголовка, даты, времени и описания события, а также для выполнения публикации события.

## Подробней

Модуль содержит набор функций, которые взаимодействуют с веб-страницей Facebook через WebDriver для автоматизации процесса создания и публикации событий. Он использует локаторы, загруженные из JSON-файла, для определения элементов веб-страницы, с которыми необходимо взаимодействовать.

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

**Назначение**: Отправляет заголовок события.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `title` (str): Заголовок события.

**Возвращает**:

-   `bool`: `True`, если заголовок успешно отправлен, иначе `None`.

**Как работает функция**:

Функция использует метод `execute_locator` объекта `Driver` для отправки заголовка события, найденного по локатору `locator.event_title`. В случае неудачи регистрирует ошибку и возвращает `None`.

**Примеры**:

```python
driver = Driver(Firefox)
title = "Заголовок события"
result = post_title(driver, title)
print(result)  # Вывод: True или None в случае ошибки
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

**Назначение**: Отправляет дату события.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `date` (str): Дата события.

**Возвращает**:

-   `bool`: `True`, если дата успешно отправлена, иначе `None`.

**Как работает функция**:

Функция использует метод `execute_locator` объекта `Driver` для отправки даты события, найденной по локатору `locator.start_date`. В случае неудачи регистрирует ошибку и возвращает `None`.

**Примеры**:

```python
driver = Driver(Firefox)
date = "2024-08-30"
result = post_date(driver, date)
print(result)  # Вывод: True или None в случае ошибки
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

**Назначение**: Отправляет время события.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `time` (str): Время события.

**Возвращает**:

-   `bool`: `True`, если время успешно отправлено, иначе `None`.

**Как работает функция**:

Функция использует метод `execute_locator` объекта `Driver` для отправки времени события, найденного по локатору `locator.start_time`. В случае неудачи регистрирует ошибку и возвращает `None`.

**Примеры**:

```python
driver = Driver(Firefox)
time = "18:00"
result = post_time(driver, time)
print(result)  # Вывод: True или None в случае ошибки
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

**Назначение**: Отправляет описание события.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `description` (str): Описание события.

**Возвращает**:

-   `bool`: `True`, если описание успешно отправлено, иначе `None`.

**Как работает функция**:

Функция выполняет скролл страницы вниз, а затем использует метод `execute_locator` объекта `Driver` для отправки описания события, найденного по локатору `locator.event_description`. В случае неудачи регистрирует ошибку и возвращает `None`.

**Примеры**:

```python
driver = Driver(Firefox)
description = "Описание события"
result = post_description(driver, description)
print(result)  # Вывод: True или None в случае ошибки
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
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> promote_post(driver, category, products)
    """
    ...
```

**Назначение**: Управляет процессом публикации события, отправляя заголовок, дату, время и описание события.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `event` (SimpleNamespace): Объект, содержащий данные события, такие как заголовок, дата, время, описание и промо-ссылка.

**Возвращает**:

-   `bool`: `True`, если событие успешно опубликовано, иначе `None`.

**Как работает функция**:

Функция последовательно вызывает функции `post_title`, `post_date`, `post_time` и `post_description` для отправки соответствующих данных события. Затем она нажимает на элемент, найденный по локатору `locator.event_send`, чтобы опубликовать событие. После этого функция ждет 30 секунд и возвращает `True`.

**Примеры**:

```python
driver = Driver(Firefox)
event = SimpleNamespace(
    title="Заголовок события",
    start="2024-08-30 18:00",
    description="Описание события",
    promotional_link="https://example.com"
)
result = post_event(driver, event)
print(result)  # Вывод: True или None в случае ошибки