# Модуль для определения и проверки пропозиций в контексте TinyTroupe
==================================================================

Модуль содержит класс :class:`Proposition`, который используется для определения и проверки пропозиций (утверждений) относительно целей (например, `TinyWorld`, `TinyPerson` или их комбинаций) в контексте симуляции многоагентной среды TinyTroupe. Также содержит функцию :func:`check_proposition`, которая предоставляет удобный способ проверки пропозиций без необходимости создания объекта `Proposition`.

## Обзор

Этот модуль предназначен для работы с пропозициями (утверждениями) о поведении агентов или состоянии среды в симуляции. Он позволяет задавать цели, формулировать утверждения и проверять их истинность на основе контекста, предоставляемого симуляцией.

## Подробнее

Модуль позволяет оценивать утверждения о симуляции многоагентной среды, используя контекст, который может включать траектории симуляции агентов и состояние среды в определенные моменты времени. Для оценки истинности утверждений используется языковая модель (LLM), которая анализирует контекст и выносит решение.

## Классы

### `Proposition`

**Описание**: Класс для определения пропозиции как утверждения о цели (или целях), которой может быть `TinyWorld`, `TinyPerson` или их список.

**Атрибуты**:
- `targets` (list): Список целей пропозиции (`TinyWorld` или `TinyPerson`).
- `claim` (str): Утверждение, которое необходимо проверить.
- `first_n` (int, optional): Количество первых взаимодействий для рассмотрения в контексте.
- `last_n` (int, optional): Количество последних взаимодействий для рассмотрения в контексте.
- `value` (bool, optional): Значение пропозиции (True или False) после проверки.
- `justification` (str, optional): Обоснование значения пропозиции, полученное от языковой модели.
- `confidence` (float, optional): Уверенность языковой модели в значении пропозиции.
- `raw_llm_response` (str, optional): Необработанный ответ от языковой модели.

**Методы**:
- `__init__(target, claim, first_n=None, last_n=None)`: Инициализирует объект пропозиции.
- `__call__(additional_context=None)`: Вызывает метод `check` для проверки пропозиции.
- `check(additional_context="No additional context available.")`: Проверяет пропозицию и возвращает её значение.

#### `__init__(self, target, claim: str, first_n: int = None, last_n: int = None)`

```python
    def __init__(self, target, claim:str, first_n:int=None, last_n:int=None):
        """
        Define a proposition as a (textual) claim about a target, which can be a TinyWorld, a TinyPerson or several of any.

        Args:
            target (TinyWorld, TinyPerson, list): the target or targets of the proposition
            claim (str): the claim of the proposition
            first_n (int): the number of first interactions to consider in the context
            last_n (int): the number of last interactions (most recent) to consider in the context

        """
        ...
```

**Назначение**: Инициализирует объект `Proposition`, определяя цель (или цели), утверждение и контекст для оценки.

**Параметры**:
- `target` (TinyWorld, TinyPerson, list): Цель или цели, к которым относится пропозиция. Может быть экземпляром `TinyWorld`, `TinyPerson` или списком экземпляров этих классов.
- `claim` (str): Текстовое утверждение, которое необходимо проверить относительно цели.
- `first_n` (int, optional): Количество первых взаимодействий, которые следует учитывать в контексте. По умолчанию `None`.
- `last_n` (int, optional): Количество последних взаимодействий (самых недавних), которые следует учитывать в контексте. По умолчанию `None`.

**Как работает**:
- Конструктор проверяет тип цели (или целей) и сохраняет их в атрибуте `targets`.
- Устанавливает утверждение (`claim`), а также количество первых (`first_n`) и последних (`last_n`) взаимодействий для рассмотрения.
- Инициализирует атрибуты `value`, `justification` и `confidence` значениями `None`.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

# Пример с TinyWorld
world = TinyWorld(name='MyWorld')
proposition = Proposition(target=world, claim='The world is peaceful.')

# Пример с TinyPerson
person = TinyPerson(name='Alice')
proposition = Proposition(target=person, claim='Alice is happy.')

# Пример со списком целей
proposition = Proposition(target=[world, person], claim='Both are doing well.')
```

#### `__call__(self, additional_context=None)`

```python
    def __call__(self, additional_context=None):
        """ """
        return self.check(additional_context=additional_context)
```

**Назначение**: Позволяет вызывать объект `Proposition` как функцию, что эквивалентно вызову метода `check`.

**Параметры**:
- `additional_context` (str, optional): Дополнительный контекст для предоставления языковой модели. По умолчанию `None`.

**Возвращает**:
- Результат вызова метода `check`.

**Как работает**:
- Этот метод просто вызывает метод `check` с предоставленным дополнительным контекстом и возвращает результат.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

person = TinyPerson(name='Alice')
proposition = Proposition(target=person, claim='Alice is happy.')

# Вызов пропозиции как функции
result = proposition(additional_context='Alice received a gift.')
print(result)
```

#### `check(self, additional_context="No additional context available.")`

```python
    def check(self, additional_context="No additional context available."):
        """ """

        context = ""

        for target in self.targets:
            target_trajectory = target.pretty_current_interactions(max_content_length=None, first_n=self.first_n, last_n=self.last_n)

            if isinstance(target, TinyPerson):
                context += f"## Agent '{target.name}' Simulation Trajectory\\n\\n"
            elif isinstance(target, TinyWorld):
                context += f"## Environment '{target.name}' Simulation Trajectory\\n\\n"

            context += target_trajectory + "\\n\\n"

        llm_request = LLMRequest(system_prompt="""
                                    You are a system that evaluates whether a proposition is true or false with respect to a given context. This context
                                    always refers to a multi-agent simulation. The proposition is a claim about the behavior of the agents or the state of their environment
                                    in the simulation.
                                
                                    The context you receive can contain one or more of the following:
                                    - the trajectory of a simulation of one or more agents. This means what agents said, did, thought, or perceived at different times.
                                    - the state of the environment at a given time.
                                
                                    Your output **must**:\n
                                    - necessarily start with the word "True" or "False";\n
                                    - optionally be followed by a justification.\n
                                 \n
                                    For example, the output could be of the form: "True, because <REASON HERE>." or merely "True" if no justification is needed.\n
                                    """,

                                    user_prompt=f"""
                                    Evaluate the following proposition with respect to the context provided. Is it True or False?\n

                                    # Proposition\n

                                    This is the proposition you must evaluate:\n
                                    {self.claim}\n

                                    # Context\n

                                    The context you must consider is the following.\n

                                    {context}\n

                                    # Additional Context (if any)\n

                                    {additional_context}   \n
                                    """,

                                    output_type=bool)


        self.value = llm_request()
        self.justification = llm_request.response_justification
        self.confidence = llm_request.response_confidence

        self.raw_llm_response = llm_request.response_raw

        return self.value
```

**Назначение**: Проверяет пропозицию на основе контекста, извлеченного из целей, и дополнительного контекста, используя языковую модель (LLM).

**Параметры**:
- `additional_context` (str, optional): Дополнительный контекст для предоставления языковой модели. По умолчанию "No additional context available.".

**Возвращает**:
- `bool`: Значение пропозиции (True или False).

**Как работает**:
1. **Построение контекста**:
   - Создает контекст из траекторий целей (`TinyWorld` или `TinyPerson`).
   - Для каждой цели извлекает траекторию взаимодействий с помощью метода `pretty_current_interactions`.
   - Добавляет заголовок, указывающий тип цели ("Agent" или "Environment"), и траекторию в общий контекст.
2. **Формирование запроса к LLM**:
   - Создает объект `LLMRequest` с системным запросом, указывающим LLM оценивать истинность пропозиции на основе предоставленного контекста.
   - Формирует пользовательский запрос, включающий пропозицию, контекст и дополнительный контекст.
   - Указывает, что ожидаемый тип вывода - `bool`.
3. **Выполнение запроса к LLM**:
   - Вызывает объект `LLMRequest` для получения ответа от языковой модели.
   - Сохраняет значение пропозиции, обоснование и уверенность, полученные из ответа LLM, в атрибутах объекта `Proposition`.
4. **Возврат значения**:
   - Возвращает значение пропозиции (True или False).

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

person = TinyPerson(name='Alice')
proposition = Proposition(target=person, claim='Alice is happy.')

# Проверка пропозиции
result = proposition.check(additional_context='Alice received a gift.')
print(result)
```

## Функции

### `check_proposition(target, claim, additional_context="No additional context available.", first_n=None, last_n=None)`

```python
def check_proposition(target, claim:str, additional_context="No additional context available.",
                      first_n:int=None, last_n:int=None):
    """
    Check whether a propositional claim holds for the given target(s). This is meant as a
    convenience method to avoid creating a Proposition object (which you might not need
    if you are not interested in the justification or confidence of the claim, or will
    not use it again).

    Args:
        target (TinyWorld, TinyPerson, list): the target or targets of the proposition
        claim (str): the claim of the proposition
        additional_context (str): additional context to provide to the LLM
        first_n (int): the number of first interactions to consider in the context
        last_n (int): the number of last interactions (most recent) to consider in the context

    Returns:
        bool: whether the proposition holds for the given target(s)
    """
    ...
```

**Назначение**: Проверяет, выполняется ли пропозициональное утверждение для заданной цели (или целей). Это удобный метод, позволяющий избежать создания объекта `Proposition`, если нет необходимости в обосновании или уверенности утверждения, или если оно не будет использоваться повторно.

**Параметры**:
- `target` (TinyWorld, TinyPerson, list): Цель или цели пропозиции.
- `claim` (str): Утверждение пропозиции.
- `additional_context` (str, optional): Дополнительный контекст для предоставления LLM. По умолчанию "No additional context available.".
- `first_n` (int, optional): Количество первых взаимодействий для рассмотрения в контексте.
- `last_n` (int, optional): Количество последних взаимодействий (самых недавних) для рассмотрения в контексте.

**Возвращает**:
- `bool`: `True`, если пропозиция выполняется для заданной цели (или целей), `False` в противном случае.

**Как работает**:
1. **Создание объекта `Proposition`**:
   - Создает экземпляр класса `Proposition` с предоставленными целью, утверждением, `first_n` и `last_n`.
2. **Проверка пропозиции**:
   - Вызывает метод `check` объекта `Proposition` с предоставленным `additional_context`.
3. **Возврат значения**:
   - Возвращает результат проверки пропозиции.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

person = TinyPerson(name='Alice')

# Проверка пропозиции с использованием функции check_proposition
result = check_proposition(target=person, claim='Alice is happy.', additional_context='Alice received a gift.')
print(result)