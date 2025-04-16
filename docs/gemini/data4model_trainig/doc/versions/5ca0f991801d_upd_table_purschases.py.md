# upd table purschases

Обновить таблицу purchases

Revision ID: 5ca0f991801d
Revises: 1720ca777755
Create Date: 2024-12-26 13:28:44.493520

```rst
.. module:: src.endpoints.bots.telegram.digital_market.bot.migration.versions.5ca0f991801d_upd_table_purschases
```

## Обзор

Модуль представляет собой скрипт миграции Alembic, добавляющий столбец `payment_type` в таблицу `purchases` и создающий уникальный индекс для столбца `payment_id`.

## Подробней

Модуль содержит функции `upgrade` и `downgrade` для выполнения и отката миграции.

## Переменные

*   `revision` (str): ID ревизии (значение: `'5ca0f991801d'`).
*   `down_revision` (str | None): ID предыдущей ревизии (значение: `'1720ca777755'`).
*   `branch_labels` (str | Sequence[str] | None): Метки ветвей (значение: `None`).
*   `depends_on` (str | Sequence[str] | None): Зависимости (значение: `None`).

## Функции

### `upgrade`

```python
def upgrade() -> None:
```

**Назначение**: Выполняет миграцию (добавляет столбец `payment_type` в таблицу `purchases` и создает уникальный индекс для столбца `payment_id`).

**Как работает функция**:

1.  Добавляет столбец `payment_type` типа `String` в таблицу `purchases` с ограничением `nullable=False`.
2.  Создает уникальный индекс для столбца `payment_id` в таблице `purchases`.

### `downgrade`

```python
def downgrade() -> None:
```

**Назначение**: Откатывает миграцию (удаляет столбец `payment_type` и уникальный индекс для столбца `payment_id` из таблицы `purchases`).

**Как работает функция**:

1.  Удаляет уникальный индекс для столбца `payment_id` из таблицы `purchases`.
2.  Удаляет столбец `payment_type` из таблицы `purchases`.