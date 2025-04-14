# Модуль `factory.py`

## Обзор

Модуль `factory.py` содержит классы для создания фабрик, генерирующих экземпляры класса `TinyPerson`. Он включает базовый класс `TinyFactory` и его подкласс `TinyPersonFactory`, специализирующийся на создании персонажей с использованием OpenAI LLM. Модуль также реализует механизмы кэширования для эффективного управления и повторного использования фабрик и сгенерированных агентов.

## Подробнее

Модуль предоставляет инструменты для создания и управления фабриками, генерирующими виртуальных персонажей (`TinyPerson`) на основе заданного контекста. Это позволяет создавать разнообразных персонажей для симуляций или других приложений, использующих искусственный интеллект. Модуль также включает поддержку транзакционного кэширования, что позволяет эффективно управлять состоянием фабрик и агентов, а также избегать повторной генерации одних и тех же персонажей.

## Классы

### `TinyFactory`

**Описание**:
Базовый класс для различных типов фабрик. Обеспечивает основу для расширения системы и реализации транзакционного кэширования.

**Принцип работы**:
`TinyFactory` служит базовым классом для создания фабрик различных типов. Он управляет списком всех созданных фабрик и обеспечивает механизмы для кэширования и восстановления состояния фабрик. Это позволяет эффективно управлять ресурсами и обеспечивать консистентность данных при работе с агентами.

**Атрибуты**:
- `all_factories` (dict): Словарь, содержащий все созданные фабрики (`name -> factories`).
- `name` (str): Уникальное имя фабрики.
- `simulation_id` (str, optional): Идентификатор симуляции, к которой принадлежит фабрика. По умолчанию `None`.

**Методы**:
- `__init__(self, simulation_id: str = None) -> None`:
    ```python
    def __init__(self, simulation_id: str = None) -> None:
        """
        Инициализирует экземпляр TinyFactory.

        Args:
            simulation_id (str, optional): Идентификатор симуляции. По умолчанию `None`.
        """
    ```

- `__repr__(self) -> str`:
    ```python
    def __repr__(self):
        """
        Возвращает строковое представление объекта TinyFactory.
        """
    ```

- `set_simulation_for_free_factories(simulation)`:
    ```python
    @staticmethod
    def set_simulation_for_free_factories(simulation):
        """
        Устанавливает симуляцию для "свободных" фабрик (с `simulation_id=None`).
        Позволяет привязать фабрики к определенной симуляции.
        """
    ```

- `add_factory(factory)`:
    ```python
    @staticmethod
    def add_factory(factory):
        """
        Добавляет фабрику в список всех фабрик. Имена фабрик должны быть уникальными.

        Args:
            factory (TinyFactory): Экземпляр фабрики для добавления.

        Raises:
            ValueError: Если фабрика с таким именем уже существует.
        """
    ```

- `clear_factories()`:
    ```python
    @staticmethod
    def clear_factories():
        """
        Очищает глобальный список всех фабрик.
        """
    ```

- `encode_complete_state(self) -> dict`:
    ```python
    def encode_complete_state(self) -> dict:
        """
        Кодирует полное состояние фабрики. Подклассы должны переопределять этот метод,
        если имеют несериализуемые элементы.

        Returns:
            dict: Словарь, представляющий состояние фабрики.
        """
    ```

- `decode_complete_state(self, state: dict) -> TinyFactory`:
    ```python
    def decode_complete_state(self, state: dict):
        """
        Декодирует полное состояние фабрики. Подклассы должны переопределять этот метод,
        если имеют несериализуемые элементы.

        Args:
            state (dict): Словарь, представляющий состояние фабрики.

        Returns:
            TinyFactory: Экземпляр фабрики с восстановленным состоянием.
        """
    ```

### `TinyPersonFactory`

**Описание**:
Подкласс `TinyFactory`, специализирующийся на создании экземпляров класса `TinyPerson` с использованием OpenAI LLM.

**Принцип работы**:
`TinyPersonFactory` использует контекстный текст и OpenAI LLM для генерации персонажей (`TinyPerson`). Он также поддерживает отслеживание сгенерированных персонажей, чтобы избежать дублирования. Фабрика предоставляет методы для генерации отдельных персонажей и настройки их параметров.

**Наследует**:
- `TinyFactory`: Наследует функциональность базовой фабрики, такую как управление списком фабрик и кэширование состояния.

**Атрибуты**:
- `person_prompt_template_path` (str): Путь к шаблону mustache для генерации запросов к LLM.
- `context_text` (str): Контекстный текст, используемый для генерации экземпляров `TinyPerson`.
- `generated_minibios` (list): Список сгенерированных `minibio` персонажей. Используется для предотвращения генерации одинаковых персонажей.
- `generated_names` (list): Список сгенерированных имен персонажей.

**Методы**:
- `__init__(self, context_text, simulation_id: str = None) -> None`:
    ```python
    def __init__(self, context_text, simulation_id: str = None):
        """
        Инициализирует экземпляр TinyPersonFactory.

        Args:
            context_text (str): Контекстный текст, используемый для генерации экземпляров TinyPerson.
            simulation_id (str, optional): Идентификатор симуляции. По умолчанию `None`.
        """
    ```

- `generate_person_factories(number_of_factories, generic_context_text) -> list | None`:
    ```python
    @staticmethod
    def generate_person_factories(number_of_factories, generic_context_text):
        """
        Генерирует список экземпляров TinyPersonFactory, используя OpenAI LLM.

        Args:
            number_of_factories (int): Количество экземпляров TinyPersonFactory для генерации.
            generic_context_text (str): Общий контекстный текст, используемый для генерации экземпляров TinyPersonFactory.

        Returns:
            list | None: Список экземпляров TinyPersonFactory или `None` в случае ошибки.
        """
    ```

- `generate_person(self, agent_particularities: str = None, temperature: float = 1.5, attepmpts: int = 5) -> TinyPerson | None`:
    ```python
    def generate_person(self, agent_particularities:str=None, temperature:float=1.5, attepmpts:int=5):
        """
        Генерирует экземпляр TinyPerson, используя OpenAI LLM.

        Args:
            agent_particularities (str): Особенности агента.
            temperature (float): Температура для использования при выборке из LLM.
            attepmpts (int): Количество попыток генерации агента.

        Returns:
            TinyPerson | None: Экземпляр TinyPerson или `None`, если не удалось сгенерировать.
        """
    ```
    **Внутренние функции**:
    - `aux_generate() -> dict | None`:
        ```python
        def aux_generate():
            """
            Внутренняя функция для генерации спецификации агента с использованием LLM.

            Returns:
                dict | None: Спецификация агента в виде словаря или None, если не удалось сгенерировать.
            """
        ```
        **Как работает функция**:
        1. Формирует запрос к LLM, включая системное сообщение и контекст пользователя.
        2. Вызывает метод `_aux_model_call` для отправки запроса и получения ответа от LLM.
        3. Извлекает JSON из ответа.
        4. Проверяет уникальность имени сгенерированного агента.
        5. Возвращает спецификацию агента или `None`, если генерация не удалась.

    **ASII flowchart**:

    ```
    Начало процесса генерации персонажа
    │
    ├──► Формирование запроса для LLM (prompt)
    │   │  Включает системное сообщение и контекст пользователя
    │   │
    │   └──► Отправка запроса к LLM (_aux_model_call)
    │       │  Параметры: messages, temperature
    │       │
    │       └──► Получение ответа от LLM (message)
    │           │
    │           └──► Извлечение JSON из ответа (result)
    │               │  Анализ содержимого 'content' в message
    │               │
    │               └──► Проверка уникальности имени агента
    │                   │  Сравнение с self.generated_names
    │                   │
    │                   └──► Возврат спецификации агента (agent_spec) или None
    │
    Конец процесса генерации персонажа
    ```

- `_aux_model_call(self, messages, temperature)`:
    ```python
    @transactional
    def _aux_model_call(self, messages, temperature):
        """
        Вспомогательный метод для выполнения вызова модели. Используется для обеспечения
        транзакционного кэширования.

        Args:
            messages (list): Список сообщений для отправки в модель.
            temperature (float): Температура для использования при выборке из LLM.

        Returns:
            dict: Ответ от модели.
        """
    ```

- `_setup_agent(self, agent, configuration)`:
    ```python
    @transactional
    def _setup_agent(self, agent, configuration):
        """
        Настраивает агента с необходимыми элементами.

        Args:
            agent (TinyPerson): Экземпляр агента для настройки.
            configuration (dict): Словарь конфигурации агента.
        """
    ```

## Функции

### `generate_person_factories`

```python
    @staticmethod
    def generate_person_factories(number_of_factories, generic_context_text):
        """
        Генерирует список экземпляров TinyPersonFactory, используя OpenAI LLM.

        Args:
            number_of_factories (int): Количество экземпляров TinyPersonFactory для генерации.
            generic_context_text (str): Общий контекстный текст, используемый для генерации экземпляров TinyPersonFactory.

        Returns:
            list | None: Список экземпляров TinyPersonFactory или `None` в случае ошибки.
        """
```
**Назначение**: Генерация списка фабрик персонажей на основе заданного контекста с использованием OpenAI LLM.

**Параметры**:
- `number_of_factories` (int): Количество фабрик для генерации.
- `generic_context_text` (str): Общий контекст, используемый для создания описаний фабрик.

**Возвращает**:
- `list | None`: Список сгенерированных экземпляров `TinyPersonFactory` или `None` в случае ошибки.

**Как работает функция**:
1. Формирует запрос к OpenAI LLM, включающий системный промпт и пользовательский промпт с указанием количества фабрик и контекста.
2. Отправляет запрос к LLM и получает ответ с описаниями фабрик.
3. Извлекает JSON из ответа.
4. Создает экземпляры `TinyPersonFactory` на основе полученных описаний.
5. Возвращает список созданных фабрик.

**ASII flowchart**:

```
Начало процесса генерации фабрик
│
├──► Логирование начала генерации
│   │  Сообщение о начале генерации с указанием number_of_factories и generic_context_text
│   │
│   └──► Формирование системного промпта
│       │  Чтение содержимого файла 'prompts/generate_person_factory.md'
│       │
│   └──► Формирование пользовательского промпта
│       │  Подстановка значений number_of_factories и context в шаблон
│       │
│   └──► Отправка сообщения в OpenAI LLM
│       │  Параметры: messages (системный и пользовательский промпты)
│       │
│   └──► Получение ответа от OpenAI LLM (response)
│       │
│   └──► Извлечение JSON из ответа (result)
│       │  Анализ содержимого 'content' в response
│       │
│   └──► Создание экземпляров TinyPersonFactory
│       │  Цикл по диапазону number_of_factories
│       │  Создание фабрики с описанием из result[i]
│       │
│   └──► Возврат списка фабрик (factories) или None (в случае ошибки)
│
Конец процесса генерации фабрик
```
**Примеры**:

```python
# Пример вызова функции
number_of_factories = 3
generic_context_text = "Студенты университета"
factories = TinyPersonFactory.generate_person_factories(number_of_factories, generic_context_text)
if factories:
    print(f"Сгенерировано {len(factories)} фабрик")
else:
    print("Не удалось сгенерировать фабрики")
```
### `generate_person`

```python
    def generate_person(self, agent_particularities:str=None, temperature:float=1.5, attepmpts:int=5):
        """
        Генерирует экземпляр TinyPerson, используя OpenAI LLM.

        Args:
            agent_particularities (str): Особенности агента.
            temperature (float): Температура для использования при выборке из LLM.
            attepmpts (int): Количество попыток генерации агента.

        Returns:
            TinyPerson | None: Экземпляр TinyPerson или `None`, если не удалось сгенерировать.
        """
```

**Назначение**: Генерация экземпляра `TinyPerson` с использованием OpenAI LLM.

**Параметры**:
- `agent_particularities` (str, optional): Дополнительные особенности агента. По умолчанию `None`.
- `temperature` (float, optional): Температура для использования при выборке из LLM. По умолчанию 1.5.
- `attepmpts` (int, optional): Количество попыток генерации агента. По умолчанию 5.

**Возвращает**:
- `TinyPerson | None`: Экземпляр `TinyPerson` или `None`, если не удалось сгенерировать.

**Как работает функция**:
1. Формирует запрос к OpenAI LLM на основе шаблона mustache, контекста и особенностей агента.
2. Вызывает внутреннюю функцию `aux_generate` для отправки запроса и получения ответа от LLM.
3. Извлекает JSON из ответа.
4. Проверяет уникальность имени сгенерированного агента.
5. Создает экземпляр `TinyPerson` на основе полученных параметров.
6. Настраивает агента с использованием метода `_setup_agent`.
7. Добавляет `minibio` и имя агента в списки сгенерированных.
8. Возвращает созданного агента.

Если после нескольких попыток не удается сгенерировать агента, возвращает `None`.

**ASII flowchart**:

```
Начало процесса генерации персонажа
│
├──► Логирование начала генерации
│   │  Сообщение о начале генерации с указанием context_text
│   │
│   └──► Формирование промпта
│       │  Чтение содержимого файла person_prompt_template_path
│       │  Подстановка значений context, agent_particularities и already_generated в шаблон
│       │
│   └──► Вызов aux_generate для получения спецификации агента
│       │  Включает отправку промпта в OpenAI LLM и извлечение JSON из ответа
│       │
│   └──► Проверка, что спецификация агента не None
│       │
│   └──► Создание экземпляра TinyPerson (person)
│       │  Параметры: agent_spec["name"]
│       │
│   └──► Настройка агента (_setup_agent)
│       │  Параметры: person, agent_spec["_configuration"]
│       │
│   └──► Добавление minibio и имени агента в списки сгенерированных
│       │  self.generated_minibios.append(person.minibio())
│       │  self.generated_names.append(person.get("name").lower())
│       │
│   └──► Возврат созданного агента (person)
│       │
│   └──► Если agent_spec is None (после нескольких попыток):
│       │   Логирование ошибки
│       │   Возврат None
│
Конец процесса генерации персонажа
```
**Примеры**:

```python
# Пример вызова функции
factory = TinyPersonFactory("Контекст для генерации персонажа")
agent = factory.generate_person(agent_particularities="С особыми навыками")
if agent:
    print(f"Сгенерирован агент с именем {agent.name}")
else:
    print("Не удалось сгенерировать агента")
```

### `_aux_model_call`

```python
    @transactional
    def _aux_model_call(self, messages, temperature):
        """
        Вспомогательный метод для выполнения вызова модели. Используется для обеспечения
        транзакционного кэширования.

        Args:
            messages (list): Список сообщений для отправки в модель.
            temperature (float): Температура для использования при выборке из LLM.

        Returns:
            dict: Ответ от модели.
        """
```

**Назначение**: Вспомогательный метод для выполнения вызова языковой модели (LLM) с поддержкой транзакционного кэширования.

**Параметры**:
- `messages` (list): Список сообщений для отправки в модель.
- `temperature` (float): Температура для использования при выборке из LLM.

**Возвращает**:
- `dict`: Ответ от модели.

**Как работает функция**:
1. Отправляет сообщения в языковую модель (LLM) с указанной температурой.
2. Возвращает ответ, полученный от модели.

**ASII flowchart**:

```
Начало процесса вызова модели
│
├──► Отправка сообщения в OpenAI LLM
│   │  Параметры: messages (список сообщений), temperature
│   │
│   └──► Получение ответа от OpenAI LLM (response)
│       │
│   └──► Возврат ответа от модели (response)
│
Конец процесса вызова модели
```

**Примеры**:

```python
# Пример вызова функции
factory = TinyPersonFactory("Контекст")
messages = [{"role": "system", "content": "Ты - полезный ассистент"}, {"role": "user", "content": "Привет!"}]
temperature = 0.7
response = factory._aux_model_call(messages, temperature)
print(f"Ответ от модели: {response}")
```

### `_setup_agent`

```python
    @transactional
    def _setup_agent(self, agent, configuration):
        """
        Настраивает агента с необходимыми элементами.

        Args:
            agent (TinyPerson): Экземпляр агента для настройки.
            configuration (dict): Словарь конфигурации агента.
        """
```

**Назначение**: Настройка агента с использованием предоставленной конфигурации.

**Параметры**:
- `agent` (TinyPerson): Экземпляр агента для настройки.
- `configuration` (dict): Словарь конфигурации агента.

**Как работает функция**:
1. Перебирает элементы конфигурации.
2. Если значение является списком, вызывает метод `agent.define_several` для определения нескольких атрибутов агента.
3. Если значение не является списком, вызывает метод `agent.define` для определения одного атрибута агента.

**ASII flowchart**:

```
Начало процесса настройки агента
│
├──► Перебор элементов конфигурации (configuration.items())
│   │
│   └──► Проверка, является ли значение списком
│       │
│   └──► Если значение - список:
│       │   Вызов agent.define_several(key, value)
│       │
│   └──► Если значение - не список:
│       │   Вызов agent.define(key, value)
│
Конец процесса настройки агента
```

**Примеры**:

```python
# Пример вызова функции
factory = TinyPersonFactory("Контекст")
agent = TinyPerson("Имя агента")
configuration = {"name": "Новое имя", "skills": ["skill1", "skill2"]}
factory._setup_agent(agent, configuration)
print(f"Имя агента после настройки: {agent.name}")
print(f"Навыки агента после настройки: {agent.get('skills')}")
```