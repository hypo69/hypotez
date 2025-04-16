# Модуль `tiny_person_factory.py`

## Обзор

Модуль `tiny_person_factory.py` предназначен для создания экземпляров класса `TinyPerson` с использованием OpenAI LLM. Он предоставляет функциональность для генерации как отдельных персонажей, так и списков персонажей на основе заданного контекста и параметров. Модуль включает в себя классы для управления процессом генерации, использования шаблонов и интеграции с OpenAI API.

## Подробней

Этот модуль является частью системы, где необходимо генерировать реалистичные симуляции людей. Он использует `TinyPersonFactory` для создания персонажей с уникальными характеристиками, именами и биографиями. `TinyPersonFactory` использует OpenAI LLM для генерации этих персонажей на основе заданного контекста.

## Классы

### `TinyPersonFactory`

**Описание**: Фабрика для создания экземпляров `TinyPerson`.

**Наследует**: `TinyFactory`

**Атрибуты**:
- `context_text` (str): Контекст, используемый для генерации персонажей.
- `person_prompt_template_path` (str): Путь к файлу шаблона для генерации запросов к OpenAI.
- `generated_minibios` (list): Список сгенерированных мини-биографий персонажей.
- `generated_names` (list): Список сгенерированных имен персонажей.

**Методы**:
- `__init__(self, context_text, simulation_id: str = None)`: Инициализирует экземпляр `TinyPersonFactory`.
- `generate_person_factories(number_of_factories, generic_context_text)`: Генерирует список экземпляров `TinyPersonFactory`.
- `generate_person(self, agent_particularities: str = None, temperature: float = 1.5, frequency_penalty: float = 0.0, presence_penalty: float = 0.0, attepmpts: int = 10)`: Генерирует экземпляр `TinyPerson` с использованием OpenAI LLM.
- `generate_people(self, number_of_people: int, agent_particularities: str = None, temperature: float = 1.5, frequency_penalty: float = 0.0, presence_penalty: float = 0.0, attepmpts: int = 10, verbose: bool = False) -> list`: Генерирует список экземпляров `TinyPerson` с использованием OpenAI LLM.
- `_aux_model_call(self, messages, temperature, frequency_penalty, presence_penalty)`: Вспомогательный метод для выполнения вызова модели OpenAI.
- `_setup_agent(self, agent, configuration)`: Настраивает агента с необходимыми элементами.

#### `__init__`
```python
def __init__(self, context_text, simulation_id:str=None):
    """
    Initialize a TinyPersonFactory instance.

    Args:
        context_text (str): The context text used to generate the TinyPerson instances.
        simulation_id (str, optional): The ID of the simulation. Defaults to None.
    """
```
- **Назначение**: Инициализирует экземпляр класса `TinyPersonFactory`.
- **Параметры**:
    - `context_text` (str): Контекст, используемый для генерации `TinyPerson`.
    - `simulation_id` (str, optional): Идентификатор симуляции. По умолчанию `None`.
- **Как работает функция**:
    - Вызывает конструктор родительского класса `TinyFactory` с параметром `simulation_id`.
    - Определяет путь к файлу шаблона для генерации персонажей (`person_prompt_template_path`).
    - Сохраняет переданный контекст (`context_text`) в атрибуте экземпляра класса.
    - Инициализирует пустые списки `generated_minibios` и `generated_names` для отслеживания сгенерированных персонажей и их имен, чтобы избежать повторной генерации.

#### `generate_person_factories`
```python
@staticmethod
def generate_person_factories(number_of_factories, generic_context_text):
    """
    Generate a list of TinyPersonFactory instances using OpenAI's LLM.

    Args:
        number_of_factories (int): The number of TinyPersonFactory instances to generate.
        generic_context_text (str): The generic context text used to generate the TinyPersonFactory instances.

    Returns:
        list: A list of TinyPersonFactory instances.
    """
```
- **Назначение**: Генерирует список экземпляров `TinyPersonFactory` с использованием OpenAI LLM.
- **Параметры**:
    - `number_of_factories` (int): Количество экземпляров `TinyPersonFactory` для генерации.
    - `generic_context_text` (str): Общий контекст, используемый для генерации экземпляров `TinyPersonFactory`.
- **Возвращает**:
    - `list`: Список экземпляров `TinyPersonFactory`.
    - `None`: Если ответ от OpenAI API равен `None`.
- **Как работает функция**:
    - Логирует начало процесса генерации фабрик персонажей.
    - Читает системный промпт из файла `prompts/generate_person_factory.md`.
    - Формирует пользовательский промпт на основе шаблона с использованием библиотеки `chevron`.
    - Отправляет сообщение в OpenAI API и извлекает JSON из ответа.
    - Создает экземпляры `TinyPersonFactory` на основе извлеченных данных и возвращает их в виде списка.
    - Логирует описание каждой созданной фабрики.

#### `generate_person`
```python
def generate_person(self, 
                    agent_particularities:str=None, 
                    temperature:float=1.5, 
                    frequency_penalty:float=0.0,
                    presence_penalty:float=0.0, 
                    attepmpts:int=10):
    """
    Generate a TinyPerson instance using OpenAI's LLM.

    Args:
        agent_particularities (str): The particularities of the agent.
        temperature (float): The temperature to use when sampling from the LLM.

    Returns:
        TinyPerson: A TinyPerson instance generated using the LLM.
    """
```
- **Назначение**: Генерирует экземпляр `TinyPerson` с использованием OpenAI LLM.
- **Параметры**:
    - `agent_particularities` (str, optional): Особенности агента. По умолчанию `None`.
    - `temperature` (float, optional): Температура для выборки из LLM. По умолчанию `1.5`.
    - `frequency_penalty` (float, optional): Штраф за частоту. По умолчанию `0.0`.
    - `presence_penalty` (float, optional): Штраф за присутствие. По умолчанию `0.0`.
    - `attepmpts` (int, optional): Количество попыток генерации. По умолчанию `10`.
- **Возвращает**:
    - `TinyPerson`: Экземпляр `TinyPerson`, сгенерированный с использованием LLM.
    - `None`: Если не удалось сгенерировать персонажа после нескольких попыток.
- **Как работает функция**:
    - Логирует начало процесса генерации персонажа.
    - Загружает примеры спецификаций агентов из файлов `Friedrich_Wolf.agent.json` и `Sophie_Lefevre.agent.json`.
    - Формирует промпт на основе шаблона с использованием библиотеки `chevron`.
    - Определяет внутреннюю функцию `aux_generate` для выполнения фактического вызова модели, чтобы можно было использовать декоратор `transactional`.
        - Внутренняя функция `aux_generate(attempt)`:
            - Формирует сообщения для OpenAI API.
            - Вызывает метод `_aux_model_call` для получения ответа от OpenAI API.
            - Извлекает JSON из ответа.
            - Проверяет, что имя сгенерированного персонажа не повторяется.
    - Пытается сгенерировать спецификацию агента несколько раз, пока не будет получен подходящий результат.
    - Создает экземпляр `TinyPerson` на основе сгенерированной спецификации и настраивает его с использованием метода `_setup_agent`.
    - Добавляет мини-биографию и имя персонажа в списки `generated_minibios` и `generated_names` соответственно.
    - В случае ошибки логирует сообщение об ошибке.

#### `generate_people`
```python
def generate_people(self, number_of_people:int, 
                    agent_particularities:str=None, 
                    temperature:float=1.5, 
                    frequency_penalty:float=0.0,
                    presence_penalty:float=0.0,
                    attepmpts:int=10, 
                    verbose:bool=False) -> list:
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
```
- **Назначение**: Генерирует список экземпляров `TinyPerson` с использованием OpenAI LLM.
- **Параметры**:
    - `number_of_people` (int): Количество экземпляров `TinyPerson` для генерации.
    - `agent_particularities` (str, optional): Особенности агента. По умолчанию `None`.
    - `temperature` (float, optional): Температура для выборки из LLM. По умолчанию `1.5`.
    - `frequency_penalty` (float, optional): Штраф за частоту. По умолчанию `0.0`.
    - `presence_penalty` (float, optional): Штраф за присутствие. По умолчанию `0.0`.
    - `attepmpts` (int, optional): Количество попыток генерации. По умолчанию `10`.
    - `verbose` (bool, optional): Флаг для вывода подробной информации. По умолчанию `False`.
- **Возвращает**:
    - `list`: Список экземпляров `TinyPerson`, сгенерированных с использованием LLM.
- **Как работает функция**:
    - Итерирует указанное количество раз (`number_of_people`).
    - На каждой итерации вызывает метод `generate_person` для генерации одного персонажа.
    - Добавляет сгенерированного персонажа в список `people`.
    - Логирует информацию о сгенерированном персонаже.
    - В случае ошибки логирует сообщение об ошибке.

#### `_aux_model_call`
```python
@transactional
def _aux_model_call(self, messages, temperature, frequency_penalty, presence_penalty):
    """
    Auxiliary method to make a model call. This is needed in order to be able to use the transactional decorator,
    due too a technicality - otherwise, the agent creation would be skipped during cache reutilization, and
    we don't want that.
    """
```
- **Назначение**: Вспомогательный метод для выполнения вызова модели OpenAI.
- **Параметры**:
    - `messages` (list): Список сообщений для отправки в OpenAI API.
    - `temperature` (float): Температура для выборки из LLM.
    - `frequency_penalty` (float): Штраф за частоту.
    - `presence_penalty` (float): Штраф за присутствие.
- **Возвращает**:
    - Ответ от OpenAI API.
- **Как работает функция**:
    - Вызывает метод `send_message` из модуля `openai_utils` для отправки сообщения в OpenAI API с указанными параметрами.
    - Используется декоратор `@transactional` для кэширования результатов вызова модели.

#### `_setup_agent`
```python
@transactional
def _setup_agent(self, agent, configuration):
    """
    Sets up the agent with the necessary elements.
    """
```
- **Назначение**: Настраивает агента с необходимыми элементами.
- **Параметры**:
    - `agent` (TinyPerson): Экземпляр агента для настройки.
    - `configuration` (dict): Конфигурация агента.
- **Возвращает**:
    - Ничего (None).
- **Как работает функция**:
    - Вызывает метод `include_persona_definitions` агента для включения определений персонажа.
    - Не возвращает ничего, чтобы избежать кэширования объекта агента.

## Параметры класса

- `context_text` (str): Контекст, используемый для генерации персонажей.
- `person_prompt_template_path` (str): Путь к файлу шаблона для генерации запросов к OpenAI.
- `generated_minibios` (list): Список сгенерированных мини-биографий персонажей.
- `generated_names` (list): Список сгенерированных имен персонажей.

## Примеры

### Создание экземпляра `TinyPersonFactory`

```python
from tinytroupe.factory.tiny_person_factory import TinyPersonFactory

factory = TinyPersonFactory(context_text="Some context")
```

### Генерация списка `TinyPersonFactory`

```python
from tinytroupe.factory.tiny_person_factory import TinyPersonFactory

factories = TinyPersonFactory.generate_person_factories(number_of_factories=2, generic_context_text="Generic context")
```

### Генерация `TinyPerson`

```python
from tinytroupe.factory.tiny_person_factory import TinyPersonFactory

factory = TinyPersonFactory(context_text="Some context")
person = factory.generate_person(agent_particularities="Some particularities")
```

### Генерация списка `TinyPerson`

```python
from tinytroupe.factory.tiny_person_factory import TinyPersonFactory

factory = TinyPersonFactory(context_text="Some context")
people = factory.generate_people(number_of_people=2, agent_particularities="Some particularities")
```