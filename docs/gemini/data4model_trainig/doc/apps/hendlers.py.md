## \\file /src/endpoints/bots/telegram/digital_market/bot/user/user_router.py

# Модуль маршрутизации пользователя для Telegram-бота

```rst
.. module:: src.endpoints.bots.telegram.digital_market.bot.user.user_router
```

Этот модуль содержит обработчики для различных пользовательских сценариев в Telegram-боте.

## Обзор

Модуль `src.endpoints.bots.telegram.digital_market.bot.user.user_router` предоставляет маршрутизаторы для обработки запросов, связанных с пользователем в Telegram-боте.

## Подробней

Модуль содержит обработчики для команды `/start`, отображения главной страницы и выполнения поиска фильмов.

## Функции

### `command_start_handler`

```python
@router.message(CommandStart())
async def command_start_handler(message: Message, session_with_commit: AsyncSession) -> None:
```

**Назначение**: Обрабатывает команду `/start`.

**Параметры**:

*   `message` (Message): Объект сообщения Telegram.
*   `session_with_commit` (AsyncSession): Асинхронная сессия базы данных с коммитом.

**Как работает функция**:

1.  Получает ID пользователя из объекта сообщения.
2.  Ищет пользователя в базе данных, используя `UserDAO.find_one_or_none`.
3.  Если пользователь найден, отправляет приветственное сообщение с клавиатурой основного меню.
4.  Если пользователь не найден, создает нового пользователя в базе данных, используя `UserDAO.add`, и отправляет приветственное сообщение с клавиатурой основного меню.

### `page_home`

```python
@user_router.callback_query(F.data == "home")
async def page_home(call: CallbackQuery):
```

**Назначение**: Обрабатывает нажатие кнопки "home" для отображения главной страницы.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.

**Как работает функция**:

1.  Отправляет уведомление о переходе на главную страницу.
2.  Отправляет приветственное сообщение с клавиатурой основного меню.

### `movie_handler`

```python
@router.callback_query(F.data == 'new_movies')
async def movie_handler(callback: CallbackQuery, state: FSMContext) -> None:
```

**Назначение**: Обрабатывает нажатие кнопки "new\_movies" для поиска фильмов.

**Параметры**:

*   `callback` (CallbackQuery): Объект обратного вызова.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Устанавливает состояние машины состояний в `Params.type_movie`.
2.  Отправляет пользователю сообщение с запросом указать тип фильма (фильм или сериал) и предоставляет клавиатуру выбора.

### `series_handler`

```python
@router.callback_query(F.data == 'series')
async def series_handler(callback: CallbackQuery, state: FSMContext) -> None:
```

**Назначение**: Обрабатывает нажатие кнопки "series" для поиска сериала.

**Параметры**:

*   `callback` (CallbackQuery): Объект обратного вызова.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Удаляет предыдущее сообщение.
2.  Обновляет состояние машины состояний, устанавливая тип фильма в `'series'`.
3.  Переходит в состояние `Params.name`.
4.  Отправляет пользователю сообщение с запросом ввести название сериала.

### `film_handler`

```python
@router.callback_query(F.data == 'film')
async def film_handler(callback: CallbackQuery, state: FSMContext) -> None:
```

**Назначение**: Обрабатывает нажатие кнопки "film" для поиска фильма.

**Параметры**:

*   `callback` (CallbackQuery): Объект обратного вызова.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Удаляет предыдущее сообщение.
2.  Обновляет состояние машины состояний, устанавливая тип фильма в `'film'`.
3.  Переходит в состояние `Params.name`.
4.  Отправляет пользователю сообщение с запросом ввести название фильма.

### `name_handler`

```python
@router.message(Params.name)
async def name_handler(message: Message, state: FSMContext) -> None:
```

**Назначение**: Обрабатывает ввод названия фильма или сериала.

**Параметры**:

*   `message` (Message): Объект сообщения Telegram.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Сохраняет название фильма или сериала в состоянии машины состояний.
2.  Извлекает данные из состояния.
3.  Выполняет поиск фильма или сериала, используя функцию `search_query`.
4.  Отправляет пользователю сообщение с информацией о найденном фильме или сериале (название, тип, описание, ссылка).
5.  Отправляет пользователю клавиатуру для поиска нового фильма.
6.  Очищает состояние машины состояний.