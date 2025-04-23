# Модуль `tiny_person_factory.py`

## Обзор

Модуль `tiny_person_factory.py` предназначен для создания экземпляров класса `TinyPerson`, представляющих собой симуляцию личности. Он использует OpenAI LLM (Large Language Model) для генерации описаний персонажей на основе заданного контекста. Модуль содержит классы для управления фабриками персонажей и генерации отдельных личностей с учетом уникальных параметров и ограничений.

## Подробнее

Модуль предоставляет функциональность для создания симулированных персонажей с использованием моделей OpenAI. Он включает в себя классы для управления генерацией персонажей на основе заданного контекста, а также утилиты для обработки и извлечения информации из ответов моделей.

## Классы

### `TinyPersonFactory`

**Описание**: Фабрика для создания экземпляров класса `TinyPerson`. Использует OpenAI LLM для генерации персонажей на основе заданного контекста.

**Наследует**:

-   `TinyFactory`: Базовый класс для фабрик, предоставляющий общую функциональность.

**Атрибуты**:

-   `person_prompt_template_path` (str): Путь к шаблону mustache, используемому для генерации запросов к модели.
-   `context_text` (str): Текст контекста, используемый для генерации персонажей.
-   `generated_minibios` (list): Список сгенерированных мини-биографий, чтобы избежать повторной генерации одинаковых персонажей.
-   `generated_names` (list): Список сгенерированных имен персонажей для обеспечения их уникальности.

**Методы**:

-   `generate_person_factories(number_of_factories, generic_context_text)`: Генерирует список экземпляров `TinyPersonFactory` с использованием OpenAI LLM.
-   `generate_person(agent_particularities, temperature, frequency_penalty, presence_penalty, attepmpts)`: Генерирует экземпляр `TinyPerson` с использованием OpenAI LLM.
-   `generate_people(number_of_people, agent_particularities, temperature, frequency_penalty, presence_penalty, attepmpts, verbose)`: Генерирует список экземпляров `TinyPerson` с использованием OpenAI LLM.
-   `_aux_model_call(messages, temperature, frequency_penalty, presence_penalty)`: Вспомогательный метод для выполнения вызова модели. Используется для обхода технических ограничений при использовании декоратора `transactional`.
-   `_setup_agent(agent, configuration)`: Настраивает агента с необходимыми элементами.

## Методы класса

### `generate_person_factories`

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

**Назначение**: Генерирует список экземпляров `TinyPersonFactory` на основе заданного контекста, используя OpenAI LLM.

**Параметры**:

-   `number_of_factories` (int): Количество экземпляров `TinyPersonFactory` для генерации.
-   `generic_context_text` (str): Общий текст контекста, используемый для генерации экземпляров `TinyPersonFactory`.

**Возвращает**:

-   `list`: Список экземпляров `TinyPersonFactory`.

**Как работает функция**:

1.  Логирует начало процесса генерации фабрик персонажей.
2.  Считывает системный промпт из файла `prompts/generate_person_factory.md`.
3.  Формирует пользовательский промпт на основе шаблона и заданного контекста.
4.  Отправляет сообщение в OpenAI LLM и извлекает результаты в формате JSON.
5.  Создает экземпляры `TinyPersonFactory` на основе извлеченных данных.

**Примеры**:

```python
factories = TinyPersonFactory.generate_person_factories(2, "A small town in the countryside")
print(factories)
```

### `generate_person`

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

**Назначение**: Генерирует экземпляр `TinyPerson` с использованием OpenAI LLM.

**Параметры**:

-   `agent_particularities` (str, optional): Дополнительные особенности агента. По умолчанию `None`.
-   `temperature` (float, optional): Температура для использования при выборке из LLM. По умолчанию `1.5`.
-   `frequency_penalty` (float, optional): Штраф за частоту. По умолчанию `0.0`.
-   `presence_penalty` (float, optional): Штраф за присутствие. По умолчанию `0.0`.
-   `attepmpts` (int, optional): Количество попыток генерации. По умолчанию `10`.

**Возвращает**:

-   `TinyPerson`: Экземпляр `TinyPerson`, сгенерированный с использованием LLM.

**Внутренние функции**:

*   `aux_generate(attempt)`:
    *   **Назначение**: Вспомогательная функция для генерации спецификации агента.
    *   **Параметры**:
        *   `attempt` (int): Номер попытки генерации.
    *   **Как работает функция**:
        1.  Формирует сообщения для отправки в модель, включая системные инструкции и пользовательский запрос.
        2.  Вызывает метод `_aux_model_call` для отправки запроса в модель и получения ответа.
        3.  Извлекает JSON из ответа модели.
        4.  Проверяет уникальность имени сгенерированного персонажа.
        5.  В случае успешной генерации и уникальности имени возвращает спецификацию агента.
    *   **Возвращает**:
        *   `dict`: Спецификация агента в случае успешной генерации и уникальности имени, иначе `None`.

**Как работает функция**:

1.  Логирует начало процесса генерации персонажа.
2.  Загружает примеры спецификаций агентов из файлов.
3.  Формирует промпт на основе шаблона и заданного контекста, включая примеры и список уже сгенерированных имен.
4.  Вызывает внутреннюю функцию `aux_generate` для генерации спецификации агента.
5.  Создает экземпляр `TinyPerson` на основе сгенерированной спецификации.
6.  Добавляет мини-биографию и имя персонажа в списки сгенерированных данных.

**Примеры**:

```python
factory = TinyPersonFactory("A scientist working in a lab")
person = factory.generate_person(agent_particularities="Likes to solve complex problems", temperature=0.8)
print(person)
```

### `generate_people`

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

**Назначение**: Генерирует список экземпляров `TinyPerson` с использованием OpenAI LLM.

**Параметры**:

-   `number_of_people` (int): Количество экземпляров `TinyPerson` для генерации.
-   `agent_particularities` (str, optional): Дополнительные особенности агента. По умолчанию `None`.
-   `temperature` (float, optional): Температура для использования при выборке из LLM. По умолчанию `1.5`.
-   `frequency_penalty` (float, optional): Штраф за частоту. По умолчанию `0.0`.
-   `presence_penalty` (float, optional): Штраф за присутствие. По умолчанию `0.0`.
-   `attepmpts` (int, optional): Количество попыток генерации. По умолчанию `10`.
-   `verbose` (bool, optional): Флаг для вывода подробной информации. По умолчанию `False`.

**Возвращает**:

-   `list`: Список экземпляров `TinyPerson`, сгенерированных с использованием LLM.

**Как работает функция**:

1.  Итерируется по заданному количеству людей.
2.  Вызывает метод `generate_person` для каждого персонажа.
3.  Добавляет сгенерированного персонажа в список.
4.  Логирует информацию о сгенерированном персонаже.

**Примеры**:

```python
factory = TinyPersonFactory("A group of friends living in a city")
people = factory.generate_people(3, agent_particularities="Enjoy going to concerts", temperature=0.8, verbose=True)
print(people)
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
```

**Назначение**: Вспомогательный метод для выполнения вызова модели OpenAI LLM.

**Параметры**:

-   `messages` (list): Список сообщений для отправки в модель.
-   `temperature` (float): Температура для использования при выборке из LLM.
-   `frequency_penalty` (float): Штраф за частоту.
-   `presence_penalty` (float): Штраф за присутствие.

**Возвращает**:

-   `dict`: Ответ от OpenAI LLM.

**Как работает функция**:

1.  Отправляет сообщение в OpenAI LLM с заданными параметрами.

### `_setup_agent`

```python
    @transactional
    def _setup_agent(self, agent, configuration):
        """
        Sets up the agent with the necessary elements.
        """
```

**Назначение**: Настраивает агента с необходимыми элементами.

**Параметры**:

-   `agent` (TinyPerson): Агент для настройки.
-   `configuration` (dict): Конфигурация агента.

**Как работает функция**:

1.  Включает определения персонажа в агента на основе заданной конфигурации.

## Параметры класса

-   `person_prompt_template_path` (str): Путь к шаблону для генерации запросов.
-   `context_text` (str): Текст контекста для генерации персонажей.
-   `generated_minibios` (list): Список сгенерированных мини-биографий.
-   `generated_names` (list): Список сгенерированных имен персонажей.

## Примеры

```python
from tinytroupe.factory.tiny_person_factory import TinyPersonFactory

# Создание фабрики персонажей
factory = TinyPersonFactory(context_text="Живет в большом городе")

# Генерация одного персонажа
person = factory.generate_person(agent_particularities="Любит читать книги", temperature=0.7)
if person:
    print(f"Сгенерирован персонаж: {person.get('name')}")
else:
    print("Не удалось сгенерировать персонажа")

# Генерация нескольких персонажей
people = factory.generate_people(number_of_people=2, agent_particularities="Интересуются наукой", temperature=0.7)
if people:
    for person in people:
        print(f"Сгенерирован персонаж: {person.get('name')}")
else:
    print("Не удалось сгенерировать персонажей")