# Модуль validation.py

## Обзор

Модуль `validation.py` предназначен для валидации экземпляров класса `TinyPerson` с использованием OpenAI LLM. Он содержит класс `TinyPersonValidator` с методом `validate_person`, который отправляет серию вопросов экземпляру `TinyPerson` и оценивает ответы на основе заданных ожиданий.

## Подробней

Модуль использует шаблоны Mustache для генерации промптов, которые затем отправляются в OpenAI для оценки ответов `TinyPerson`. Валидация включает в себя оценку уверенности (confidence score) и обоснование (justification) оценки. Логирование процесса валидации осуществляется через модуль `src.logger`.

## Классы

### `TinyPersonValidator`

**Описание**: Класс, содержащий статический метод для валидации экземпляров `TinyPerson`.

**Атрибуты**:
- Отсутствуют. Класс содержит только статические методы.

**Методы**:
- `validate_person`: Статический метод, выполняющий валидацию экземпляра `TinyPerson`.

## Методы класса

### `validate_person`

```python
    @staticmethod
    def validate_person(person, expectations=None, include_agent_spec=True, max_content_length=default_max_content_display_length) -> tuple[float, str] | tuple[None, None]:
        """
        Validate a TinyPerson instance using OpenAI\'s LLM.\n

        This method sends a series of questions to the TinyPerson instance to validate its responses using OpenAI\'s LLM.\n
        The method returns a float value representing the confidence score of the validation process.\n
        If the validation process fails, the method returns None.\n

        Args:\n
            person (TinyPerson): The TinyPerson instance to be validated.\n
            expectations (str, optional): The expectations to be used in the validation process. Defaults to None.\n
            include_agent_spec (bool, optional): Whether to include the agent specification in the prompt. Defaults to True.\n
            max_content_length (int, optional): The maximum length of the content to be displayed when rendering the conversation.\n

        Returns:\n
            float: The confidence score of the validation process (0.0 to 1.0), or None if the validation process fails.\n
            str: The justification for the validation score, or None if the validation process fails.
        """
```

**Назначение**: Валидация экземпляра `TinyPerson` с использованием OpenAI LLM.

**Параметры**:
- `person` (TinyPerson): Экземпляр `TinyPerson`, который необходимо проверить.
- `expectations` (str, optional): Ожидания, используемые в процессе проверки. По умолчанию `None`.
- `include_agent_spec` (bool, optional): Флаг, указывающий, следует ли включать спецификацию агента в запрос. По умолчанию `True`.
- `max_content_length` (int, optional): Максимальная длина содержимого, отображаемого при рендеринге разговора.

**Возвращает**:
- `tuple[float, str] | tuple[None, None]`: Кортеж, содержащий оценку уверенности (confidence score) и обоснование оценки, или `None`, если проверка не удалась.

**Как работает функция**:
1. **Инициализация**:
   - Инициализируется список сообщений `current_messages` для хранения контекста разговора с LLM.

2. **Подготовка промпта**:
   - Определяется путь к шаблону промпта `check_person.mustache`.
   - Шаблон загружается и рендерится с использованием библиотеки `chevron`, вставляя в него предоставленные ожидания `expectations`.
   - Создается `system_prompt` на основе отрендеренного шаблона.

3. **Формирование пользовательского промпта**:
   - Формируется `user_prompt` с инструкциями для LLM, включающий характеристики `TinyPerson`.
   - Если `include_agent_spec` имеет значение `True`, в промпт добавляется спецификация агента, сгенерированная методом `person.generate_agent_specification()`.
   - В противном случае, в промпт добавляется мини-биография `TinyPerson`, полученная методом `person.minibio()`.

4. **Взаимодействие с LLM**:
   - В список сообщений добавляются `system_prompt` и `user_prompt`.
   - Сообщение отправляется в OpenAI с использованием `openai_utils.client().send_message(current_messages)`.
   - В цикле происходит обмен вопросами и ответами между LLM и `TinyPerson` до тех пор, пока в ответе LLM не появится маркер завершения `termination_mark` (```json).
   - Вопросы от LLM логируются с уровнем `INFO` с использованием `logger.info(f"Question validation:\n{questions}")`.
   - Ответы `TinyPerson` на вопросы получаются с помощью метода `person.listen_and_act(questions, max_content_length=max_content_length)`, а затем извлекаются с использованием `person.pop_actions_and_get_contents_for("TALK", False)`.
   - Ответы `TinyPerson` также логируются с уровнем `INFO` с использованием `logger.info(f"Person reply:\n{responses}")`.

5. **Извлечение результатов валидации**:
   - После получения сообщения с маркером завершения, извлекается JSON-содержимое из ответа LLM с помощью функции `utils.extract_json(message['content'])`.
   - Извлекаются значения `score` и `justification` из JSON-содержимого.
   - Результаты валидации логируются с уровнем `INFO` с использованием `logger.info(f"Validation score: {score:.2f}; Justification: {justification}")`.

6. **Возврат результатов**:
   - Возвращается кортеж, содержащий оценку `score` и обоснование `justification`.
   - Если в процессе выполнения произошла ошибка или не удалось получить результаты, возвращается кортеж `(None, None)`.

**Примеры**:

Пример вызова функции:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.validation import TinyPersonValidator

# Пример создания экземпляра TinyPerson (предположим, что такой код существует)
person = TinyPerson(name="TestPerson", description="A test person", persona="A test persona")

# Пример вызова validate_person
score, justification = TinyPersonValidator.validate_person(person, expectations="Some expectations")

if score is not None and justification is not None:
    print(f"Score: {score}, Justification: {justification}")
else:
    print("Validation failed.")
```

## Параметры класса

- `default_max_content_display_length` (int): Максимальная длина отображаемого контента. Получается из конфигурационного файла.

```python
default_max_content_display_length = config["OpenAI"].getint("MAX_CONTENT_DISPLAY_LENGTH", 1024)