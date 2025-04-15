# Модуль для создания историй в TinyTroupe
## Обзор

Модуль предоставляет класс `TinyStory`, который помогает в создании историй для симуляций в TinyTroupe. Он позволяет генерировать истории на основе окружения или агента, а также управлять контекстом и параметрами генерации.

## Подробнее

Этот модуль предназначен для упрощения процесса создания увлекательных и реалистичных историй в рамках симуляций TinyTroupe. Он предоставляет гибкий интерфейс для управления сюжетом, контекстом и параметрами генерации истории, а также интегрируется с AI-моделями для автоматического создания контента.

## Классы

### `TinyStory`

**Описание**: Класс для создания историй на основе окружения или агента в симуляции TinyTroupe.

**Атрибуты**:
- `environment` (TinyWorld, optional): Окружение, в котором происходит история. По умолчанию `None`.
- `agent` (TinyPerson, optional): Агент, о котором рассказывается история. По умолчанию `None`.
- `purpose` (str, optional): Цель истории. Используется для направления генерации истории. По умолчанию "Be a realistic simulation.".
- `context` (str, optional): Текущий контекст истории. Фактическая история будет добавлена к этому контексту. По умолчанию "".
- `first_n` (int, optional): Количество первых взаимодействий, которые нужно включить в историю. По умолчанию 10.
- `last_n` (int, optional): Количество последних взаимодействий, которые нужно включить в историю. По умолчанию 20.
- `include_omission_info` (bool, optional): Определяет, следует ли включать информацию об опущенных взаимодействиях. По умолчанию `True`.
- `current_story` (str): Текущая история, которая формируется в процессе работы методов класса.

**Методы**:
- `__init__`: Инициализирует объект истории.
- `start_story`: Начинает новую историю.
- `continue_story`: Предлагает продолжение истории.
- `_current_story`: Получает текущую историю.

#### `__init__`
```python
def __init__(self, environment:TinyWorld=None, agent:TinyPerson=None, purpose:str="Be a realistic simulation.", context:str="",
                 first_n=10, last_n=20, include_omission_info:bool=True) -> None:
        """
        Инициализирует историю. История может быть об окружении или агенте. У нее также есть цель, которая
        используется для направления генерации истории. Истории знают, что они связаны с симуляциями, поэтому можно
        указать цели, связанные с симуляцией.

        Args:
            environment (TinyWorld, optional): Окружение, в котором происходит история. По умолчанию `None`.
            agent (TinyPerson, optional): Агент в истории. По умолчанию `None`.
            purpose (str, optional): Цель истории. По умолчанию "Be a realistic simulation.".
            context (str, optional): Текущий контекст истории. По умолчанию "". Фактическая история будет добавлена к этому контексту.
            first_n (int, optional): Количество первых взаимодействий, которые нужно включить в историю. По умолчанию 10.
            last_n (int, optional): Количество последних взаимодействий, которые нужно включить в историю. По умолчанию 20.
            include_omission_info (bool, optional): Следует ли включать информацию об опущенных взаимодействиях. По умолчанию `True`.

        Raises:
            Exception: Если одновременно предоставлены и `environment`, и `agent`.
            Exception: Если не предоставлен ни `environment`, ни `agent`.
        """
```

**Как работает класс**:

- Класс `TinyStory` предназначен для создания историй, связанных с симуляциями TinyTroupe.
- При инициализации класса необходимо указать либо окружение (`environment`), либо агента (`agent`), о котором будет рассказываться история.
- Параметр `purpose` определяет цель истории и используется для направления генерации контента.
- Контекст истории (`context`) позволяет добавлять дополнительную информацию, которая будет учитываться при создании истории.
- Параметры `first_n` и `last_n` определяют, какое количество первых и последних взаимодействий агента или окружения следует включить в историю.
- Параметр `include_omission_info` определяет, следует ли включать информацию об опущенных взаимодействиях.

#### `start_story`
```python
 def start_story(self, requirements="Start some interesting story about the agents.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
        """
        Начать новую историю.

        Args:
            requirements (str, optional): Требования к началу истории. По умолчанию "Start some interesting story about the agents.".
            number_of_words (int, optional): Количество слов в начале истории. По умолчанию 100.
            include_plot_twist (bool, optional): Включить ли в историю неожиданный поворот. По умолчанию `False`.

        Returns:
            str: Начало истории.
        """
```

**Как работает функция**:

- Функция `start_story` начинает новую историю, используя предоставленные требования, количество слов и флаг включения неожиданного поворота.
- Она использует шаблоны сообщений для составления запроса к языковой модели (LLM) и получает ответ с началом истории.
- Полученный текст добавляется к текущей истории и возвращается.
- Для составления сообщений используются функции `utils.compose_initial_LLM_messages_with_templates` и `openai_utils.client().send_message`.
- Результат форматируется с использованием `utils.dedent` и добавляется в `self.current_story`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.story import TinyStory

# Пример создания окружения
env = TinyWorld()

# Пример создания истории на основе окружения
story = TinyStory(environment=env)

# Пример запуска истории
start = story.start_story(requirements="Начни интересную историю о развитии города.", number_of_words=150)
print(start)
```

#### `continue_story`
```python
def continue_story(self, requirements="Continue the story in an interesting way.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
        """
        Предложить продолжение истории.

        Args:
            requirements (str, optional): Требования к продолжению истории. По умолчанию "Continue the story in an interesting way.".
            number_of_words (int, optional): Количество слов в продолжении истории. По умолчанию 100.
            include_plot_twist (bool, optional): Включить ли в историю неожиданный поворот. По умолчанию `False`.

        Returns:
            str: Продолжение истории.
        """
```

**Как работает функция**:

- Функция `continue_story` предлагает продолжение истории, используя предоставленные требования, количество слов и флаг включения неожиданного поворота.
- Она использует шаблоны сообщений для составления запроса к языковой модели (LLM) и получает ответ с продолжением истории.
- Полученный текст добавляется к текущей истории и возвращается.
- Для составления сообщений используются функции `utils.compose_initial_LLM_messages_with_templates` и `openai_utils.client().send_message`.
- Результат форматируется с использованием `utils.dedent` и добавляется в `self.current_story`.

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.story import TinyStory

# Пример создания окружения
env = TinyWorld()

# Пример создания истории на основе окружения
story = TinyStory(environment=env)

# Пример запуска истории
start = story.start_story(requirements="Начни интересную историю о развитии города.", number_of_words=150)
print(start)

# Пример продолжения истории
continuation = story.continue_story(requirements="Пусть жители города столкнутся с неожиданной проблемой.", number_of_words=120)
print(continuation)
```

#### `_current_story`
```python
def _current_story(self) -> str:
        """
        Получить текущую историю.

        Returns:
            str: Текущая история.
        """
```

**Как работает функция**:

- Функция `_current_story` возвращает текущую историю, включая информацию о взаимодействиях агента или окружения.
- Если в истории участвует агент (`self.agent is not None`), она добавляет информацию о его взаимодействиях, используя метод `self.agent.pretty_current_interactions`.
- Если в истории участвует окружение (`self.environment is not None`), она добавляет информацию о его взаимодействиях, используя метод `self.environment.pretty_current_interactions`.
- Информация о взаимодействиях форматируется с использованием `utils.dedent` и добавляется в `self.current_story`.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.story import TinyStory

# Пример создания агента
agent = TinyPerson(name="Агент 007")

# Пример создания истории на основе агента
story = TinyStory(agent=agent)

# Пример получения текущей истории
current_story = story._current_story()
print(current_story)