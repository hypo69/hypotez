# Модуль `tiny_story.py`

## Обзор

Модуль `tiny_story.py` предназначен для создания и управления историями в контексте симуляций TinyTroupe. Он предоставляет класс `TinyStory`, который помогает создавать истории на основе окружения или агента, участвующего в симуляции.

## Подробнее

Модуль предоставляет инструменты для генерации историй с использованием AI-моделей, таких как OpenAI. Он позволяет задавать цель истории, добавлять контекст, определять количество взаимодействий, включаемых в историю, и управлять её развитием.

## Классы

### `TinyStory`

**Описание**: Класс для создания и управления историями в симуляциях TinyTroupe.

**Атрибуты**:
- `environment` (TinyWorld, optional): Окружение, в котором происходит история. По умолчанию `None`.
- `agent` (TinyPerson, optional): Агент, являющийся главным героем истории. По умолчанию `None`.
- `purpose` (str): Цель истории. Используется для направления генерации истории. По умолчанию "Be a realistic simulation.".
- `current_story` (str): Текущий контекст истории.
- `first_n` (int): Количество первых взаимодействий, включаемых в историю. По умолчанию 10.
- `last_n` (int): Количество последних взаимодействий, включаемых в историю. По умолчанию 20.
- `include_omission_info` (bool): Флаг, указывающий, следует ли включать информацию об опущенных взаимодействиях. По умолчанию `True`.

**Методы**:
- `__init__`: Инициализирует объект истории.
- `start_story`: Начинает новую историю.
- `continue_story`: Предлагает продолжение истории.
- `_current_story`: Возвращает текущую историю.

### `__init__`

```python
def __init__(self, environment: TinyWorld = None, agent: TinyPerson = None, purpose: str = "Be a realistic simulation.", context: str = "",
                 first_n=10, last_n=20, include_omission_info: bool = True) -> None:
    """
    Инициализирует объект истории.

    Args:
        environment (TinyWorld, optional): Окружение, в котором происходит история. По умолчанию None.
        agent (TinyPerson, optional): Агент, являющийся главным героем истории. По умолчанию None.
        purpose (str, optional): Цель истории. Используется для направления генерации истории. По умолчанию "Be a realistic simulation.".
        context (str, optional): Текущий контекст истории. По умолчанию "". Новая история будет добавлена к этому контексту.
        first_n (int, optional): Количество первых взаимодействий, включаемых в историю. По умолчанию 10.
        last_n (int, optional): Количество последних взаимодействий, включаемых в историю. По умолчанию 20.
        include_omission_info (bool, optional): Флаг, указывающий, следует ли включать информацию об опущенных взаимодействиях. По умолчанию True.

    Raises:
        Exception: Если переданы одновременно и environment, и agent, или если не передан ни один из них.
    """
```

**Как работает функция**:
- Функция инициализирует объект `TinyStory`.
- Проверяет, что передан либо `environment`, либо `agent`, но не оба одновременно.
- Сохраняет переданные параметры в атрибутах объекта.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Пример инициализации с окружением
environment = TinyWorld()
story = TinyStory(environment=environment)

# Пример инициализации с агентом
agent = TinyPerson()
story = TinyStory(agent=agent)
```

### `start_story`

```python
def start_story(self, requirements="Start some interesting story about the agents.", number_of_words: int = 100, include_plot_twist: bool = False) -> str:
    """
    Начинает новую историю.

    Args:
        requirements (str, optional): Требования к началу истории. По умолчанию "Start some interesting story about the agents.".
        number_of_words (int, optional): Количество слов в сгенерированном начале истории. По умолчанию 100.
        include_plot_twist (bool, optional): Флаг, указывающий, следует ли включать сюжетный поворот. По умолчанию False.

    Returns:
        str: Начало истории.
    """
```

**Как работает функция**:
- Функция начинает новую историю, генерируя текст с использованием AI-модели.
- Формирует конфигурацию для генерации истории, включая цель, требования, текущий контекст, количество слов и необходимость сюжетного поворота.
- Компонует сообщения для AI-модели, используя шаблоны "story.start.system.mustache" и "story.start.user.mustache".
- Отправляет сообщение AI-модели и получает ответ с началом истории.
- Добавляет начало истории к текущему контексту истории.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Пример начала истории
environment = TinyWorld()
story = TinyStory(environment=environment)
start = story.start_story()
print(start)
```

### `continue_story`

```python
def continue_story(self, requirements="Continue the story in an interesting way.", number_of_words: int = 100, include_plot_twist: bool = False) -> str:
    """
    Предлагает продолжение истории.

    Args:
        requirements (str, optional): Требования к продолжению истории. По умолчанию "Continue the story in an interesting way.".
        number_of_words (int, optional): Количество слов в сгенерированном продолжении истории. По умолчанию 100.
        include_plot_twist (bool, optional): Флаг, указывающий, следует ли включать сюжетный поворот. По умолчанию False.

    Returns:
        str: Продолжение истории.
    """
```

**Как работает функция**:
- Функция предлагает продолжение истории, генерируя текст с использованием AI-модели.
- Формирует конфигурацию для генерации истории, включая цель, требования, текущий контекст, количество слов и необходимость сюжетного поворота.
- Компонует сообщения для AI-модели, используя шаблоны "story.continuation.system.mustache" и "story.continuation.user.mustache".
- Отправляет сообщение AI-модели и получает ответ с продолжением истории.
- Добавляет продолжение истории к текущему контексту истории.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Пример продолжения истории
agent = TinyPerson()
story = TinyStory(agent=agent)
story.start_story()
continuation = story.continue_story()
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
- Функция возвращает текущую историю, включая информацию о взаимодействиях агента или окружения.
- Получает историю взаимодействий агента или окружения.
- Добавляет историю взаимодействий к текущему контексту истории.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld

# Пример получения текущей истории
environment = TinyWorld()
story = TinyStory(environment=environment)
story.start_story()
current_story = story._current_story()
print(current_story)
```