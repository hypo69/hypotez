# Модуль для валидации TinyPerson

## Обзор

Модуль `tiny_person_validator.py` содержит класс `TinyPersonValidator`, который используется для валидации экземпляров класса `TinyPerson` с использованием языковой модели OpenAI (LLM). Он предоставляет механизм для оценки соответствия персонажа заданным ожиданиям и характеристикам.

## Подробней

Модуль содержит статический метод `validate_person`, который отправляет серию вопросов экземпляру `TinyPerson` для проверки его ответов с использованием LLM OpenAI. Метод возвращает оценку достоверности процесса валидации и обоснование этой оценки. Валидация производится на основе заданных ожиданий и спецификаций агента.
В проекте `hypotez` этот модуль используется для оценки качества создаваемых персонажей в Tiny Troupe, что позволяет убедиться в их соответствии заданным критериям и ролям.

## Классы

### `TinyPersonValidator`

**Описание**: Класс, предоставляющий статический метод для валидации экземпляров `TinyPerson`.

**Методы**:

- `validate_person`: Статический метод для валидации персонажа.

## Методы класса

### `validate_person`

```python
@staticmethod
def validate_person(person, expectations=None, include_agent_spec=True, max_content_length=default_max_content_display_length) -> tuple[float, str]:
    """
    Validate a TinyPerson instance using OpenAI's LLM.

    This method sends a series of questions to the TinyPerson instance to validate its responses using OpenAI's LLM.
    The method returns a float value representing the confidence score of the validation process.
    If the validation process fails, the method returns None.

    Args:
        person (TinyPerson): The TinyPerson instance to be validated.
        expectations (str, optional): The expectations to be used in the validation process. Defaults to None.
        include_agent_spec (bool, optional): Whether to include the agent specification in the prompt. Defaults to False.
        max_content_length (int, optional): The maximum length of the content to be displayed when rendering the conversation.

    Returns:
        float: The confidence score of the validation process (0.0 to 1.0), or None if the validation process fails.
        str: The justification for the validation score, or None if the validation process fails.
    """
    ...
```

**Назначение**: Валидация экземпляра `TinyPerson` с использованием LLM OpenAI. Метод отправляет серию вопросов `TinyPerson` для проверки его ответов.

**Параметры**:

- `person` (TinyPerson): Экземпляр `TinyPerson`, который необходимо проверить.
- `expectations` (str, optional): Ожидания, используемые в процессе валидации. По умолчанию `None`.
- `include_agent_spec` (bool, optional): Флаг, указывающий, следует ли включать спецификацию агента в запрос. По умолчанию `True`.
- `max_content_length` (int, optional): Максимальная длина содержимого, отображаемого при рендеринге разговора. По умолчанию значение берется из конфига `default_max_content_display_length`.

**Возвращает**:

- `tuple[float, str]`: Кортеж, содержащий оценку достоверности процесса валидации (от 0.0 до 1.0) и обоснование оценки. Возвращает `None, None` в случае неудачи.

**Как работает функция**:
- Функция начинает с инициализации списка сообщений `current_messages`.
- Далее формируется системный запрос на основе шаблона `check_person.mustache`, в который передаются ожидания (`expectations`).
- Формируется пользовательский запрос, который включает либо мини-биографию персонажа, либо его полную спецификацию (`_persona`).
- Затем, отправляются начальные сообщения в LLM.
- В цикле, пока не будет достигнут маркер завершения (`termination_mark`), функция получает вопросы от LLM, задает их персонажу через метод `person.listen_and_act` и отправляет ответы персонажа обратно в LLM.
- После завершения цикла функция извлекает оценку и обоснование из JSON, содержащегося в последнем сообщении, и возвращает их.
- Логирование осуществляется с использованием модуля `logger` из `src.logger`.

**Примеры**:

```python
# Пример использования функции validate_person
from tinytroupe.agent import TinyPerson
from tinytroupe.tinyperson_validator import TinyPersonValidator

# Создание экземпляра TinyPerson (предположим, что есть такой класс и инициализация)
person = TinyPerson(name="TestPerson", age=30, occupation="Tester")

# Валидация персонажа
score, justification = TinyPersonValidator.validate_person(person, expectations="Ожидается, что персонаж будет честным и открытым.")

if score is not None:
    print(f"Оценка валидации: {score:.2f}")
    print(f"Обоснование: {justification}")
else:
    print("Процесс валидации не удался.")
```

## Параметры класса

- `default_max_content_display_length` (int): Максимальная длина отображаемого содержимого.

```python
default_max_content_display_length = config["OpenAI"].getint("MAX_CONTENT_DISPLAY_LENGTH", 1024)
```

**Назначение**: Определение максимальной длины контента, отображаемого при рендеринге разговора.

**Примеры**:

```python
# Пример использования параметра default_max_content_display_length
print(f"Максимальная длина контента: {default_max_content_display_length}")