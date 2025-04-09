# Модуль `tiny_story.py`

## Обзор

Модуль `tiny_story.py` предоставляет класс `TinyStory`, который помогает создавать истории для симуляций в TinyTroupe. Этот класс облегчает создание историй, связанных с окружением или агентами, и позволяет задавать цели для генерации истории.

## Подробней

Модуль содержит класс `TinyStory`, который используется для создания и развития историй в контексте симуляций TinyTroupe. Истории могут быть сфокусированы на окружении или на отдельных агентах. Класс предоставляет методы для начала истории, её продолжения и получения текущего состояния истории, основываясь на взаимодействиях в симуляции.

## Классы

### `TinyStory`

**Описание**: Класс `TinyStory` предоставляет механизмы для создания историй в TinyTroupe.

**Атрибуты**:
- `environment` (TinyWorld): Окружение, в котором происходит история.
- `agent` (TinyPerson): Агент, о котором рассказывается история.
- `purpose` (str): Цель истории.
- `current_story` (str): Текущий контекст истории.
- `first_n` (int): Количество первых взаимодействий для включения в историю.
- `last_n` (int): Количество последних взаимодействий для включения в историю.
- `include_omission_info` (bool): Флаг, указывающий, следует ли включать информацию об опущенных взаимодействиях.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `TinyStory`.
- `start_story`: Начинает новую историю.
- `continue_story`: Предлагает продолжение истории.
- `_current_story`: Возвращает текущую историю.

### `__init__`

```python
def __init__(self, environment:TinyWorld=None, agent:TinyPerson=None, purpose:str="Be a realistic simulation.", context:str="",
                 first_n=10, last_n=20, include_omission_info:bool=True) -> None:
    """
    Инициализирует экземпляр класса `TinyStory`.

    Args:
        environment (TinyWorld, optional): Окружение, в котором происходит история. По умолчанию `None`.
        agent (TinyPerson, optional): Агент, о котором рассказывается история. По умолчанию `None`.
        purpose (str, optional): Цель истории. По умолчанию "Be a realistic simulation.".
        context (str, optional): Текущий контекст истории. По умолчанию "".
        first_n (int, optional): Количество первых взаимодействий для включения в историю. По умолчанию 10.
        last_n (int, optional): Количество последних взаимодействий для включения в историю. По умолчанию 20.
        include_omission_info (bool, optional): Флаг, указывающий, следует ли включать информацию об опущенных взаимодействиях. По умолчанию `True`.

    Raises:
        Exception: Если предоставлены и `environment`, и `agent` одновременно.
        Exception: Если не предоставлен ни `environment`, ни `agent`.
    """
```

**Как работает функция**:
Функция инициализирует объект `TinyStory`, устанавливая параметры окружения, агента, цели истории, контекста, количества первых и последних взаимодействий, а также флаг включения информации об опущенных взаимодействиях. Проверяется, что предоставлен либо агент, либо окружение, но не оба сразу.

### `start_story`

```python
def start_story(self, requirements="Start some interesting story about the agents.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
    """
    Начинает новую историю.

    Args:
        requirements (str, optional): Требования к началу истории. По умолчанию "Start some interesting story about the agents.".
        number_of_words (int, optional): Количество слов в начале истории. По умолчанию 100.
        include_plot_twist (bool, optional): Флаг, указывающий, следует ли включать сюжетный поворот. По умолчанию `False`.

    Returns:
        str: Начало истории.
    """
```

**Как работает функция**:
Функция `start_story` генерирует начало истории, используя предоставленные требования, количество слов и флаг сюжетного поворота. Она использует шаблоны сообщений для составления запроса к языковой модели и добавляет сгенерированное начало истории к текущему контексту истории.

**Примеры**:
```python
story = TinyStory(agent=some_agent)
start = story.start_story(requirements="Начни историю о том, как агент исследует мир.", number_of_words=150)
print(start)
```

### `continue_story`

```python
def continue_story(self, requirements="Continue the story in an interesting way.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
    """
    Предлагает продолжение истории.

    Args:
        requirements (str, optional): Требования к продолжению истории. По умолчанию "Continue the story in an interesting way.".
        number_of_words (int, optional): Количество слов в продолжении истории. По умолчанию 100.
        include_plot_twist (bool, optional): Флаг, указывающий, следует ли включать сюжетный поворот. По умолчанию `False`.

    Returns:
        str: Продолжение истории.
    """
```

**Как работает функция**:
Функция `continue_story` генерирует продолжение истории, используя предоставленные требования, количество слов и флаг сюжетного поворота. Она использует шаблоны сообщений для составления запроса к языковой модели и добавляет сгенерированное продолжение истории к текущему контексту истории.

**Примеры**:
```python
story = TinyStory(agent=some_agent, context="История началась с того, что...")
continuation = story.continue_story(requirements="Продолжи историю, добавив конфликт.", number_of_words=120)
print(continuation)
```

### `_current_story`

```python
def _current_story(self) -> str:
    """
    Возвращает текущую историю.

    Returns:
        str: Текущая история.
    """
```

**Как работает функция**:
Функция `_current_story` возвращает текущую историю, добавляя информацию о взаимодействиях агента или окружения в зависимости от того, что было предоставлено при инициализации класса. Информация о взаимодействиях форматируется с использованием метода `pretty_current_interactions` класса `TinyPerson` или `TinyWorld`.

**Примеры**:
```python
story = TinyStory(agent=some_agent)
current = story._current_story()
print(current)
```
```python
story = TinyStory(environment=some_environment)
current = story._current_story()
print(current)