# Модуль TinyFactory

## Обзор

Модуль `factory.py` предоставляет классы для создания и управления агентами в системе `TinyTroupe`. 

## Подробней

Модуль содержит два класса:

* `TinyFactory`: Базовый класс для различных типов фабрик.
* `TinyPersonFactory`: Фабрика, которая генерирует агентов типа `TinyPerson`.

## Классы

### `TinyFactory`

**Описание**: Базовый класс для различных типов фабрик.

**Атрибуты**:

* `name` (str): Имя фабрики.
* `simulation_id` (str, optional): Идентификатор симуляции. По умолчанию `None`.

**Методы**:

* `__init__(self, simulation_id:str=None) -> None`: Инициализирует экземпляр `TinyFactory`.
* `__repr__(self) -> str`: Возвращает строковое представление объекта.
* `set_simulation_for_free_factories(simulation)`: Устанавливает симуляцию, если она равна `None`. 
* `add_factory(factory)`: Добавляет фабрику в список всех фабрик.
* `clear_factories()`: Очищает глобальный список всех фабрик.
* `encode_complete_state(self) -> dict`: Кодирует полное состояние фабрики.
* `decode_complete_state(self, state:dict)`: Декодирует полное состояние фабрики.

**Принцип работы**: 

Класс `TinyFactory` является базовым классом для различных типов фабрик. Он обеспечивает механизм для хранения и управления фабриками.
* `all_factories` (dict): Хранит список всех созданных фабрик.
* `encode_complete_state(self) -> dict`: Метод для кодирования состояния фабрики в виде словаря.
* `decode_complete_state(self, state:dict)`: Метод для декодирования состояния фабрики из словаря.

### `TinyPersonFactory`

**Описание**: Фабрика, которая генерирует агентов типа `TinyPerson`.

**Атрибуты**:

* `context_text` (str): Контекстный текст, используемый для генерации экземпляров `TinyPerson`.
* `simulation_id` (str, optional): Идентификатор симуляции. По умолчанию `None`.
* `person_prompt_template_path` (str): Путь к шаблону запроса для генерации персонажей.
* `generated_minibios` (list): Список сгенерированных мини-био.
* `generated_names` (list): Список сгенерированных имен.

**Методы**:

* `__init__(self, context_text, simulation_id:str=None)`: Инициализирует экземпляр `TinyPersonFactory`.
* `generate_person_factories(number_of_factories, generic_context_text)`: Генерация списка фабрик `TinyPersonFactory` с использованием LLM от OpenAI.
* `generate_person(self, agent_particularities:str=None, temperature:float=1.5, attepmpts:int=5)`: Генерация экземпляра `TinyPerson` с использованием LLM от OpenAI.
* `_aux_model_call(self, messages, temperature)`: Вспомогательный метод для вызова модели. 
* `_setup_agent(self, agent, configuration)`: Настраивает агента необходимыми элементами.

**Принцип работы**:

Класс `TinyPersonFactory` использует LLM от OpenAI для генерации агентов типа `TinyPerson`. 
* `generate_person(self, agent_particularities:str=None, temperature:float=1.5, attepmpts:int=5)`: Метод, который использует шаблон запроса `generate_person.mustache`, чтобы сгенерировать спецификацию агента `TinyPerson`. 
* `_setup_agent(self, agent, configuration)`: Метод, который настраивает агента `TinyPerson` с использованием полученной спецификации, определяя его характеристики (например, "name", "profession").

**Примеры**:

```python
# Создание фабрики персонажей
factory = TinyPersonFactory("Описание контекста")

# Генерация персонажа
person = factory.generate_person()

# Получение имени персонажа
name = person.get("name")

# Вывод имени
print(f"Сгенерирован персонаж с именем: {name}")
```

## Внутренние функции

### `_aux_model_call(self, messages, temperature)`

**Описание**: Вспомогательный метод для вызова модели OpenAI.

**Параметры**:

* `messages` (list): Список сообщений для отправки в модель.
* `temperature` (float): Температура для выборки из модели.

**Возвращает**:

* `dict | None`: Ответ от модели или `None`, если произошла ошибка.

**Как работает функция**: 

Функция `_aux_model_call` отправляет список сообщений в модель OpenAI и возвращает ответ. Она используется внутри метода `generate_person`, чтобы генерировать характеристики персонажа.

### `_setup_agent(self, agent, configuration)`

**Описание**: Настраивает агента с помощью предоставленной спецификации.

**Параметры**:

* `agent` (TinyPerson): Экземпляр агента `TinyPerson`, который нужно настроить.
* `configuration` (dict): Спецификация агента.

**Как работает функция**:

Функция `_setup_agent` добавляет характеристики из спецификации к агенту `TinyPerson`. Она используется внутри метода `generate_person`, чтобы завершить создание агента после генерации его характеристик. 

## Параметры класса

* `context_text` (str): Контекстный текст, который используется для генерации экземпляров `TinyPerson`. 
* `simulation_id` (str, optional): Идентификатор симуляции.
* `person_prompt_template_path` (str): Путь к шаблону запроса для генерации персонажей.
* `generated_minibios` (list): Список сгенерированных мини-био.
* `generated_names` (list): Список сгенерированных имен.

## Примеры

**Пример 1**: Создание фабрики персонажей и генерация персонажа с именем

```python
# Создание фабрики персонажей
factory = TinyPersonFactory("Описание контекста")

# Генерация персонажа
person = factory.generate_person()

# Получение имени персонажа
name = person.get("name")

# Вывод имени
print(f"Сгенерирован персонаж с именем: {name}")
```

**Пример 2**: Генерация нескольких фабрик персонажей

```python
# Генерация 5 фабрик персонажей
factories = TinyPersonFactory.generate_person_factories(5, "Описание контекста")

# Вывод имен всех сгенерированных персонажей
for factory in factories:
    person = factory.generate_person()
    print(f"Сгенерирован персонаж с именем: {person.get('name')}")
```