# Модуль factory.py

## Обзор

Модуль `factory.py` предоставляет классы и функции для создания экземпляров агентов (`TinyPerson`) в рамках симуляции. Он содержит фабрики, которые генерируют агентов на основе заданного контекста и обеспечивают уникальность создаваемых персонажей. Модуль также включает механизмы кэширования для оптимизации производительности.

## Подробней

Этот модуль играет важную роль в проекте `hypotez`, поскольку он отвечает за создание и конфигурацию агентов, которые взаимодействуют в симуляции. Он использует OpenAI LLM для генерации персонажей на основе заданного контекста и обеспечивает уникальность этих персонажей. Модуль также включает механизмы кэширования для оптимизации производительности.

## Классы

### `TinyFactory`

**Описание**: Базовый класс для различных типов фабрик. Он обеспечивает основу для расширения системы, особенно в отношении кэширования транзакций.

**Атрибуты**:
- `all_factories` (dict): Словарь всех созданных фабрик (имя -> фабрика).
- `name` (str): Имя фабрики.
- `simulation_id` (str): Идентификатор симуляции, к которой принадлежит фабрика.

**Методы**:
- `__init__(self, simulation_id: str = None) -> None`: Инициализирует экземпляр `TinyFactory`.
- `__repr__(self)`: Возвращает строковое представление объекта `TinyFactory`.
- `set_simulation_for_free_factories(simulation)`: Назначает симуляцию фабрикам, у которых еще нет идентификатора симуляции.
- `add_factory(factory)`: Добавляет фабрику в список всех фабрик.
- `clear_factories()`: Очищает глобальный список всех фабрик.
- `encode_complete_state() -> dict`: Кодирует полное состояние фабрики для кэширования.
- `decode_complete_state(state: dict)`: Декодирует состояние фабрики из кэша.

#### `__init__`

```python
def __init__(self, simulation_id: str = None) -> None:
    """
    Инициализирует экземпляр TinyFactory.

    Args:
        simulation_id (str, optional): ID симуляции. По умолчанию None.
    """
    ...
```
#### `set_simulation_for_free_factories`

```python
@staticmethod
def set_simulation_for_free_factories(simulation):
    """
    Устанавливает симуляцию, если она None. Это позволяет захватывать свободные среды определенными областями симуляции,
    если это необходимо.
    """
    ...
```

#### `add_factory`

```python
@staticmethod
def add_factory(factory):
    """
    Добавляет фабрику в список всех фабрик. Имена фабрик должны быть уникальными,
    поэтому, если фабрика с таким же именем уже существует, возникает ошибка.
    """
    ...
```

#### `clear_factories`

```python
@staticmethod
def clear_factories():
    """
    Очищает глобальный список всех фабрик.
    """
    ...
```

#### `encode_complete_state`

```python
def encode_complete_state(self) -> dict:
    """
    Кодирует полное состояние фабрики. Если подклассы имеют элементы, которые не сериализуются, они должны переопределить этот метод.
    """
    ...
```

#### `decode_complete_state`

```python
def decode_complete_state(self, state: dict):
    """
    Декодирует полное состояние фабрики. Если подклассы имеют элементы, которые не сериализуются, они должны переопределить этот метод.
    """
    ...
```

### `TinyPersonFactory`

**Описание**: Класс, который создает экземпляры `TinyPerson` на основе заданного контекста, используя OpenAI LLM.

**Наследует**: `TinyFactory`

**Атрибуты**:
- `person_prompt_template_path` (str): Путь к шаблону mustache для генерации промпта персонажа.
- `context_text` (str): Контекстный текст, используемый для генерации экземпляров `TinyPerson`.
- `generated_minibios` (list): Список сгенерированных мини-биографий, чтобы избежать повторной генерации одного и того же персонажа.
- `generated_names` (list): Список сгенерированных имен, чтобы обеспечить уникальность имен.

**Методы**:
- `__init__(self, context_text, simulation_id: str = None)`: Инициализирует экземпляр `TinyPersonFactory`.
- `generate_person_factories(number_of_factories, generic_context_text)`: Генерирует список экземпляров `TinyPersonFactory` с использованием OpenAI LLM.
- `generate_person(self, agent_particularities: str = None, temperature: float = 1.5, attepmpts: int = 5)`: Генерирует экземпляр `TinyPerson` с использованием OpenAI LLM.
- `_aux_model_call(self, messages, temperature)`: Вспомогательный метод для выполнения вызова модели.
- `_setup_agent(self, agent, configuration)`: Настраивает агента с необходимыми элементами.

#### `__init__`

```python
def __init__(self, context_text, simulation_id: str = None):
    """
    Инициализирует экземпляр TinyPersonFactory.

    Args:
        context_text (str): Контекстный текст, используемый для генерации экземпляров TinyPerson.
        simulation_id (str, optional): ID симуляции. По умолчанию None.
    """
    ...
```

#### `generate_person_factories`

```python
@staticmethod
def generate_person_factories(number_of_factories, generic_context_text):
    """
    Генерирует список экземпляров TinyPersonFactory, используя LLM OpenAI.

    Args:
        number_of_factories (int): Количество экземпляров TinyPersonFactory для генерации.
        generic_context_text (str): Общий контекстный текст, используемый для генерации экземпляров TinyPersonFactory.

    Returns:
        list: Список экземпляров TinyPersonFactory.
    """
    ...
```

#### `generate_person`

```python
def generate_person(self, agent_particularities: str = None, temperature: float = 1.5, attepmpts: int = 5):
    """
    Генерирует экземпляр TinyPerson, используя LLM OpenAI.

    Args:
        agent_particularities (str): Особенности агента.
        temperature (float): Температура, используемая при выборке из LLM.

    Returns:
        TinyPerson: Экземпляр TinyPerson, сгенерированный с использованием LLM.
    """
    ...
```
Внутри данной функции `generate_person` определена вложенная функция `aux_generate`. Рассмотрим ее подробнее.
##### `aux_generate`
```python
def aux_generate():
    """
    Вспомогательная функция для генерации агента.

    Returns:
        dict | None: Спецификация агента, если он был успешно сгенерирован, иначе None.
    """
    messages = []
    messages += [{"role": "system", "content": "You are a system that generates specifications of artificial entities."},
                {"role": "user", "content": prompt}]

    # due to a technicality, we need to call an auxiliary method to be able to use the transactional decorator.
    message = self._aux_model_call(messages=messages, temperature=temperature)

    if message is not None:
        result = utils.extract_json(message["content"])

        logger.debug(f"Generated person parameters:\n{json.dumps(result, indent=4, sort_keys=True)}")

        # only accept the generated spec if the name is not already in the generated names, because they must be unique.
        if result["name"].lower() not in self.generated_names:
            return result

    return None # no suitable agent was generated
```

#### `_aux_model_call`

```python
@transactional
def _aux_model_call(self, messages, temperature):
    """
    Вспомогательный метод для выполнения вызова модели. Это необходимо для того, чтобы иметь возможность использовать декоратор transactional,
    из-за технической детали - в противном случае создание агента будет пропущено во время повторного использования кэша, и
    мы не хотим этого.
    """
    ...
```

#### `_setup_agent`

```python
@transactional
def _setup_agent(self, agent, configuration):
    """
    Настраивает агента с необходимыми элементами.
    """
    ...
```

## Примеры

### Создание фабрики и генерация персонажа

```python
from tinytroupe.factory import TinyPersonFactory

# Создание фабрики
factory = TinyPersonFactory(context_text="A person living in a small town.")

# Генерация персонажа
person = factory.generate_person(agent_particularities="A friendly neighbor.")

if person:
    print(f"Generated person: {person.get('name')}")
```
```python
from tinytroupe.factory import TinyPersonFactory

# Пример генерации нескольких фабрик персонажей
number_of_factories = 3
generic_context_text = "Описание общего контекста для фабрик."
factories = TinyPersonFactory.generate_person_factories(number_of_factories, generic_context_text)

if factories:
    for factory in factories:
        print(f"Создана фабрика персонажей: {factory}")
```
```python
import os
import json
from tinytroupe.agent import TinyPerson
from tinytroupe.factory import TinyPersonFactory

# Пример использования с сохранением и загрузкой состояния фабрики
# (предполагается, что transactional и utils.save/load определены)

# 1. Создание и настройка фабрики
factory = TinyPersonFactory(context_text="Описание контекста")
#person = factory.generate_person()  # сгенерируем персонажа один раз

# 2. Кодирование состояния
state = factory.encode_complete_state()

# utils.save(state, "factory_state.json") # сохнанение не возможно так как нет метода save

# 3. Загрузка состояния (имитация)
#loaded_state = utils.load("factory_state.json")
#loaded_factory = TinyPersonFactory(context_text="Описание контекста").decode_complete_state(state)

# 4. Проверка
# После загрузки можно продолжить генерировать новых персонажей
#person2 = loaded_factory.generate_person()
#if person2:
#    print(f"Сгенерирован персонаж: {person2.get('name')}")
```
```python
# Пример использования _setup_agent для настройки персонажа после генерации

from tinytroupe.factory import TinyPersonFactory
from tinytroupe.agent import TinyPerson

# 1. Создание фабрики
factory = TinyPersonFactory(context_text="Описание контекста")

# 2. Пример конфигурации (в реальном коде она может генерироваться)
configuration = {
    "ключ1": "значение1",
    "ключ2": ["значение2_1", "значение2_2"]
}

# 3. Создание и настройка агента
agent = TinyPerson("Имя")
factory._setup_agent(agent, configuration)

# 4. Теперь у агента должны быть определены атрибуты
print(agent.get("ключ1"))
print(agent.get("ключ2"))