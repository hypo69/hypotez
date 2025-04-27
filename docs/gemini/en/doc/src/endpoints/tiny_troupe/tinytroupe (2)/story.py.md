# TinyStory

## Overview

Этот модуль предоставляет вспомогательные механизмы для создания соответствующих историй в TinyTroupe.

## Details

Этот модуль предоставляет механизмы для создания историй, которые отражают симуляции. 

## Classes

### `TinyStory`

**Description**: Класс для создания и продолжения историй, основанных на симуляциях TinyTroupe.

**Attributes**:
- `environment` (TinyWorld, optional):  Среда, в которой происходит история. По умолчанию `None`.
- `agent` (TinyPerson, optional):  Агент, участвующий в истории. По умолчанию `None`.
- `purpose` (str, optional): Цель истории. По умолчанию "Be a realistic simulation.".
- `context` (str, optional): Текущий контекст истории. По умолчанию "". К этому контексту будет добавлена фактическая история.
- `first_n` (int, optional): Количество первых взаимодействий, которые нужно включить в историю. По умолчанию 10.
- `last_n` (int, optional): Количество последних взаимодействий, которые нужно включить в историю. По умолчанию 20.
- `include_omission_info` (bool, optional):  Флаг, указывающий, нужно ли включать информацию о пропущенных взаимодействиях. По умолчанию `True`.

**Methods**:
- `start_story(requirements="Start some interesting story about the agents.", number_of_words:int=100, include_plot_twist:bool=False) -> str`:  Начинает новую историю.
- `continue_story(requirements="Continue the story in an interesting way.", number_of_words:int=100, include_plot_twist:bool=False) -> str`: Предлагает продолжение истории.
- `_current_story() -> str`: Получает текущую историю.

## Class Methods

### `start_story`

```python
    def start_story(self, requirements="Start some interesting story about the agents.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
        """
        Начинает новую историю.

        Args:
            requirements (str, optional): Требования к истории. По умолчанию "Start some interesting story about the agents.".
            number_of_words (int, optional): Желаемое количество слов в истории. По умолчанию 100.
            include_plot_twist (bool, optional): Включить ли неожиданный поворот сюжета. По умолчанию `False`.

        Returns:
            str: Начальный фрагмент истории.

        Example:
            >>> story = TinyStory(agent=agent)
            >>> start = story.start_story()
            >>> print(start)
            <Start of the story>
        """
```

### `continue_story`

```python
    def continue_story(self, requirements="Continue the story in an interesting way.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
        """
        Предлагает продолжение истории.

        Args:
            requirements (str, optional): Требования к продолжению истории. По умолчанию "Continue the story in an interesting way.".
            number_of_words (int, optional): Желаемое количество слов в продолжении истории. По умолчанию 100.
            include_plot_twist (bool, optional): Включить ли неожиданный поворот сюжета. По умолчанию `False`.

        Returns:
            str:  Продолжение истории.

        Example:
            >>> story = TinyStory(agent=agent)
            >>> story.start_story()
            >>> continuation = story.continue_story()
            >>> print(continuation)
            <Continuation of the story>
        """
```

### `_current_story`

```python
    def _current_story(self) -> str:
        """
        Получает текущую историю, включая контекст и историю взаимодействий.

        Returns:
            str: Текущая история.
        """
```

## Parameter Details

- `environment` (TinyWorld, optional): Среда, в которой происходит история.
- `agent` (TinyPerson, optional): Агент, участвующий в истории.
- `purpose` (str, optional): Цель истории.
- `context` (str, optional): Текущий контекст истории. 
- `first_n` (int, optional): Количество первых взаимодействий, которые нужно включить в историю.
- `last_n` (int, optional): Количество последних взаимодействий, которые нужно включить в историю.
- `include_omission_info` (bool, optional):  Флаг, указывающий, нужно ли включать информацию о пропущенных взаимодействиях.
- `requirements` (str, optional): Требования к истории или продолжению истории.
- `number_of_words` (int, optional):  Желаемое количество слов в истории.
- `include_plot_twist` (bool, optional): Включить ли неожиданный поворот сюжета.

## Examples

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson
from tinytroupe.story import TinyStory

# Создаем среду и агента
environment = TinyWorld()
agent = TinyPerson(environment=environment)

# Создаем экземпляр TinyStory
story = TinyStory(agent=agent)

# Начинаем историю
start = story.start_story()
print(start)

# Продолжаем историю
continuation = story.continue_story()
print(continuation)

# Получаем текущую историю
current_story = story._current_story()
print(current_story)
```