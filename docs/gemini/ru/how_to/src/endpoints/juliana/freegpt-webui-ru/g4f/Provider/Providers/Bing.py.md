### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код реализует взаимодействие с Bing AI для генерации текста на основе заданного запроса. Он включает в себя создание conversation, установку соединения через WebSocket, отправку запроса и обработку потоковых ответов.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Импортируются необходимые библиотеки, такие как `os`, `json`, `random`, `uuid`, `ssl`, `certifi`, `aiohttp`, `asyncio` и `requests`.
   - Определяются глобальные переменные, такие как `url` (URL Bing Chat), `model` (используемая модель, например, 'gpt-4'), `supports_stream` (поддержка потоковой передачи), `needs_auth` (требование авторизации).
   - Создается SSL-контекст для безопасного соединения.

2. **Определение классов**:
   - Класс `optionsSets` определяет структуру опций для настройки поведения Bing AI.
   - Класс `Defaults` содержит значения по умолчанию, такие как разделитель, IP-адрес, разрешенные типы сообщений, идентификаторы срезов и параметры местоположения.

3. **Функция `_format`**:
   - Преобразует сообщение в JSON-формат и добавляет разделитель `Defaults.delimiter`.
   - Используется для форматирования сообщений, отправляемых через WebSocket.

   ```python
   def _format(msg: dict) -> str:
       return json.dumps(msg, ensure_ascii=False) + Defaults.delimiter
   ```

4. **Функция `create_conversation`**:
   - Выполняет несколько попыток создания conversation с Bing AI.
   - Отправляет GET-запрос к `https://www.bing.com/turing/conversation/create` с необходимыми заголовками.
   - Извлекает `conversationId`, `clientId` и `conversationSignature` из JSON-ответа.
   - Возвращает полученные идентификаторы для использования в дальнейших запросах.

   ```python
   async def create_conversation():
       for _ in range(5):
           create = requests.get('https://www.bing.com/turing/conversation/create',
                                 headers={
                                     'authority': 'edgeservices.bing.com',
                                     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                                     'accept-language': 'en-US,en;q=0.9',
                                     'cache-control': 'max-age=0',
                                     'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
                                     'sec-ch-ua-arch': '"x86"',
                                     'sec-ch-ua-bitness': '"64"',
                                     'sec-ch-ua-full-version': '"110.0.1587.69"',
                                     'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.192", "Not A(Brand";v="24.0.0.0", "Microsoft Edge";v="110.0.1587.69"',
                                     'sec-ch-ua-mobile': '?0',
                                     'sec-ch-ua-model': '""',
                                     'sec-ch-ua-platform': '"Windows"',
                                     'sec-ch-ua-platform-version': '"15.0.0"',
                                     'sec-fetch-dest': 'document',
                                     'sec-fetch-mode': 'navigate',
                                     'sec-fetch-site': 'none',
                                     'sec-fetch-user': '?1',
                                     'upgrade-insecure-requests': '1',
                                     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
                                     'x-edge-shopping-flag': '1',
                                     'x-forwarded-for': Defaults.ip_address
                                 })

           conversationId = create.json().get('conversationId')
           clientId = create.json().get('clientId')
           conversationSignature = create.json().get('conversationSignature')

           if not conversationId or not clientId or not conversationSignature and _ == 4:
               raise Exception('Failed to create conversation.')

           return conversationId, clientId, conversationSignature
   ```

5. **Функция `stream_generate`**:
   - Устанавливает WebSocket-соединение с сервером Bing AI.
   - Отправляет запрос с использованием параметров conversation, prompt и mode.
   - Получает потоковые ответы от сервера и извлекает текст из них.
   - Возвращает текст в виде генератора.
   - Параметр `prompt` содержит текст запроса пользователя.
   - Параметр `mode` определяет набор опций для запроса (например, `optionsSets.jailbreak`).
   - Параметр `context` позволяет передавать предыдущие сообщения для сохранения контекста.

   ```python
   async def stream_generate(prompt: str, mode: optionsSets.optionSet = optionsSets.jailbreak, context: bool or str = False):
       timeout = aiohttp.ClientTimeout(total=900)
       session = aiohttp.ClientSession(timeout=timeout)

       conversationId, clientId, conversationSignature = await create_conversation()

       wss = await session.ws_connect('wss://sydney.bing.com/sydney/ChatHub', ssl=ssl_context, autoping=False,
                                      headers={
                                          'accept': 'application/json',
                                          'accept-language': 'en-US,en;q=0.9',
                                          'content-type': 'application/json',
                                          'sec-ch-ua': '"Not_A Brand";v="99", "Microsoft Edge";v="110", "Chromium";v="110"',
                                          'sec-ch-ua-arch': '"x86"',
                                          'sec-ch-ua-bitness': '"64"',
                                          'sec-ch-ua-full-version': '"109.0.1518.78"',
                                          'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.192", "Not A(Brand";v="24.0.0.0", "Microsoft Edge";v="110.0.1587.69"',
                                          'sec-ch-ua-mobile': '?0',
                                          'sec-ch-ua-model': '',
                                          'sec-ch-ua-platform': '"Windows"',
                                          'sec-ch-ua-platform-version': '"15.0.0"',
                                          'sec-fetch-dest': 'empty',
                                          'sec-fetch-mode': 'cors',
                                          'sec-fetch-site': 'same-origin',
                                          'x-ms-client-request-id': str(uuid.uuid4()),
                                          'x-ms-useragent': 'azsdk-js-api-client-factory/1.0.0-beta.1 core-rest-pipeline/1.10.0 OS/Win32',
                                          'Referer': 'https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx',
                                          'Referrer-Policy': 'origin-when-cross-origin',
                                          'x-forwarded-for': Defaults.ip_address
                                      })

       await wss.send_str(_format({'protocol': 'json', 'version': 1}))
       await wss.receive(timeout=900)

       struct = {
           'arguments': [
               {
                   **mode,
                   'source': 'cib',
                   'allowedMessageTypes': Defaults.allowedMessageTypes,
                   'sliceIds': Defaults.sliceIds,
                   'traceId': os.urandom(16).hex(),
                   'isStartOfSession': True,
                   'message': Defaults.location | {
                       'author': 'user',
                       'inputMethod': 'Keyboard',
                       'text': prompt,
                       'messageType': 'Chat'
                   },
                   'conversationSignature': conversationSignature,
                   'participant': {
                       'id': clientId
                   },
                   'conversationId': conversationId
               }
           ],
           'invocationId': '0',
           'target': 'chat',
           'type': 4
       }

       if context:
           struct['arguments'][0]['previousMessages'] = [
               {
                   "author": "user",
                   "description": context,
                   "contextType": "WebPage",
                   "messageType": "Context",
                   "messageId": "discover-web--page-ping-mriduna-----"
               }
           ]

       await wss.send_str(_format(struct))

       final = False
       draw = False
       resp_txt = ''
       result_text = ''
       resp_txt_no_link = ''
       cache_text = ''

       while not final:
           msg = await wss.receive(timeout=900)
           objects = msg.data.split(Defaults.delimiter)

           for obj in objects:
               if obj is None or not obj:
                   continue

               response = json.loads(obj)
               if response.get('type') == 1 and response['arguments'][0].get('messages',):
                   if not draw:
                       if (response['arguments'][0]['messages'][0]['contentOrigin'] != 'Apology') and not draw:
                           resp_txt = result_text + \
                               response['arguments'][0]['messages'][0]['adaptiveCards'][0]['body'][0].get(
                                   'text', '')
                           resp_txt_no_link = result_text + \
                               response['arguments'][0]['messages'][0].get(
                                   'text', '')

                           if response['arguments'][0]['messages'][0].get('messageType',):
                               resp_txt = (
                                   resp_txt
                                   + response['arguments'][0]['messages'][0]['adaptiveCards'][0]['body'][0]['inlines'][0].get('text')
                                   + '\\n'
                               )
                               result_text = (
                                   result_text
                                   + response['arguments'][0]['messages'][0]['adaptiveCards'][0]['body'][0]['inlines'][0].get('text')
                                   + '\\n'
                               )

                   if cache_text.endswith('   '):
                       final = True
                       if wss and not wss.closed:
                           await wss.close()
                       if session and not session.closed:
                           await session.close()

                   yield (resp_txt.replace(cache_text, ''))
                   cache_text = resp_txt

               elif response.get('type') == 2:
                   if response['item']['result'].get('error'):
                       if wss and not wss.closed:
                           await wss.close()
                       if session and not session.closed:
                           await session.close()

                       raise Exception(
                           f"{response['item']['result']['value']}: {response['item']['result']['message']}")

                   if draw:
                       cache = response['item']['messages'][1]['adaptiveCards'][0]['body'][0]['text']
                       response['item']['messages'][1]['adaptiveCards'][0]['body'][0]['text'] = (
                           cache + resp_txt)

                   if (response['item']['messages'][-1]['contentOrigin'] == 'Apology' and resp_txt):
                       response['item']['messages'][-1]['text'] = resp_txt_no_link
                       response['item']['messages'][-1]['adaptiveCards'][0]['body'][0]['text'] = resp_txt

                       # print('Preserved the message from being deleted', file=sys.stderr)

                   final = True
                   if wss and not wss.closed:
                       await wss.close()
                   if session and not session.closed:
                       await session.close()
   ```

6. **Функция `run`**:
   - Преобразует асинхронный генератор в синхронный, позволяя итерироваться по нему в синхронном коде.
   - Использует `asyncio.get_event_loop()` для запуска асинхронных операций.

   ```python
   def run(generator):
       loop = asyncio.get_event_loop()
       gen = generator.__aiter__()

       while True:
           try:
               next_val = loop.run_until_complete(gen.__anext__())
               yield next_val

           except StopAsyncIteration:
               break
   ```

7. **Функция `convert`**:
   - Преобразует список сообщений в строку контекста для Bing AI.
   - Форматирует каждое сообщение как `[role](#message)\ncontent\n\n`.

   ```python
   def convert(messages):
       context = ""

       for message in messages:
           context += "[%s](#message)\\n%s\\n\\n" % (message['role'],
                                                  message['content'])

       return context
   ```

8. **Функция `_create_completion`**:
   - Определяет логику создания запроса к Bing AI на основе списка сообщений.
   - Если сообщений меньше двух, используется только последнее сообщение как prompt.
   - Если сообщений два и более, используется последнее сообщение как prompt, а предыдущие сообщения преобразуются в context.
   - Использует функцию `run` для получения потоковых ответов от `stream_generate`.
   - Возвращает генератор токенов ответа.

   ```python
   def _create_completion(model: str, messages: list, stream: bool, **kwargs):
       if len(messages) < 2:
           prompt = messages[0]['content']
           context = False

       else:
           prompt = messages[-1]['content']
           context = convert(messages[:-1])

       response = run(stream_generate(prompt, optionsSets.jailbreak, context))
       for token in response:
           yield (token)
   ```

9. **Параметры**:
   - Определяет параметры, поддерживаемые провайдером, используя `get_type_hints` для получения типов аргументов функции `_create_completion`.

   ```python
   params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
       '(%s)' % ', '.join(
           [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
   ```

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.juliana.freegpt_webui_ru.g4f.Provider.Providers import Bing

async def main():
    messages = [
        {"role": "user", "content": "Напиши стихотворение о природе"}
    ]
    
    generator = Bing._create_completion(model="gpt-4", messages=messages, stream=True)
    
    for token in generator:
        print(token, end="")

if __name__ == "__main__":
    asyncio.run(main())