# Initial revision

Начальная редакция

Revision ID: 47f559ec82bb
Revises:
Create Date: 2024-12-20 10:56:04.228993

```rst
.. module:: src.endpoints.bots.telegram.digital_market.bot.migration.versions.47f559ec82bb_initial_revision
```

## Обзор

Модуль представляет собой скрипт начальной миграции Alembic, который не выполняет никаких действий.

## Подробней

Модуль содержит пустые функции `upgrade` и `downgrade`, что означает, что он не вносит никаких изменений в схему базы данных.

## Переменные

*   `revision` (str): ID ревизии (значение: `'47f559ec82bb'`).
*   `down_revision` (str | None): ID предыдущей ревизии (значение: `None`).
*   `branch_labels` (str | Sequence[str] | None): Метки ветвей (значение: `None`).
*   `depends_on` (str | Sequence[str] | None): Зависимости (значение: `None`).

## Функции

### `upgrade`

```python
def upgrade() -> None:
```

**Назначение**: Выполняет миграцию (в данном случае не выполняет никаких действий).

**Как работает функция**:

1.  Не выполняет никаких действий (`pass`).

### `downgrade`

```python
def downgrade() -> None:
```

**Назначение**: Откатывает миграцию (в данном случае не выполняет никаких действий).

**Как работает функция**:

1.  Не выполняет никаких действий (`pass`).