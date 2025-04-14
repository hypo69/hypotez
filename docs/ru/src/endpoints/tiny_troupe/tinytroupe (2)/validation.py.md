# Модуль валидации персонажа TinyPerson

## Обзор

Модуль `validation.py` предназначен для валидации экземпляров класса `TinyPerson` с использованием языковой модели OpenAI (LLM). Он содержит класс `TinyPersonValidator` с методом `validate_person`, который отправляет серию вопросов экземпляру `TinyPerson` и оценивает ответы с помощью LLM.

## Подробнее

Модуль использует шаблоны `mustache` для генерации подсказок (prompt), которые затем отправляются в OpenAI LLM для валидации ответов `TinyPerson`. Валидация включает в себя оценку соответствия ответов заданным ожиданиям и правилам.

## Классы

### `TinyPersonValidator`

**Описание**: Класс, содержащий статический метод для валидации экземпляров `TinyPerson`.

**Методы**:

- `validate_person(person, expectations=None, include_agent_spec=True, max_content_length=default_max_content_display_length)`: Статический метод, выполняющий валидацию экземпляра `TinyPerson` с использованием OpenAI LLM.

## Функции

### `validate_person`

```python
    @staticmethod
    def validate_person(person, expectations=None, include_agent_spec=True, max_content_length=default_max_content_display_length):\n        """\n        Validate a TinyPerson instance using OpenAI\'s LLM.\n\n        This method sends a series of questions to the TinyPerson instance to validate its responses using OpenAI\'s LLM.\n        The method returns a float value representing the confidence score of the validation process.\n        If the validation process fails, the method returns None.\n\n        Args:\n            person (TinyPerson): The TinyPerson instance to be validated.\n            expectations (str, optional): The expectations to be used in the validation process. Defaults to None.\n            include_agent_spec (bool, optional): Whether to include the agent specification in the prompt. Defaults to True.\n            max_content_length (int, optional): The maximum length of the content to be displayed when rendering the conversation.\n\n        Returns:\n            float: The confidence score of the validation process (0.0 to 1.0), or None if the validation process fails.\n            str: The justification for the validation score, or None if the validation process fails.\n        """
```

**Назначение**: Валидация экземпляра `TinyPerson` с использованием языковой модели OpenAI.

**Параметры**:

- `person` (TinyPerson): Экземпляр `TinyPerson`, который необходимо валидировать.
- `expectations` (str, optional): Ожидания, используемые в процессе валидации. По умолчанию `None`.
- `include_agent_spec` (bool, optional): Флаг, указывающий, следует ли включать спецификацию агента в запрос. По умолчанию `True`.
- `max_content_length` (int, optional): Максимальная длина содержимого, отображаемого при рендеринге разговора.

**Возвращает**:

- `float`: Оценка уверенности процесса валидации (от 0.0 до 1.0), или `None`, если процесс валидации завершается неудачно.
- `str`: Обоснование оценки валидации, или `None`, если процесс валидации завершается неудачно.

**Как работает функция**:

1.  **Инициализация**: Инициализируются переменные, такие как `current_messages` для хранения сообщений обмена с LLM, и определяется путь к шаблону запроса `check_person_prompt_template_path`.
2.  **Чтение шаблона запроса**: Считывается шаблон запроса из файла `check_person.mustache`.
3.  **Формирование системного запроса**: Формируется системный запрос на основе шаблона и переданных ожиданий (`expectations`).
4.  **Формирование пользовательского запроса**: Формируется пользовательский запрос, включающий либо спецификацию агента (`person.generate_agent_specification()`), либо мини-биографию (`person.minibio()`), в зависимости от значения `include_agent_spec`.
5.  **Логирование**: Инициализируется логгер и записывается информация о начале валидации.
6.  **Отправка начальных сообщений**: Отправляются начальные сообщения (системный и пользовательский запросы) в LLM.
7.  **Цикл валидации**:
    *   LLM генерирует вопросы (`message["content"]`).
    *   Вопросы добавляются к текущим сообщениям (`current_messages`).
    *   `TinyPerson` отвечает на вопросы, используя методы `listen_and_act` и `pop_actions_and_get_contents_for`.
    *   Ответы добавляются к текущим сообщениям.
    *   Цикл продолжается, пока не будет достигнут маркер завершения (`termination_mark`) или пока LLM не вернет `None`.
8.  **Извлечение результата**: Извлекается JSON-контент из последнего сообщения, содержащий оценку (`score`) и обоснование (`justification`).
9.  **Логирование и возврат результата**: Записывается информация об оценке валидации и обосновании, и возвращается кортеж `(score, justification)`.
10. **Обработка неудачи**: Если валидация завершается неудачно (например, LLM возвращает `None`), возвращается `(None, None)`.

```
    Инициализация --> Чтение шаблона запроса --> Формирование системного запроса 
        |
        --> Формирование пользовательского запроса --> Логирование
        |
        --> Отправка начальных сообщений --> Цикл валидации
        |                                        |
        |                                        --> LLM генерирует вопросы
        |                                        |
        |                                        --> TinyPerson отвечает
        |                                        |
        |                                        --> Ответы добавляются к сообщениям
        |                                        |
        <-- Проверка маркера завершения <-- 
        |
        --> Извлечение результата
        |
        --> Логирование и возврат результата
```

**Примеры**:

Пример валидации персонажа с использованием ожиданий:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.validation import TinyPersonValidator

# Пример создания TinyPerson (предполагается, что TinyPerson имеет имя, возраст и профессию)
person = TinyPerson(name="Alice", age=30, profession="Software Engineer")
expectations = "The person should be a software engineer with at least 5 years of experience."

score, justification = TinyPersonValidator.validate_person(person, expectations=expectations)

if score is not None:
    print(f"Validation score: {score:.2f}")
    print(f"Justification: {justification}")
else:
    print("Validation failed.")