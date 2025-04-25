# Фабрика персонажей для TinyTroupe

## Обзор

Этот модуль содержит класс `TinyPersonFactory`, который используется для создания персонажей (`TinyPerson`) для симуляции TinyTroupe. Фабрика использует OpenAI's LLM для генерации персонализированных описаний персонажей на основе заданного контекста. 

## Подробней

Класс `TinyPersonFactory` генерирует персонажей для симуляции `TinyTroupe`. Он основан на концепции "маленьких людей" (`TinyPeople`) - персонажей, которые взаимодействуют друг с другом в заданном контексте.

## Классы

### `TinyPersonFactory`

**Описание**: Класс, отвечающий за генерацию персонажей (`TinyPerson`) для TinyTroupe. 

**Наследует**: `TinyFactory`

**Атрибуты**:

- `person_prompt_template_path (str)`: Путь к шаблону подсказки для генерации персонажей.
- `context_text (str)`: Контекст, используемый для генерации персонажей.
- `generated_minibios (list)`: Список уже сгенерированных коротких описаний (minibios) персонажей.
- `generated_names (list)`: Список уже сгенерированных имен персонажей.

**Методы**:

- `__init__(self, context_text, simulation_id:str=None)`: Инициализирует объект `TinyPersonFactory`.
    - **Параметры**:
        - `context_text (str)`: Контекст, используемый для генерации персонажей.
        - `simulation_id (str, optional)`: Идентификатор симуляции. По умолчанию `None`.

- `generate_person_factories(number_of_factories, generic_context_text)`: Генерирует список объектов `TinyPersonFactory` на основе заданного контекста. 
    - **Параметры**:
        - `number_of_factories (int)`: Количество объектов `TinyPersonFactory`, которые нужно создать.
        - `generic_context_text (str)`: Общий контекст для генерации объектов `TinyPersonFactory`.
    - **Возвращает**:
        - `list`: Список объектов `TinyPersonFactory`. 

- `generate_person(self, agent_particularities:str=None, temperature:float=1.5, frequency_penalty:float=0.0, presence_penalty:float=0.0, attepmpts:int=10)`: Генерирует объект `TinyPerson` на основе заданного контекста.
    - **Параметры**:
        - `agent_particularities (str)`:  Характеристики агента.
        - `temperature (float)`: Температура для LLM, чем выше температура, тем более случайным будет результат.
        - `frequency_penalty (float)`: Штраф за частоту использования слов.
        - `presence_penalty (float)`: Штраф за присутствие слов.
        - `attepmpts (int)`: Количество попыток генерации.
    - **Возвращает**:
        - `TinyPerson`: Объект `TinyPerson`, сгенерированный LLM.

- `generate_people(self, number_of_people:int, agent_particularities:str=None, temperature:float=1.5, frequency_penalty:float=0.0, presence_penalty:float=0.0, attepmpts:int=10, verbose:bool=False)`: Генерирует список объектов `TinyPerson` на основе заданного контекста. 
    - **Параметры**:
        - `number_of_people (int)`: Количество персонажей (`TinyPerson`), которые нужно создать.
        - `agent_particularities (str)`:  Характеристики агента.
        - `temperature (float)`: Температура для LLM, чем выше температура, тем более случайным будет результат.
        - `frequency_penalty (float)`: Штраф за частоту использования слов.
        - `presence_penalty (float)`: Штраф за присутствие слов.
        - `attepmpts (int)`: Количество попыток генерации.
        - `verbose (bool)`: Флаг, указывающий, нужно ли выводить подробную информацию.
    - **Возвращает**:
        - `list`: Список объектов `TinyPerson`. 

- `_aux_model_call(self, messages, temperature, frequency_penalty, presence_penalty)`: Вспомогательный метод для вызова модели LLM.
    - **Параметры**:
        - `messages (list)`: Список сообщений для LLM.
        - `temperature (float)`: Температура для LLM, чем выше температура, тем более случайным будет результат.
        - `frequency_penalty (float)`: Штраф за частоту использования слов.
        - `presence_penalty (float)`: Штраф за присутствие слов.

- `_setup_agent(self, agent, configuration)`: Устанавливает необходимые параметры для персонажей (`TinyPerson`).
    - **Параметры**:
        - `agent (TinyPerson)`: Объект `TinyPerson`, для которого устанавливаются параметры.
        - `configuration (dict)`: Конфигурация персонажа.

## Функции

### `generate_person_factories(number_of_factories, generic_context_text)`

**Назначение**: Генерирует список объектов `TinyPersonFactory` на основе заданного контекста.

**Параметры**:

- `number_of_factories (int)`: Количество объектов `TinyPersonFactory`, которые нужно создать.
- `generic_context_text (str)`: Общий контекст для генерации объектов `TinyPersonFactory`.

**Возвращает**:

- `list`: Список объектов `TinyPersonFactory`.

**Как работает функция**:

1. Считывает системную подсказку из файла `prompts/generate_person_factory.md`.
2. Формирует пользовательскую подсказку с использованием шаблона `chevron` для генерации описаний персонажей.
3. Использует `openai_utils.client().send_message()` для отправки подсказки в OpenAI's LLM.
4. Извлекает сгенерированные описания персонажей из ответа LLM.
5. Создает объекты `TinyPersonFactory` для каждого сгенерированного описания.
6. Возвращает список созданных объектов `TinyPersonFactory`.

**Примеры**:

```python
# Генерация 5 фабрик персонажей на основе контекста "Винный бар"
factories = TinyPersonFactory.generate_person_factories(5, "Винный бар")

# Проверка результата
print(f"Создано {len(factories)} фабрик персонажей.")
```

## Методы класса

### `generate_person(self, agent_particularities:str=None, temperature:float=1.5, frequency_penalty:float=0.0, presence_penalty:float=0.0, attepmpts:int=10)`

**Назначение**: Генерирует объект `TinyPerson` на основе заданного контекста.

**Параметры**:

- `agent_particularities (str)`:  Характеристики агента.
- `temperature (float)`: Температура для LLM, чем выше температура, тем более случайным будет результат.
- `frequency_penalty (float)`: Штраф за частоту использования слов.
- `presence_penalty (float)`: Штраф за присутствие слов.
- `attepmpts (int)`: Количество попыток генерации.

**Возвращает**:

- `TinyPerson`: Объект `TinyPerson`, сгенерированный LLM.

**Как работает функция**:

1. Считывает шаблон подсказки из файла `prompts/generate_person.mustache`.
2. Формирует подсказку для LLM с использованием шаблона `chevron` и заданных параметров.
3. Использует `openai_utils.client().send_message()` для отправки подсказки в OpenAI's LLM.
4. Извлекает сгенерированные данные персонажа из ответа LLM.
5. Проверяет, не было ли сгенерировано имя персонажа ранее.
6. Если имя не повторяется, создает объект `TinyPerson` с использованием сгенерированных данных.
7. Возвращает объект `TinyPerson`. 

**Примеры**:

```python
# Генерация персонажа с заданными характеристиками
person = factory.generate_person(agent_particularities="Дружелюбный бармен", temperature=1.0)

# Проверка результата
print(f"Сгенерирован персонаж: {person.minibio()}")
```

### `generate_people(self, number_of_people:int, agent_particularities:str=None, temperature:float=1.5, frequency_penalty:float=0.0, presence_penalty:float=0.0, attepmpts:int=10, verbose:bool=False)`

**Назначение**: Генерирует список объектов `TinyPerson` на основе заданного контекста. 

**Параметры**:

- `number_of_people (int)`: Количество персонажей (`TinyPerson`), которые нужно создать.
- `agent_particularities (str)`:  Характеристики агента.
- `temperature (float)`: Температура для LLM, чем выше температура, тем более случайным будет результат.
- `frequency_penalty (float)`: Штраф за частоту использования слов.
- `presence_penalty (float)`: Штраф за присутствие слов.
- `attepmpts (int)`: Количество попыток генерации.
- `verbose (bool)`: Флаг, указывающий, нужно ли выводить подробную информацию.

**Возвращает**:

- `list`: Список объектов `TinyPerson`.

**Как работает функция**:

1. Итерирует `number_of_people` раз.
2. В каждой итерации вызывает `generate_person()` для генерации нового персонажа.
3. Добавляет сгенерированного персонажа в список, если он был успешно создан.
4. Возвращает список созданных персонажей.

**Примеры**:

```python
# Генерация 3 персонажей с заданными характеристиками
people = factory.generate_people(3, agent_particularities="Гость бара", temperature=1.2)

# Проверка результата
for person in people:
    print(f"Сгенерирован персонаж: {person.minibio()}")
```

### `_aux_model_call(self, messages, temperature, frequency_penalty, presence_penalty)`

**Назначение**: Вспомогательный метод для вызова модели LLM.

**Параметры**:

- `messages (list)`: Список сообщений для LLM.
- `temperature (float)`: Температура для LLM, чем выше температура, тем более случайным будет результат.
- `frequency_penalty (float)`: Штраф за частоту использования слов.
- `presence_penalty (float)`: Штраф за присутствие слов.

**Возвращает**:

- `dict`: Ответ LLM.

**Как работает функция**:

1. Использует `openai_utils.client().send_message()` для отправки сообщений в OpenAI's LLM.
2. Возвращает ответ LLM.

### `_setup_agent(self, agent, configuration)`

**Назначение**: Устанавливает необходимые параметры для персонажей (`TinyPerson`).

**Параметры**:

- `agent (TinyPerson)`: Объект `TinyPerson`, для которого устанавливаются параметры.
- `configuration (dict)`: Конфигурация персонажа.

**Как работает функция**:

1. Вызывает метод `include_persona_definitions()` у объекта `agent` для установки конфигурации.

## Параметры класса

- `person_prompt_template_path (str)`: Путь к шаблону подсказки для генерации персонажей.
- `context_text (str)`: Контекст, используемый для генерации персонажей.
- `generated_minibios (list)`: Список уже сгенерированных коротких описаний (minibios) персонажей.
- `generated_names (list)`: Список уже сгенерированных имен персонажей.

## Примеры

```python
# Создание фабрики персонажей на основе контекста "Школа"
factory = TinyPersonFactory("Школа")

# Генерация 2 персонажей
people = factory.generate_people(2)

# Вывод информации о персонажах
for person in people:
    print(f"Имя: {person.get('name')}")
    print(f"Описание: {person.minibio()}")
```