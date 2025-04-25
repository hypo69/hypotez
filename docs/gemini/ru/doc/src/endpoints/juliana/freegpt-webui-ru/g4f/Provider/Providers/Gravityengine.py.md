# Gravityengine.py

## Обзор

Этот файл содержит код для взаимодействия с сервисом GravityEngine, который предоставляет API для работы с языковыми моделями. 

## Подробней

Файл содержит функции, отвечающие за отправку запросов на API GravityEngine. 

### Как работает код

1.  **Загрузка модулей:**  Код импортирует необходимые модули, такие как `json` для работы с JSON, `requests` для отправки HTTP запросов, `uuid` для генерации уникальных идентификаторов, `get_type_hints` для получения информации о типах аргументов функций.
2.  **Определение констант:**  Определены переменные:
    *   `url`:  URL-адрес API GravityEngine.
    *   `model`:  Список поддерживаемых моделей, таких как `gpt-3.5-turbo-16k`.
    *   `supports_stream`:  Флаг, указывающий на поддержку потокового вывода.
    *   `needs_auth`:  Флаг, указывающий на необходимость аутентификации.
3.  **Функция `_create_completion`:**
    *   Функция принимает на вход модель (`model`), список сообщений (`messages`), флаг потокового вывода (`stream`) и другие аргументы (`**kwargs`).
    *   Функция создает заголовки HTTP-запроса (`headers`) и данные (`data`) для отправки на API.
    *   Функция отправляет POST-запрос на API GravityEngine с использованием модуля `requests`.
    *   Функция возвращает генератор (`yield`), который позволяет получать ответ API частями.
4.  **Определение параметров:**  Определяется строка, содержащая информацию о поддерживаемых типах аргументов функции `_create_completion`.

## Функции

### `_create_completion`

**Назначение**: 
Функция формирует и отправляет запрос на API GravityEngine, чтобы получить ответ от языковой модели.

**Параметры**:

*   `model` (str): Имя модели, например `gpt-3.5-turbo-16k`.
*   `messages` (list): Список сообщений для отправки в модель.
*   `stream` (bool): Флаг, указывающий на необходимость потокового вывода.

**Возвращает**:
*   `Generator[str, None, None]`: Генератор, который позволяет получать ответ API частями.

**Вызывает исключения**:
*   `None`.

**Как работает функция**:

1.  **Создание заголовков и данных**: Функция создает заголовки (`headers`) и данные (`data`) для POST-запроса на API. В данные добавляются модель (`model`), сообщения (`messages`), а также другие параметры, такие как `temperature`, `presence_penalty` и т. д.
2.  **Отправка запроса**: Функция отправляет POST-запрос на API GravityEngine (`url + '/api/openai/v1/chat/completions'`) с помощью модуля `requests`.
3.  **Обработка ответа**: Функция получает ответ API в виде JSON (`response.json()`) и извлекает из него текст сообщения (`response.json()['choices'][0]['message']['content']`).
4.  **Возврат генератора**: Функция возвращает генератор (`yield`) для получения ответа API частями.

**Пример**:

```python
messages = [
    {"role": "user", "content": "Привет, как дела?"},
]

for part in _create_completion(model="gpt-3.5-turbo-16k", messages=messages, stream=True):
    print(part)
```

## Примеры

```python
# Пример использования функции _create_completion
model = "gpt-3.5-turbo-16k"
messages = [
    {"role": "user", "content": "Привет, как дела?"},
]
for part in _create_completion(model=model, messages=messages, stream=True):
    print(part)
```

```python
# Пример использования функции _create_completion
model = "gpt-3.5-turbo-16k"
messages = [
    {"role": "user", "content": "Привет, как дела?"},
]
for part in _create_completion(model=model, messages=messages, stream=True):
    print(part)
```
```markdown