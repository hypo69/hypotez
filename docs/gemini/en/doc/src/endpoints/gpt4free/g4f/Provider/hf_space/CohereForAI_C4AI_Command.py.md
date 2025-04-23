# Модуль `CohereForAI_C4AI_Command.py`

## Обзор

Модуль предоставляет реализацию асинхронного генератора для взаимодействия с моделью CohereForAI C4AI Command. Он позволяет отправлять сообщения и получать ответы от модели через API, поддерживая управление историей разговоров и обработку ошибок.

## Более детально

Этот модуль обеспечивает взаимодействие с API CohereForAI C4AI Command через асинхронные запросы. Он поддерживает различные модели, управление заголовками запросов, обработку ответов в реальном времени и управление историей разговоров. Модуль также обрабатывает ошибки, возникающие при взаимодействии с API, и предоставляет гибкие возможности для настройки параметров запросов.

## Классы

### `CohereForAI_C4AI_Command`

**Описание**: Класс для взаимодействия с моделью CohereForAI C4AI Command.
**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `label` (str): Метка провайдера ("CohereForAI C4AI Command").
- `url` (str): Базовый URL для API ("https://cohereforai-c4ai-command.hf.space").
- `conversation_url` (str): URL для управления разговорами (комбинация `url` и "/conversation").
- `working` (bool): Указывает, работает ли провайдер (всегда `True`).
- `default_model` (str): Модель, используемая по умолчанию ("command-a-03-2025").
- `model_aliases` (dict): Псевдонимы моделей для упрощения использования.
- `models` (list): Список поддерживаемых моделей.

**Принцип работы**:
Класс предоставляет методы для создания асинхронного генератора, отправки сообщений и получения ответов от модели CohereForAI C4AI Command. Он управляет заголовками запросов, обрабатывает ответы в реальном времени и поддерживает управление историей разговоров.

**Методы**:
- `get_model(model: str, **kwargs) -> str`: Возвращает полное имя модели на основе псевдонима или имени.
- `create_async_generator(model: str, messages: Messages, api_key: str = None, proxy: str = None, conversation: JsonConversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с моделью.

## Методы класса

### `get_model`

```python
@classmethod
def get_model(cls, model: str, **kwargs) -> str:
    """
    Возвращает полное имя модели на основе псевдонима или имени.

    Args:
        model (str): Имя модели или псевдоним.
        **kwargs: Дополнительные аргументы.

    Returns:
        str: Полное имя модели.
    """
    if model in cls.model_aliases.values():
        return model
    return super().get_model(model, **kwargs)
```

**Назначение**: Функция определяет полное имя модели, проверяя, является ли входное значение псевдонимом или полным именем модели.

**Параметры**:
- `model` (str): Имя модели или псевдоним.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `str`: Полное имя модели.

**Как работает функция**:
- Функция проверяет, содержится ли входное имя модели в значениях `model_aliases`. Если да, то возвращается это имя.
- Если имя модели не найдено в псевдонимах, вызывается метод `get_model` родительского класса для дальнейшей обработки.

**Примеры**:
```python
# Пример вызова с псевдонимом модели
model_name = CohereForAI_C4AI_Command.get_model("command-a")
print(model_name)

# Пример вызова с полным именем модели
model_name = CohereForAI_C4AI_Command.get_model("command-a-03-2025")
print(model_name)
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls, model: str, messages: Messages,
    api_key: str = None, 
    proxy: str = None,
    conversation: JsonConversation = None,
    return_conversation: bool = False,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с моделью.

    Args:
        model (str): Имя модели.
        messages (Messages): Список сообщений для отправки.
        api_key (str, optional): API ключ. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        conversation (JsonConversation, optional): Объект истории разговоров. По умолчанию `None`.
        return_conversation (bool, optional): Флаг возврата объекта разговора. По умолчанию `False`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор ответов от модели.
    """
    model = cls.get_model(model)
    headers = {
        "Origin": cls.url,
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://cohereforai-c4ai-command.hf.space/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4",
    }
    if api_key is not None:
        headers["Authorization"] = f"Bearer {api_key}"
    async with ClientSession(
        headers=headers,
        cookies=None if conversation is None else conversation.cookies
    ) as session:
        system_prompt = "\\n".join([message["content"] for message in messages if message["role"] == "system"])
        messages = [message for message in messages if message["role"] != "system"]
        inputs = format_prompt(messages) if conversation is None else get_last_user_message(messages)
        if conversation is None or conversation.model != model or conversation.preprompt != system_prompt:
            data = {"model": model, "preprompt": system_prompt}
            async with session.post(cls.conversation_url, json=data, proxy=proxy) as response:
                await raise_for_status(response)
                conversation = JsonConversation(
                    **await response.json(),
                    **data,
                    cookies={n: c.value for n, c in response.cookies.items()}
                )
                if return_conversation:
                    yield conversation
        async with session.get(f"{cls.conversation_url}/{conversation.conversationId}/__data.json?x-sveltekit-invalidated=11", proxy=proxy) as response:
            await raise_for_status(response)
            node = json.loads((await response.text()).splitlines()[0])["nodes"][1]
            if node["type"] == "error":
                raise RuntimeError(node["error"])
            data = node["data"]
            message_id = data[data[data[data[0]["messages"]][-1]]["id"]]
        data = FormData()
        data.add_field(
            "data",
            json.dumps({"inputs": inputs, "id": message_id, "is_retry": False, "is_continue": False, "web_search": False, "tools": []}),
            content_type="application/json"
        )
        async with session.post(f"{cls.conversation_url}/{conversation.conversationId}", data=data, proxy=proxy) as response:
            await raise_for_status(response)
            async for chunk in response.content:
                try:
                    data = json.loads(chunk)
                except (json.JSONDecodeError) as ex:
                    raise RuntimeError(f"Failed to read response: {chunk.decode(errors='replace')}", ex)
                if data["type"] == "stream":
                    yield data["token"].replace("\\u0000", "")
                elif data["type"] == "title":
                    yield TitleGeneration(data["title"])
                elif data["type"] == "finalAnswer":
                    break
```

**Назначение**: Функция создает асинхронный генератор для взаимодействия с моделью CohereForAI C4AI Command.

**Параметры**:
- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений для отправки.
- `api_key` (str, optional): API ключ. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `conversation` (JsonConversation, optional): Объект истории разговоров. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг возврата объекта разговора. По умолчанию `False`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор ответов от модели.

**Как работает функция**:
1. **Определение модели**:
   - Функция вызывает `cls.get_model(model)` для получения полного имени модели на основе предоставленного имени или псевдонима.
2. **Формирование заголовков**:
   - Создаются заголовки запроса, включающие Origin, User-Agent, Accept, Accept-Language, Referer, Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site и Priority.
   - Если предоставлен `api_key`, он добавляется в заголовок Authorization.
3. **Создание асинхронной сессии**:
   - Создается асинхронная сессия `ClientSession` с настроенными заголовками и cookie (если предоставлена история разговоров).
4. **Обработка сообщений**:
   - Извлекается системное сообщение из списка сообщений и объединяется в строку `system_prompt`.
   - Отфильтровываются системные сообщения из списка `messages`.
   - Формируется входное сообщение `inputs` с использованием `format_prompt` или `get_last_user_message` в зависимости от наличия истории разговоров.
5. **Управление историей разговоров**:
   - Если история разговоров (`conversation`) не предоставлена или модель/системное сообщение изменились:
     - Отправляется POST-запрос к `cls.conversation_url` для создания нового разговора.
     - Из ответа извлекается информация о разговоре и создается объект `JsonConversation`.
     - Если `return_conversation` установлен в `True`, объект разговора возвращается как первое значение генератора.
6. **Получение данных о сообщении**:
   - Отправляется GET-запрос для получения данных о сообщении из API.
   - Извлекается `message_id` из полученных данных.
7. **Отправка данных и получение ответа**:
   - Формируются данные формы `FormData` с входными сообщениями, `message_id` и другими параметрами.
   - Отправляется POST-запрос к API с данными формы.
   - Асинхронно обрабатываются чанки ответа:
     - Если `data["type"]` равен `"stream"`, извлекается токен и возвращается (заменяя `\\u0000`).
     - Если `data["type"]` равен `"title"`, возвращается объект `TitleGeneration` с заголовком.
     - Если `data["type"]` равен `"finalAnswer"`, цикл прерывается.
8. **Обработка ошибок**:
   - Если во время разбора JSON возникает `json.JSONDecodeError`, поднимается исключение `RuntimeError`.
   - Если узел имеет тип `"error"`, поднимается исключение `RuntimeError` с сообщением об ошибке.

**Примеры**:
```python
# Пример вызова функции с минимальными параметрами
messages = [{"role": "user", "content": "Hello, model!"}]
async_generator = CohereForAI_C4AI_Command.create_async_generator(model="command-a", messages=messages)

# Пример вызова функции с API ключом и прокси
messages = [{"role": "user", "content": "Hello, model!"}]
async_generator = CohereForAI_C4AI_Command.create_async_generator(model="command-a", messages=messages, api_key="YOUR_API_KEY", proxy="http://your_proxy:8080")
```

## Параметры класса

- `label` (str): Метка провайдера ("CohereForAI C4AI Command").
- `url` (str): Базовый URL для API ("https://cohereforai-c4ai-command.hf.space").
- `conversation_url` (str): URL для управления разговорами (комбинация `url` и "/conversation").
- `working` (bool): Указывает, работает ли провайдер (всегда `True`).
- `default_model` (str): Модель, используемая по умолчанию ("command-a-03-2025").
- `model_aliases` (dict): Псевдонимы моделей для упрощения использования.
- `models` (list): Список поддерживаемых моделей.