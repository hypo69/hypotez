# Модуль публикации событий в Facebook

## Обзор

Этот модуль содержит набор функций для публикации календарных событий в группах Facebook. Он обеспечивает функциональность для отправки заголовка, даты, времени, описания и отправки события. Модуль использует WebDriver (Selenium) для взаимодействия с веб-страницей Facebook и работает с локаторами, определенными в отдельном файле конфигурации.

## Подробности

Модуль `post_event.py` предоставляет функции для публикации календарных событий в группах Facebook. 

- **Функции**:
  - `post_title(d: Driver, title: str) -> bool`: Отправляет заголовок события.
  - `post_date(d: Driver, date: str) -> bool`: Отправляет дату события.
  - `post_time(d: Driver, time: str) -> bool`: Отправляет время события.
  - `post_description(d: Driver, description: str) -> bool`: Отправляет описание события.
  - `post_event(d: Driver, event: SimpleNamespace) -> bool`: Управляет процессом публикации события.
  
## Классы

### `post_event.post_title(d: Driver, title: str) -> bool`

**Описание**: Отправляет заголовок события.

**Параметры**:

- `d` (Driver): Экземпляр WebDriver, используемый для взаимодействия с веб-страницей.
- `title` (str): Заголовок события.

**Возвращает**:

- `bool`: `True`, если заголовок был отправлен успешно, иначе `None`.

**Пример**:

```python
>>> driver = Driver(Chrome) 
>>> post_title(driver, title='Название события')
True 
```

**Как работает функция**:

- Использует локатор `locator.event_title` из файла конфигурации `post_event.json`.
- Выполняет отправку заголовка с помощью `d.execute_locator`.
- В случае ошибки логирует сообщение с помощью `logger.error`.


### `post_event.post_date(d: Driver, date: str) -> bool`

**Описание**: Отправляет дату события.

**Параметры**:

- `d` (Driver): Экземпляр WebDriver, используемый для взаимодействия с веб-страницей.
- `date` (str): Дата события.

**Возвращает**:

- `bool`: `True`, если дата была отправлена успешно, иначе `None`.

**Пример**:

```python
>>> driver = Driver(Chrome)
>>> post_date(driver, date='2024-03-01')
True
```

**Как работает функция**:

- Использует локатор `locator.start_date` из файла конфигурации `post_event.json`.
- Выполняет отправку даты с помощью `d.execute_locator`.
- В случае ошибки логирует сообщение с помощью `logger.error`.

### `post_event.post_time(d: Driver, time: str) -> bool`

**Описание**: Отправляет время события.

**Параметры**:

- `d` (Driver): Экземпляр WebDriver, используемый для взаимодействия с веб-страницей.
- `time` (str): Время события.

**Возвращает**:

- `bool`: `True`, если время было отправлено успешно, иначе `None`.

**Пример**:

```python
>>> driver = Driver(Chrome)
>>> post_time(driver, time='18:00')
True
```

**Как работает функция**:

- Использует локатор `locator.start_time` из файла конфигурации `post_event.json`.
- Выполняет отправку времени с помощью `d.execute_locator`.
- В случае ошибки логирует сообщение с помощью `logger.error`.

### `post_event.post_description(d: Driver, description: str) -> bool`

**Описание**: Отправляет описание события.

**Параметры**:

- `d` (Driver): Экземпляр WebDriver, используемый для взаимодействия с веб-страницей.
- `description` (str): Описание события.

**Возвращает**:

- `bool`: `True`, если описание было отправлено успешно, иначе `None`.

**Пример**:

```python
>>> driver = Driver(Chrome)
>>> post_description(driver, description='Описание события')
True
```

**Как работает функция**:

- Использует локатор `locator.event_description` из файла конфигурации `post_event.json`.
- Выполняет отправку описания с помощью `d.execute_locator`.
- В случае ошибки логирует сообщение с помощью `logger.error`.


### `post_event.post_event(d: Driver, event: SimpleNamespace) -> bool`

**Описание**: Управляет процессом публикации события.

**Параметры**:

- `d` (Driver): Экземпляр WebDriver, используемый для взаимодействия с веб-страницей.
- `event` (SimpleNamespace):  Объект, содержащий информацию о событии.
 
**Возвращает**:

- `bool`: `True`, если событие было отправлено успешно, иначе `None`.

**Пример**:

```python
>>> driver = Driver(Chrome)
>>> event = SimpleNamespace(title='Название события', start='2024-03-01 18:00', description='Описание события')
>>> post_event(driver, event)
True
```

**Как работает функция**:

- Вызывает функции `post_title`, `post_date`, `post_time`, `post_description` для отправки данных о событии.
- Отправляет событие с помощью локатора `locator.event_send` из файла конфигурации `post_event.json`.
- В случае ошибки логирует сообщение с помощью `logger.error`.

## Примеры

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Публикация события
event = SimpleNamespace(title='Название события', start='2024-03-01 18:00', description='Описание события')
post_event(driver, event)