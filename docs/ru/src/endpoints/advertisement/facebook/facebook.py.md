# Модуль `facebook`

## Обзор

Модуль `facebook` предназначен для автоматизации действий в социальной сети Facebook с использованием веб-драйвера. Он включает в себя функции для входа в аккаунт, продвижения постов и других взаимодействий, таких как загрузка медиа-файлов и обновление подписей к изображениям.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для автоматизации задач, связанных с рекламой и продвижением в Facebook. Он использует веб-драйвер для эмуляции действий пользователя в браузере, что позволяет автоматизировать такие задачи, как вход в аккаунт, публикация сообщений и загрузка медиафайлов.

## Классы

### `Facebook`

**Описание**: Класс для взаимодействия с Facebook через веб-драйвер.

**Атрибуты**:
- `d` (Driver): Инстанс веб-драйвера для управления браузером.
- `start_page` (str): URL начальной страницы Facebook (`https://www.facebook.com/hypotez.promocodes`).
- `promoter` (str): Имя пользователя, осуществляющего продвижение.

**Методы**:
- `__init__`: Инициализирует класс `Facebook` и выполняет первоначальную настройку драйвера.
- `login`: Выполняет вход в аккаунт Facebook.
- `promote_post`: Продвигает пост в Facebook.
- `promote_event`: Продвигает событие в Facebook.

### `__init__`
```python
    def __init__(self, driver: 'Driver', promoter: str, group_file_paths: list[str], *args, **kwargs):
        """ Я могу передать уже запущенный инстанс драйвера. Например, из алиэкспресс
        @todo:
            - Добавить проверку на какой странице открылся фейсбук. Если открылась страница логина - выполнитл сценарий логина
        """
        self.d = driver
        self.promoter = promoter
        ...
        
        #self.driver.get_url (self.start_page)
        #switch_account(self.driver) # <- переключение профиля, если не на своей странице
```
**Назначение**: Инициализация экземпляра класса `Facebook`.

**Параметры**:
- `driver` (Driver): Инстанс веб-драйвера.
- `promoter` (str): Имя пользователя, осуществляющего продвижение.
- `group_file_paths` (list[str]): Список путей к файлам групп.
- `*args`: Произвольные позиционные аргументы.
- `**kwargs`: Произвольные именованные аргументы.

**Как работает функция**:
- Функция принимает инстанс веб-драйвера, имя пользователя, осуществляющего продвижение, и список путей к файлам групп.
- Она сохраняет инстанс веб-драйвера в атрибуте `d`, имя пользователя в атрибуте `promoter`.
- Оставляет заполнитель `...` для дальнейшей настройки.
- Закомментированы строки для перехода на стартовую страницу и переключения аккаунта.

### `login`

```python
    def login(self) -> bool:
        return login(self)
```
**Назначение**: Выполняет вход в аккаунт Facebook.

**Возвращает**:
- `bool`: `True`, если вход выполнен успешно, иначе `False`.

**Как работает функция**:
- Функция вызывает функцию `login` из модуля `.scenarios.login` и передает ей текущий экземпляр класса `Facebook`.
- Возвращает результат выполнения функции `login`.

**Примеры**:

```python
# Пример вызова функции login
facebook_instance = Facebook(driver=driver_instance, promoter="username", group_file_paths=[])
result = facebook_instance.login()
print(f"Login successful: {result}")
```

### `promote_post`

```python
    def promote_post(self, item: SimpleNamespace) -> bool:
        """ Функция отправляет текст в форму сообщения 
        @param message: сообщение текстом. Знаки `;` будут заменеы на `SHIFT+ENTER`
        @returns `True`, если успешно, иначе `False`
        """
        ...
        return promote_post(self.d, item)
```
**Назначение**: Продвигает пост в Facebook, отправляя текст сообщения.

**Параметры**:
- `item` (SimpleNamespace): Объект, содержащий информацию о посте, включая текст сообщения.

**Возвращает**:
- `bool`: `True`, если продвижение поста выполнено успешно, иначе `False`.

**Как работает функция**:
- Функция принимает объект `SimpleNamespace`, содержащий информацию о посте.
- Вызывает функцию `promote_post` из модуля `.scenarios` и передает ей инстанс веб-драйвера (`self.d`) и объект `item`.
- Функция `promote_post` отправляет текст сообщения в форму на странице Facebook.
- Возвращает результат выполнения функции `promote_post`.

**Примеры**:

```python
# Пример вызова функции promote_post
item_data = SimpleNamespace(message="Check out my new post!")
facebook_instance = Facebook(driver=driver_instance, promoter="username", group_file_paths=[])
result = facebook_instance.promote_post(item_data)
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
- `event` (SimpleNamespace): Объект, содержащий информацию о событии.

**Как работает функция**:
- Функция принимает объект `SimpleNamespace`, содержащий информацию о событии.
- Оставляет заполнитель `...` для дальнейшей реализации логики продвижения события.

**Примеры**:

```python
# Пример вызова функции promote_event
event_data = SimpleNamespace(name="My Event", description="Join us!")
facebook_instance = Facebook(driver=driver_instance, promoter="username", group_file_paths=[])
facebook_instance.promote_event(event_data)