# Модуль `Qwen_Qwen_2_72B`

## Обзор

Модуль `Qwen_Qwen_2_72B` предоставляет асинхронный генератор для взаимодействия с моделью Qwen Qwen-2 72B, размещенной на платформе Hugging Face Space. Он позволяет отправлять запросы к модели и получать ответы в режиме реального времени через асинхронные потоки данных. Модуль поддерживает потоковую передачу данных, системные сообщения и предоставляет возможность работы через прокси.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с различными AI-моделями. Он использует асинхронные запросы для взаимодействия с API Hugging Face Space, обеспечивая эффективную и неблокирующую обработку данных. Модуль предоставляет удобный интерфейс для отправки запросов и получения ответов, а также обработки ошибок и отладки.

## Классы

### `Qwen_Qwen_2_72B`

**Описание**: Класс `Qwen_Qwen_2_72B` является асинхронным генератором, который реализует взаимодействие с моделью Qwen Qwen-2 72B через API Hugging Face Space.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Метка провайдера, отображаемая в интерфейсе. Значение: `"Qwen Qwen-2.72B"`.
- `url` (str): URL страницы модели на Hugging Face Space. Значение: `"https://qwen-qwen2-72b-instruct.hf.space"`.
- `api_endpoint` (str): URL API для отправки запросов. Значение: `"https://qwen-qwen2-72b-instruct.hf.space/queue/join?"`.
- `working` (bool): Флаг, указывающий, работает ли провайдер. Значение: `True`.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных. Значение: `True`.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения. Значение: `True`.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений. Значение: `False`.
- `default_model` (str): Модель, используемая по умолчанию. Значение: `"qwen-qwen2-72b-instruct"`.
- `model_aliases` (dict): Псевдонимы моделей. Значение: `{"qwen-2-72b": default_model}`.
- `models` (list): Список поддерживаемых моделей. Значение: `list(model_aliases.keys())`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с моделью.

## Функции

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
    """Создает асинхронный генератор для взаимодействия с моделью Qwen Qwen-2 72B.

    Args:
        cls (Qwen_Qwen_2_72B): Класс, для которого создается генератор.
        model (str): Название модели, которую необходимо использовать.
        messages (Messages): Список сообщений для отправки в модель.
        proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от модели.

    **Внутренние функции**:
    - `generate_session_hash`: Генерирует уникальный хеш сессии.

    **Как работает функция**:

    1. **Генерация хеша сессии**: Вызывается функция `generate_session_hash` для создания уникального идентификатора сессии.
    2. **Подготовка заголовков**: Формируются заголовки для HTTP-запросов, включая информацию о типе контента, User-Agent и Referer.
    3. **Подготовка промпта**: Извлекаются системные сообщения и формируется общий промпт для модели.
    4. **Подготовка полезной нагрузки**: Создается полезная нагрузка (payload) для отправки запроса, включающая промпт, системный промпт и хеш сессии.
    5. **Отправка запроса**: Используется `aiohttp.ClientSession` для отправки POST-запроса к API Hugging Face Space.
    6. **Получение и обработка данных**: Полученные данные обрабатываются построчно, извлекаются фрагменты текста из JSON-ответов и передаются через генератор.
    7. **Обработка завершения**: При получении сообщения о завершении процесса извлекается итоговый ответ, очищается от дубликатов и передается через генератор.
    8. **Обработка ошибок**: В случае ошибки декодирования JSON, информация об ошибке логируется.

    ASCII flowchart:

    ```
    A: Генерация хеша сессии
    ↓
    B: Подготовка заголовков и промпта
    ↓
    C: Подготовка полезной нагрузки
    ↓
    D: Отправка POST-запроса к API
    ↓
    E: Получение и обработка данных
    ↓
    F: Обработка завершения или ошибок
    ```

    **Примеры**:
    ```python
    # Пример использования create_async_generator
    import asyncio
    from typing import List, Dict, AsyncGenerator

    async def main():
        model = "qwen-2-72b"
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]

        generator: AsyncGenerator[str, None] = await Qwen_Qwen_2_72B.create_async_generator(model=model, messages=messages)
        async for chunk in generator:
            print(chunk, end="")

    if __name__ == "__main__":
        asyncio.run(main())
    ```
    """

    def generate_session_hash() -> str:
        """Generate a unique session hash."""
        return str(uuid.uuid4()).replace('-', '')[:12]

    # Generate a unique session hash
    session_hash: str = generate_session_hash()

    headers_join: Dict[str, str] = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': f'{cls.url}',
        'referer': f'{cls.url}/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    # Prepare the prompt
    system_prompt: str = "\n".join([message["content"] for message in messages if message["role"] == "system"])
    messages: List[Dict[str, str]] = [message for message in messages if message["role"] != "system"]
    prompt: str = format_prompt(messages)

    payload_join: Dict[str, object] = {
        "data": [prompt, [], system_prompt],
        "event_data": None,
        "fn_index": 0,
        "trigger_id": 11,
        "session_hash": session_hash
    }

    async with aiohttp.ClientSession() as session:
        # Send join request
        async with session.post(cls.api_endpoint, headers=headers_join, json=payload_join) as response:
            event_id: str = (await response.json())['event_id']

        # Prepare data stream request
        url_data: str = f'{cls.url}/queue/data'

        headers_data: Dict[str, str] = {
            'accept': 'text/event-stream',
            'accept-language': 'en-US,en;q=0.9',
            'referer': f'{cls.url}/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

        params_data: Dict[str, str] = {
            'session_hash': session_hash
        }

        # Send data stream request
        async with session.get(url_data, headers=headers_data, params=params_data) as response:
            full_response: str = ""
            final_full_response: str = ""
            async for line in response.content:
                decoded_line: str = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    try:
                        json_data: Dict[str, object] = json.loads(decoded_line[6:])

                        # Look for generation stages
                        if json_data.get('msg') == 'process_generating':
                            if 'output' in json_data and 'data' in json_data['output']:
                                output_data: List[object] = json_data['output']['data']
                                if len(output_data) > 1 and len(output_data[1]) > 0:
                                    for item in output_data[1]:
                                        if isinstance(item, list) and len(item) > 1:
                                            fragment: str = str(item[1])
                                            # Ignore [0, 1] type fragments and duplicates
                                            if not re.match(r'^\\[.*\\]$', fragment) and not full_response.endswith(fragment):
                                                full_response += fragment
                                                yield fragment

                        # Check for completion
                        if json_data.get('msg') == 'process_completed':
                            # Final check to ensure we get the complete response
                            if 'output' in json_data and 'data' in json_data['output']:
                                output_data: List[object] = json_data['output']['data']
                                if len(output_data) > 1 and len(output_data[1]) > 0:
                                    final_full_response: str = output_data[1][0][1]
                                    
                                    # Clean up the final response
                                    if final_full_response.startswith(full_response):
                                        final_full_response = final_full_response[len(full_response):]
                                    
                                    # Yield the remaining part of the final response
                                    if final_full_response:
                                        yield final_full_response
                                break

                    except json.JSONDecodeError:
                        debug.log("Could not parse JSON:", decoded_line)
```

### `generate_session_hash`

```python
def generate_session_hash() -> str:
    """Генерирует уникальный хеш сессии.

    Returns:
        str: Уникальный хеш сессии.

    **Как работает функция**:
    1. **Генерация UUID**: Создается UUID (Universally Unique Identifier) с помощью функции `uuid.uuid4()`.
    2. **Преобразование в строку**: UUID преобразуется в строку.
    3. **Удаление дефисов**: Из строки удаляются все дефисы.
    4. **Извлечение первых 12 символов**: Из полученной строки извлекаются первые 12 символов.

    ASCII flowchart:

    ```
    A: Генерация UUID
    ↓
    B: Преобразование в строку
    ↓
    C: Удаление дефисов
    ↓
    D: Извлечение первых 12 символов
    ```

    **Примеры**:
    ```python
    # Пример использования generate_session_hash
    session_hash = generate_session_hash()
    print(f"Session hash: {session_hash}")
    ```
    """
    return str(uuid.uuid4()).replace('-', '')[:12]