# Модуль для создания историй в TinyTroupe

## Обзор

Этот модуль предоставляет вспомогательные механизмы для создания историй в TinyTroupe. Он позволяет создавать истории на основе симуляций, учитывая окружение и агентов. Модуль включает функциональность для начала и продолжения историй, а также для включения информации о взаимодействиях в симуляции.

## Подробней

Этот модуль предназначен для генерации историй на основе симуляций, проводимых в TinyTroupe. Он предоставляет классы и методы для управления контекстом истории, добавления информации о взаимодействиях агентов и окружающей среды, а также для генерации текста истории с использованием OpenAI.

## Классы

### `TinyStory`

**Описание**: Класс для создания и управления историями в TinyTroupe.

**Атрибуты**:
- `environment` (TinyWorld, optional): Окружение, в котором происходит история. По умолчанию `None`.
- `agent` (TinyPerson, optional): Агент, о котором рассказывается история. По умолчанию `None`.
- `purpose` (str, optional): Цель истории. По умолчанию `"Be a realistic simulation."`.
- `context` (str, optional): Текущий контекст истории. По умолчанию `""`. Фактическая история будет добавлена к этому контексту.
- `first_n` (int, optional): Количество первых взаимодействий, которые нужно включить в историю. По умолчанию `10`.
- `last_n` (int, optional): Количество последних взаимодействий, которые нужно включить в историю. По умолчанию `20`.
- `include_omission_info` (bool, optional): Флаг, указывающий, следует ли включать информацию об опущенных взаимодействиях. По умолчанию `True`.
- `current_story` (str): Текущая история.

**Методы**:
- `__init__`: Инициализирует историю.
- `start_story`: Начинает новую историю.
- `continue_story`: Предлагает продолжение истории.
- `_current_story`: Получает текущую историю.

#### `__init__(self, environment: TinyWorld = None, agent: TinyPerson = None, purpose: str = "Be a realistic simulation.", context: str = "", first_n: int = 10, last_n: int = 20, include_omission_info: bool = True) -> None`

**Назначение**: Инициализирует экземпляр класса `TinyStory`.

**Параметры**:
- `environment` (TinyWorld, optional): Окружение, в котором происходит история. По умолчанию `None`.
- `agent` (TinyPerson, optional): Агент, о котором рассказывается история. По умолчанию `None`.
- `purpose` (str, optional): Цель истории. По умолчанию `"Be a realistic simulation."`.
- `context` (str, optional): Текущий контекст истории. По умолчанию `""`. Фактическая история будет добавлена к этому контексту.
- `first_n` (int, optional): Количество первых взаимодействий, которые нужно включить в историю. По умолчанию `10`.
- `last_n` (int, optional): Количество последних взаимодействий, которые нужно включить в историю. По умолчанию `20`.
- `include_omission_info` (bool, optional): Флаг, указывающий, следует ли включать информацию об опущенных взаимодействиях. По умолчанию `True`.

**Как работает функция**:
- Проверяет, что предоставлен либо `environment`, либо `agent`, но не оба сразу.
- Инициализирует атрибуты класса значениями переданных параметров.

**Примеры**:
```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

# Пример инициализации с окружением
environment = TinyWorld()
story_env = TinyStory(environment=environment)

# Пример инициализации с агентом
agent = TinyPerson()
story_agent = TinyStory(agent=agent)
```

#### `start_story(self, requirements: str = "Start some interesting story about the agents.", number_of_words: int = 100, include_plot_twist: bool = False) -> str`

**Назначение**: Начинает новую историю, генерируя начальный текст на основе предоставленных требований и текущего контекста.

**Параметры**:
- `requirements` (str, optional): Требования к началу истории. По умолчанию `"Start some interesting story about the agents."`.
- `number_of_words` (int, optional): Количество слов в сгенерированном тексте. По умолчанию `100`.
- `include_plot_twist` (bool, optional): Флаг, указывающий, следует ли включать неожиданный поворот в сюжет. По умолчанию `False`.

**Внутренние функции**:
- Здесь нет внутренних функций.

**Как работает функция**:
- Формирует словарь `rendering_configs` с параметрами для генерации истории.
- Использует `utils.compose_initial_LLM_messages_with_templates` для создания сообщений для языковой модели.
- Отправляет сообщение в OpenAI с помощью `openai_utils.client().send_message` и получает ответ.
- Добавляет сгенерированный текст в `self.current_story`.
- Возвращает сгенерированный текст.

**Примеры**:
```python
# Пример вызова функции start_story
from tinytroupe.environment import TinyWorld
environment = TinyWorld()
story = TinyStory(environment=environment)
start = story.start_story(requirements="Начни историю о приключениях в лесу.", number_of_words=150, include_plot_twist=True)
print(start)
```

#### `continue_story(self, requirements: str = "Continue the story in an interesting way.", number_of_words: int = 100, include_plot_twist: bool = False) -> str`

**Назначение**: Предлагает продолжение истории, генерируя текст продолжения на основе предоставленных требований и текущего контекста.

**Параметры**:
- `requirements` (str, optional): Требования к продолжению истории. По умолчанию `"Continue the story in an interesting way."`.
- `number_of_words` (int, optional): Количество слов в сгенерированном тексте. По умолчанию `100`.
- `include_plot_twist` (bool, optional): Флаг, указывающий, следует ли включать неожиданный поворот в сюжет. По умолчанию `False`.

**Внутренние функции**:
- Здесь нет внутренних функций.

**Как работает функция**:
- Формирует словарь `rendering_configs` с параметрами для генерации истории.
- Использует `utils.compose_initial_LLM_messages_with_templates` для создания сообщений для языковой модели.
- Отправляет сообщение в OpenAI с помощью `openai_utils.client().send_message` и получает ответ.
- Добавляет сгенерированный текст в `self.current_story`.
- Возвращает сгенерированный текст.

**Примеры**:
```python
# Пример вызова функции continue_story
from tinytroupe.environment import TinyWorld
environment = TinyWorld()
story = TinyStory(environment=environment)
story.start_story()
continuation = story.continue_story(requirements="Продолжи историю, добавив нового персонажа.", number_of_words=120)
print(continuation)
```

#### `_current_story(self) -> str`

**Назначение**: Получает текущую историю, добавляя в нее информацию о последних взаимодействиях агента или окружающей среды.

**Параметры**:
- Отсутствуют.

**Внутренние функции**:
- Здесь нет внутренних функций.

**Как работает функция**:
- Получает историю взаимодействий агента или окружающей среды с помощью `pretty_current_interactions`.
- Добавляет информацию о взаимодействиях в `self.current_story`.
- Возвращает `self.current_story`.

**Примеры**:
```python
# Пример вызова функции _current_story
from tinytroupe.environment import TinyWorld
environment = TinyWorld()
story = TinyStory(environment=environment)
current_story = story._current_story()
print(current_story)