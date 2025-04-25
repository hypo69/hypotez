# Модуль для работы с провайдером ChatGLM

## Обзор

Модуль `hypotez/src/endpoints/gpt4free/g4f/Provider/ChatGLM.py` содержит класс `ChatGLM`, реализующий асинхронный генератор для работы с провайдером ChatGLM. 

## Подробнее

Класс `ChatGLM` наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он предоставляет асинхронный генератор, который позволяет взаимодействовать с API ChatGLM для получения ответов от модели ChatGLM.  

## Классы

### `class ChatGLM`

**Описание**: Класс `ChatGLM` реализует асинхронный генератор для работы с провайдером ChatGLM.

**Наследует**:
- `AsyncGeneratorProvider`:  Базовый класс для асинхронных генераторов провайдеров.
- `ProviderModelMixin`:  Миксин для управления моделями провайдера.

**Атрибуты**:

- `url` (str):  Базовый URL для API ChatGLM.
- `api_endpoint` (str):  URL для API ChatGLM.
- `working` (bool):  Флаг, указывающий, что провайдер работает.
- `supports_stream` (bool):  Флаг, указывающий, что провайдер поддерживает потоковую передачу.
- `supports_system_message` (bool):  Флаг, указывающий, что провайдер поддерживает системные сообщения.
- `supports_message_history` (bool):  Флаг, указывающий, что провайдер поддерживает историю сообщений.
- `default_model` (str):  Название модели по умолчанию.
- `models` (list):  Список доступных моделей.

**Методы**:

- `create_async_generator()`:  Создает асинхронный генератор для работы с API ChatGLM.

**Принцип работы**:

1. **Инициализация**:  Класс `ChatGLM` инициализируется с базовым URL, URL API, флагами поддержки потоковой передачи, системных сообщений и истории сообщений, моделью по умолчанию и списком моделей.
2. **Создание асинхронного генератора**:  Метод `create_async_generator()` создает асинхронный генератор, который принимает модель, сообщения, прокси-сервер и другие параметры в качестве аргументов.
3. **Отправка запроса**:  Генератор отправляет POST-запрос на API ChatGLM с данными, включающими ID ассистента, ID разговора, метаданные, сообщения и другие параметры.
4. **Получение ответов**:  Генератор получает ответы от API ChatGLM в формате потоковой передачи.
5. **Обработка ответов**:  Генератор обрабатывает полученные ответы, извлекая текст и  информацию о завершении работы модели (FinishReason).
6. **Возврат ответа**:  Генератор возвращает текст,  описывающий статус выполнения модели.


## Методы класса

### `create_async_generator()`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        device_id = str(uuid.uuid4()).replace('-\', '')
        
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'App-Name': 'chatglm',
            'Authorization': 'undefined',
            'Content-Type': 'application/json',
            'Origin': 'https://chatglm.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'X-App-Platform': 'pc',
            'X-App-Version': '0.0.1',
            'X-Device-Id': device_id,
            'Accept': 'text/event-stream'
        }
        
        async with ClientSession(headers=headers) as session:
            data = {
                "assistant_id": "65940acff94777010aa6b796",
                "conversation_id": "",
                "meta_data": {
                    "if_plus_model": False,
                    "is_test": False,
                    "input_question_type": "xxxx",
                    "channel": "",
                    "draft_id": "",
                    "quote_log_id": "",
                    "platform": "pc"
                },
                "messages": [
                    {
                        "role": message["role"],
                        "content": [
                            {
                                "type": "text",
                                "text": message["content"]
                            }
                        ]
                    }
                    for message in messages
                ]
            }
            
            yield_text = 0
            async with session.post(cls.api_endpoint, json=data, proxy=proxy) as response:
                await raise_for_status(response)
                async for chunk in response.content:
                    if chunk:
                        decoded_chunk = chunk.decode('utf-8')
                        if decoded_chunk.startswith('data: '):
                            try:
                                json_data = json.loads(decoded_chunk[6:])
                                parts = json_data.get('parts', [])
                                if parts:
                                    content = parts[0].get('content', [])
                                    if content:
                                        text_content = content[0].get('text', '')
                                        text = text_content[yield_text:]
                                        if text:
                                            yield text
                                            yield_text += len(text)
                                # Yield FinishReason when status is 'finish'
                                if json_data.get('status') == 'finish':
                                    yield FinishReason("stop")
                            except json.JSONDecodeError:
                                pass

```

**Назначение**: 
- Создает асинхронный генератор, который отправляет запрос на API ChatGLM.
- Получает ответы в формате потоковой передачи.
- Обрабатывает ответы, извлекая текст и  информацию о завершении работы модели.
- Возвращает текст,  описывающий статус выполнения модели.

**Параметры**:
- `model` (str):  Название модели.
- `messages` (Messages):  Список сообщений для ChatGLM.
- `proxy` (str, optional):  URL прокси-сервера. По умолчанию `None`.

**Возвращает**:
- `AsyncResult`:  Асинхронный генератор, который будет выдавать ответы от ChatGLM.

**Принцип работы**:

1. **Инициализация**:  Метод инициализирует заголовки запроса, данные запроса, а также создает асинхронную сессию с помощью `ClientSession`.
2. **Отправка запроса**:  Метод отправляет POST-запрос на API ChatGLM с данными запроса.
3. **Обработка ответов**:  Метод перебирает ответы в формате потоковой передачи, извлекая текст и информацию о завершении работы модели.
4. **Выдача результатов**:  Метод выдает извлеченные ответы в виде текста.
5. **Завершение**:  Метод выдает `FinishReason("stop")`, когда модель завершила работу.


## Параметры класса

- `url` (str):  Базовый URL для API ChatGLM.
- `api_endpoint` (str):  URL для API ChatGLM.
- `working` (bool):  Флаг, указывающий, что провайдер работает.
- `supports_stream` (bool):  Флаг, указывающий, что провайдер поддерживает потоковую передачу.
- `supports_system_message` (bool):  Флаг, указывающий, что провайдер поддерживает системные сообщения.
- `supports_message_history` (bool):  Флаг, указывающий, что провайдер поддерживает историю сообщений.
- `default_model` (str):  Название модели по умолчанию.
- `models` (list):  Список доступных моделей.