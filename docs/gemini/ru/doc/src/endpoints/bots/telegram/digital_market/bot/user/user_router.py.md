# Модуль для маршрутизации запросов пользователя

## Обзор

Модуль `user_router.py` содержит маршрутизацию запросов пользователя в телеграм-боте. Он обрабатывает команды, связанные с пользователем, такие как:

- `/start`: регистрация нового пользователя, приветствие.
- Кнопки в клавиатуре: "Главная страница", "О магазине", "Мой профиль", "Мои покупки".

## Подробнее

Этот модуль является частью системы телеграм-бота, который реализует функционал магазина. 

- Обработчики команд и кнопок используют `aiogram` для обработки входящих запросов от пользователя.
- `UserDAO` - это слой доступа к данным, который используется для взаимодействия с базой данных и сохранения информации о пользователях.
- `main_user_kb` и `purchases_kb` - это функции, которые создают клавиатуру с кнопками для взаимодействия с пользователем.

## Классы

### `user_router`

**Описание**: Объект класса `Router` для обработки запросов пользователя.
**Наследует**: `aiogram.Router`

**Атрибуты**: 
- Нет

**Методы**: 
- `cmd_start`: Обработчик команды `/start`.
- `page_home`: Обработчик кнопки "Главная страница".
- `page_about`: Обработчик кнопки "О магазине".
- `page_my_profile`: Обработчик кнопки "Мой профиль".
- `page_user_purchases`: Обработчик кнопки "Мои покупки".

## Функции

### `cmd_start`

**Назначение**: Обрабатывает команду `/start`. Проверяет, зарегистрирован ли пользователь в базе данных. 

**Параметры**:

- `message` (`aiogram.types.Message`): Сообщение от пользователя.
- `session_with_commit` (`sqlalchemy.ext.asyncio.AsyncSession`): Сессия базы данных.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `Exception`: Если возникла ошибка при обработке запроса.

**Как работает**: 

1. Извлекает идентификатор пользователя (`user_id`) из `message.from_user.id`.
2. Ищет пользователя в базе данных по `user_id`.
3. Если пользователь уже существует, отправляет приветственное сообщение с основной клавиатурой (`main_user_kb`).
4. Если пользователь новый, создает запись о нем в базе данных и отправляет сообщение с приветствием и основной клавиатурой.

**Примеры**:

```python
# Сообщение от нового пользователя
>>> message = {'from_user': {'id': 123456789, 'full_name': 'Иван Иванов'}}
>>> cmd_start(message, session_with_commit)
# Сообщение от существующего пользователя
>>> message = {'from_user': {'id': 987654321, 'full_name': 'Петр Петров'}}
>>> cmd_start(message, session_with_commit)
```

### `page_home`

**Назначение**: Обрабатывает кнопку "Главная страница". 

**Параметры**:

- `call` (`aiogram.types.CallbackQuery`): Запрос от пользователя.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `Exception`: Если возникла ошибка при обработке запроса.

**Как работает**: 

1. Отправляет ответ на запрос (`await call.answer`) с текстом "Главная страница".
2. Отправляет сообщение с приветствием и основной клавиатурой (`main_user_kb`).

**Примеры**:

```python
# Запрос от пользователя
>>> call = {'from_user': {'id': 123456789, 'full_name': 'Иван Иванов'}, 'data': 'home'}
>>> page_home(call)
```

### `page_about`

**Назначение**: Обрабатывает кнопку "О магазине". 

**Параметры**:

- `call` (`aiogram.types.CallbackQuery`): Запрос от пользователя.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `Exception`: Если возникла ошибка при обработке запроса.

**Как работает**: 

1. Отправляет ответ на запрос (`await call.answer`) с текстом "О магазине".
2. Отправляет сообщение с информацией о магазине и тестовыми данными для оплаты.

**Примеры**:

```python
# Запрос от пользователя
>>> call = {'from_user': {'id': 123456789, 'full_name': 'Иван Иванов'}, 'data': 'about'}
>>> page_about(call)
```

### `page_my_profile`

**Назначение**: Обрабатывает кнопку "Мой профиль". 

**Параметры**:

- `call` (`aiogram.types.CallbackQuery`): Запрос от пользователя.
- `session_without_commit` (`sqlalchemy.ext.asyncio.AsyncSession`): Сессия базы данных.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `Exception`: Если возникла ошибка при обработке запроса.

**Как работает**: 

1. Отправляет ответ на запрос (`await call.answer`) с текстом "Профиль".
2. Получает статистику покупок пользователя (`purchases`) из базы данных.
3. Формирует сообщение с информацией о профиле и статистикой покупок.
4. Отправляет сообщение с информацией о профиле и клавиатурой с кнопкой "Мои покупки" (`purchases_kb`).

**Примеры**:

```python
# Запрос от пользователя
>>> call = {'from_user': {'id': 123456789, 'full_name': 'Иван Иванов'}, 'data': 'my_profile'}
>>> page_my_profile(call, session_without_commit)
```

### `page_user_purchases`

**Назначение**: Обрабатывает кнопку "Мои покупки". 

**Параметры**:

- `call` (`aiogram.types.CallbackQuery`): Запрос от пользователя.
- `session_without_commit` (`sqlalchemy.ext.asyncio.AsyncSession`): Сессия базы данных.

**Возвращает**: 
- `None`

**Вызывает исключения**: 
- `Exception`: Если возникла ошибка при обработке запроса.

**Как работает**: 

1. Отправляет ответ на запрос (`await call.answer`) с текстом "Мои покупки".
2. Удаляет предыдущее сообщение (`await call.message.delete`).
3. Получает список покупок пользователя (`purchases`) из базы данных.
4. Если список покупок пуст, отправляет сообщение с текстом "У вас пока нет покупок".
5. Если список покупок не пуст, для каждой покупки:
    - Получает информацию о товаре (`product`).
    - Формирует сообщение с информацией о товаре.
    - Отправляет сообщение с информацией о товаре и файлом, если он есть.
6. Отправляет сообщение с текстом "Спасибо за доверие!" и основной клавиатурой.

**Примеры**:

```python
# Запрос от пользователя
>>> call = {'from_user': {'id': 123456789, 'full_name': 'Иван Иванов'}, 'data': 'purchases'}
>>> page_user_purchases(call, session_without_commit)
```

## Параметры класса

- Нет

## Примеры

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Получение информации о веб-элементе по локатору
result = driver.execute_locator(close_banner) 
```