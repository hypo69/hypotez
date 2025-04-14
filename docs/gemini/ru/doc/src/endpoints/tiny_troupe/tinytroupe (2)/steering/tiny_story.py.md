# Модуль `tiny_story.py`

## Обзор

Модуль `tiny_story.py` предназначен для создания и управления историями, сгенерированными на основе симуляций в TinyTroupe. Он предоставляет механизмы для формирования связных и интересных повествований, основанных на взаимодействиях агентов или изменениях в окружающей среде.

## Подробней

Модуль содержит класс `TinyStory`, который позволяет задавать цели истории, контекст, а также включать информацию об окружении или агентах. Он использует шаблоны для генерации текста с помощью языковой модели (LLM) и предоставляет методы для начала и продолжения истории. Этот код важен для создания динамических и контекстно-зависимых историй, которые отражают ход симуляции.

## Классы

### `TinyStory`

**Описание**: Класс `TinyStory` предоставляет функциональность для создания и управления историями, основанными на симуляциях в TinyTroupe.

**Атрибуты**:
- `environment` (TinyWorld, optional): Окружение, в котором происходит история. По умолчанию `None`.
- `agent` (TinyPerson, optional): Агент, являющийся главным героем истории. По умолчанию `None`.
- `purpose` (str, optional): Цель истории. По умолчанию `"Be a realistic simulation."`.
- `current_story` (str): Текущий контекст истории.
- `first_n` (int): Количество первых взаимодействий, включаемых в историю. По умолчанию `10`.
- `last_n` (int): Количество последних взаимодействий, включаемых в историю. По умолчанию `20`.
- `include_omission_info` (bool): Флаг, указывающий, следует ли включать информацию об опущенных взаимодействиях. По умолчанию `True`.

**Принцип работы**:
Класс инициализируется с окружением или агентом (но не одновременно). Он хранит контекст истории и использует методы для генерации новых фрагментов истории на основе текущего состояния симуляции. Методы `start_story` и `continue_story` используют языковую модель для создания текста, который добавляется к текущей истории.

**Методы**:
- `__init__`: Инициализирует объект истории.
- `start_story`: Начинает новую историю.
- `continue_story`: Предлагает продолжение истории.
- `_current_story`: Возвращает текущую историю.

## Методы класса

### `__init__`

```python
def __init__(self, environment:TinyWorld=None, agent:TinyPerson=None, purpose:str="Be a realistic simulation.", context:str="",
                 first_n=10, last_n=20, include_omission_info:bool=True) -> None:
    """
    Инициализирует объект истории.

    Args:
        environment (TinyWorld, optional): Окружение, в котором происходит история. По умолчанию `None`.
        agent (TinyPerson, optional): Агент, являющийся главным героем истории. По умолчанию `None`.
        purpose (str, optional): Цель истории. По умолчанию "Be a realistic simulation.".
        context (str, optional): Начальный контекст истории. По умолчанию "".
        first_n (int, optional): Количество первых взаимодействий, включаемых в историю. По умолчанию 10.
        last_n (int, optional): Количество последних взаимодействий, включаемых в историю. По умолчанию 20.
        include_omission_info (bool, optional): Флаг, указывающий, следует ли включать информацию об опущенных взаимодействиях. По умолчанию True.

    Raises:
        Exception: Если одновременно переданы и `environment`, и `agent`, или если ни один из них не передан.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `TinyStory`. Устанавливает окружение, агента, цель истории, начальный контекст, количество первых и последних взаимодействий, а также флаг включения информации об опущенных взаимодействиях.

**Как работает функция**:
Функция проверяет, что передан либо агент, либо окружение, но не оба одновременно. Если условия не соблюдены, вызывается исключение. Затем она сохраняет переданные параметры в атрибуты экземпляра класса.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Пример инициализации с окружением
env = TinyWorld()
story = TinyStory(environment=env, purpose="Тест окружения")

# Пример инициализации с агентом
agent = TinyPerson()
story = TinyStory(agent=agent, purpose="Тест агента")
```

### `start_story`

```python
def start_story(self, requirements="Start some interesting story about the agents.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
    """
    Начинает новую историю.

    Args:
        requirements (str, optional): Требования к началу истории. По умолчанию "Start some interesting story about the agents.".
        number_of_words (int, optional): Количество слов в начале истории. По умолчанию 100.
        include_plot_twist (bool, optional): Флаг, указывающий, следует ли включать неожиданный поворот сюжета. По умолчанию False.

    Returns:
        str: Начало истории.
    """
    ...
```

**Назначение**: Генерирует начало истории на основе предоставленных требований и текущего контекста симуляции.

**Как работает функция**:
Функция создает словарь `rendering_configs` с параметрами, необходимыми для генерации истории. Затем она использует функцию `utils.compose_initial_LLM_messages_with_templates` для создания сообщений для языковой модели. После этого она отправляет сообщения в языковую модель с помощью `openai_utils.client().send_message` и получает сгенерированный текст. Текст добавляется к текущей истории и возвращается.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

env = TinyWorld()
story = TinyStory(environment=env, purpose="Интересная история")

# Пример начала истории
start = story.start_story(requirements="Начни с описания окружения", number_of_words=150)
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
        include_plot_twist (bool, optional): Флаг, указывающий, следует ли включать неожиданный поворот сюжета. По умолчанию False.

    Returns:
        str: Продолжение истории.
    """
    ...
```

**Назначение**: Генерирует продолжение истории на основе предоставленных требований и текущего контекста симуляции.

**Как работает функция**:
Функция аналогична `start_story`, но использует другие шаблоны сообщений для языковой модели (`story.continuation.system.mustache` и `story.continuation.user.mustache`). Она создает словарь `rendering_configs` с параметрами, необходимыми для генерации продолжения истории. Затем она использует функцию `utils.compose_initial_LLM_messages_with_templates` для создания сообщений для языковой модели. После этого она отправляет сообщения в языковую модель с помощью `openai_utils.client().send_message` и получает сгенерированный текст. Текст добавляется к текущей истории и возвращается.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

env = TinyWorld()
story = TinyStory(environment=env, purpose="Интересная история")
story.start_story(requirements="Начни с описания окружения", number_of_words=150)

# Пример продолжения истории
continuation = story.continue_story(requirements="Добавь взаимодействие агентов", number_of_words=120)
print(continuation)
```

### `_current_story`

```python
def _current_story(self) -> str:
    """
    Получает текущую историю.

    Returns:
        str: Текущая история.
    """
    ...
```

**Назначение**: Возвращает текущую историю с добавлением информации о последних взаимодействиях агента или изменениях в окружающей среде.

**Как работает функция**:
Функция получает историю взаимодействий агента или окружения с помощью методов `pretty_current_interactions` и добавляет эту историю к текущей истории. Возвращает обновленную историю.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

env = TinyWorld()
story = TinyStory(environment=env, purpose="Интересная история")

# Пример получения текущей истории
current_story = story._current_story()
print(current_story)
```

## Параметры класса

- `environment` (TinyWorld, optional): Окружение, в котором происходит история. По умолчанию `None`.
- `agent` (TinyPerson, optional): Агент, являющийся главным героем истории. По умолчанию `None`.
- `purpose` (str, optional): Цель истории. По умолчанию `"Be a realistic simulation."`.
- `context` (str, optional): Начальный контекст истории. По умолчанию `""`.
- `first_n` (int, optional): Количество первых взаимодействий, включаемых в историю. По умолчанию `10`.
- `last_n` (int, optional): Количество последних взаимодействий, включаемых в историю. По умолчанию `20`.
- `include_omission_info` (bool, optional): Флаг, указывающий, следует ли включать информацию об опущенных взаимодействиях. По умолчанию `True`.

## Примеры

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Пример инициализации с окружением
env = TinyWorld()
story = TinyStory(environment=env, purpose="Тест окружения")
start = story.start_story(requirements="Начни с описания окружения", number_of_words=150)
continuation = story.continue_story(requirements="Добавь взаимодействие агентов", number_of_words=120)
current_story = story._current_story()
print(current_story)

# Пример инициализации с агентом
agent = TinyPerson()
story = TinyStory(agent=agent, purpose="Тест агента")
start = story.start_story(requirements="Начни с описания агента", number_of_words=150)
continuation = story.continue_story(requirements="Добавь действия агента", number_of_words=120)
current_story = story._current_story()
print(current_story)