# add column pay id

Добавить столбец pay_id

Revision ID: 1720ca777755
Revises: 1b95d36c8908
Create Date: 2024-12-20 21:59:03.848433

```rst
.. module:: src.endpoints.bots.telegram.digital_market.bot.migration.versions.1720ca777755_add_column_pay_id
```

## Обзор

Модуль представляет собой скрипт миграции Alembic, добавляющий столбец `payment_id` в таблицу `purchases`.

## Подробней

Модуль содержит функции `upgrade` и `downgrade` для выполнения и отката миграции.

## Переменные

*   `revision` (str): ID ревизии (значение: `'1720ca777755'`).
*   `down_revision` (str | None): ID предыдущей ревизии (значение: `'1b95d36c8908'`).
*   `branch_labels` (str | Sequence[str] | None): Метки ветвей (значение: `None`).
*   `depends_on` (str | Sequence[str] | None): Зависимости (значение: `None`).

## Функции

### `upgrade`

```python
def upgrade() -> None:
```

**Назначение**: Выполняет миграцию (добавляет столбец `payment_id` в таблицу `purchases`).

**Как работает функция**:

1.  Проверяет, существует ли уже столбец `payment_id` в таблице `purchases`.
2.  Если столбец не существует, добавляет столбец типа `String` с именем `payment_id` и устанавливает ограничение уникальности.
3.  Если столбец уже существует, выводит сообщение о пропуске добавления.

### `downgrade`

```python
def downgrade() -> None:
```

**Назначение**: Откатывает миграцию (удаляет столбец `payment_id` из таблицы `purchases`).

**Как работает функция**:

1.  Проверяет, существует ли столбец `payment_id` в таблице `purchases`.
2.  Если столбец существует, удаляет ограничение уникальности и столбец `payment_id`.
3.  Если столбец не существует, выводит сообщение о пропуске удаления.