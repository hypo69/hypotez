# Модуль валидации TinyPerson

## Обзор

Модуль `validation.py` предназначен для валидации экземпляров класса `TinyPerson` с использованием языковой модели OpenAI. Он содержит класс `TinyPersonValidator` с методом `validate_person`, который отправляет серию вопросов экземпляру `TinyPerson` и оценивает ответы с помощью LLM.

## Подробней

Модуль выполняет проверку соответствия поведения виртуального персонажа заданным ожиданиям. Он использует шаблоны для генерации запросов к языковой модели, а также функции для извлечения JSON из ответов модели. Валидация включает в себя обмен сообщениями с `TinyPerson`, логирование процесса и оценку полученных результатов. Располагается в подкаталоге `tinytroupe` и является частью системы моделирования виртуальных персонажей.

## Классы

### `TinyPersonValidator`

**Описание**: Класс, содержащий статический метод для валидации экземпляров `TinyPerson`.

**Атрибуты**:
-   Отсутствуют.

**Методы**:
-   `validate_person`: Статический метод для валидации `TinyPerson`.

## Методы класса

### `validate_person`

```python
@staticmethod
def validate_person(person, expectations=None, include_agent_spec=True, max_content_length=default_max_content_display_length) -> float:
    """
    Validate a TinyPerson instance using OpenAI's LLM.

    This method sends a series of questions to the TinyPerson instance to validate its responses using OpenAI's LLM.
    The method returns a float value representing the confidence score of the validation process.
    If the validation process fails, the method returns None.

    Args:
        person (TinyPerson): The TinyPerson instance to be validated.
        expectations (str, optional): The expectations to be used in the validation process. Defaults to None.
        include_agent_spec (bool, optional): Whether to include the agent specification in the prompt. Defaults to True.
        max_content_length (int, optional): The maximum length of the content to be displayed when rendering the conversation.

    Returns:
        float: The confidence score of the validation process (0.0 to 1.0), or None if the validation process fails.
        str: The justification for the validation score, or None if the validation process fails.
    """
    ...
```

**Назначение**: Валидирует экземпляр `TinyPerson`, используя языковую модель OpenAI.

**Параметры**:
-   `person` (`TinyPerson`): Экземпляр `TinyPerson`, который необходимо проверить.
-   `expectations` (`str`, optional): Ожидания, используемые в процессе валидации. По умолчанию `None`.
-   `include_agent_spec` (`bool`, optional): Определяет, включать ли спецификацию агента в запрос. По умолчанию `True`.
-   `max_content_length` (`int`, optional): Максимальная длина контента, отображаемого при рендеринге разговора. По умолчанию берется из конфигурации `config["OpenAI"].getint("MAX_CONTENT_DISPLAY_LENGTH", 1024)`.

**Возвращает**:
-   `float`: Оценка уверенности в процессе валидации (от 0.0 до 1.0).
-   `str`: Обоснование оценки валидации.
    Возвращает `None, None`, если процесс валидации завершается неудачей.

**Как работает функция**:

1.  Инициализирует список `current_messages` для хранения сообщений, которыми обменивается валидатор и `TinyPerson`.
2.  Формирует запрос `check_agent_prompt_template` на основе шаблона `prompts/check_person.mustache` и заданных ожиданий `expectations`.
3.  Создает системное сообщение `system_prompt` на основе сформированного шаблона.
4.  Формирует пользовательский запрос `user_prompt` на основе характеристик `person` и правил, заданных ранее. Добавляет либо спецификацию агента (`person.generate_agent_specification()`), либо мини-биографию (`person.minibio()`) в зависимости от значения `include_agent_spec`.
5.  Инициализирует логгер `logger` для записи информации о процессе валидации.
6.  Отправляет начальные сообщения в LLM, добавляя системное сообщение `system_prompt` и пользовательский запрос `user_prompt` в `current_messages`.
7.  Получает ответ `message` от LLM с помощью `openai_utils.client().send_message(current_messages)`.
8.  Запускает цикл `while`, который продолжается до тех пор, пока `message` не равно `None` и пока в содержимом `message` не будет найдена строка завершения `termination_mark = "```json"`.
9.  В цикле:
    -   Извлекает вопросы `questions` из содержимого `message` и добавляет их в `current_messages`.
    -   Записывает вопросы в лог с помощью `logger.info(f"Question validation:\\n{questions}")`.
    -   Запрашивает ответы у `person` с помощью `person.listen_and_act(questions, max_content_length=max_content_length)`.
    -   Получает ответы `responses` от `person` с помощью `person.pop_actions_and_get_contents_for("TALK", False)` и записывает их в лог.
    -   Добавляет ответы `responses` в `current_messages` и отправляет новый запрос в LLM.
10. После завершения цикла проверяет, что `message` не равно `None`. Если это так:
    -   Извлекает JSON из содержимого `message` с помощью `utils.extract_json(message['content'])`.
    -   Извлекает оценку `score` и обоснование `justification` из JSON.
    -   Записывает оценку и обоснование в лог.
    -   Возвращает оценку `score` и обоснование `justification`.
11. Если `message` равно `None`, возвращает `None, None`.

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.validation import TinyPersonValidator

# Пример создания экземпляра TinyPerson (предположим, что параметры определены)
person = TinyPerson(name="TestPerson", description="A test person", age=25)

# Пример вызова validate_person с минимальными параметрами
score, justification = TinyPersonValidator.validate_person(person)
if score is not None:
    print(f"Validation score: {score:.2f}")
    print(f"Justification: {justification}")
else:
    print("Validation failed.")

# Пример вызова validate_person с указанием ожиданий
score, justification = TinyPersonValidator.validate_person(person, expectations="The person should be friendly and helpful.")
if score is not None:
    print(f"Validation score: {score:.2f}")
    print(f"Justification: {justification}")
else:
    print("Validation failed.")
```

## Параметры класса

-   `default_max_content_display_length` (`int`): Максимальная длина отображаемого содержимого по умолчанию, извлекается из конфигурации `config["OpenAI"].getint("MAX_CONTENT_DISPLAY_LENGTH", 1024)`.