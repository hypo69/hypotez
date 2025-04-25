# Модуль `tiny_person.py`

## Обзор

Этот модуль содержит класс `TinyPerson`, который представляет собой агента, способного взаимодействовать с пользователем. 

## Подробей

Модуль `tiny_person.py` реализует агента `TinyPerson` с помощью библиотеки `tinytroupe`. 

`TinyPerson` - это класс, который представляет собой простого агента, который может взаимодействовать с пользователем. 

## Классы

### `TinyPerson`

**Описание**:  Класс `TinyPerson` представляет собой агента, способного взаимодействовать с пользователем, отвечая на заданные вопросы, запоминая информацию и реагируя на действия.

**Атрибуты**:

- `name` (str): Имя агента.
- `age` (int):  Возраст агента (по умолчанию `None`).
- `occupation` (str):  Профессия агента (по умолчанию `None`).
- `nationality` (str):  Национальность агента (по умолчанию `None`).
- `skills` (list):  Список навыков агента (по умолчанию `None`).
- `current_interactions` (list):  Список последних взаимодействий агента с пользователем (по умолчанию `None`).

**Методы**:

- `define(key, value)`:  Устанавливает или обновляет характеристику агента, задавая ключ `key` и значение `value`.
- `listen(user_input)`:  Добавляет входящее сообщение пользователя `user_input` к списку последних взаимодействий.
- `act()`:  Реагирует на последнее сообщение пользователя в зависимости от заданных характеристик. 
- `pp_current_interactions()`:  Выводит список последних взаимодействий агента с пользователем в удобочитаемом формате. 


**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Создаем инстанс TinyPerson
john = TinyPerson(name="John")

# Определяем некоторые характеристики
john.define("age", 35)
john.define("occupation", "Software Engineer")
john.define("nationality", "American")
john.define("skills", [{"skill": "Coding in python"}])

# Взаимодействуем с агентом
john.listen("Hello, John! How are you today?")
john.act()
john.pp_current_interactions()

```

## Методы класса

### `define`

```python
def define(self, key: str, value: Any):
    """
    Устанавливает или обновляет характеристику агента.

    Args:
        key (str): Ключ для характеристики (например, 'age', 'occupation').
        value (Any): Значение характеристики.

    Returns:
        None
    """
```

### `listen`

```python
def listen(self, user_input: str):
    """
    Добавляет входящее сообщение пользователя к списку последних взаимодействий.

    Args:
        user_input (str): Сообщение пользователя.

    Returns:
        None
    """
```

### `act`

```python
def act(self):
    """
    Реагирует на последнее сообщение пользователя. 

    Returns:
        None
    """
```

### `pp_current_interactions`

```python
def pp_current_interactions(self):
    """
    Выводит список последних взаимодействий агента с пользователем в удобочитаемом формате.

    Returns:
        None
    """
```

## Параметры класса

- `name` (str): Имя агента.
- `age` (int):  Возраст агента (по умолчанию `None`).
- `occupation` (str):  Профессия агента (по умолчанию `None`).
- `nationality` (str):  Национальность агента (по умолчанию `None`).
- `skills` (list):  Список навыков агента (по умолчанию `None`).
- `current_interactions` (list):  Список последних взаимодействий агента с пользователем (по умолчанию `None`).

## Примеры

```python
from tinytroupe.agent import TinyPerson

# Создаем инстанс TinyPerson
john = TinyPerson(name="John")

# Определяем некоторые характеристики
john.define("age", 35)
john.define("occupation", "Software Engineer")
john.define("nationality", "American")
john.define("skills", [{"skill": "Coding in python"}])

# Взаимодействуем с агентом
john.listen("Hello, John! How are you today?")
john.act()
john.pp_current_interactions()