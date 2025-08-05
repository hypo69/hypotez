# Модуль Aichat 

## Обзор

Данный модуль предоставляет реализацию провайдера `Aichat` для `g4f`. 

`Aichat` - это провайдер, который использует API от `chat-gpt.org` для генерации текста. 

## Подробней

Модуль предоставляет следующие возможности:

- Генерация текста через `_create_completion` функцию.
-  Использование HTTP запросов для взаимодействия с `chat-gpt.org` API.
-  Определение поддерживаемых параметров для `_create_completion`.

## Классы

### `class Aichat`

**Описание**: 
Класс `Aichat`  реализует провайдера `Aichat` для `g4f`. 

**Атрибуты**:
 -  `url`: URL адрес сервера для взаимодействия.
 -  `model`: Список поддерживаемых моделей. 
 -  `supports_stream`: Флаг, который указывает, поддерживает ли провайдер потоковый режим.
 -  `needs_auth`: Флаг, который указывает, требуется ли авторизация для использования провайдера. 

**Методы**:
 -  `_create_completion`: Функция для создания запроса для генерации текста. 


## Функции

### `_create_completion`

**Назначение**: 
Функция `_create_completion` создает запрос для генерации текста. 

**Параметры**:
 -  `model`:  Название модели, которая используется для генерации текста. 
 -  `messages`: Список сообщений, которые используются для генерации текста.
 -  `stream`: Флаг, который указывает, нужно ли использовать потоковый режим. 
 -  `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
 -  `Generator[str, None, None]`: Генератор строк, содержащих текст, сгенерированный моделью.

**Вызывает исключения**:
 -  `requests.exceptions.RequestException`: Если возникает ошибка при отправке запроса на сервер.

**Как работает функция**:

 -  Сначала функция собирает сообщения из списка `messages` в единую строку `base`,  представляя их в формате, который ожидает API `chat-gpt.org`.
 -  Затем функция формирует заголовки `headers` для запроса. 
 -  Функция создает  `json_data`, который включает в себя `base`,  температуру  `temperature`, штраф за наличие  `presence_penalty`,  верхний p  `top_p`,  штраф за частоту  `frequency_penalty`.
 -  `json_data`  отправляется  `POST`  запросом на  `https://chat-gpt.org/api/text`  с  `headers`  и  `json_data`. 
 -  Функция возвращает  `Generator[str, None, None]`,  генерируя части  `message`  из ответа сервера.

**Примеры**:

```python
>>> messages = [
...     {'role': 'user', 'content': 'Привет, как дела?'},
... ]
>>> generator = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=False)
>>> next(generator)
'Привет! Как дела? У меня все отлично.'
```


## Параметры

 -  `url`: URL адрес сервера для взаимодействия.
 -  `model`: Список поддерживаемых моделей. 
 -  `supports_stream`: Флаг, который указывает, поддерживает ли провайдер потоковый режим.
 -  `needs_auth`: Флаг, который указывает, требуется ли авторизация для использования провайдера. 

**Примеры**:
```python
>>> from g4f.Provider.Providers.Aichat import Aichat
>>> provider = Aichat()
>>> provider.url
'https://chat-gpt.org/chat'
>>> provider.model
['gpt-3.5-turbo']
>>> provider.supports_stream
False
>>> provider.needs_auth
False
```

```python
>>> from g4f.Provider.Providers.Aichat import Aichat
>>> provider = Aichat()
>>> messages = [
...     {'role': 'user', 'content': 'Привет, как дела?'},
... ]
>>> generator = provider._create_completion(model='gpt-3.5-turbo', messages=messages, stream=False)
>>> next(generator)
'Привет! Как дела? У меня все отлично.'