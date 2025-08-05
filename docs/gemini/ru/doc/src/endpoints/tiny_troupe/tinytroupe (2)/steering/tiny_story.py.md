# TinyStory: Рассказы для TinyTroupe

## Обзор

Модуль `TinyStory` обеспечивает механизмы для создания историй в `TinyTroupe`. 

## Подробнее

В `TinyTroupe` каждая симуляция представляет собой историю.  `TinyStory`  помогает создавать подходящие истории, предоставляя инструменты для управления контекстом и сценарием. Класс `TinyStory`  запоминает контекст симуляции, историю взаимодействия и может генерировать тексты, подходящие для описания поведения агентов и окружающей среды в `TinyTroupe`. 

## Классы

### `TinyStory`

**Описание**:  Класс `TinyStory`  служит для генерации историй в `TinyTroupe`. 

**Атрибуты**:

- `environment` (TinyWorld):  Окружающая среда симуляции (необязательно).
- `agent` (TinyPerson):  Агент в симуляции (необязательно).
- `purpose` (str):  Цель, определяющая стиль истории (например, "Будь реалистичной симуляцией").
- `context` (str):  Текущий контекст истории. 
- `first_n` (int):  Количество первых взаимодействий, которые следует включить в историю.
- `last_n` (int):  Количество последних взаимодействий, которые следует включить в историю.
- `include_omission_info` (bool):  Указывает, следует ли включать информацию о пропущенных взаимодействиях.


**Методы**:

- `start_story(requirements="Start some interesting story about the agents.", number_of_words:int=100, include_plot_twist:bool=False) -> str`:  Создает начало истории.
- `continue_story(requirements="Continue the story in an interesting way.", number_of_words:int=100, include_plot_twist:bool=False) -> str`:  Продолжает историю.
- `_current_story() -> str`:  Получает текущий контекст истории, включая информацию о последних взаимодействиях.

**Как работает класс**:

Класс `TinyStory`  создает  тексты  описывающие происходящее в симуляции. `TinyStory`  анализирует  `TinyWorld`  и  `TinyPerson`  (если они заданы),  использует их для  подбора  ключевых событий, действий агентов и других элементов, которые необходимо  включить в историю.  `TinyStory`  учитывает цель истории, заданную  `purpose`  при  инициализации. 

**Примеры**:

```python
from tinytroupe.extraction import logger
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
import tinytroupe.utils as utils
from tinytroupe import openai_utils
from tinytroupe.steering.tiny_story import TinyStory

# Создание окружения
world = TinyWorld(purpose="Be a realistic simulation.")

# Создание агента
agent = TinyPerson(purpose="Be a good person and a helpful assistant")

# Создание истории
story = TinyStory(agent=agent)

# Запуск истории
start = story.start_story()

# Продолжение истории
continuation = story.continue_story()

# Получение полной истории
full_story = story._current_story()
```

## Методы класса

### `start_story`

```python
    def start_story(self, requirements="Start some interesting story about the agents.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
        """
        Создает начало истории.
        """
        
        rendering_configs = {
                             "purpose": self.purpose,
                             "requirements": requirements,
                             "current_simulation_trace": self._current_story(),
                             "number_of_words": number_of_words,
                             "include_plot_twist": include_plot_twist
                            }

        messages = utils.compose_initial_LLM_messages_with_templates("story.start.system.mustache", "story.start.user.mustache", 
                                                                     base_module_folder="steering",
                                                                     rendering_configs=rendering_configs)
        next_message = openai_utils.client().send_message(messages, temperature=1.5)

        start = next_message["content"]

        self.current_story += utils.dedent(
            f"""

            ## The story begins

            {start}

            """
            )

        return start
```

**Назначение**:  `start_story`  генерирует  начало истории  основываясь на  заданном  `purpose`  и  других  параметрах.  

**Параметры**:

- `requirements` (str, optional):  Дополнительные  требования  к  истории, например "Начать  интересную  историю  о  героях". По умолчанию: `"Start some interesting story about the agents."`.
- `number_of_words` (int, optional):  Желаемое  количество  слов  в  начале  истории.  По умолчанию:  `100`.
- `include_plot_twist` (bool, optional):  Указывает,  следует  ли  включить  непредсказуемый  поворот  в  сюжете  истории.  По умолчанию:  `False`.

**Возвращает**:

- `str`:  Генерированный  начальный  отрывок  истории.

**Как работает функция**:

`start_story`  создает  набор  сообщений  для  LLM  (модели  искусственного  интеллекта),  включая  цель  (`purpose`),  требования  (`requirements`),  контекст  симуляции  (`_current_story()`) и другие  параметры.  Затем  отправляет  эти  сообщения  в  LLM  и  получает  от  него  текст  начальной  части  истории.  

**Примеры**:

```python
# Создание истории
story = TinyStory(agent=agent, purpose="Be a story about a robot in a city")

# Запуск истории
start = story.start_story(requirements="The robot is trying to find his friend", number_of_words=50)
```

### `continue_story`

```python
    def continue_story(self, requirements="Continue the story in an interesting way.", number_of_words:int=100, include_plot_twist:bool=False) -> str:
        """
        Продолжает историю.
        """
        
        rendering_configs = {
                             "purpose": self.purpose,
                             "requirements": requirements,
                             "current_simulation_trace": self._current_story(),
                             "number_of_words": number_of_words,
                             "include_plot_twist": include_plot_twist
                            }

        messages = utils.compose_initial_LLM_messages_with_templates("story.continuation.system.mustache", "story.continuation.user.mustache", 
                                                                     base_module_folder="steering",
                                                                     rendering_configs=rendering_configs)
        next_message = openai_utils.client().send_message(messages, temperature=1.5)

        continuation = next_message["content"]

        self.current_story += utils.dedent(
            f"""

            ## The story continues

            {continuation}

            """
            )

        return continuation
```

**Назначение**:  `continue_story`  генерирует  продолжение  истории,  учитывая  ее  текущий  контекст.  

**Параметры**:

- `requirements` (str, optional):  Дополнительные  требования  к  продолжению  истории,  например "Продолжить  историю  в  интересном  ключе".  По умолчанию: `"Continue the story in an interesting way."`.
- `number_of_words` (int, optional):  Желаемое  количество  слов  в  продолжении  истории.  По умолчанию:  `100`.
- `include_plot_twist` (bool, optional):  Указывает,  следует  ли  включить  непредсказуемый  поворот  в  сюжете  продолжения  истории.  По умолчанию:  `False`.

**Возвращает**:

- `str`:  Генерированный  отрывок  продолжения  истории.

**Как работает функция**:

`continue_story`  работает  аналогично  `start_story`,  но  использует  другие  шаблоны  сообщений  (`story.continuation.system.mustache`  и  `story.continuation.user.mustache`),  а также  включает  в  сообщения  текущий  контекст  истории  (`_current_story()`).

**Примеры**:

```python
# Продолжение истории
continuation = story.continue_story(requirements="The robot needs to find a way to fix his friend", number_of_words=75)
```

### `_current_story`

```python
    def _current_story(self) -> str:
        """
        Получает текущий контекст истории.
        """
        interaction_history = ""
        
        if self.agent is not None:
            interaction_history += self.agent.pretty_current_interactions(first_n=self.first_n, last_n=self.last_n, include_omission_info=self.include_omission_info)
        elif self.environment is not None:
            interaction_history += self.environment.pretty_current_interactions(first_n=self.first_n, last_n=self.last_n, include_omission_info=self.include_omission_info)

        self.current_story += utils.dedent(
            f"""

            ## New simulation interactions to consider

            {interaction_history}

            """
            )
            
        return self.current_story
```

**Назначение**:  `_current_story`  возвращает  текст  текущего  контекста  истории,  включая  информацию  о  последних  взаимодействиях  в  симуляции.

**Параметры**:

- Нет параметров.

**Возвращает**:

- `str`:  Текстовое  представление  текущего  контекста  истории.

**Как работает функция**:

`_current_story`  считывает  информацию  о  последних  взаимодействиях  из  `agent`  или  `environment`  (в  зависимости  от  того,  какой  из  них  был  задан  при  инициализации  `TinyStory`).  Затем  она  добавляет  эту  информацию  в  `current_story`  и  возвращает  ее. 

**Примеры**:

```python
# Получение полной истории
full_story = story._current_story()
```

## Параметры класса

- `environment` (TinyWorld):  Окружающая  среда  симуляции  (необязательно).  Если  передана  `TinyWorld`,  то  в  историю  будут  включены  данные  о  взаимодействиях  с  этой  средой. 

- `agent` (TinyPerson):  Агент  в  симуляции  (необязательно).  Если  передан  `TinyPerson`,  то  в  историю  будут  включены  данные  о  взаимодействиях  этого  агента.

- `purpose` (str):  Цель  истории.  Определяет  стиль  и  направление  рассказа.  Например,  "Будь  реалистичной  симуляцией"  может  привести  к  более  детальному  описанию  действий  агентов,  в  то  время  как  "Будь  смешной  историей"  может  привести  к  более  легкомысленному  и  юмористическому  тексту.

- `context` (str):  Текущий  контекст  истории.  Используется  для  сохранения  предыдущих  частей  рассказа.

- `first_n` (int):  Количество  первых  взаимодействий,  которые  следует  включить  в  историю.  Помогает  ограничить  количество  информации,  включенной  в  историю,  чтобы  сделать  ее  более  сжатой.

- `last_n` (int):  Количество  последних  взаимодействий,  которые  следует  включить  в  историю.  Помогает  ограничить  количество  информации,  включенной  в  историю,  чтобы  сделать  ее  более  сжатой.

- `include_omission_info` (bool):  Указывает,  следует  ли  включать  информацию  о  пропущенных  взаимодействиях.  

## Примеры

**Пример 1: История о роботе**

```python
from tinytroupe.extraction import logger
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
import tinytroupe.utils as utils
from tinytroupe import openai_utils
from tinytroupe.steering.tiny_story import TinyStory

# Создание окружения
world = TinyWorld(purpose="Be a realistic simulation.")

# Создание агента
agent = TinyPerson(purpose="Be a good person and a helpful assistant", name="R2-D2")

# Создание истории
story = TinyStory(agent=agent, purpose="Be a story about a robot in a city")

# Запуск истории
start = story.start_story(requirements="The robot is trying to find his friend", number_of_words=50)

# Продолжение истории
continuation = story.continue_story(requirements="The robot needs to find a way to fix his friend", number_of_words=75)

# Получение полной истории
full_story = story._current_story()

print(full_story)
```

**Пример 2: История о волшебном лесу**

```python
from tinytroupe.extraction import logger
from tinytroupe.environment import TinyWorld
import tinytroupe.utils as utils
from tinytroupe import openai_utils
from tinytroupe.steering.tiny_story import TinyStory

# Создание окружения
world = TinyWorld(purpose="Be a realistic simulation of a magic forest.")

# Создание истории
story = TinyStory(environment=world, purpose="Be a story about a group of adventurers in a magic forest")

# Запуск истории
start = story.start_story(requirements="The adventurers are looking for a magical artifact", number_of_words=100)

# Продолжение истории
continuation = story.continue_story(requirements="The adventurers encounter a dangerous creature", number_of_words=150)

# Получение полной истории
full_story = story._current_story()

print(full_story)
```

## Дополнительные замечания

- Модуль `TinyStory` использует `openai_utils`  для  взаимодействия  с  LLM. 
-  `_current_story`  создает  текст  с  заголовками  и  отступами  для  лучшей  читабельности.
-  `TinyStory`  может  быть  расширен  для  поддержки  разных  стилей  историй,  включая  фантастику,  научную  фантастику,  детектив  и  другие  жанры.