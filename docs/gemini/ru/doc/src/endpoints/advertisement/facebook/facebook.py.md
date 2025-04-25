# Модуль рекламы на фейсбук

## Обзор

Модуль `src.endpoints.advertisement.facebook.facebook` предоставляет функциональность для взаимодействия с платформой Facebook через вебдрайвер. Он содержит класс `Facebook`, который реализует сценарии для работы с рекламными кампаниями, включая:

- **Авторизацию:** Логин на Facebook.
- **Публикация постов:** Отправка текстовых сообщений и загрузка медиафайлов.
- **Продвижение постов:** Проведение рекламных кампаний.

## Подробей

Модуль работает с помощью вебдрайвера, обеспечивая автоматизацию действий на платформе Facebook. Он использует различные сценарии для выполнения задач, таких как:

- **`login`**:  Логин в аккаунт Facebook.
- **`post_message`**:  Отправка текстового сообщения в форму.
- **`upload_media`**:  Загрузка файлов или списка файлов.

## Классы

### `Facebook`

**Описание**: Класс для взаимодействия с Facebook через вебдрайвер.

**Атрибуты**:

- `d` (`Driver`): Вебдрайвер для взаимодействия с Facebook.
- `start_page` (`str`): URL-адрес стартовой страницы Facebook.
- `promoter` (`str`): Имя пользователя, от имени которого производится продвижение.

**Методы**:

- `__init__(self, driver: 'Driver', promoter: str, group_file_paths: list[str], *args, **kwargs)`:  Инициализирует объект `Facebook`.  Принимает в качестве аргумента драйвер, имя пользователя и пути к файлам групп.
- `login(self) -> bool`:  Выполняет сценарий входа на Facebook.
- `promote_post(self, item: SimpleNamespace) -> bool`:  Отправляет текст в форму сообщения.
- `promote_event(self, event: SimpleNamespace)`:  Пример функции для продвижения события.

## Методы класса

### `login(self) -> bool`

```python
    def login(self) -> bool:
        return login(self)
```

**Назначение**: Выполняет сценарий входа на Facebook.

**Параметры**:

- `self`:  Ссылка на экземпляр класса `Facebook`.

**Возвращает**:

- `bool`: `True`, если вход успешен, иначе `False`.

**Как работает функция**:

- Вызывает функцию `login` из модуля `scenarios.login` для выполнения сценария входа.
- Возвращает результат выполнения сценария входа.


### `promote_post(self, item: SimpleNamespace) -> bool`

```python
    def promote_post(self, item: SimpleNamespace) -> bool:
        """ Функция отправляет текст в форму сообщения 
        @param message: сообщение текстом. Знаки `;` будут заменеы на `SHIFT+ENTER`
        @returns `True`, если успешно, иначе `False`
        """
        ...
        return promote_post(self.d, item)
```

**Назначение**: Отправляет текст в форму сообщения.

**Параметры**:

- `self`:  Ссылка на экземпляр класса `Facebook`.
- `item` (`SimpleNamespace`): Объект с информацией о посте.

**Возвращает**:

- `bool`: `True`, если отправка успешна, иначе `False`.

**Как работает функция**:

- Вызывает функцию `promote_post` из модуля `scenarios` для отправки сообщения.
- Передает в функцию `promote_post` вебдрайвер (`self.d`) и объект `item` с информацией о посте.
- Возвращает результат выполнения сценария отправки сообщения.

### `promote_event(self, event: SimpleNamespace)`

```python
    def promote_event(self, event: SimpleNamespace):
        """ Пример функции для продвижения события """
        ...
```

**Назначение**: Пример функции для продвижения события.

**Параметры**:

- `self`:  Ссылка на экземпляр класса `Facebook`.
- `event` (`SimpleNamespace`): Объект с информацией о событии.

**Как работает функция**:

- Эта функция является примером и не реализована.
- Она предназначена для продвижения событий на Facebook.
- В теле функции нужно добавить логику взаимодействия с Facebook для продвижения событий.

## Параметры класса

- `d` (`Driver`): Вебдрайвер для взаимодействия с Facebook. 
- `start_page` (`str`): URL-адрес стартовой страницы Facebook.
- `promoter` (`str`): Имя пользователя, от имени которого производится продвижение.

## Примеры

```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Chrome) # создаем драйвер
facebook = Facebook(driver, promoter='test_user', group_file_paths=[]) # создаем объект facebook
facebook.login() # логинимся на фейсбук
facebook.promote_post({'post_text': 'Test message'}) # отправляем сообщение
```

**Пример:**

```python
facebook = Facebook(driver, promoter='test_user', group_file_paths=[]) # создаем объект facebook
facebook.promote_post({'post_text': 'Test message'}) # отправляем сообщение