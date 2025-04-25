# Модуль OpenaiAPI

## Обзор

Модуль `OpenaiAPI` предоставляет класс `OpenaiAPI`, который представляет собой реализацию API OpenAI для взаимодействия с платформой OpenAI. 

## Подробней

Класс `OpenaiAPI` наследует от базового класса `OpenaiTemplate` и определяет константы, необходимые для работы с API OpenAI. 

- `label`:  Название API (OpenAI API)
- `url`:  URL-адрес платформы OpenAI
- `login_url`: URL-адрес для входа в аккаунт
- `api_base`: Базовый URL для вызова API-методов OpenAI 
- `working`: Флаг, показывающий, доступен ли API (True - доступен)
- `needs_auth`: Флаг, показывающий, требуется ли авторизация для доступа к API (True - требуется)

## Классы

### `class OpenaiAPI`

**Описание**: Класс `OpenaiAPI` реализует API OpenAI для взаимодействия с платформой OpenAI.

**Наследует**: `OpenaiTemplate`

**Атрибуты**:

- `label` (str): Название API.
- `url` (str): URL-адрес платформы OpenAI.
- `login_url` (str): URL-адрес для входа в аккаунт.
- `api_base` (str): Базовый URL для вызова API-методов OpenAI.
- `working` (bool): Флаг, показывающий, доступен ли API.
- `needs_auth` (bool): Флаг, показывающий, требуется ли авторизация для доступа к API.


## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.OpenaiAPI import OpenaiAPI

openai_api = OpenaiAPI()