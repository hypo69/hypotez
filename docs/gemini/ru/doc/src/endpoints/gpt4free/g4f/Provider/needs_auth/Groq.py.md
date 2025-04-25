# Модуль Groq

## Обзор

Модуль `Groq` предоставляет класс `Groq`, который представляет собой реализацию провайдера для доступа к модели `Groq` через API `OpenAI`. 

## Подробно

Класс `Groq` наследует от `OpenaiTemplate` и определяет конфигурацию для взаимодействия с API `Groq`. Он устанавливает URL-адреса для доступа к веб-интерфейсу, API и авторизации, а также определяет ряд атрибутов, необходимых для работы с API:

* `working`: Указывает, работает ли провайдер.
* `needs_auth`: Указывает, требуется ли авторизация для доступа к API.
* `default_model`: Имя модели по умолчанию, используемой для запросов.
* `fallback_models`: Список резервных моделей, которые могут быть использованы в случае недоступности основной модели.
* `model_aliases`: Словарь, связывающий псевдонимы моделей с их фактическими именами.

## Классы

### `class Groq`

**Описание**: Класс `Groq` представляет собой реализацию провайдера для доступа к модели `Groq` через API `OpenAI`.

**Наследует**: `OpenaiTemplate`

**Атрибуты**:

* `url`: URL-адрес веб-интерфейса.
* `login_url`: URL-адрес для авторизации.
* `api_base`: Базовый URL-адрес API.
* `working`: Указывает, работает ли провайдер.
* `needs_auth`: Указывает, требуется ли авторизация для доступа к API.
* `default_model`: Имя модели по умолчанию.
* `fallback_models`: Список резервных моделей.
* `model_aliases`: Словарь псевдонимов моделей.

**Методы**:

* `get_response(self, query: str, model: str = None, temperature: float = 0.5, max_tokens: int = 1024, **kwargs) -> dict`: Отправляет запрос к API `Groq` и возвращает ответ в виде словаря.
* `get_response_stream(self, query: str, model: str = None, temperature: float = 0.5, max_tokens: int = 1024, **kwargs) -> Generator[str, None, None]`: Отправляет запрос к API `Groq` с использованием потоковой передачи и возвращает генератор, который выдает части ответа по мере их доступности.
* `get_stream_response(self, query: str, model: str = None, temperature: float = 0.5, max_tokens: int = 1024, **kwargs) -> Generator[str, None, None]`: Отправляет запрос к API `Groq` с использованием потоковой передачи и возвращает генератор, который выдает части ответа по мере их доступности.
* `get_model_name(self, model: str = None) -> str`: Возвращает имя модели, которую следует использовать для запроса.
* `_get_auth_token(self) -> str`: Возвращает токен аутентификации, необходимый для доступа к API.


**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Groq import Groq

groq = Groq()

# Отправка запроса к модели
response = groq.get_response("Какой сегодня день?")

# Вывод ответа
print(response.get("choices", [{}])[0].get("message", {}).get("content"))
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Groq import Groq

groq = Groq()

# Отправка запроса к модели с использованием потоковой передачи
for chunk in groq.get_response_stream("Какой сегодня день?"):
    print(chunk, end="")
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Groq import Groq

groq = Groq()

# Получение имени модели
model_name = groq.get_model_name()
print(model_name)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Groq import Groq

groq = Groq()

# Получение токена аутентификации
auth_token = groq._get_auth_token()
print(auth_token)
```

## Внутренние функции

**`_get_auth_token(self) -> str`**: Возвращает токен аутентификации, необходимый для доступа к API.

**Описание**: Функция `_get_auth_token` реализует получение токена аутентификации для доступа к API `Groq`.

**Как работает функция**: Функция использует API `Groq` для получения токена аутентификации. Она отправляет запрос к URL-адресу `login_url` и обрабатывает ответ, извлекая токен аутентификации из него.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Groq import Groq

groq = Groq()

# Получение токена аутентификации
auth_token = groq._get_auth_token()
print(auth_token)
```
```markdown