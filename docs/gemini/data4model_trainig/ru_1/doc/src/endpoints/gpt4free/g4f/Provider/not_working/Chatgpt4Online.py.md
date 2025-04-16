# Модуль `Chatgpt4Online.py`

## Обзор

Модуль предоставляет асинхронный класс `Chatgpt4Online`, который является провайдером для взаимодействия с онлайн-сервисом ChatGPT4. Он позволяет отправлять запросы к API сервиса и получать ответы в режиме реального времени.

## Подробнее

Модуль использует библиотеки `aiohttp` для асинхронных HTTP-запросов и `json` для работы с данными в формате JSON. Он также включает в себя вспомогательные функции для форматирования запросов и обработки ответов.

## Классы

### `Chatgpt4Online`

**Описание**: Класс `Chatgpt4Online` является асинхронным провайдером, предназначенным для взаимодействия с сервисом ChatGPT4 Online. Он наследуется от класса `AsyncGeneratorProvider` и реализует методы для отправки запросов и получения ответов в асинхронном режиме.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL-адрес сервиса ChatGPT4 Online.
- `api_endpoint` (str): Endpoint API для отправки запросов.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4`).
- `models` (list): Список поддерживаемых моделей.

**Методы**:
- `get_nonce(headers: dict) -> str`: Асинхронный метод для получения nonce (одноразового ключа) сессии.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Асинхронный метод для создания асинхронного генератора, который отправляет запросы к API и возвращает ответы.

## Функции

### `get_nonce`

```python
    async def get_nonce(headers: dict) -> str:
        """ Асинхронно получает nonce (одноразовый ключ) сессии.
        Args:
            headers (dict): Словарь HTTP-заголовков для запроса.

        Returns:
            str: Nonce, полученный из ответа сервера.
        """
        ...
```

**Назначение**: Получение nonce (одноразового ключа) сессии для аутентификации запросов.

**Параметры**:
- `headers` (dict): Словарь HTTP-заголовков, используемых для запроса.

**Возвращает**:
- `str`: Nonce, полученный из ответа сервера.

**Как работает функция**:
1. Создается асинхронная сессия с использованием `ClientSession` и переданных заголовков.
2. Выполняется POST-запрос к endpoint `/wp-json/mwai/v1/start_session` для получения nonce.
3. Извлекается значение nonce из JSON-ответа и возвращается.

**Примеры**:

```python
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
nonce = await Chatgpt4Online.get_nonce(headers)
print(nonce)
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """ Создает асинхронный генератор для взаимодействия с API ChatGPT4 Online.

        Args:
            model (str): Модель для использования в запросе.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API.
        """
        ...
```

**Назначение**: Создание асинхронного генератора для взаимодействия с API ChatGPT4 Online.

**Параметры**:
- `model` (str): Модель для использования в запросе.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Как работает функция**:
1. Формируются HTTP-заголовки, включая полученный nonce.
2. Создается асинхронная сессия с использованием `ClientSession` и сформированных заголовков.
3. Форматируется запрос с использованием функции `format_prompt`.
4. Формируются данные запроса в формате JSON, включающие идентификатор бота, сообщение и флаг стриминга.
5. Выполняется POST-запрос к API endpoint `/wp-json/mwai-ui/v1/chats/submit`.
6. Извлекаются данные из чанков ответа, декодируются и извлекаются JSON-объекты.
7. Фильтруются данные типа `live` и `end`, и возвращаются в виде асинхронного генератора.

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, ChatGPT4 Online!"}]
async for response in Chatgpt4Online.create_async_generator(model="gpt-4", messages=messages):
    print(response)
```
```python
messages = [{"role": "user", "content": "Как дела?"}]
async for chunk in Chatgpt4Online.create_async_generator(model='gpt-4', messages=messages, proxy=None):
    print(chunk)
```
```python
messages = [{"role": "user", "content": "Расскажи о Python"}]
async for item in Chatgpt4Online.create_async_generator(model="gpt-4", messages=messages):
    print(item)
```
```python
messages = [{"role": "user", "content": "Напиши Hello World на Python"}]
async for response in Chatgpt4Online.create_async_generator(model="gpt-4", messages=messages):
    print(response)
```
```python
messages = [{"role": "user", "content": "Как создать fastapi endpoint?"}]
async for response in Chatgpt4Online.create_async_generator(model="gpt-4", messages=messages):
    print(response)
```
```python
messages = [{"role": "user", "content": "Что такое машинное обучение?"}]
async for response in Chatgpt4Online.create_async_generator(model="gpt-4", messages=messages):
    print(response)