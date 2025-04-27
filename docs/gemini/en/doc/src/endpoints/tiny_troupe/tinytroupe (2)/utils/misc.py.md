# Модуль `misc`

## Обзор

Этот модуль содержит набор вспомогательных функций, используемых в проекте `TinyTroupe`. Функции предоставляют возможности для работы с именами агентов и сред, генерации хэшей, получения уникальных идентификаторов и т.д.

## Детали

Этот модуль используется для предоставления вспомогательных функций, которые облегчают разработку логики TinyTroupe. Функции, описанные в этом модуле, используются для выполнения таких задач, как:

- Получение имени агента или среды.
- Генерация уникального хэша для объекта.
- Создание уникальных идентификаторов для объектов.
- Сброс счетчика уникальных идентификаторов.

## Функции

### `name_or_empty`

**Purpose**: Возвращает имя заданного агента или среды, или пустую строку, если агент равен `None`.

**Parameters**:
- `named_entity` (AgentOrWorld): Агент или среда, для которого необходимо получить имя.

**Returns**:
- `str`: Имя агента или среды, или пустая строка, если агент равен `None`.

**Examples**:

```python
>>> from hypotez.src.endpoints.tiny_troupe.tinytroupe (2).utils.misc import name_or_empty
>>> from hypotez.src.endpoints.tiny_troupe.tinytroupe (2).utils.misc import AgentOrWorld
>>> from hypotez.src.endpoints.tiny_troupe.tinytroupe (2).models.tiny_agent import TinyPerson
>>> agent = TinyPerson(name='Alice')
>>> name_or_empty(agent)
'Alice'
>>> name_or_empty(None)
''
```

### `custom_hash`

**Purpose**: Возвращает хэш для заданного объекта. Объект сначала преобразуется в строку, чтобы сделать его хешируемым. Этот метод детерминированный, в отличие от встроенной функции `hash()`.

**Parameters**:
- `obj`: Объект, для которого необходимо получить хэш.

**Returns**:
- `str`: Хэш объекта.

**Examples**:

```python
>>> from hypotez.src.endpoints.tiny_troupe.tinytroupe (2).utils.misc import custom_hash
>>> custom_hash('Hello, world!')
'3e23e8160039594a33894f6564e1b1348a65a581d4e7d7ccfb798275387d53f7'
>>> custom_hash({'name': 'Alice', 'age': 30})
'8a3c09765f40a3903a42d79730f81d0c2e294833d809e36e7824d79670515502'
```

### `fresh_id`

**Purpose**: Возвращает свежий ID для нового объекта. Это полезно для генерации уникальных идентификаторов для объектов.

**Parameters**:
- None

**Returns**:
- `int`: Свежий ID.

**Examples**:

```python
>>> from hypotez.src.endpoints.tiny_troupe.tinytroupe (2).utils.misc import fresh_id
>>> fresh_id()
1
>>> fresh_id()
2
>>> fresh_id()
3
```

### `reset_fresh_id`

**Purpose**: Сбрасывает счетчик свежих ID. Это полезно для целей тестирования.

**Parameters**:
- None

**Returns**:
- None

**Examples**:

```python
>>> from hypotez.src.endpoints.tiny_troupe.tinytroupe (2).utils.misc import fresh_id
>>> from hypotez.src.endpoints.tiny_troupe.tinytroupe (2).utils.misc import reset_fresh_id
>>> fresh_id()
1
>>> fresh_id()
2
>>> reset_fresh_id()
>>> fresh_id()
1
```