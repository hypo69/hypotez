# Модуль для валидации TinyPerson
## Обзор

Модуль `tiny_person_validator.py` предназначен для проверки экземпляров класса `TinyPerson` с использованием языковой модели OpenAI. Он содержит класс `TinyPersonValidator` с методом `validate_person`, который оценивает соответствие `TinyPerson` заданным ожиданиям и возвращает оценку уверенности и обоснование.

## Подробнее

Этот модуль играет важную роль в проекте `hypotez`, поскольку обеспечивает механизм для оценки и проверки поведения виртуальных персонажей (TinyPerson) на основе заданных критериев. Он использует OpenAI LLM для анализа ответов персонажа и определения, насколько они соответствуют ожидаемым. Это позволяет автоматизировать процесс проверки и оценки качества виртуальных агентов.

## Классы

### `TinyPersonValidator`

**Описание**: Класс, содержащий статический метод для валидации экземпляров `TinyPerson`.

**Методы**:

- `validate_person`: Статический метод, выполняющий валидацию `TinyPerson` с использованием OpenAI LLM.

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

**Назначение**: Валидация экземпляра `TinyPerson` с использованием языковой модели OpenAI.

**Параметры**:

- `person` (TinyPerson): Экземпляр `TinyPerson`, который необходимо проверить.
- `expectations` (str, optional): Ожидания, используемые в процессе валидации. По умолчанию `None`.
- `include_agent_spec` (bool, optional): Флаг, определяющий, следует ли включать спецификацию агента в запрос. По умолчанию `False`.
- `max_content_length` (int, optional): Максимальная длина контента, отображаемого при рендеринге разговора. По умолчанию `default_max_content_display_length`.

**Возвращает**:

- `tuple[float, str]`: Кортеж, содержащий оценку уверенности валидации (от 0.0 до 1.0) и обоснование оценки. Возвращает `None, None`, если процесс валидации завершается неудачно.

**Как работает функция**:

1.  Инициализирует список сообщений для текущего разговора (`current_messages`).
2.  Формирует системный промпт (`system_prompt`) на основе шаблона `check_person.mustache`, который содержит ожидания относительно поведения персонажа.
3.  Формирует пользовательский промпт (`user_prompt`), который включает в себя характеристики проверяемого персонажа (мини-биографию или полную спецификацию).
4.  Отправляет начальные сообщения в LLM (языковую модель).
5.  В цикле, пока не будет достигнута метка завершения (`termination_mark`), отправляет вопросы персонажу, получает ответы, добавляет их в историю разговора и отправляет следующий запрос в LLM.
6.  Извлекает оценку и обоснование из JSON-контента, содержащегося в последнем сообщении от LLM.
7.  Логирует оценку и обоснование.
8.  Возвращает оценку и обоснование в виде кортежа.

**Примеры**:

```python
# Пример вызова функции validate_person
from tinytroupe.agent import TinyPerson
# from src.endpoints.tiny_troupe.tinytroupe (2)/validation.tiny_person_validator import TinyPersonValidator # fix import
person = TinyPerson(name="TestPerson", profile="TestProfile")
score, justification = TinyPersonValidator.validate_person(person, expectations="Must be friendly")
if score is not None:
    print(f"Validation score: {score:.2f}")
    print(f"Justification: {justification}")
else:
    print("Validation failed")
```
## Переменные модуля

- `default_max_content_display_length` (int): Максимальная длина отображаемого контента, устанавливается из конфигурации OpenAI. По умолчанию 1024.

```python
default_max_content_display_length = config["OpenAI"].getint("MAX_CONTENT_DISPLAY_LENGTH", 1024)