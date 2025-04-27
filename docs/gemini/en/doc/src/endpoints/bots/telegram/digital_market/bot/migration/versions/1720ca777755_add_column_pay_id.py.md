# Модуль миграции базы данных
## Обзор

Данный модуль представляет собой миграцию базы данных для проекта `hypotez`, которая добавляет колонку `payment_id` в таблицу `purchases`. 

## Детали

Миграция `1720ca777755_add_column_pay_id.py` предназначена для обновления базы данных `hypotez`. Она добавляет колонку `payment_id` в таблицу `purchases`, что может быть необходимо для хранения информации о платежах или идентификаторах транзакций. 

## Функции

### `upgrade()`

**Описание**: Функция обновляет схему базы данных, добавляя колонку `payment_id` в таблицу `purchases`. Если колонка уже существует, функция выводит сообщение и пропускает добавление.

**Параметры**: Нет

**Возвращает**: Нет

**Пример**:

```python
def upgrade() -> None:
    # Проверяем, существует ли колонка перед добавлением
    conn = op.get_bind()
    result = conn.execute(
        sa.text("PRAGMA table_info('purchases')")
    )
    columns = [row[1] for row in result]  # Индекс 1 — это имя колонки в результатах PRAGMA
    if 'payment_id' not in columns:
        op.add_column('purchases', sa.Column('payment_id', sa.String(), nullable=False))
        op.create_unique_constraint('uq_purchases_payment_id', 'purchases', ['payment_id'])
    else:
        print("Колонка 'payment_id' уже существует, пропускаем добавление")
```

### `downgrade()`

**Описание**: Функция отменяет изменения, внесенные функцией `upgrade()`, удаляя колонку `payment_id` из таблицы `purchases`. Если колонка не существует, функция выводит сообщение и пропускает удаление.

**Параметры**: Нет

**Возвращает**: Нет

**Пример**:

```python
def downgrade() -> None:
    # Проверяем, существует ли колонка перед удалением
    conn = op.get_bind()
    result = conn.execute(
        sa.text("PRAGMA table_info('purchases')")
    )
    columns = [row[1] for row in result]  # Индекс 1 — это имя колонки в результатах PRAGMA
    if 'payment_id' in columns:
        op.drop_constraint('uq_purchases_payment_id', 'purchases', type_='unique')
        op.drop_column('purchases', 'payment_id')
    else:
        print("Колонка 'payment_id' не существует, пропускаем удаление")
```

## Примечания

- Миграция использует библиотеку `alembic` для управления изменениями схемы базы данных. 
- Функции `upgrade()` и `downgrade()` обеспечивают возможность отмены изменений, что важно для управления версиями базы данных. 
- Миграция проверяет наличие колонки `payment_id` перед ее добавлением или удалением, чтобы избежать ошибок.
- `op` - это объект из библиотеки `alembic`, который предоставляет методы для изменения схемы базы данных.
- `sa.text()` - это функция из библиотеки `sqlalchemy`, которая позволяет выполнять SQL-запросы.
- `conn.execute()` - это метод объекта соединения, который выполняет SQL-запрос. 
- `sa.Column()` - это класс из библиотеки `sqlalchemy`, который создает описание колонки для таблицы. 
- `sa.String()` - это тип данных для хранения текстовых значений. 
- `nullable=False` - определяет, что колонка не может содержать значение `NULL`.
- `op.create_unique_constraint()` - создает уникальный индекс для колонки `payment_id`.
- `op.drop_constraint()` - удаляет уникальный индекс. 
- `op.drop_column()` - удаляет колонку из таблицы.