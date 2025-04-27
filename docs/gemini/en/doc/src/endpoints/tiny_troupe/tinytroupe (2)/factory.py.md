# Модуль TinyFactory
## Обзор

Модуль `factory.py` предоставляет базовый класс `TinyFactory` для создания различных типов фабрик в системе `TinyTroupe`. Этот модуль также включает `TinyPersonFactory` для создания объектов `TinyPerson` - персонажей, которые будут использоваться в симуляции. 

## Детали

Модуль `factory.py`  является важной частью системы `TinyTroupe`, так как он отвечает за создание объектов, которые будут использоваться в симуляции. 

## Классы
### `class TinyFactory`
**Описание**: Базовый класс для различных типов фабрик, используемых в TinyTroupe.

**Inherits**: 
- Ни от чего не наследуется

**Attributes**: 
- `name` (str): Имя фабрики, генерируемое автоматически, используя `utils.fresh_id()`. 
- `simulation_id` (str): Идентификатор симуляции, к которой принадлежит фабрика (может быть `None`).

**Methods**: 
- `__init__(self, simulation_id: str = None) -> None`: Инициализирует экземпляр класса `TinyFactory`. 
- `__repr__(self)`: Возвращает строковое представление объекта фабрики.
- `set_simulation_for_free_factories(simulation)`: Статический метод, который устанавливает симуляцию для фабрик, у которых `simulation_id` равен `None`. 
- `add_factory(factory)`: Статический метод, который добавляет фабрику в список всех фабрик. 
- `clear_factories()`: Статический метод, который очищает глобальный список всех фабрик. 
- `encode_complete_state(self) -> dict`: Кодирует полное состояние фабрики. 
- `decode_complete_state(self, state: dict)`: Декодирует полное состояние фабрики. 

**Как работает**: 
- Класс `TinyFactory` обеспечивает общий интерфейс для всех типов фабрик. 
- Он позволяет создавать фабрики с уникальными именами, а также предоставляет механизмы для кеширования фабрик, чтобы они могли быть сохранены и использованы повторно. 

**Примеры**: 
- Создание фабрики:
```python
factory = TinyFactory(simulation_id='sim1')
```
- Получение представления фабрики:
```python
print(factory)  # Вывод: TinyFactory(name='Factory 1234')
```


### `class TinyPersonFactory(TinyFactory)`
**Описание**: Класс, который создает фабрики для `TinyPerson` (персонажи в симуляции).

**Inherits**: 
- Наследуется от `TinyFactory`.

**Attributes**: 
- `person_prompt_template_path` (str): Путь к шаблону запроса для генерации `TinyPerson`. 
- `context_text` (str): Текстовый контекст, который используется для генерации `TinyPerson`. 
- `generated_minibios` (list): Список сгенерированных персонажей, для избежания повторной генерации одинаковых персонажей. 
- `generated_names` (list): Список сгенерированных имен персонажей, для обеспечения уникальности имен. 

**Methods**: 
- `__init__(self, context_text, simulation_id:str=None)`: Инициализирует экземпляр класса `TinyPersonFactory`. 
- `generate_person_factories(number_of_factories, generic_context_text)`: Статический метод, который создает список фабрик `TinyPersonFactory` с помощью модели OpenAI. 
- `generate_person(self, agent_particularities: str = None, temperature: float = 1.5, attempts: int = 5)`:  Создает `TinyPerson` с помощью модели OpenAI, используя контекст и заданные параметры.
- `_aux_model_call(self, messages, temperature)`: Вспомогательный метод для вызова модели OpenAI (используется с декоратором `@transactional`). 
- `_setup_agent(self, agent, configuration)`: Настраивает агента с необходимыми элементами. 

**Как работает**: 
- Класс `TinyPersonFactory` использует модель OpenAI для генерации персонажей. 
- Он принимает текстовый контекст, который описывает персонажей, и параметры, которые могут быть использованы для настройки генерации. 
- Фабрика следит за тем, чтобы сгенерированные имена персонажей были уникальны, и предоставляет механизм кеширования для повторного использования ранее сгенерированных персонажей.

**Примеры**: 
- Создание фабрики персонажей:
```python
factory = TinyPersonFactory(context_text="A group of friends planning a trip to the mountains.", simulation_id='sim1')
```
- Создание персонажа:
```python
person = factory.generate_person(agent_particularities="A person who enjoys hiking.", temperature=1.0)
```

**Inner Functions**: 
- `aux_generate()`: Вспомогательная функция, которая генерирует спецификации персонажа с помощью модели OpenAI. 
- `_aux_model_call(self, messages, temperature)`: Вспомогательный метод для вызова модели OpenAI (используется с декоратором `@transactional`). 
- `_setup_agent(self, agent, configuration)`: Настраивает агента с необходимыми элементами. 

**Примеры вызова**:
- `generate_person_factories()`:
```python
factories = TinyPersonFactory.generate_person_factories(number_of_factories=5, generic_context_text="A group of friends planning a trip to the mountains.")
```
- `generate_person()`:
```python
person = factory.generate_person(agent_particularities="A person who enjoys hiking.", temperature=1.0)
```
- `_aux_model_call(self, messages, temperature)`:
```python
messages = [{"role": "system", "content": "You are a system that generates specifications of artificial entities."}, {"role": "user", "content": prompt}]
message = factory._aux_model_call(messages=messages, temperature=1.0)
```
- `_setup_agent(self, agent, configuration)`:
```python
configuration = {"name": "Alice", "age": 30, "hobbies": ["hiking", "reading"]}
factory._setup_agent(person, configuration)
```

## Дополнительные сведения

- `utils.fresh_id()`: Функция, которая генерирует уникальный идентификатор.
- `chevron`: Библиотека, используемая для рендеринга шаблонов Mustache.
- `transactional`: Декоратор, который используется для кеширования результатов функций. 
- `openai_utils.client()`: Функция, которая возвращает экземпляр клиента OpenAI.
- `utils.extract_json(response['content'])`: Функция, которая извлекает JSON-данные из ответа модели OpenAI. 
- `json.dumps(result, indent=4, sort_keys=True)`: Функция, которая преобразует словарь Python в JSON-строку с отступами.
- `logging.getLogger("tinytroupe")`:  Функция, которая получает логгер для модуля `tinytroupe`.


##  Комментарии

-  Вместо `# Получаем значение параметра` используй `# Функция извлекает значение параметра`
- Вместо `# Переходим к следующей директории, если текущая не существует` используй  `# Переход к следующей директории, если текущая не существует`