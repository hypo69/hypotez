# Документация модуля `RubiksAI.py`

## Обзор

Модуль `RubiksAI.py` предоставляет класс `RubiksAI`, который является асинхронным генератором для взаимодействия с API Rubiks AI. Он поддерживает потоковую передачу ответов, системные сообщения и историю сообщений. Модуль предназначен для использования в проектах, требующих взаимодействия с большими языковыми моделями через API Rubiks AI.

## Подробнее

Модуль содержит класс `RubiksAI`, который наследует `AsyncGeneratorProvider` и `ProviderModelMixin`. Он определяет методы для создания запросов к API Rubiks AI, обработки ответов и генерации уникальных идентификаторов. Класс поддерживает различные модели, предоставляемые Rubiks AI, и позволяет включать веб-поиск в запросы.

## Классы

### `RubiksAI`

**Описание**: Класс для взаимодействия с API Rubiks AI. Поддерживает асинхронную генерацию ответов, потоковую передачу, системные сообщения и историю сообщений.
**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:

-   `label` (str): Метка провайдера ("Rubiks AI").
-   `url` (str): URL главной страницы Rubiks AI ("https://rubiks.ai").
-   `api_endpoint` (str): URL API Rubiks AI ("https://rubiks.ai/search/api/").
-   `working` (bool): Указывает, работает ли провайдер (True).
-   `supports_stream` (bool): Поддержка потоковой передачи (True).
-   `supports_system_message` (bool): Поддержка системных сообщений (True).
-   `supports_message_history` (bool): Поддержка истории сообщений (True).
-   `default_model` (str): Модель, используемая по умолчанию ('gpt-4o-mini').
-   `models` (List[str]): Список поддерживаемых моделей.
-   `model_aliases` (Dict[str, str]): Псевдонимы моделей.

**Методы**:

-   `generate_mid()`: Генерирует уникальный идентификатор сообщения.
-   `create_referer(q: str, mid: str, model: str = '')`: Создает URL Referer с параметрами запроса.
-   `create_async_generator(model: str, messages: Messages, proxy: str = None, web_search: bool = False, temperature: float = 0.6, \*\*kwargs)`: Создает асинхронный генератор для отправки запросов к API Rubiks AI.

## Методы класса

### `generate_mid`

```python
    @staticmethod
    def generate_mid() -> str:
        """
        Generates a 'mid' string following the pattern:
        6 characters - 4 characters - 4 characters - 4 characters - 12 characters
        Example: 0r7v7b-quw4-kdy3-rvdu-ekief6xbuuq4
        """
        ...
```

**Назначение**: Генерирует уникальный идентификатор сообщения (mid) в формате `xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`, где `x` - случайный символ из букв и цифр.

**Возвращает**:

-   `str`: Уникальный идентификатор сообщения.

**Как работает функция**:

-   Функция создает пять частей идентификатора, каждая из которых состоит из случайных символов (букв и цифр).
-   Эти части соединяются дефисами для формирования окончательного идентификатора.

**Примеры**:

```python
RubiksAI.generate_mid()
# Пример возвращаемого значения: 'a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5'
```

### `create_referer`

```python
    @staticmethod
    def create_referer(q: str, mid: str, model: str = '') -> str:
        """
        Creates a Referer URL with dynamic q and mid values, using urlencode for safe parameter encoding.
        """
    ...
```

**Назначение**: Создает URL Referer с динамическими значениями параметров запроса (`q`, `mid`, `model`).

**Параметры**:

-   `q` (str): Текст запроса.
-   `mid` (str): Уникальный идентификатор сообщения.
-   `model` (str, optional): Модель, используемая для запроса. По умолчанию пустая строка.

**Возвращает**:

-   `str`: Сформированный URL Referer.

**Как работает функция**:

-   Функция принимает текст запроса, идентификатор сообщения и модель.
-   Формирует словарь с параметрами запроса.
-   Использует `urllib.parse.urlencode` для безопасного кодирования параметров в URL.
-   Возвращает URL Referer, включающий закодированные параметры.

**Примеры**:

```python
RubiksAI.create_referer(q='Как создать сайт?', mid='a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5', model='gpt-4o')
# Пример возвращаемого значения: 'https://rubiks.ai/search/?q=%D0%9A%D0%B0%D0%BA+%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C+%D1%81%D0%B0%D0%B9%D1%82%3F&model=gpt-4o&mid=a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5'
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        web_search: bool = False,
        temperature: float = 0.6,
        **kwargs
    ) -> AsyncResult:
        """
        Creates an asynchronous generator that sends requests to the Rubiks AI API and yields the response.

        Parameters:
        - model (str): The model to use in the request.
        - messages (Messages): The messages to send as a prompt.
        - proxy (str, optional): Proxy URL, if needed.
        - web_search (bool, optional): Indicates whether to include search sources in the response. Defaults to False.
        """
        ...
```

**Назначение**: Создает асинхронный генератор, который отправляет запросы к API Rubiks AI и возвращает ответы.

**Параметры**:

-   `model` (str): Модель для использования в запросе.
-   `messages` (Messages): Список сообщений для отправки в качестве запроса.
-   `proxy` (str, optional): URL прокси-сервера (если требуется). По умолчанию `None`.
-   `web_search` (bool, optional): Указывает, следует ли включать источники веб-поиска в ответ. По умолчанию `False`.
-   `temperature` (float, optional): Температура модели. По умолчанию 0.6.
-   `**kwargs`: Дополнительные параметры.

**Возвращает**:

-   `AsyncResult`: Асинхронный генератор, возвращающий текст ответа и источники веб-поиска (если включено).

**Как работает функция**:

1.  Извлекает модель, используя `cls.get_model(model)`.
2.  Генерирует уникальный идентификатор сообщения, используя `cls.generate_mid()`.
3.  Создает URL Referer, используя `cls.create_referer()`.
4.  Формирует словарь `data` с параметрами запроса, включая сообщения, модель, флаг веб-поиска и температуру.
5.  Устанавливает заголовки запроса, включая Referer и User-Agent.
6.  Использует `aiohttp.ClientSession` для отправки POST-запроса к API Rubiks AI.
7.  Обрабатывает ответ построчно, декодирует данные и извлекает контент.
8.  Если включен веб-поиск, извлекает источники и возвращает их в виде `Sources`.

**Внутренние функции**:

Внутри функции `create_async_generator` происходит обработка ответа от API Rubiks AI в асинхронном режиме. Рассмотрим подробнее этот процесс:

-   async for line in response.content::  Асинхронно перебирает строки в содержимом ответа.

    -   decoded_line = line.decode('utf-8').strip(): Декодирует каждую строку из байтов в UTF-8 и удаляет пробельные символы в начале и конце строки.

    -   if not decoded_line.startswith('data: '): continue: Проверяет, начинается ли строка с префикса "data: ". Если нет, переходит к следующей строке.

    -   data = decoded_line[6:]: Извлекает данные, начиная с 7-го символа (после "data: ").

    -   if data in ('[DONE]', '{"done": ""}'): break: Проверяет, являются ли данные строками "[DONE]" или '{"done": ""}'. Если да, прерывает цикл.

    -   try::  Начинает блок обработки исключений.

        -   json_data = json.loads(data): Пытается преобразовать данные из формата JSON в объект Python (словарь).

        -   except json.JSONDecodeError::  Перехватывает исключение, если происходит ошибка при декодировании JSON.

            -   continue: Переходит к следующей строке, если произошла ошибка при декодировании JSON.

        -   if 'url' in json_data and 'title' in json_data:: Проверяет, содержатся ли ключи 'url' и 'title' в декодированном JSON-объекте.

            -   if web_search:: Проверяет, включен ли веб-поиск.

                -   sources.append(json_data): Добавляет JSON-объект в список sources.

        -   elif 'choices' in json_data:: Проверяет, содержится ли ключ 'choices' в декодированном JSON-объекте.

            -   for choice in json_data['choices']::  Перебирает элементы в списке 'choices'.

                -   delta = choice.get('delta', {}): Извлекает значение ключа 'delta' из текущего элемента choice, возвращая пустой словарь, если ключ отсутствует.

                -   content = delta.get('content', ''): Извлекает значение ключа 'content' из словаря delta, возвращая пустую строку, если ключ отсутствует.

                -   if content:: Проверяет, является ли значение content непустой строкой.

                    -   yield content: Возвращает значение content как часть асинхронной генерации.

-   if web_search and sources:: Проверяет, включен ли веб-поиск и содержит ли список sources какие-либо элементы.

    -   yield Sources(sources): Возвращает список sources, обернутый в объект Sources.

## Параметры класса

-   `label` (str): Метка провайдера.
-   `url` (str): URL главной страницы Rubiks AI.
-   `api_endpoint` (str): URL API Rubiks AI.
-   `working` (bool): Указывает, работает ли провайдер.
-   `supports_stream` (bool): Поддержка потоковой передачи.
-   `supports_system_message` (bool): Поддержка системных сообщений.
-   `supports_message_history` (bool): Поддержка истории сообщений.
-   `default_model` (str): Модель, используемая по умолчанию.
-   `models` (List[str]): Список поддерживаемых моделей.
-   `model_aliases` (Dict[str, str]): Псевдонимы моделей.

## Примеры

```python
# Пример использования create_async_generator
import asyncio
from src.endpoints.gpt4free.g4f.Provider.not_working.RubiksAI import RubiksAI

async def main():
    model = "gpt-4o-mini"
    messages = [{"role": "user", "content": "Как создать веб-сайт?"}]
    
    async for message in RubiksAI.create_async_generator(model=model, messages=messages, web_search=True):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())