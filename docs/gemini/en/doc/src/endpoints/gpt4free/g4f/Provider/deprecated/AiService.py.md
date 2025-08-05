# Модуль `AiService`

## Обзор

Модуль предоставляет класс `AiService`, реализующий взаимодействие с сервисом `aiservice.vercel.app` для генерации ответов на основе моделей GPT-3.5 Turbo. 

## Детали

`AiService` является наследником абстрактного класса `AbstractProvider` из модуля `base_provider`. Он предоставляет метод `create_completion`, который отправляет запрос на сервер `aiservice.vercel.app` для генерации ответа модели.

## Классы

### `class AiService`

**Описание**: Класс `AiService` представляет собой провайдера, который использует сервис `aiservice.vercel.app` для генерации текста с помощью моделей GPT-3.5 Turbo. 

**Наследует**: `AbstractProvider` из модуля `base_provider`

**Атрибуты**:

- `url (str)`: Базовый URL сервиса, с которым взаимодействует провайдер.
- `working (bool)`: Флаг, указывающий на доступность провайдера.
- `supports_gpt_35_turbo (bool)`: Флаг, указывающий на поддержку модели GPT-3.5 Turbo.

**Методы**:

- `create_completion(model: str, messages: Messages, stream: bool, **kwargs: Any) -> CreateResult`

## Классные методы

### `create_completion`

**Описание**: Метод `create_completion` отправляет запрос на сервер `aiservice.vercel.app` для генерации ответа модели. 

**Параметры**:

- `model (str)`: Имя модели. 
- `messages (Messages)`: Список сообщений, которые используются для генерации ответа.
- `stream (bool)`: Флаг, указывающий на то, нужно ли отправлять ответ по частям.
- `**kwargs (Any)`: Дополнительные параметры для запроса.

**Возвращает**:

- `CreateResult`: Объект, содержащий информацию о результатах запроса. 

**Как работает**:

1. Формируется сообщение в формате, понятном сервису `aiservice.vercel.app` - строка с ролью (`role`) и контентом (`content`) каждого сообщения из списка `messages`.
2. Формируются заголовки запроса, определяющие тип данных и другие параметры. 
3. Отправляется POST-запрос на URL `https://aiservice.vercel.app/api/chat/answer`, передавая сформированное сообщение и заголовки. 
4. Проверяется статус ответа. 
5. Извлекается JSON-данные ответа. 

**Примеры**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.AiService import AiService
>>> from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
>>> messages: Messages = [
...     {'role': 'user', 'content': 'What is the capital of France?'},
... ]
>>> ai_service = AiService()
>>> response = ai_service.create_completion(model='gpt-3.5-turbo', messages=messages, stream=False)
>>> print(next(response))
{'data': 'The capital of France is Paris.'}
```