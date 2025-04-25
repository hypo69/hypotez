# Модуль H2o 

## Обзор

Этот модуль предоставляет класс `H2o`, который реализует провайдера для модели H2o AI, доступной через  [GPT-GM](https://gpt-gm.h2o.ai). 

## Подробней

Модуль реализует провайдера  `H2o` для  `g4f.Provider.Providers`  в  `hypotez`  и  `freegpt-webui-ru`  проектах. Провайдер предоставляет доступ к моделям  H2o AI  с помощью API GPT-GM.

## Классы 

### `class H2o` 

**Описание**: Класс, реализующий провайдера для моделей H2o AI.

**Наследует**: 
 -  `g4f.Provider.Providers.BaseProvider`


**Атрибуты**:
 -  `url` (str): URL-адрес API GPT-GM.
 -  `model` (list): Список доступных моделей.
 -  `supports_stream` (bool): True, если модель поддерживает потоковую передачу.
 -  `needs_auth` (bool): False, так как для  H2o AI  аутентификация не требуется.
 -  `models` (dict): Словарь, сопоставляющий имена моделей с их идентификаторами в  H2o AI.


**Методы**:

 -  `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: Создает завершение текста с использованием модели H2o AI. 


 ## Методы класса 

### `_create_completion(model: str, messages: list, stream: bool, **kwargs)`


```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает завершение текста с использованием модели H2o AI.

    Args:
        model (str): Имя модели H2o AI.
        messages (list): Список сообщений в диалоге.
        stream (bool): True, если необходимо использовать потоковую передачу.
        **kwargs: Дополнительные параметры для модели.

    Returns:
        Generator[str, None, None]: Генератор токенов завершения текста.

    Raises:
        Exception: Если возникает ошибка во время создания завершения.
    """
    conversation = 'instruction: this is a conversation beween, a user and an AI assistant, respond to the latest message, referring to the conversation if needed\\n'
    for message in messages:
        conversation += '%s: %s\\n' % (message['role'], message['content'])
    conversation += 'assistant:'
    
    client = Session()
    client.headers = {
        'authority': 'gpt-gm.h2o.ai',
        'origin': 'https://gpt-gm.h2o.ai',
        'referer': 'https://gpt-gm.h2o.ai/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    
    client.get('https://gpt-gm.h2o.ai/')
    response = client.post('https://gpt-gm.h2o.ai/settings', data={
        'ethicsModalAccepted': 'true',
        'shareConversationsWithModelAuthors': 'true',
        'ethicsModalAcceptedAt': '',
        'activeModel': 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1',
        'searchEnabled': 'true',
    })
    
    headers = {
        'authority': 'gpt-gm.h2o.ai',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'origin': 'https://gpt-gm.h2o.ai',
        'referer': 'https://gpt-gm.h2o.ai/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    
    json_data = {
        'model': models[model]
    }
    
    response = client.post('https://gpt-gm.h2o.ai/conversation',
                            headers=headers, json=json_data)
    conversationId = response.json()['conversationId']
    
    completion = client.post(f'https://gpt-gm.h2o.ai/conversation/{conversationId}', stream=True, json = {
        'inputs': conversation,
        'parameters': {
            'temperature': kwargs.get('temperature', 0.4),
            'truncate': kwargs.get('truncate', 2048),
            'max_new_tokens': kwargs.get('max_new_tokens', 1024),
            'do_sample': kwargs.get('do_sample', True),
            'repetition_penalty': kwargs.get('repetition_penalty', 1.2),
            'return_full_text': kwargs.get('return_full_text', False)
        },
        'stream': True,
        'options': {
            'id': kwargs.get('id', str(uuid4())),
            'response_id': kwargs.get('response_id', str(uuid4())),
            'is_retry': False,
            'use_cache': False,
            'web_search_id': ''
        }
    })
    
    for line in completion.iter_lines():
        if b'data' in line:
            line = loads(line.decode('utf-8').replace('data:', ''))
            token = line['token']['text']
            
            if token == '<|endoftext|>\':
                break
            else:
                yield (token)
```
**Назначение**: Метод создает завершение текста с использованием модели H2o AI. 

**Параметры**:
 -  `model` (str): Имя модели H2o AI.
 -  `messages` (list): Список сообщений в диалоге.
 -  `stream` (bool): True, если необходимо использовать потоковую передачу.
 -  `**kwargs`: Дополнительные параметры для модели.

**Возвращает**:
 -  `Generator[str, None, None]`: Генератор токенов завершения текста.

**Вызывает исключения**:
 -  `Exception`: Если возникает ошибка во время создания завершения.

**Как работает функция**: 
 -  Функция  `_create_completion`  подготавливает разговорную историю, добавляя к ней текущее сообщение.
 -  Она затем использует  `requests`  для отправки запроса к API GPT-GM, чтобы получить завершение текста.
 -  Функция  `_create_completion`  проверяет, есть ли в ответе данные, и если да, то извлекает токены завершения текста.
 -  Функция  `_create_completion`  выдает токены завершения текста в виде генератора, что позволяет обрабатывать текст по частям.
 -  Функция  `_create_completion`  поддерживает потоковую передачу (если  `stream`  равен True).

**Примеры**:
```python
# Пример использования функции
messages = [
    {'role': 'user', 'content': 'Привет! Как дела?'},
    {'role': 'assistant', 'content': 'У меня все отлично, как у тебя?'}
]
model = 'falcon-7b'
completion = _create_completion(model=model, messages=messages, stream=True)
for token in completion:
    print(token, end='')