# Модуль Ails

## Обзор

Модуль `Ails` предоставляет функции для взаимодействия с API-интерфейсом чат-бота Ails, 
а также для создания запросов к нему и обработки ответов. 

## Подробней

Модуль содержит функцию `_create_completion`, которая используется для создания запросов к API-интерфейсу Ails. 
Он также содержит класс `Utils` для форматирования дат, хэширования данных и выполнения других вспомогательных задач.

**Как работает:**

1. Функция `_create_completion` формирует JSON-запрос к API-интерфейсу Ails, 
   устанавливая заголовки и параметры для запроса.
2. В запросе используется `Bearer` токен "free" для аутентификации.
3. Функция `_create_completion` отправляет POST-запрос на URL-адрес API-интерфейса и 
   возвращает ответ в виде потока токенов. 
4. Класс `Utils` используется для хэширования данных и форматирования временных меток.

## Классы

### `class Utils`

**Описание**: Класс `Utils` содержит набор вспомогательных функций для работы с 
модулем `Ails`.

**Атрибуты**: 

**Методы**:

- `hash(json_data: Dict[str, str]) -> sha256`: Функция генерирует хэш-сумму 
  используя SHA-256 алгоритм для заданного JSON-объекта.
  
  **Параметры**:
  - `json_data` (Dict[str, str]): Входной JSON-объект, который нужно хэшировать.

  **Возвращает**:
  - `sha256`: Хэш-сумма JSON-объекта.

  **Как работает**: 
  - Функция преобразует JSON-объект в строку.
  - Функция добавляет секретный ключ и длину строки к строке.
  - Функция использует SHA-256 алгоритм для генерации хэш-суммы.
  - Функция возвращает хэш-сумму в виде шестнадцатеричного представления.

- `format_timestamp(timestamp: int) -> str`: Функция форматирует временную метку.

  **Параметры**:
  - `timestamp` (int): Временная метка в миллисекундах.

  **Возвращает**:
  - `str`: Форматированная временная метка.

  **Как работает**: 
  - Функция вычисляет секунды с момента эпохи.
  - Функция возвращает форматированную временную метку.

## Функции

### `_create_completion(model: str, messages: list, temperature: float = 0.6, stream: bool = False, **kwargs)`

**Назначение**: Функция создает запрос к API-интерфейсу Ails для генерации 
комментариев.

**Параметры**:

- `model` (str): Имя модели.
- `messages` (list): Список сообщений для чат-бота.
- `temperature` (float, optional): Параметр, отвечающий за креативность 
  и разнообразие ответов. По умолчанию 0.6.
- `stream` (bool, optional): Флаг, определяющий, нужно ли получать ответ в виде 
  потока токенов. По умолчанию `False`.

**Возвращает**:
- `Generator[str, None, None]`: Генератор, который возвращает токены ответа 
  в виде строк.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при отправке запроса.

**Как работает**:

1. Функция устанавливает заголовки для запроса.
2. Функция создает JSON-объект запроса, включающий в себя сообщения, 
   параметры модели и временную метку.
3. Функция хэширует сообщение using `Utils.hash`.
4. Функция отправляет POST-запрос к API-интерфейсу Ails.
5. Функция получает ответ в виде потока токенов.
6. Функция возвращает генератор, который выдает токены ответа в виде строк.

**Примеры**:

```python
from g4f.Provider.Providers.Ails import _create_completion

messages = [
    {'role': 'user', 'content': 'Привет! Как дела?'},
]

response = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True)

for token in response:
    print(token)
```

## Параметры

## Примеры

```python
# Пример хэширования JSON-объекта
from g4f.Provider.Providers.Ails import Utils

json_data = {
    't': '1683335888839',
    'm': 'Привет! Как дела?'
}

hash_value = Utils.hash(json_data)

print(f'Hash: {hash_value}')

# Пример форматирования временной метки
from g4f.Provider.Providers.Ails import Utils

timestamp = int(time.time() * 1000)

formatted_timestamp = Utils.format_timestamp(timestamp)

print(f'Formatted timestamp: {formatted_timestamp}')
```