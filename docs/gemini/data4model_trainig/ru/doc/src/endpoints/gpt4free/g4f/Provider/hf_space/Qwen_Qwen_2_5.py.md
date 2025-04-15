# Модуль Qwen_Qwen_2_5

## Обзор

Модуль `Qwen_Qwen_2_5` предоставляет асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5 через API Hugging Face Space. Он поддерживает потоковую передачу данных и системные сообщения.

## Подробней

Этот модуль позволяет использовать модель Qwen Qwen-2.5 для генерации текста. Он отправляет запросы к API Hugging Face Space и обрабатывает потоковые ответы для предоставления сгенерированного текста. Модуль поддерживает как системные сообщения, так и обычные сообщения пользователя, а также предоставляет возможность использования прокси-сервера.

## Классы

### `Qwen_Qwen_2_5`

**Описание**: Класс `Qwen_Qwen_2_5` предоставляет методы для взаимодействия с моделью Qwen Qwen-2.5 через API Hugging Face Space.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера (Qwen Qwen-2.5).
- `url` (str): URL Hugging Face Space.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель по умолчанию (qwen-qwen2-5).
- `model_aliases` (dict): Псевдонимы моделей.
- `models` (list): Список поддерживаемых моделей.

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
    """Создает асинхронный генератор для получения ответов от модели Qwen Qwen-2.5.

    Args:
        model (str): Имя модели.
        messages (Messages): Список сообщений для отправки модели.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

    Raises:
        aiohttp.ClientError: Если возникает ошибка при отправке запроса или получении ответа.
        json.JSONDecodeError: Если не удается декодировать JSON из ответа.
        Exception: Если возникает любая другая ошибка.

    Как работает функция:
    - Генерирует уникальный session_hash для идентификации сессии.
    - Формирует заголовки для HTTP-запросов.
    - Подготавливает prompt, объединяя системные сообщения и сообщения пользователя.
    - Отправляет POST-запрос к API для присоединения к очереди.
    - Отправляет GET-запрос к API для получения потока данных.
    - Обрабатывает каждый фрагмент данных, извлекая и возвращая текст по частям.
    - Проверяет завершение процесса генерации и возвращает финальный результат.
    - Обрабатывает ошибки декодирования JSON и логирует их.

    Внутренние функции:
        generate_session_hash: Генерирует уникальный идентификатор сессии.

    """
    def generate_session_hash():
        """Генерирует уникальный session_hash.

        Returns:
            str: Уникальный идентификатор сессии.
        """
        return str(uuid.uuid4()).replace('-', '')[:10]

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

## Параметры класса

- `model` (str): Имя модели для использования.
- `messages` (Messages): Список сообщений, отправляемых модели. Сообщения должны быть в формате, ожидаемом API.
- `proxy` (str, optional): URL прокси-сервера для использования при отправке запросов. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в API.

## Примеры

Пример использования:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_5 import Qwen_Qwen_2_5

async def main():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]

    async for response in Qwen_Qwen_2_5.create_async_generator(model="qwen-2.5", messages=messages):
        print(response, end="")

if __name__ == "__main__":
    asyncio.run(main())
```
Этот код создаст асинхронный генератор, который отправит запрос к модели Qwen Qwen-2.5 и напечатает ответ по частям.