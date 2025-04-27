# Публикация календарного события в группах Facebook

## Обзор

Модуль содержит функции для автоматизации процесса публикации календарных событий в группах Facebook. 

## Подробности

Модуль использует `selenium` для взаимодействия с веб-страницей Facebook. 

## Классы

### `Driver`

**Описание**: Класс, который обеспечивает взаимодействие с веб-браузером с помощью Selenium.

**Атрибуты**:

- `driver` (webdriver): Объект WebDriver, предоставляющий доступ к веб-браузеру.

**Методы**:

- `execute_locator(l:dict)`: Выполняет действие над элементом веб-страницы по локатору.

## Функции

### `post_title(d: Driver, title:str) -> bool`

**Цель**: Отправляет заголовок события в поле ввода на странице Facebook.

**Параметры**:

- `d` (Driver): Объект WebDriver, используемый для взаимодействия с веб-страницей.
- `title` (str): Заголовок события.

**Возвращает**:

- `bool`: `True`, если заголовок события был успешно отправлен, иначе `False`.

**Примеры**:

```python
>>> driver = Driver(...)
>>> title = "Campaign Title"
>>> post_title(driver, title)
True
```

### `post_date(d: Driver, date:str) -> bool`

**Цель**: Отправляет дату события в поле ввода на странице Facebook.

**Параметры**:

- `d` (Driver): Объект WebDriver, используемый для взаимодействия с веб-страницей.
- `date` (str): Дата события в формате "ДД.ММ.ГГГГ".

**Возвращает**:

- `bool`: `True`, если дата события была успешно отправлена, иначе `False`.

**Примеры**:

```python
>>> driver = Driver(...)
>>> date = "22.04.2024"
>>> post_date(driver, date)
True
```

### `post_time(d: Driver, time:str) -> bool`

**Цель**: Отправляет время события в поле ввода на странице Facebook.

**Параметры**:

- `d` (Driver): Объект WebDriver, используемый для взаимодействия с веб-страницей.
- `time` (str): Время события в формате "ЧЧ:ММ".

**Возвращает**:

- `bool`: `True`, если время события было успешно отправлено, иначе `False`.

**Примеры**:

```python
>>> driver = Driver(...)
>>> time = "19:00"
>>> post_time(driver, time)
True
```

### `post_description(d: Driver, description: str) -> bool`

**Цель**: Отправляет описание события в поле ввода на странице Facebook.

**Параметры**:

- `d` (Driver): Объект WebDriver, используемый для взаимодействия с веб-страницей.
- `description` (str): Описание события.

**Возвращает**:

- `bool`: `True`, если описание события было успешно отправлено, иначе `False`.

**Примеры**:

```python
>>> driver = Driver(...)
>>> description = "Event Description"
>>> post_description(driver, description)
True
```

### `post_event(d: Driver, event: SimpleNamespace) -> bool`

**Цель**: Управляет процессом публикации события в Facebook, включая заголовок, описание и дату.

**Параметры**:

- `d` (Driver): Объект WebDriver, используемый для взаимодействия с веб-страницей.
- `event` (SimpleNamespace): Объект, содержащий информацию о событии, включая заголовок, описание, дату и время.

**Примеры**:

```python
>>> driver = Driver(...)
>>> event = SimpleNamespace(title="Campaign Title", description="Event Description", start="22.04.2024 19:00")
>>> post_event(driver, event)
True
```