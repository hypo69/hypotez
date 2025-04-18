# Модуль миграции базы данных: добавление колонки `pay_id`

## Обзор

Модуль предназначен для миграции базы данных, добавляя колонку `payment_id` в таблицу `purchases`, если она еще не существует. Также создается уникальный индекс для этой колонки. Модуль использует библиотеку `alembic` для управления миграциями базы данных.

## Подробней

Этот код используется для автоматического изменения структуры базы данных при обновлении версии программного обеспечения. Он гарантирует, что необходимые изменения в схеме базы данных будут внесены автоматически и безопасно.

## Переменные модуля

- `revision` (str): Идентификатор текущей ревизии миграции.
- `down_revision` (Union[str, None]): Идентификатор предыдущей ревизии миграции.
- `branch_labels` (Union[str, Sequence[str], None]): Метки ветвей.
- `depends_on` (Union[str, Sequence[str], None]): Зависимости от других миграций.

## Функции

### `upgrade`

**Назначение**: Добавляет колонку `payment_id` в таблицу `purchases`, если она еще не существует.

**Параметры**:
- Нет

**Возвращает**:
- `None`

**Как работает функция**:

1.  Получает соединение с базой данных с использованием `op.get_bind()`.
2.  Проверяет, существует ли колонка `payment_id` в таблице `purchases` с помощью запроса `PRAGMA table_info('purchases')`.
3.  Если колонка не существует, добавляет ее с помощью `op.add_column()`, устанавливая тип данных `String` и `nullable=False`.
4.  Создает уникальный индекс `uq_purchases_payment_id` для колонки `payment_id` с помощью `op.create_unique_constraint()`.
5.  Если колонка уже существует, выводит сообщение в консоль.

**Примеры**:

```python
# Пример вызова функции upgrade (обычно вызывается alembic)
upgrade()
```

### `downgrade`

**Назначение**: Удаляет колонку `payment_id` из таблицы `purchases`, если она существует.

**Параметры**:
- Нет

**Возвращает**:
- `None`

**Как работает функция**:

1.  Получает соединение с базой данных с использованием `op.get_bind()`.
2.  Проверяет, существует ли колонка `payment_id` в таблице `purchases` с помощью запроса `PRAGMA table_info('purchases')`.
3.  Если колонка существует, удаляет уникальный индекс `uq_purchases_payment_id` с помощью `op.drop_constraint()`.
4.  Удаляет колонку `payment_id` с помощью `op.drop_column()`.
5.  Если колонка не существует, выводит сообщение в консоль.

**Примеры**:

```python
# Пример вызова функции downgrade (обычно вызывается alembic)
downgrade()