# Модуль `Qwen_Qwen_2_5`

## Обзор

Модуль `Qwen_Qwen_2_5` предоставляет асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5. Он поддерживает потоковую передачу ответов, системные сообщения и предоставляет API для подключения к сервису через HTTP.

## Детали

Этот модуль предназначен для работы с моделью Qwen Qwen-2.5 через API, предоставляемое сервисом. Он включает в себя функции для формирования запросов, обработки ответов и обеспечения асинхронной генерации результатов. Модуль также обрабатывает различные этапы генерации, проверяет завершение процесса и извлекает фрагменты текста из ответов.

## Классы

### `Qwen_Qwen_2_5`

**Описание**: Класс `Qwen_Qwen_2_5` предоставляет функциональность для взаимодействия с моделью Qwen Qwen-2.5.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, `"Qwen Qwen-2.5"`.
- `url` (str): URL сервиса, `"https://qwen-qwen2-5.hf.space"`.
- `api_endpoint` (str): URL API для присоединения к очереди, `"https://qwen-qwen2-5.hf.space/queue/join"`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу, `True`.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения, `True`.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений, `False`.
- `default_model` (str): Модель по умолчанию, `"qwen-qwen2-5"`.
- `model_aliases` (dict): Псевдонимы моделей, `{"qwen-2.5": default_model}`.
- `models` (list): Список моделей, извлеченный из `model_aliases`.

**Принцип работы**:
Класс использует `aiohttp` для выполнения асинхронных HTTP-запросов к API Qwen Qwen-2.5. Он генерирует уникальный идентификатор сессии, формирует заголовки и полезные нагрузки для запросов, отправляет запросы на присоединение и получение данных, а также обрабатывает потоковые ответы для извлечения и генерации фрагментов текста.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от модели.

## Методы класса

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
    """Создает асинхронный генератор для получения ответов от модели.

    Args:
        cls (Qwen_Qwen_2_5): Ссылка на класс.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки в модель.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, предоставляющий ответы от модели.
    """
    def generate_session_hash() -> str:
        """Генерирует уникальный хеш сессии.

        Returns:
            str: Уникальный хеш сессии.
        """
        ...

    session_hash = generate_session_hash()

    headers_join = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': f'{cls.url}/?__theme=system',
        'content-type': 'application/json',
        'Origin': cls.url,
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    system_prompt = "\n".join([message["content"] for message in messages if message["role"] == "system"])
    if not system_prompt:
        system_prompt = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
    messages = [message for message in messages if message["role"] != "system"]
    prompt = format_prompt(messages)

    payload_join = {
        "data": [prompt, [], system_prompt, "72B"],
        "event_data": None,
        "fn_index": 3,
        "trigger_id": 25,
        "session_hash": session_hash
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(cls.api_endpoint, headers=headers_join, json=payload_join) as response:
            event_id = (await response.json())['event_id']

        url_data = f'{cls.url}/queue/data'

        headers_data = {
            'Accept': 'text/event-stream',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': f'{cls.url}/?__theme=system',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
        }

        params_data = {
            'session_hash': session_hash
        }

        async with session.get(url_data, headers=headers_data, params=params_data) as response:
            full_response = ""
            async for line in response.content:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    try:
                        json_data = json.loads(decoded_line[6:])

                        if json_data.get('msg') == 'process_generating':
                            if 'output' in json_data and 'data' in json_data['output']:
                                output_data = json_data['output']['data']
                                if len(output_data) > 1 and len(output_data[1]) > 0:
                                    for item in output_data[1]:
                                        if isinstance(item, list) and len(item) > 1:
                                            fragment = item[1]
                                            if isinstance(fragment, dict) and 'text' in fragment:
                                                fragment = fragment['text']
                                            else:
                                                fragment = str(fragment)

                                            if not re.match(r'^\\[.*\\]$', fragment) and not full_response.endswith(fragment):
                                                full_response += fragment
                                                yield fragment

                        if json_data.get('msg') == 'process_completed':
                            if 'output' in json_data and 'data' in json_data['output']:
                                output_data = json_data['output']['data']
                                if len(output_data) > 1 and len(output_data[1]) > 0:
                                    response_item = output_data[1][0][1]
                                    if isinstance(response_item, dict) and 'text' in response_item:
                                        final_full_response = response_item['text']
                                    else:
                                        final_full_response = str(response_item)

                                    if isinstance(final_full_response, str) and final_full_response.startswith(full_response):
                                        final_text = final_full_response[len(full_response):]
                                    else:
                                        final_text = final_full_response

                                    if final_text and final_text != full_response:
                                        yield final_text
                                break

                    except json.JSONDecodeError as ex:
                        debug.log("Could not parse JSON:", decoded_line)

**Параметры**:
- `cls` (Qwen_Qwen_2_5): Ссылка на класс.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки в модель.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, предоставляющий ответы от модели.

**Как работает функция**:
1. **Генерация уникального хеша сессии**:
   - Вызывается внутренняя функция `generate_session_hash()`, которая генерирует уникальный хеш сессии, необходимый для идентификации сессии с сервером.
   - Хеш сессии генерируется как UUID и обрезается до первых 10 символов.

2. **Формирование заголовков запроса**:
   - Определяются заголовки `headers_join` для запроса на присоединение к очереди.
   - Эти заголовки включают User-Agent, Accept, Referer и другие метаданные, необходимые для правильной обработки запроса сервером.

3. **Формирование системного запроса**:
   - Формируется системный запрос `system_prompt` путем объединения содержимого всех сообщений с ролью `"system"`.
   - Если системный запрос отсутствует, используется запрос по умолчанию: `"You are Qwen, created by Alibaba Cloud. You are a helpful assistant."`.
   - Оставляются только те сообщения, у которых роль не `"system"`.
   - Формируется основной запрос `prompt` с помощью функции `format_prompt(messages)`.

4. **Формирование полезной нагрузки (payload)**:
   - Формируется полезная нагрузка `payload_join` для запроса на присоединение, содержащая основной запрос, пустой список, системный запрос, `"72B"`, и хеш сессии.

5. **Отправка запроса на присоединение и получение идентификатора события**:
   - Открывается асинхронная сессия с помощью `aiohttp.ClientSession()`.
   - Отправляется `POST` запрос на `cls.api_endpoint` с заголовками `headers_join` и полезной нагрузкой `payload_join`.
   - Полученный ответ преобразуется в JSON, и извлекается идентификатор события `event_id`.

6. **Подготовка к запросу потока данных**:
   - Формируется URL `url_data` для запроса потока данных.
   - Определяются заголовки `headers_data` для запроса потока данных, включая Accept и User-Agent.
   - Определяются параметры `params_data` для запроса потока данных, включающие хеш сессии.

7. **Отправка запроса потока данных и обработка ответов**:
   - Отправляется `GET` запрос на `url_data` с заголовками `headers_data` и параметрами `params_data`.
   - Начинается асинхронный перебор строк в потоке ответа.
   - Каждая строка декодируется из `utf-8`.
   - Если строка начинается с `'data: '`, она обрабатывается как JSON.

8. **Обработка JSON данных**:
   - Извлекаются JSON данные из строки.
   - Проверяется, содержит ли JSON сообщение `'msg': 'process_generating'`, что указывает на этап генерации.
     - Если сообщение указывает на этап генерации, извлекаются данные из `json_data['output']['data']`.
     - Извлекаются и генерируются фрагменты текста, которые не соответствуют регулярному выражению `r'^\\[.*\\]$'` и не заканчиваются уже сгенерированным текстом.

9. **Проверка завершения процесса**:
   - Проверяется, содержит ли JSON сообщение `'msg': 'process_completed'`, что указывает на завершение процесса.
     - Если сообщение указывает на завершение, извлекаются данные из `json_data['output']['data']`.
     - Извлекается и генерируется оставшаяся часть текста.

10. **Обработка ошибок JSON**:
    - Если происходит ошибка `json.JSONDecodeError`, она регистрируется с помощью `debug.log`.

**Примеры**:

Пример вызова функции:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a joke."}
]
model = "qwen-2.5"

async def main():
    async for fragment in Qwen_Qwen_2_5.create_async_generator(model=model, messages=messages):
        print(fragment, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())