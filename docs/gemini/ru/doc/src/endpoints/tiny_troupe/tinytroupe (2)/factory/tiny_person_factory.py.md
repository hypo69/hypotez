# Модуль `tiny_person_factory.py`

## Обзор

Модуль предоставляет класс `TinyPersonFactory`, который используется для генерации экземпляров класса `TinyPerson` с использованием OpenAI LLM. Он позволяет создавать персонажей с заданными характеристиками на основе контекста, указанного в текстовом формате.

## Подробней

Модуль содержит класс `TinyPersonFactory`, который является фабрикой для создания объектов `TinyPerson`. Он использует OpenAI LLM для генерации персонажей на основе заданного контекста. Класс имеет методы для генерации как одного персонажа, так и списка персонажей. Также, класс включает механизм для предотвращения повторной генерации одинаковых персонажей. Для работы с OpenAI используется модуль `openai_utils`, а для логирования - модуль `logger` из `src.logger`.
В данном коде используется декоратор `@transactional`, который позволяет обеспечить транзакционность операций.

## Классы

### `TinyPersonFactory`

**Описание**: Фабрика для создания экземпляров класса `TinyPerson` с использованием OpenAI LLM.

**Наследует**:

- `TinyFactory`: Класс `TinyPersonFactory` наследует функциональность от класса `TinyFactory`.

**Атрибуты**:

- `person_prompt_template_path (str)`: Путь к шаблону mustache, используемому для генерации запроса к LLM.
- `context_text (str)`: Контекст, используемый для генерации персонажей.
- `generated_minibios (list)`: Список сгенерированных мини-биографий, чтобы избежать повторной генерации тех же персонажей.
- `generated_names (list)`: Список сгенерированных имен, чтобы избежать повторной генерации персонажей с одинаковыми именами.

**Методы**:

- `__init__(self, context_text: str, simulation_id: str = None)`: Инициализирует экземпляр класса `TinyPersonFactory`.
- `generate_person_factories(number_of_factories: int, generic_context_text: str) -> list`: Генерирует список экземпляров `TinyPersonFactory` с использованием OpenAI LLM.
- `generate_person(self, agent_particularities: str = None, temperature: float = 1.5, frequency_penalty: float = 0.0, presence_penalty: float = 0.0, attepmpts: int = 10) -> TinyPerson`: Генерирует экземпляр `TinyPerson` с использованием OpenAI LLM.
- `generate_people(self, number_of_people: int, agent_particularities: str = None, temperature: float = 1.5, frequency_penalty: float = 0.0, presence_penalty: float = 0.0, attepmpts: int = 10, verbose: bool = False) -> list`: Генерирует список экземпляров `TinyPerson` с использованием OpenAI LLM.
- `_aux_model_call(self, messages: list, temperature: float, frequency_penalty: float, presence_penalty: float) -> dict`: Вспомогательный метод для выполнения вызова модели.
- `_setup_agent(self, agent: TinyPerson, configuration: dict)`: Настраивает агента с необходимыми элементами.

### `__init__`

```python
def __init__(self, context_text: str, simulation_id: str = None):
    """
    Initialize a TinyPersonFactory instance.

    Args:
        context_text (str): The context text used to generate the TinyPerson instances.
        simulation_id (str, optional): The ID of the simulation. Defaults to None.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `TinyPersonFactory`.

**Параметры**:

- `context_text (str)`: Контекст, используемый для генерации экземпляров `TinyPerson`.
- `simulation_id (str, optional)`: ID симуляции. По умолчанию `None`.

**Как работает функция**:

- Вызывает конструктор родительского класса `TinyFactory` с параметром `simulation_id`.
- Определяет путь к шаблону `generate_person.mustache`.
- Сохраняет `context_text` в атрибуте `self.context_text`.
- Инициализирует пустой список `self.generated_minibios` для хранения сгенерированных мини-биографий.
- Инициализирует пустой список `self.generated_names` для хранения сгенерированных имен.

**Примеры**:

```python
factory = TinyPersonFactory(context_text="Some context", simulation_id="123")
```

### `generate_person_factories`

```python
@staticmethod
def generate_person_factories(number_of_factories: int, generic_context_text: str) -> list:
    """
    Generate a list of TinyPersonFactory instances using OpenAI's LLM.

    Args:
        number_of_factories (int): The number of TinyPersonFactory instances to generate.
        generic_context_text (str): The generic context text used to generate the TinyPersonFactory instances.

    Returns:
        list: A list of TinyPersonFactory instances.
    """
    ...
```

**Назначение**: Генерирует список экземпляров `TinyPersonFactory` с использованием OpenAI LLM.

**Параметры**:

- `number_of_factories (int)`: Количество экземпляров `TinyPersonFactory` для генерации.
- `generic_context_text (str)`: Общий контекст, используемый для генерации экземпляров `TinyPersonFactory`.

**Как работает функция**:

1. Логирует начало генерации фабрик персонажей на основе заданного контекста.
2. Открывает и считывает содержимое файла `prompts/generate_person_factory.md`, который содержит системный промт для OpenAI.
3. Формирует сообщение для OpenAI, содержащее запрос на создание указанного количества описаний персонажей на основе заданного контекста.
4. Отправляет сообщение в OpenAI LLM с использованием `openai_utils.client().send_message(messages)`.
5. Извлекает JSON из ответа OpenAI.
6. Создает список экземпляров `TinyPersonFactory`, используя извлеченные описания.
7. Логирует процесс генерации каждой фабрики персонажей.
8. Возвращает список созданных фабрик.

**Примеры**:

```python
factories = TinyPersonFactory.generate_person_factories(number_of_factories=2, generic_context_text="Generic context")
```

### `generate_person`

```python
def generate_person(self,
                    agent_particularities: str = None,
                    temperature: float = 1.5,
                    frequency_penalty: float = 0.0,
                    presence_penalty: float = 0.0,
                    attepmpts: int = 10) -> TinyPerson:
    """
    Generate a TinyPerson instance using OpenAI's LLM.

    Args:
        agent_particularities (str): The particularities of the agent.
        temperature (float): The temperature to use when sampling from the LLM.

    Returns:
        TinyPerson: A TinyPerson instance generated using the LLM.
    """
    ...
```

**Назначение**: Генерирует экземпляр `TinyPerson` с использованием OpenAI LLM.

**Параметры**:

- `agent_particularities (str, optional)`: Особенности агента. По умолчанию `None`.
- `temperature (float, optional)`: Температура для использования при выборке из LLM. По умолчанию `1.5`.
- `frequency_penalty (float, optional)`: Штраф за частоту. По умолчанию `0.0`.
- `presence_penalty (float, optional)`: Штраф за присутствие. По умолчанию `0.0`.
- `attepmpts (int, optional)`: Количество попыток. По умолчанию `10`.

**Как работает функция**:

1.  Логирует начало генерации персонажа на основе заданного контекста.
2.  Загружает примеры спецификаций агентов из файлов `Friedrich_Wolf.agent.json` и `Sophie_Lefevre.agent.json`.
3.  Формирует промт для OpenAI, используя шаблон из файла `self.person_prompt_template_path`. Промт включает контекст, особенности агента, примеры спецификаций и список уже сгенерированных имен.
4.  Определяет внутреннюю функцию `aux_generate(attempt)`, которая отправляет запрос в OpenAI и извлекает спецификацию персонажа из ответа.
    -   Внутренняя функция `aux_generate(attempt)`:
        -   Формирует список сообщений для отправки в OpenAI, включая системное сообщение и пользовательский промт.
        -   Если это не первая попытка генерации, добавляет дополнительное сообщение с требованием уникальности имени.
        -   Вызывает метод `self._aux_model_call` для отправки запроса в OpenAI.
        -   Если ответ получен, извлекает JSON из ответа и проверяет уникальность имени.
        -   Если имя уникально, возвращает спецификацию персонажа.
        -   Иначе, логирует сообщение о повторном использовании имени.
5.  Вызывает `aux_generate(attempt)` в цикле до тех пор, пока не будет сгенерирована подходящая спецификация или не будет достигнуто максимальное количество попыток.
6.  Если спецификация сгенерирована, создает экземпляр `TinyPerson`, настраивает его с использованием `self._setup_agent`, добавляет мини-биографию в `self.generated_minibios`, добавляет имя в `self.generated_names` и возвращает созданного персонажа.
7.  Если после всех попыток не удалось сгенерировать персонажа, логирует сообщение об ошибке и возвращает `None`.

### `generate_people`

```python
def generate_people(self, number_of_people: int,
                    agent_particularities: str = None,
                    temperature: float = 1.5,
                    frequency_penalty: float = 0.0,
                    presence_penalty: float = 0.0,
                    attepmpts: int = 10,
                    verbose: bool = False) -> list:
    """
    Generate a list of TinyPerson instances using OpenAI's LLM.

    Args:
        number_of_people (int): The number of TinyPerson instances to generate.
        agent_particularities (str): The particularities of the agent.
        temperature (float): The temperature to use when sampling from the LLM.
        verbose (bool): Whether to print verbose information.

    Returns:
        list: A list of TinyPerson instances generated using the LLM.
    """
    ...
```

**Назначение**: Генерирует список экземпляров `TinyPerson` с использованием OpenAI LLM.

**Параметры**:

-   `number_of_people (int)`: Количество экземпляров `TinyPerson` для генерации.
-   `agent_particularities (str, optional)`: Особенности агента. По умолчанию `None`.
-   `temperature (float, optional)`: Температура для использования при выборке из LLM. По умолчанию `1.5`.
-   `frequency_penalty (float, optional)`: Штраф за частоту. По умолчанию `0.0`.
-   `presence_penalty (float, optional)`: Штраф за присутствие. По умолчанию `0.0`.
-   `attepmpts (int, optional)`: Количество попыток. По умолчанию `10`.
-   `verbose (bool, optional)`: Определяет, выводить ли подробную информацию. По умолчанию `False`.

**Как работает функция**:

1.  Инициализирует пустой список `people` для хранения сгенерированных персонажей.
2.  В цикле генерирует указанное количество персонажей с использованием метода `self.generate_person`.
3.  Если персонаж успешно сгенерирован, добавляет его в список `people`, логирует информацию о сгенерированном персонаже и, если `verbose` установлен в `True`, выводит информацию в консоль.
4.  Если не удалось сгенерировать персонажа, логирует сообщение об ошибке.
5.  Возвращает список сгенерированных персонажей.

**Примеры**:

```python
people = factory.generate_people(number_of_people=3, agent_particularities="Some particularities", verbose=True)
```

### `_aux_model_call`

```python
@transactional
def _aux_model_call(self, messages, temperature, frequency_penalty, presence_penalty):
    """
    Auxiliary method to make a model call. This is needed in order to be able to use the transactional decorator,
    due too a technicality - otherwise, the agent creation would be skipped during cache reutilization, and
    we don't want that.
    """
    ...
```

**Назначение**: Вспомогательный метод для выполнения вызова модели.

**Параметры**:

-   `messages (list)`: Список сообщений для отправки в OpenAI.
-   `temperature (float)`: Температура для использования при выборке из LLM.
-   `frequency_penalty (float)`: Штраф за частоту.
-   `presence_penalty (float)`: Штраф за присутствие.

**Как работает функция**:

1. Отправляет сообщение в OpenAI LLM с использованием `openai_utils.client().send_message()`.
2. Параметры `temperature`, `frequency_penalty` и `presence_penalty` передаются в вызов OpenAI.
3. Параметр `response_format={"type": "json_object"}` указывает, что ожидается ответ в формате JSON.
4. Возвращает ответ от OpenAI.
**Примеры**:

```python
response = self._aux_model_call(messages=messages, temperature=0.7, frequency_penalty=0.5, presence_penalty=0.5)
```

### `_setup_agent`

```python
@transactional
def _setup_agent(self, agent, configuration):
    """
    Sets up the agent with the necessary elements.
    """
    ...
```

**Назначение**: Настраивает агента с необходимыми элементами.

**Параметры**:

-   `agent (TinyPerson)`: Экземпляр `TinyPerson` для настройки.
-   `configuration (dict)`: Конфигурация агента.

**Как работает функция**:

1.  Включает определения персонажа в агента с использованием `agent.include_persona_definitions(configuration)`.
2.  Не возвращает ничего, так как не нужно кэшировать сам объект агента.

**Примеры**:

```python
self._setup_agent(person, agent_spec)
```