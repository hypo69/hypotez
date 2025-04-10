# Модуль Replicate

## Обзор

Модуль `Replicate` предназначен для взаимодействия с платформой Replicate, которая предоставляет доступ к различным моделям машинного обучения. Этот модуль позволяет генерировать текст на основе предоставленных сообщений, используя API Replicate. Он поддерживает как потоковую передачу данных (async generator), так и аутентификацию через API-ключ.

## Подробней

Модуль предоставляет асинхронный генератор для получения ответов от Replicate. Он использует `StreamSession` для асинхронных HTTP-запросов и обрабатывает ответы в формате `text/event-stream`. Для работы требуется API-ключ, который передается в заголовках запроса.

## Классы

### `Replicate`

**Описание**: Класс `Replicate` является асинхронным провайдером и миксином моделей. Он отвечает за создание асинхронного генератора для взаимодействия с API Replicate.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовую структуру для асинхронных провайдеров.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL платформы Replicate.
- `login_url` (str): URL для получения API-токенов.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от Replicate.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    api_key: str = None,
    proxy: str = None,
    timeout: int = 180,
    system_prompt: str = None,
    max_tokens: int = None,
    temperature: float = None,
    top_p: float = None,
    top_k: float = None,
    stop: list = None,
    extra_data: dict = {},
    headers: dict = {
        "accept": "application/json",
    },
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от Replicate.

    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Максимальное время ожидания запроса в секундах. По умолчанию `180`.
        system_prompt (str, optional): Системное сообщение для модели. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию `None`.
        temperature (float, optional): Параметр температуры для модели. По умолчанию `None`.
        top_p (float, optional): Параметр top_p для модели. По умолчанию `None`.
        top_k (float, optional): Параметр top_k для модели. По умолчанию `None`.
        stop (list[str], optional): Список стоп-слов. По умолчанию `None`.
        extra_data (dict, optional): Дополнительные данные для отправки в запросе. По умолчанию `{}`.
        headers (dict, optional): Дополнительные заголовки для запроса. По умолчанию `{"accept": "application/json"}`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий текст от модели.

    Raises:
        MissingAuthError: Если `needs_auth` равно `True`, а `api_key` не предоставлен.
        ResponseError: Если получен невалидный ответ от API.
        Exception: Если возникает ошибка при выполнении HTTP-запроса.
    """
    model = cls.get_model(model)
    if cls.needs_auth and api_key is None:
        raise MissingAuthError("api_key is missing")
    if api_key is not None:
        headers["Authorization"] = f"Bearer {api_key}"
        api_base = "https://api.replicate.com/v1/models/"
    else:
        api_base = "https://replicate.com/api/models/"
    async with StreamSession(
        proxy=proxy,
        headers=headers,
        timeout=timeout
    ) as session:
        data = {
            "stream": True,
            "input": {
                "prompt": format_prompt(messages),
                **filter_none(
                    system_prompt=system_prompt,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    stop_sequences=",".join(stop) if stop else None
                ),
                **extra_data
            },
        }
        url = f"{api_base.rstrip('/')}/{model}/predictions"
        async with session.post(url, json=data) as response:
            message = "Model not found" if response.status == 404 else None
            await raise_for_status(response, message)
            result = await response.json()
            if "id" not in result:
                raise ResponseError(f"Invalid response: {result}")
            async with session.get(result["urls"]["stream"], headers={"Accept": "text/event-stream"}) as response:
                await raise_for_status(response)
                event = None
                async for line in response.iter_lines():
                    if line.startswith(b"event: "):
                        event = line[7:]
                        if event == b"done":
                            break
                    elif event == b"output":
                        if line.startswith(b"data: "):
                            new_text = line[6:].decode()
                            if new_text:
                                yield new_text
                            else:
                                yield "\\n"

**Как работает функция**:

1. **Подготовка**:
   - Извлекается имя модели с помощью `cls.get_model(model)`.
   - Проверяется наличие API-ключа, если требуется аутентификация. Если ключ отсутствует, вызывается исключение `MissingAuthError`.
   - Формируются заголовки запроса, включая API-ключ, если он предоставлен.
   - Определяется базовый URL API в зависимости от наличия API-ключа.

2. **Создание сессии**:
   - Создается асинхронная сессия с использованием `StreamSession` для управления HTTP-подключениями.
   - Устанавливаются параметры прокси, заголовки и таймаут.

3. **Формирование данных запроса**:
   - Формируются данные запроса в формате JSON, включая:
     - `stream`: Устанавливается в `True` для потоковой передачи данных.
     - `input`: Содержит параметры для модели, такие как:
       - `prompt`: Форматированные сообщения с использованием `format_prompt(messages)`.
       - Дополнительные параметры, такие как `system_prompt`, `max_new_tokens`, `temperature`, `top_p`, `top_k` и `stop_sequences`, отфильтрованные с помощью `filter_none`.
       - Дополнительные данные из `extra_data`.

4. **Отправка запроса**:
   - Формируется URL для отправки запроса на основе базового URL и имени модели.
   - Отправляется POST-запрос к API Replicate с использованием `session.post`.

5. **Обработка ответа**:
   - Проверяется статус ответа. Если статус равен 404, устанавливается сообщение об ошибке "Model not found".
   - Вызывается `raise_for_status` для проверки статуса ответа и вызова исключения в случае ошибки.
   - Извлекается результат из JSON-ответа.
   - Проверяется наличие поля "id" в результате. Если поле отсутствует, вызывается исключение `ResponseError`.

6. **Получение потока данных**:
   - Отправляется GET-запрос для получения потока данных из URL, указанного в поле `result["urls"]["stream"]`.
   - Устанавливается заголовок `Accept` в значение `text/event-stream`.

7. **Обработка потока событий**:
   - Итерируется по строкам в потоке событий с использованием `response.iter_lines()`.
   - Обрабатываются события:
     - Если строка начинается с `b"event: "`, извлекается имя события.
       - Если событие равно `b"done"`, цикл завершается.
       - Если событие равно `b"output"`, извлекаются данные из строки, начинающейся с `b"data: "`.
         - Декодируется текст извлеченных данных.
         - Если текст не пустой, он передается в генератор с помощью `yield new_text`.
         - Если текст пустой, в генератор передается символ новой строки `yield "\\n"`.

```
A: Подготовка данных и URL
|
B: Создание StreamSession
|
C: Отправка POST-запроса к API Replicate
|
D: Обработка ответа, проверка наличия "id"
|
E: Отправка GET-запроса для получения потока данных
|
F: Обработка потока событий, yield new_text или "\\n"
```

**Примеры**:

```python
# Пример вызова функции с минимальными параметрами
result = Replicate.create_async_generator(model="meta/meta-llama-3-70b-instruct", messages=[{"role": "user", "content": "Hello"}], api_key="YOUR_API_KEY")

# Пример вызова функции с дополнительными параметрами
result = Replicate.create_async_generator(
    model="meta/meta-llama-3-70b-instruct",
    messages=[{"role": "user", "content": "Translate to French: Hello"}],
    api_key="YOUR_API_KEY",
    temperature=0.7,
    max_tokens=100,
    stop=["\\n"]
)