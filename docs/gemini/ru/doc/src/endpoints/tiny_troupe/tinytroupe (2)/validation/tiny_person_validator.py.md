# Модуль проверки персонажей TinyPerson

## Обзор

Этот модуль содержит класс `TinyPersonValidator`, который используется для валидации персонажей TinyPerson с помощью языковой модели OpenAI. 

## Подробнее

Валидация персонажа осуществляется путем задавания ему серии вопросов, которые генерируются языковой моделью OpenAI. Модель OpenAI оценивает ответы персонажа и выставляет ему оценку, которая отражает уровень соответствия заданным требованиям.

## Классы

### `TinyPersonValidator`

**Описание**: Класс, реализующий валидацию персонажа TinyPerson.

**Атрибуты**:

- Нет

**Методы**:

- `validate_person(person, expectations=None, include_agent_spec=True, max_content_length=default_max_content_display_length) -> tuple[float, str]`: Валидирует персонажа TinyPerson.


## Методы класса

### `validate_person`

```python
    def validate_person(person, expectations=None, include_agent_spec=True, max_content_length=default_max_content_display_length) -> tuple[float, str]:
        """
        Валидирует экземпляр TinyPerson с помощью языковой модели OpenAI.

        Этот метод отправляет серию вопросов экземпляру TinyPerson для проверки его ответов с помощью языковой модели OpenAI.
        Метод возвращает число с плавающей запятой, представляющее оценку уверенности в процессе валидации.
        Если процесс валидации завершается неудачей, метод возвращает None.

        Args:
            person (TinyPerson): Экземпляр TinyPerson для проверки.
            expectations (str, optional): Ожидания, которые будут использоваться в процессе проверки. По умолчанию None.
            include_agent_spec (bool, optional): Нужно ли включать спецификацию агента в запрос. По умолчанию True.
            max_content_length (int, optional): Максимальная длина контента для показа при отображении разговора.

        Returns:
            float: Оценка уверенности в процессе проверки (от 0.0 до 1.0), или None, если процесс проверки завершается неудачей.
            str: Обоснование оценки проверки, или None, если процесс проверки завершается неудачей.
        """
```

**Назначение**: Метод отправляет серию вопросов экземпляру TinyPerson для проверки его ответов с помощью языковой модели OpenAI.

**Параметры**:

- `person` (TinyPerson): Экземпляр TinyPerson для проверки.
- `expectations` (str, optional): Ожидания, которые будут использоваться в процессе проверки. По умолчанию None.
- `include_agent_spec` (bool, optional): Нужно ли включать спецификацию агента в запрос. По умолчанию True.
- `max_content_length` (int, optional): Максимальная длина контента для показа при отображении разговора.

**Возвращает**:

- `float`: Оценка уверенности в процессе проверки (от 0.0 до 1.0), или None, если процесс проверки завершается неудачей.
- `str`: Обоснование оценки проверки, или None, если процесс проверки завершается неудачей.

**Как работает функция**:

1. Инициализирует список текущих сообщений.
2. Генерирует запрос для проверки персонажа.
3. Вставляет спецификацию агента или мини-биографию в запрос в зависимости от параметра `include_agent_spec`.
4. Инициализирует логгер.
5. Отправляет начальные сообщения в языковую модель.
6. Определяет маркер завершения разговора.
7. В цикле повторяет следующие действия:
    - Извлекает вопросы из ответа модели.
    - Добавляет вопросы в список текущих сообщений.
    - Задает вопросы персонажу TinyPerson.
    - Получает ответы персонажа.
    - Добавляет ответы в список текущих сообщений.
    - Отправляет текущие сообщения в языковую модель.
8. Если модель вернула завершающее сообщение, извлекает оценку и обоснование.
9. Возвращает оценку и обоснование.
10. Если модель не вернула завершающего сообщения, возвращает None.

**Примеры**:

```python
#Пример вызова функции
person = TinyPerson(name='Alice', persona={'occupation': 'doctor'})
score, justification = TinyPersonValidator.validate_person(person)
print(f"Оценка: {score}, Обоснование: {justification}")

#Пример вызова функции с указанием ожиданий
expectations = 'The person should be a doctor and should be able to answer questions about their profession.'
score, justification = TinyPersonValidator.validate_person(person, expectations=expectations)
print(f"Оценка: {score}, Обоснование: {justification}")

#Пример вызова функции с отключением спецификации агента
score, justification = TinyPersonValidator.validate_person(person, include_agent_spec=False)
print(f"Оценка: {score}, Обоснование: {justification}")

#Пример вызова функции с ограничением длины контента
score, justification = TinyPersonValidator.validate_person(person, max_content_length=512)
print(f"Оценка: {score}, Обоснование: {justification}")