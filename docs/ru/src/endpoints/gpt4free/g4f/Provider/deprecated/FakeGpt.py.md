# Модуль `FakeGpt`

## Обзор

Модуль `FakeGpt` предоставляет асинхронный генератор для взаимодействия с сервисом `chat-shared2.zhile.io`. Он позволяет генерировать текст на основе предоставленных сообщений, имитируя работу с GPT-3.5 Turbo. Модуль использует `aiohttp` для асинхронных запросов и поддерживает проксирование.

## Подробней

Модуль предназначен для работы с устаревшей версией API `chat-shared2.zhile.io`. Он выполняет аутентификацию, получает токен доступа и отправляет запросы на генерацию текста. Важно отметить, что данный провайдер может быть нестабильным из-за использования неофициального API.

## Классы

### `FakeGpt`

**Описание**: Класс `FakeGpt` является асинхронным провайдером генерации текста. Он наследуется от `AsyncGeneratorProvider` и реализует метод `create_async_generator` для создания асинхронного генератора, который возвращает сгенерированный текст.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL-адрес сервиса (`https://chat-shared2.zhile.io`).
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo (`True`).
- `working` (bool): Указывает, работает ли провайдер в данный момент (`False`).
- `_access_token` (str | None): Токен доступа для аутентификации (`None`).
- `_cookie_jar` (aiohttp.CookieJar | None): CookieJar для хранения cookie сессии (`None`).

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
        """Создает асинхронный генератор для получения текстовых результатов от FakeGpt.

        Args:
            model (str): Идентификатор модели, которую необходимо использовать.
            messages (Messages): Список сообщений для формирования запроса.
            proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий текстовые фрагменты.

        Raises:
            RuntimeError: Если не получен допустимый ответ от сервера.

        Внутренние функции:
            Отсутствуют.

        Как работает функция:
        1. Функция получает или обновляет токен доступа для аутентификации.
        2. Формирует запрос к API с использованием предоставленных сообщений.
        3. Отправляет асинхронный запрос к сервису `chat-shared2.zhile.io`.
        4. Получает ответ в виде потока данных и извлекает текстовые фрагменты.
        5. Возвращает асинхронный генератор, который предоставляет эти фрагменты.

        Flowchart:
        A: Начало
        ↓
        B: Проверка наличия токена доступа
        ↓
        C: Если токен отсутствует, получение списка токенов и аутентификация
        ↓
        D: Формирование заголовков запроса
        ↓
        E: Формирование данных запроса на основе сообщений
        ↓
        F: Отправка POST запроса к API
        ↓
        G: Получение ответа в виде потока данных
        ↓
        H: Извлечение и возврат текстовых фрагментов из потока
        ↓
        I: Обработка завершения потока или ошибок
        ↓
        J: Конец

        Примеры:
        >>> async for message in FakeGpt.create_async_generator(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}]):
        ...     print(message, end="")

        >>> async for message in FakeGpt.create_async_generator(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Translate to french: Hello"}], proxy="http://proxy.example.com"):
        ...     print(message, end="")
        """
```
**Назначение**: Создает асинхронный генератор для получения текстовых результатов от FakeGpt.

**Параметры**:
- `model` (str): Идентификатор модели, которую необходимо использовать.
- `messages` (Messages): Список сообщений для формирования запроса.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий текстовые фрагменты.

**Вызывает исключения**:
- `RuntimeError`: Если не получен допустимый ответ от сервера.
```python
        headers = {
            "Accept-Language": "en-US",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Referer": "https://chat-shared2.zhile.io/?v=2",
            "sec-ch-ua": \'"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"\',\
            "sec-ch-ua-platform": \'"Linux"\',\
            "sec-ch-ua-mobile": "?0",
        }
```

```python
        async with ClientSession(headers=headers, cookie_jar=cls._cookie_jar) as session:
            if not cls._access_token:
                async with session.get(f"{cls.url}/api/loads", params={"t": int(time.time())}, proxy=proxy) as response:
                    response.raise_for_status()
                    list = (await response.json())["loads"]
                    token_ids = [t["token_id"] for t in list]
                data = {
                    "token_key": random.choice(token_ids),
                    "session_password": get_random_string()
                }
                async with session.post(f"{cls.url}/auth/login", data=data, proxy=proxy) as response:
                    response.raise_for_status()
                async with session.get(f"{cls.url}/api/auth/session", proxy=proxy) as response:
                    response.raise_for_status()
                    cls._access_token = (await response.json())["accessToken"]
                    cls._cookie_jar = session.cookie_jar
```
Этот блок кода выполняет аутентификацию, если отсутствует токен доступа.

```python
            headers = {
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
                "X-Authorization": f"Bearer {cls._access_token}",
            }
            prompt = format_prompt(messages)
            data = {
                "action": "next",
                "messages": [
                    {
                        "id": str(uuid.uuid4()),
                        "author": {"role": "user"},
                        "content": {"content_type": "text", "parts": [prompt]},
                        "metadata": {},
                    }
                ],
                "parent_message_id": str(uuid.uuid4()),
                "model": "text-davinci-002-render-sha",
                "plugin_ids": [],
                "timezone_offset_min": -120,
                "suggestions": [],
                "history_and_training_disabled": True,
                "arkose_token": "",
                "force_paragen": False,
            }
            last_message = ""
```
Этот блок формирует заголовки и данные запроса для отправки сообщения.

```python
            async with session.post(f"{cls.url}/api/conversation", json=data, headers=headers, proxy=proxy) as response:
                async for line in response.content:
                    if line.startswith(b"data: "):\
                        line = line[6:]
                        if line == b"[DONE]":
                            break
                        try:
                            line = json.loads(line)
                            if line["message"]["metadata"]["message_type"] == "next":
                                new_message = line["message"]["content"]["parts"][0]
                                yield new_message[len(last_message):]
                                last_message = new_message
                        except:\
                            continue
            if not last_message:
                raise RuntimeError("No valid response")
```
Этот блок отправляет POST-запрос и обрабатывает ответ, извлекая текстовые фрагменты и возвращая их через генератор. Если не получен допустимый ответ, выбрасывается исключение `RuntimeError`.