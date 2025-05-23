# H2o.py

## Обзор

Этот модуль предоставляет класс для взаимодействия с моделью H2o GPT, используя API h2o.ai.  Модуль поддерживает функции для создания запросов к API h2o.ai, получения ответов и обработки ответов в потоковом режиме.

## Подробности

Модуль `H2o.py` реализует функциональность для взаимодействия с моделью GPT, предоставляемой компанией H2o.ai. Он использует библиотеку `requests` для отправки HTTP-запросов к API h2o.ai и парсит ответы с использованием модуля `json`. 

## Классы

### `class _create_completion`

**Описание**: Класс реализует функцию для создания запроса к модели H2o GPT и получения ответа.

**Наследует**: 

**Атрибуты**:

**Параметры**:

**Принцип работы**: 
-  Функция `_create_completion` создает запрос к API h2o.ai с использованием библиотеки `requests`. 
- Запрос содержит информацию о модели, сообщениях в диалоге,  параметрах запроса и настройках потоковой передачи.
- Функция  `_create_completion`  обрабатывает ответ, полученный от API H2o GPT. 
- Обработка происходит в потоковом режиме: 
    - ответ разбивается на части (токены),
    - части отправляются в выходной поток.

**Методы**:

**Примеры**:

```python
from src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.H2o import _create_completion

messages = [
    {'role': 'user', 'content': 'Привет, как дела?'},
]

# создание запроса к модели H2o GPT с использованием функции _create_completion
for token in _create_completion(model='falcon-7b', messages=messages, stream=True):
    print(token)
```

## Функции

### `_create_completion`

**Назначение**: Функция отправляет запрос к модели GPT с использованием API h2o.ai и возвращает ответ в потоковом режиме.

**Параметры**:

- `model` (str): Название модели GPT (например, `falcon-7b`).
- `messages` (list): Список сообщений в диалоге.
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу данных.

**Возвращает**:

- `Generator[str, None, None]`: Генератор, возвращающий токены ответа.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при отправке запроса или получении ответа.

**Как работает функция**:

1. Формирует запрос к API h2o.ai, используя метод `post`.
2. В запросе устанавливаются заголовки (`headers`) и данные (`data`) для отправки.
3. Данные запроса включают `model`, `conversation`, `parameters` и `options`.
4. `conversation` формируется из списка сообщений в диалоге.
5. `parameters` содержит параметры модели (температура, ограничение количества токенов, повторение штрафа и т.д.)
6. `options` содержат настройки для обработки ответа.
7. Отправляет запрос к API h2o.ai.
8. Получает ответ в потоковом режиме.
9. Разбирает ответ на токены.
10. Возвращает токены через генератор.


**Примеры**:

```python
from src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.H2o import _create_completion

messages = [
    {'role': 'user', 'content': 'Привет, как дела?'},
]

# отправка запроса к модели H2o GPT и получение ответа в потоковом режиме
for token in _create_completion(model='falcon-7b', messages=messages, stream=True):
    print(token)

```

## Параметры модуля

- `url` (str): URL-адрес API h2o.ai.
- `model` (list): Список поддерживаемых моделей GPT.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли модель потоковую передачу данных.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация для доступа к API.

## Дополнительные сведения

- Модуль `H2o.py`  представляет собой класс, который реализует функциональность для взаимодействия с API h2o.ai.
- Он используется для отправки запросов к модели GPT и получения ответов в потоковом режиме. 
- Модуль реализует стандартные методы для работы с API h2o.ai.
- Модуль `H2o.py` является частью проекта `hypotez`.