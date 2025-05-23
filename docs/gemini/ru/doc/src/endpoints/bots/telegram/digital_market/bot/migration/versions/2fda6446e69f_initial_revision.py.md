# Модуль миграции базы данных для телеграм бота
## Обзор
Этот модуль содержит скрипт миграции для базы данных телеграм бота. Миграция создает таблицы для пользователей, категорий товаров, товаров, покупок.

## Подробней
Этот файл представляет собой скрипт миграции для базы данных телеграм бота, который используется для создания таблиц в базе данных, необходимых для работы бота. 

## Классы

## Функции

### `upgrade`
**Назначение**: Функция, которая выполняет миграцию базы данных. 
**Параметры**: 
- Нет параметров. 
**Возвращает**: 
- Нет возвращаемого значения. 
**Вызывает исключения**: 
- Нет исключений.

**Как работает функция**:
- Функция `upgrade` создает таблицы `categories`, `users`, `products`, `purchases`.
- Таблицы имеют следующие столбцы:
    - **categories**:
        - `category_name`: Текстовое поле для названия категории.
        - `id`: Целочисленный идентификатор категории (автоинкремент).
        - `created_at`: Дата и время создания категории.
        - `updated_at`: Дата и время последнего обновления категории.
    - **users**:
        - `telegram_id`: Целочисленный идентификатор пользователя телеграм.
        - `username`: Текстовое поле для имени пользователя.
        - `first_name`: Текстовое поле для имени пользователя.
        - `last_name`: Текстовое поле для фамилии пользователя.
        - `id`: Целочисленный идентификатор пользователя (автоинкремент).
        - `created_at`: Дата и время создания пользователя.
        - `updated_at`: Дата и время последнего обновления пользователя.
    - **products**:
        - `name`: Текстовое поле для названия товара.
        - `description`: Текстовое поле для описания товара.
        - `price`: Целочисленный столбец для цены товара.
        - `file_id`: Текстовое поле для идентификатора файла товара.
        - `category_id`: Целочисленный столбец для идентификатора категории товара.
        - `id`: Целочисленный идентификатор товара (автоинкремент).
        - `created_at`: Дата и время создания товара.
        - `updated_at`: Дата и время последнего обновления товара.
    - **purchases**:
        - `user_id`: Целочисленный столбец для идентификатора пользователя.
        - `product_id`: Целочисленный столбец для идентификатора товара.
        - `price`: Целочисленный столбец для цены покупки.
        - `id`: Целочисленный идентификатор покупки (автоинкремент).
        - `created_at`: Дата и время создания покупки.
        - `updated_at`: Дата и время последнего обновления покупки.
- Таблицы `products`, `purchases` связаны с таблицей `categories` и `users` с помощью внешних ключей `category_id` и `user_id` соответственно.
- Функция использует библиотеку `alembic` для создания таблиц.

**Примеры**:
```python
# Выполнение миграции
upgrade()
```
### `downgrade`
**Назначение**: Функция, которая откатывает миграцию базы данных. 
**Параметры**: 
- Нет параметров. 
**Возвращает**: 
- Нет возвращаемого значения. 
**Вызывает исключения**: 
- Нет исключений.

**Как работает функция**:
- Функция `downgrade` удаляет таблицы `purchases`, `products`, `users`, `categories` в обратном порядке их создания.
- Функция использует библиотеку `alembic` для удаления таблиц.

**Примеры**:
```python
# Откат миграции
downgrade()
```
## Параметры класса

## Примеры 

```python
# Выполнить миграцию
upgrade()
# Откатить миграцию
downgrade()
```