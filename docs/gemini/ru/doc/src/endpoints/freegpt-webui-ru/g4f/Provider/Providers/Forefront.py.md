# Модуль `Forefront`
## Обзор

Модуль содержит класс `Forefront` для работы с моделью Forefront от Google. Он реализует интерфейс `Provider` и предоставляет функции для отправки запросов к API Forefront и обработки ответов.

## Подробней

Этот файл является частью реализации `Provider` для модели `Forefront`, разработанной компанией Google. Forefront предоставляет доступ к передовой модели машинного обучения, которая может генерировать текст, переводить языки, писать разные виды творческих материалов и отвечать на ваши вопросы информативно.

## Классы

### `class Forefront`

**Описание**: Класс для взаимодействия с моделью Forefront от Google.

**Наследует**: `Provider`

**Атрибуты**:

- `url` (str): URL-адрес API Forefront.
- `model` (list): Список поддерживаемых моделей (в данном случае, `gpt-3.5-turbo`).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи ответов (True).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (False).

**Методы**:

- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: Функция для отправки запроса к API Forefront и обработки ответов.


## Функции

### `_create_completion(model: str, messages: list, stream: bool, **kwargs)`

**Назначение**: Отправляет запрос к API Forefront и обрабатывает ответы.

**Параметры**:

- `model` (str): Имя модели, которую следует использовать для генерации текста.
- `messages` (list): Список сообщений для модели.
- `stream` (bool): Флаг, указывающий на необходимость потоковой передачи ответов.
- `**kwargs`: Дополнительные аргументы, передаваемые в API Forefront.

**Возвращает**:

- `Generator[str, None, None]`: Генератор строк, содержащий токены ответа.

**Как работает функция**:

1. Формирует JSON-запрос к API Forefront.
2. Отправляет POST-запрос к API Forefront с помощью библиотеки `requests`.
3. Обрабатывает ответ от API в формате потока данных.
4. Извлекает токены ответа, декодируя их из JSON-формата и преобразуя в строки.
5. Возвращает генератор, который выдает токены ответа по одному.

**Примеры**:

```python
# Пример отправки запроса к API Forefront
response = _create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Привет'}], stream=True)
for token in response:
    print(token)
```

## Параметры

- `url` (str): URL-адрес API Forefront. 
- `model` (list): Список поддерживаемых моделей (в данном случае, `gpt-3.5-turbo`).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи ответов (True).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (False).

**Примеры**:

```python
# Пример использования модуля Forefront
from hypotez.src.endpoints.freegpt-webui-ru.g4f.Provider.Providers.Forefront import Forefront

# Создание инстанса класса Forefront
forefront_provider = Forefront()

# Получение списка поддерживаемых моделей
print(forefront_provider.model)

# Отправка запроса к API Forefront
response = forefront_provider.create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Привет'}], stream=True)
for token in response:
    print(token)
```