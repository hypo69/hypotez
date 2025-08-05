# Модуль TinyStory 

## Обзор

Модуль `TinyStory` обеспечивает механизмы для создания историй, основанных на симуляциях `TinyTroupe`. Каждая история связана с определенной средой (`TinyWorld`) или агентом (`TinyPerson`) и имеет цель, которая направляет процесс генерации. 

## Подробней

`TinyStory` предоставляет функции для начала истории (`start_story`), её продолжения (`continue_story`) и получения текущей истории (`_current_story`). В `TinyStory` реализована возможность использования контекста, который может включать в себя информацию о предыдущих взаимодействиях в симуляции. Кроме того, `TinyStory` поддерживает настройки, такие как количество слов в истории, включение неожиданных поворотов сюжета, а также возможность указать, сколько первых и последних взаимодействий включить в контекст истории.

## Классы

### `TinyStory`

**Описание**: Класс, представляющий собой историю в `TinyTroupe`.

**Наследует**: 
- None

**Атрибуты**:

- `environment` (`TinyWorld`): Среда, в которой происходит история.
- `agent` (`TinyPerson`): Агент, о котором идёт речь в истории.
- `purpose` (`str`): Цель, которая направляет генерацию истории.
- `context` (`str`): Текущий контекст истории.
- `first_n` (`int`): Количество первых взаимодействий, которые нужно включить в контекст истории.
- `last_n` (`int`): Количество последних взаимодействий, которые нужно включить в контекст истории.
- `include_omission_info` (`bool`): Включать ли информацию о пропущенных взаимодействиях.

**Методы**:

- `start_story`: Начать новую историю.
- `continue_story`: Предложить продолжение истории.
- `_current_story`: Получить текущую историю.

## Методы класса

### `start_story`

```python
    def start_story(self, requirements="Start some interesting story about the agents.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
        """
        Начать новую историю.

        Args:
            requirements (str, optional): Требования к началу истории. Defaults to "Start some interesting story about the agents.".
            number_of_words (int, optional): Количество слов в истории. Defaults to 100.
            include_plot_twist (bool, optional): Включать ли неожиданный поворот сюжета. Defaults to False.

        Returns:
            str: Начальный фрагмент истории.
        """
        ...
```

**Назначение**: Начать новую историю, сгенерированную моделью.

**Параметры**:

- `requirements` (`str`): Требования к началу истории.
- `number_of_words` (`int`): Количество слов в истории.
- `include_plot_twist` (`bool`): Включать ли неожиданный поворот сюжета.

**Возвращает**:

- `str`: Начальный фрагмент истории.

**Как работает функция**:

- `start_story` использует  шаблоны `story.start.system.mustache` и `story.start.user.mustache`  из  `tinytroupe.utils` для  составления  начальных сообщений  для  модели LLM.
- Сообщения отправляются  в  модель  LLM  с  помощью `openai_utils.client()`. 
- `start_story`  добавляет  генерированный  начальный  фрагмент  истории  в  `current_story` и  возвращает  его.

**Примеры**:

```python
story = TinyStory(agent=agent)
story.start_story(requirements="Start a story about an agent who is trying to find a new job.", number_of_words=50)
```

### `continue_story`

```python
    def continue_story(self, requirements="Continue the story in an interesting way.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
        """
        Предложить продолжение истории.

        Args:
            requirements (str, optional): Требования к продолжению истории. Defaults to "Continue the story in an interesting way.".
            number_of_words (int, optional): Количество слов в продолжении истории. Defaults to 100.
            include_plot_twist (bool, optional): Включать ли неожиданный поворот сюжета. Defaults to False.

        Returns:
            str: Продолжение истории.
        """
        ...
```

**Назначение**: Предложить продолжение уже начатой истории, сгенерированное моделью.

**Параметры**:

- `requirements` (`str`): Требования к продолжению истории.
- `number_of_words` (`int`): Количество слов в продолжении истории.
- `include_plot_twist` (`bool`): Включать ли неожиданный поворот сюжета.

**Возвращает**:

- `str`: Продолжение истории.

**Как работает функция**:

- `continue_story` использует  шаблоны `story.continuation.system.mustache` и `story.continuation.user.mustache`  из  `tinytroupe.utils` для  составления  сообщений  для  модели LLM.
- Сообщения отправляются  в  модель  LLM  с  помощью `openai_utils.client()`. 
- `continue_story`  добавляет  генерированное  продолжение  истории  в  `current_story` и  возвращает  его.

**Примеры**:

```python
story = TinyStory(agent=agent)
story.start_story(requirements="Start a story about an agent who is trying to find a new job.", number_of_words=50)
story.continue_story(requirements="Continue the story with a new challenge for the agent.", number_of_words=70, include_plot_twist=True)
```

### `_current_story`

```python
    def _current_story(self) -> str:
        """
        Получить текущую историю.
        """
        ...
```

**Назначение**: Получить текущую историю, включая контекст.

**Параметры**:

- None

**Возвращает**:

- `str`: Текущая история.

**Как работает функция**:

- `_current_story` сначала получает историю взаимодействий из `agent` или `environment`.
- Затем функция добавляет эту историю взаимодействий к текущему контексту истории `current_story`.
- В конце функция возвращает `current_story`.

**Примеры**:

```python
story = TinyStory(agent=agent)
print(story._current_story())
```

## Параметры класса

- `environment` (`TinyWorld`): Среда, в которой происходит история. Определяет контекст для генерации истории.
- `agent` (`TinyPerson`): Агент, о котором идёт речь в истории. Определяет контекст для генерации истории.
- `purpose` (`str`): Цель, которая направляет генерацию истории. Например, "Be a realistic simulation" или "Generate a story about a robot who wants to be a human."
- `context` (`str`): Текущий контекст истории. Может включать в себя предыдущие взаимодействия, описания персонажей, описание окружения, информацию о мире.
- `first_n` (`int`): Количество первых взаимодействий, которые нужно включить в контекст истории. 
- `last_n` (`int`): Количество последних взаимодействий, которые нужно включить в контекст истории.
- `include_omission_info` (`bool`): Включать ли информацию о пропущенных взаимодействиях.  

## Примеры

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.story import TinyStory

# Создание агента
agent = TinyPerson(name="Alice", age=30, job="Software Engineer", personality="Curious and ambitious")

# Создание истории об агенте
story = TinyStory(agent=agent, purpose="Tell a story about a software engineer who dreams of becoming a writer.")

# Начало истории
start = story.start_story(requirements="Start a story about Alice, a software engineer who always wanted to be a writer.", number_of_words=100)
print(f"Начало истории: {start}")

# Продолжение истории
continuation = story.continue_story(requirements="Continue the story with a new challenge for Alice, where she has to make a difficult choice.", number_of_words=70, include_plot_twist=True)
print(f"Продолжение истории: {continuation}")

# Получение текущей истории
current_story = story._current_story()
print(f"Текущая история: {current_story}")

# Вывод:
# Начало истории: ...
# Продолжение истории: ...
# Текущая история: ... 
```