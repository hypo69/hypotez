# Модуль `Berlin` для работы с GPT-4 Free

## Обзор

Модуль `Berlin` предоставляет реализацию асинхронного генератора для взаимодействия с API GPT-4 Free, который доступен на сайте `ai.berlin4h.top`. 

## Подробней

Модуль `Berlin` обеспечивает возможность использования GPT-4 Free  с помощью асинхронного генератора, предоставляя удобный способ обработки больших объемов данных и  выполнения задач, связанных с генерацией текста, переводом,  кодированием и др.

## Классы

### `class Berlin`

**Описание**: Класс `Berlin`  - асинхронный генератор для работы с GPT-4 Free, реализующий интерфейс `AsyncGeneratorProvider`  

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

 - `url (str)`: URL-адрес API GPT-4 Free.
 - `working (bool)`: Флаг, указывающий на то,  работает ли провайдер. 
 - `supports_gpt_35_turbo (bool)`: Флаг, указывающий, поддерживается ли модель GPT-3.5 Turbo.
 - `_token (str)`:  Токен авторизации, используемый для доступа к API.

**Методы**:

 - `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`:  Создает асинхронный генератор, который используется для взаимодействия с API GPT-4 Free.

   **Назначение**: Метод инициализирует асинхронный генератор для выполнения запросов к API GPT-4 Free.

   **Параметры**:

   - `model (str)`: Имя модели GPT-4 Free, используемой для генерации текста.
   - `messages (Messages)`: Список сообщений, которые необходимо передать в качестве входных данных  GPT-4 Free.
   - `proxy (str, optional)`: Прокси-сервер, который необходимо использовать для доступа к API. По умолчанию  `None`.
   - `**kwargs`: Дополнительные аргументы, передаваемые модели GPT-4 Free.

   **Возвращает**:
   - `AsyncResult`: Объект, содержащий результаты выполнения запроса.

   **Вызывает исключения**:
   - `RuntimeError`: Возникает, если  получен неверный ответ от API.
   - `HTTPError`:  Возникает, если произошла ошибка HTTP при выполнении запроса к API.


   **Как работает**:
   - Метод `create_async_generator`  инициализирует асинхронный генератор с использованием библиотеки `aiohttp`.
   - Он выполняет аутентификацию  с использованием `_token`, а затем отправляет запрос к API GPT-4 Free.
   - После получения ответа  от API, метод  декодирует данные в формате JSON и  возвращает асинхронный генератор, который может быть использован для получения результатов в виде  последовательных  частей ответа.

**Примеры**:
 
 ```python
 from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Berlin import Berlin
 from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
 
 messages: Messages = [
     {"role": "user", "content": "Привет, как дела?"},
 ]
 async_generator = await Berlin.create_async_generator(model="gpt-3.5-turbo", messages=messages)
 async for chunk in async_generator:
     print(f"Полученный ответ: {chunk}")
 ```

## Внутренние функции

### `_token`

**Назначение**: Геттер  для доступа к `_token`. 

**Параметры**:  
 - `None`.

**Возвращает**:
 - `str`: Токен авторизации.

**Вызывает исключения**:
 - `None`.

**Как работает**:
 -  Метод `_token`  предоставляет доступ к атрибуту  `_token`, который содержит  токен авторизации для доступа к API GPT-4 Free.
 -  Он позволяет получить значение токена  из контекста класса.

**Примеры**:
 ```python
 from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Berlin import Berlin
 
 token = Berlin._token
 print(f"Токен авторизации: {token}")
 ```

## Параметры класса

- `url (str)`:  Адрес  API GPT-4 Free.
- `working (bool)`:  Флаг, указывающий на то,  работает ли провайдер.
- `supports_gpt_35_turbo (bool)`: Флаг, указывающий, поддерживается ли модель GPT-3.5 Turbo. 
- `_token (str)`: Токен авторизации, используемый для доступа к API.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Berlin import Berlin

print(f"URL API GPT-4 Free: {Berlin.url}")
print(f"Провайдер работает: {Berlin.working}")
print(f"Поддержка GPT-3.5 Turbo: {Berlin.supports_gpt_35_turbo}")
print(f"Токен авторизации: {Berlin._token}")
```