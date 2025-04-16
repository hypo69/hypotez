# add hidden content

Добавить скрытый контент

Revision ID: 1b95d36c8908
Revises: 2fda6446e69f
Create Date: 2024-12-20 14:47:07.064138

```rst
.. module:: src.endpoints.bots.telegram.digital_market.bot.migration.versions.1b95d36c8908_add_hidden_content
```

## Обзор

Модуль представляет собой скрипт миграции Alembic, добавляющий столбец `hidden_content` в таблицу `products`.

## Подробней

Модуль содержит функции `upgrade` и `downgrade` для выполнения и отката миграции.

## Переменные

*   `revision` (str): ID ревизии (значение: `'1b95d36c8908'`).
*   `down_revision` (str | None): ID предыдущей ревизии (значение: `'2fda6446e69f'`).
*   `branch_labels` (str | Sequence[str] | None): Метки ветвей (значение: `None`).
*   `depends_on` (str | Sequence[str] | None): Зависимости (значение: `None`).

## Функции

### `upgrade`

```python
def upgrade() -> None:
```

**Назначение**: Выполняет миграцию (добавляет столбец `hidden_content` в таблицу `products`).

**Как работает функция**:

1.  Добавляет столбец `hidden_content` типа `Text` в таблицу `products` с ограничением `nullable=False`.

### `downgrade`

```python
def downgrade() -> None:
```

**Назначение**: Откатывает миграцию (удаляет столбец `hidden_content` из таблицы `products`).

**Как работает функция**:

1.  Удаляет столбец `hidden_content` из таблицы `products`.