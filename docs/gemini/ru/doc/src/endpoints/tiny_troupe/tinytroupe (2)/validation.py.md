# Модуль валидации персон TinyTroupe

## Обзор

Этот модуль предоставляет функции для валидации персон TinyTroupe с помощью OpenAI API. Модуль включает в себя класс `TinyPersonValidator`, который отвечает за процесс валидации, и функции для генерации соответствующих запросов OpenAI.

## Классы

### `TinyPersonValidator`

**Описание**: Класс, отвечающий за валидацию персон TinyTroupe.

**Атрибуты**: 

* `default_max_content_display_length (int)`: Максимальная длина выводимого текста при рендеринге разговора.

**Методы**:

* `validate_person(person, expectations=None, include_agent_spec=True, max_content_length=default_max_content_display_length)`: Функция для валидации персоны.

## Функции

### `validate_person(person, expectations=None, include_agent_spec=True, max_content_length=default_max_content_display_length)`

**Назначение**: Валидирует экземпляр `TinyPerson` с использованием LLM OpenAI.

**Параметры**:

* `person (TinyPerson)`: Экземпляр `TinyPerson`, который необходимо валидировать.
* `expectations (str, optional)`: Ожидания, которые будут использоваться в процессе валидации. По умолчанию `None`.
* `include_agent_spec (bool, optional)`: Флаг, указывающий, следует ли включать спецификацию агента в запрос. По умолчанию `True`.
* `max_content_length (int, optional)`: Максимальная длина текста, который будет отображаться при рендеринге разговора.

**Возвращает**:

* `float`: Оценка уверенности процесса валидации (от 0.0 до 1.0) или `None`, если процесс валидации завершился неудачей.
* `str`: Обоснование оценки валидации или `None`, если процесс валидации завершился неудачей.

**Как работает функция**:

1. Функция создает список `current_messages` для хранения сообщений в текущем разговоре.
2. Функция формирует запрос, который будет отправлен OpenAI API. 
3. Используется шаблон `check_person.mustache` для формирования системного запроса.
4. Шаблон рендерится с использованием значений `expectations`.
5. Формируется запрос пользователя (user prompt) с использованием  `person.generate_agent_specification()` или `person.minibio()`, в зависимости от значения `include_agent_spec`.
6. Функция отправляет начальные сообщения в LLM (OpenAI).
7. Функция циклически отправляет вопросы к LLM и получает ответы от LLM.
8. Функция получает ответы от персоны на вопросы, заданные LLM, и добавляет их в список `current_messages`.
9. Функция проверяет ответ LLM на наличие метки ````json`, указывающей на завершение диалога.
10.  Если диалог завершен, функция извлекает оценку уверенности и обоснование из ответа LLM.
11. Если процесс валидации завершился неудачей, функция возвращает `None`.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.validation import TinyPersonValidator

# Создаем экземпляр TinyPerson
person = TinyPerson(name="John Doe", minibio="John Doe is a fictional character...")

# Создаем экземпляр TinyPersonValidator
validator = TinyPersonValidator()

# Валидируем персону
score, justification = validator.validate_person(person, expectations="John Doe is a helpful and friendly person")

# Выводим результат валидации
print(f"Validation score: {score:.2f}")
print(f"Justification: {justification}")
```
```python
from tinytroupe.agent import TinyPerson
from tinytroupe.validation import TinyPersonValidator

# Создаем экземпляр TinyPerson
person = TinyPerson(name="John Doe", minibio="John Doe is a fictional character...")

# Создаем экземпляр TinyPersonValidator
validator = TinyPersonValidator()

# Валидируем персону
score, justification = validator.validate_person(person)

# Выводим результат валидации
print(f"Validation score: {score:.2f}")
print(f"Justification: {justification}")
```

## Внутренние функции

### `utils.extract_json(message['content'])`

**Описание**: Извлекает JSON-данные из текста.

**Параметры**:

* `message['content'] (str)`: Текст, содержащий JSON-данные.

**Возвращает**:

* `dict`: Словарь, полученный из JSON-данных.

**Как работает функция**:

1. Функция извлекает JSON-данные из текста `message['content']`.
2. Функция преобразует JSON-данные в словарь.

**Примеры**:

```python
from tinytroupe.utils import extract_json

json_data = "```json\n{\"score\": 0.8, \"justification\": \"Person answered correctly\"}\n```"

data = extract_json(json_data)

print(data)
```

## Дополнительная информация

* Модуль использует `chevron` для рендеринга шаблонов mustache.
* Модуль использует `logging` для записи информации о процессе валидации.

## Системные инструкции

* Модуль использует `config` для получения настроек OpenAI API.
* Модуль использует `openai_utils` для взаимодействия с OpenAI API.
* Модуль использует `utils` для вспомогательных функций.