# Модуль ChatgptFree

## Обзор

Модуль `ChatgptFree` предоставляет асинхронный генератор для взаимодействия с моделью ChatGPT Free. Он реализует протокол REST API,  делая запросы к серверу `chatgptfree.ai` и получая ответы в формате JSON.

## Подробее

Этот модуль используется для интеграции модели ChatGPT Free в проект `hypotez`. 

## Классы

### `class ChatgptFree`

**Описание**: Класс `ChatgptFree` предоставляет асинхронный генератор для получения ответов от модели ChatGPT Free.

**Наследует**:
 - `AsyncGeneratorProvider`:  Базовый класс для асинхронных генераторов.
 - `ProviderModelMixin`:  Класс для работы с моделями.

**Атрибуты**:

- `url (str)`: URL-адрес API ChatGPT Free.
- `working (bool)`: Флаг, указывающий на работоспособность провайдера.
- `_post_id (str | None)`: ID поста, который используется для отправки запросов.
- `_nonce (str | None)`:  Токен nonce, который используется для защиты от CSRF.
- `default_model (str)`:  Название модели по умолчанию.
- `models (list[str])`: Список доступных моделей.
- `model_aliases (dict[str, str])`:  Словарь для перевода псевдонимов моделей в реальные имена.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 120, cookies: dict = None, **kwargs) -> AsyncGenerator[str, None]`:  Создает асинхронный генератор для получения ответов от модели ChatGPT Free.

**Принцип работы**:

Класс `ChatgptFree` реализует следующий принцип работы:

1. **Инициализация**:  
   - При создании объекта `ChatgptFree` инициализируются  `url`, `working`, `_post_id`, `_nonce`, `default_model`, `models` и `model_aliases`.
2. **Получение ID поста и токена nonce**:  
   - При первом обращении к `create_async_generator` выполняются  запросы к `chatgptfree.ai` для получения ID поста и токена nonce.
3. **Формирование запроса**:  
   - Формируется запрос к API с помощью `format_prompt` для обработки  входных сообщений `messages`. 
4. **Отправка запроса**:
   - Выполняется POST-запрос к `wp-admin/admin-ajax.php` на `chatgptfree.ai` с данными, включая `_post_id`, `_nonce`  и prompt.
5. **Обработка ответа**:
   - Асинхронный генератор обрабатывает ответ сервера,  ищет `data: ` в строках, декодирует JSON и  выдает результат  в виде  `content`.


### `create_async_generator`

**Назначение**: Функция создает асинхронный генератор для получения ответов от модели ChatGPT Free.

**Параметры**:

- `model (str)`:  Название модели.
- `messages (Messages)`: Список сообщений, которые будут отправлены в модель.
- `proxy (str = None)`:  Прокси-сервер.
- `timeout (int = 120)`:  Таймаут запроса.
- `cookies (dict = None)`:  Словарь с куки-файлами.
- `**kwargs`:  Дополнительные аргументы.

**Возвращает**:

- `AsyncGenerator[str, None]`:  Асинхронный генератор, который выдает ответы от модели ChatGPT Free.

**Вызывает исключения**:

- `RuntimeError`:  Возникает, если  ID поста или токен nonce  не найдены.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ChatgptFree import ChatgptFree

# Создание генератора для получения ответов от модели 'gpt-4o-mini-2024-07-18'
async def get_response(messages):
    async for response in ChatgptFree.create_async_generator(
        model='gpt-4o-mini-2024-07-18',
        messages=messages,
        timeout=120
    ):
        print(response)


# Пример использования
if __name__ == '__main__':
    messages = [
        {'role': 'user', 'content': 'Привет, как дела?'}
    ]
    asyncio.run(get_response(messages))
```

**Как работает функция**:

1. **Инициализация**:  Создается асинхронный сеанс  `StreamSession` с указанными параметрами.
2. **Получение ID поста и токена nonce**: Если  `_post_id` и `_nonce`  не заданы,  выполняются запросы к `chatgptfree.ai` для получения этих значений. 
3. **Формирование запроса**:  
    - Формируется prompt из входных  `messages` с помощью `format_prompt`. 
    - Формируется  `data` для  `POST`-запроса,  включая `_post_id`, `_nonce`, prompt и  `bot_id`. 
4. **Отправка запроса**: Выполняется  `POST`-запрос к  `wp-admin/admin-ajax.php` на  `chatgptfree.ai`.
5. **Обработка ответа**: 
    -  Чтение  `response.iter_lines()`. 
    -  Обработка строк, начинающихся с  `data: `,  декодирование JSON, выдача  `content`.
    -  Обработка  `buffer` -  последнего JSON-ответа.
6. **Возвращение результата**:  Асинхронный генератор возвращает  `content` или  `data` из ответа.


## Параметры класса

### `url`

- **Описание**:  URL-адрес API ChatGPT Free.
- **Значение**:  `https://chatgptfree.ai`


### `working`

- **Описание**:  Флаг, указывающий на работоспособность провайдера.
- **Значение**:  `False`


### `_post_id`

- **Описание**:  ID поста, который используется для отправки запросов.
- **Значение**:  `None`

### `_nonce`

- **Описание**:  Токен nonce, который используется для защиты от CSRF.
- **Значение**:  `None`

### `default_model`

- **Описание**:  Название модели по умолчанию.
- **Значение**:  `'gpt-4o-mini-2024-07-18'`

### `models`

- **Описание**:  Список доступных моделей.
- **Значение**:  `[default_model]`

### `model_aliases`

- **Описание**:  Словарь для перевода псевдонимов моделей в реальные имена.
- **Значение**:  `{ "gpt-4o-mini": "gpt-4o-mini-2024-07-18", }`

## Примеры

### Пример создания генератора и получения ответа от модели

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ChatgptFree import ChatgptFree

# Создание генератора для получения ответов от модели 'gpt-4o-mini-2024-07-18'
async def get_response(messages):
    async for response in ChatgptFree.create_async_generator(
        model='gpt-4o-mini-2024-07-18',
        messages=messages,
        timeout=120
    ):
        print(response)


# Пример использования
if __name__ == '__main__':
    messages = [
        {'role': 'user', 'content': 'Привет, как дела?'}
    ]
    asyncio.run(get_response(messages))