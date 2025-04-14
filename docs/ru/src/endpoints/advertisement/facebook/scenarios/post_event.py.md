# Модуль `post_event.py`

## Обзор

Модуль предназначен для публикации календарного события в группах Facebook. Он включает функции для отправки заголовка, даты, времени и описания события, а также для управления процессом публикации события.

## Подробней

Модуль содержит функции для автоматизации процесса создания и публикации событий в Facebook группах. Он использует Selenium WebDriver для взаимодействия с веб-страницей Facebook и выполняет такие действия, как ввод заголовка, даты, времени и описания события, а также отправку события. Модуль использует локаторы, хранящиеся в JSON-файле, для поиска элементов на странице.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `post_title`

```python
def post_title(d: Driver, title: str) -> bool:
    """ Отправляет заголовок события.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        title (str): Заголовок события, который необходимо отправить.

    Returns:
        bool: `True`, если заголовок успешно отправлен, иначе `None`.

    Example:
        >>> driver = Driver(...)
        >>> event = SimpleNamespace(title="Campaign Title", description="Event Description")
        >>> post_title(driver, event)
        True
    """
```

**Назначение**: Отправляет заголовок события в соответствующее поле на веб-странице.

**Параметры**:
- `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
- `title` (str): Заголовок события, который необходимо отправить.

**Возвращает**:
- `bool`: `True`, если заголовок успешно отправлен, иначе `None`.

**Как работает функция**:
1. Пытается отправить заголовок события, используя локатор `locator.event_title`.
2. Если отправка не удалась, логирует ошибку и возвращает `None`.
3. В случае успешной отправки возвращает `True`.

**ASCII flowchart**:

```
A[Начало]
|
B[Отправка заголовка события с использованием locator.event_title]
|
C[Успешно?] -- No --> D[Логирование ошибки и возврат None]
|
Yes
|
E[Возврат True]
|
F[Конец]
```

**Примеры**:
```python
driver = Driver(Chrome)
event = SimpleNamespace(title="Campaign Title", description="Event Description")
result = post_title(driver, event.title)
print(result)  # Вывод: True или None в случае ошибки
```

### `post_date`

```python
def post_date(d: Driver, date: str) -> bool:
    """ Отправляет дату события.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        date (str): Дата события, которую необходимо отправить.

    Returns:
        bool: `True`, если дата успешно отправлена, иначе `None`.

    Example:
        >>> driver = Driver(...)
        >>> event = SimpleNamespace(title="Campaign Title", description="Event Description")
        >>> post_date(driver, event.start)
        True
    """
```

**Назначение**: Отправляет дату события в соответствующее поле на веб-странице.

**Параметры**:
- `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
- `date` (str): Дата события, которую необходимо отправить.

**Возвращает**:
- `bool`: `True`, если дата успешно отправлена, иначе `None`.

**Как работает функция**:
1. Пытается отправить дату события, используя локатор `locator.start_date`.
2. Если отправка не удалась, логирует ошибку и возвращает `None`.
3. В случае успешной отправки возвращает `True`.

**ASCII flowchart**:

```
A[Начало]
|
B[Отправка даты события с использованием locator.start_date]
|
C[Успешно?] -- No --> D[Логирование ошибки и возврат None]
|
Yes
|
E[Возврат True]
|
F[Конец]
```

**Примеры**:
```python
driver = Driver(Chrome)
event = SimpleNamespace(title="Campaign Title", description="Event Description", start="2024-08-24 10:00")
result = post_date(driver, event.start.split()[0])
print(result)  # Вывод: True или None в случае ошибки
```

### `post_time`

```python
def post_time(d: Driver, time: str) -> bool:
    """ Отправляет время события.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        time (str): Время события, которое необходимо отправить.

    Returns:
        bool: `True`, если время успешно отправлено, иначе `None`.

    Example:
        >>> driver = Driver(...)
        >>> event = SimpleNamespace(title="Campaign Title", description="Event Description")
        >>> post_time(driver, event.start)
        True
    """
```

**Назначение**: Отправляет время события в соответствующее поле на веб-странице.

**Параметры**:
- `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
- `time` (str): Время события, которое необходимо отправить.

**Возвращает**:
- `bool`: `True`, если время успешно отправлено, иначе `None`.

**Как работает функция**:
1. Пытается отправить время события, используя локатор `locator.start_time`.
2. Если отправка не удалась, логирует ошибку и возвращает `None`.
3. В случае успешной отправки возвращает `True`.

**ASCII flowchart**:

```
A[Начало]
|
B[Отправка времени события с использованием locator.start_time]
|
C[Успешно?] -- No --> D[Логирование ошибки и возврат None]
|
Yes
|
E[Возврат True]
|
F[Конец]
```

**Примеры**:
```python
driver = Driver(Chrome)
event = SimpleNamespace(title="Campaign Title", description="Event Description", start="2024-08-24 10:00")
result = post_time(driver, event.start.split()[1])
print(result)  # Вывод: True или None в случае ошибки
```

### `post_description`

```python
def post_description(d: Driver, description: str) -> bool:
    """ Отправляет описание события.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        description (str): Описание события, которое необходимо отправить.

    Returns:
        bool: `True`, если описание успешно отправлено, иначе `None`.

    Example:
        >>> driver = Driver(...)
        >>> event = SimpleNamespace(title="Campaign Title", description="Event Description")
        >>> post_description(driver, event)
        True
    """
```

**Назначение**: Отправляет описание события в соответствующее поле на веб-странице.

**Параметры**:
- `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
- `description` (str): Описание события, которое необходимо отправить.

**Возвращает**:
- `bool`: `True`, если описание успешно отправлено, иначе `None`.

**Как работает функция**:
1. Выполняет скролл страницы вниз на 300 пикселей.
2. Пытается отправить описание события, используя локатор `locator.event_description`.
3. Если отправка не удалась, логирует ошибку и возвращает `None`.
4. В случае успешной отправки возвращает `True`.

**ASCII flowchart**:

```
A[Начало]
|
B[Скролл страницы вниз]
|
C[Отправка описания события с использованием locator.event_description]
|
D[Успешно?] -- No --> E[Логирование ошибки и возврат None]
|
Yes
|
F[Возврат True]
|
G[Конец]
```

**Примеры**:
```python
driver = Driver(Chrome)
event = SimpleNamespace(title="Campaign Title", description="Event Description")
result = post_description(driver, event.description)
print(result)  # Вывод: True или None в случае ошибки
```

### `post_event`

```python
def post_event(d: Driver, event: SimpleNamespace) -> bool:
    """ Управляет процессом публикации события, включая заголовок, дату, время, описание и отправку.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        event (SimpleNamespace): Объект, содержащий данные события (заголовок, дату, время, описание и рекламную ссылку).

    Returns:
        bool: `True`, если событие успешно опубликовано, иначе `None`.

    Example:
        >>> driver = Driver(...)
        >>> event = SimpleNamespace(title="Campaign Title", description="Campaign Description", start="2024-08-24 10:00", promotional_link="https://example.com")
        >>> post_event(driver, event)
        True
    """
```

**Назначение**: Управляет процессом публикации события, включая отправку заголовка, даты, времени, описания и нажатие кнопки отправки.

**Параметры**:
- `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
- `event` (SimpleNamespace): Объект, содержащий данные события (заголовок, дату, время, описание и рекламную ссылку).

**Возвращает**:
- `bool`: `True`, если событие успешно опубликовано, иначе `None`.

**Как работает функция**:
1. Отправляет заголовок события с помощью функции `post_title`. Если отправка не удалась, функция завершается.
2. Разбивает строку даты и времени события на дату и время.
3. Отправляет дату события с помощью функции `post_date`. Если отправка не удалась, функция завершается.
4. Отправляет время события с помощью функции `post_time`. Если отправка не удалась, функция завершается.
5. Отправляет описание события, включая рекламную ссылку, с помощью функции `post_description`. Если отправка не удалась, функция завершается.
6. Нажимает кнопку отправки события, используя локатор `locator.event_send`. Если нажатие не удалось, функция завершается.
7. Ожидает 30 секунд.
8. Возвращает `True`.

**ASCII flowchart**:

```
A[Начало]
|
B[Отправка заголовка с помощью post_title]
|
C[Успешно?] -- No --> I[Завершение]
|
Yes
|
D[Разбиение даты и времени события]
|
E[Отправка даты с помощью post_date]
|
F[Успешно?] -- No --> I[Завершение]
|
Yes
|
G[Отправка времени с помощью post_time]
|
H[Успешно?] -- No --> I[Завершение]
|
Yes
|
J[Отправка описания с помощью post_description]
|
K[Успешно?] -- No --> I[Завершение]
|
Yes
|
L[Нажатие кнопки отправки с использованием locator.event_send]
|
M[Успешно?] -- No --> I[Завершение]
|
Yes
|
N[Ожидание 30 секунд]
|
O[Возврат True]
|
P[Конец]
```

**Примеры**:
```python
driver = Driver(Chrome)
event = SimpleNamespace(title="Campaign Title", description="Campaign Description", start="2024-08-24 10:00", promotional_link="https://example.com")
result = post_event(driver, event)
print(result)  # Вывод: True или None в случае ошибки