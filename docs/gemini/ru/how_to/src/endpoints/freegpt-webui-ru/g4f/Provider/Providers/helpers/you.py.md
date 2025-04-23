### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предназначен для взаимодействия с API `you.com` с целью получения ответов на запросы, используя историю сообщений чата. Он преобразует входные сообщения в формат, ожидаемый API, отправляет запрос и обрабатывает потоковые ответы, извлекая и выводя токены чата.

Шаги выполнения
-------------------------
1. **Загрузка конфигурации**:
   - Код начинает с загрузки конфигурации из аргументов командной строки, используя `json.loads(sys.argv[1])`. Функция преобразует строку JSON в объект Python (словарь).
2. **Извлечение сообщений**:
   - Извлекает сообщения из конфигурации: `messages = config['messages']`. Переменная `messages` содержит список сообщений, которыми обменивались пользователь и ассистент.
3. **Подготовка запроса**:
   - Если последнее сообщение от пользователя, оно сохраняется в `prompt`, и удаляется из `messages`. Функция проверяет, что последний элемент в `messages` имеет роль `user`, и сохраняет его содержимое в переменной `prompt`. Этот `prompt` используется как текущий вопрос пользователя.
4. **Трансформация сообщений**:
   - Вызывается функция `transform(messages)` для преобразования формата сообщений в формат, требуемый API `you.com`.
5. **Кодирование параметров запроса**:
   - Параметры запроса кодируются с использованием `urllib.parse.urlencode`. Функция кодирует параметры, включая текущий `prompt` и преобразованные сообщения чата, в формат URL.
6. **Отправка запроса и обработка ответа**:
   - Отправляется GET-запрос к API `you.com` с использованием `requests.get`.
   - Ответ обрабатывается потоково с помощью функции `output`, которая извлекает и печатает токен чата. Функция отправляет запрос к API, используя параметры и заголовки, и передает функцию `output` для обработки поступающих чанков данных.
7. **Обработка ошибок**:
   - В случае ошибки, происходит повторная попытка отправки запроса.

Пример использования
-------------------------

```python
import sys
import json
import urllib.parse

from curl_cffi import requests

def transform(messages: list) -> list:
    result = []
    i = 0

    while i < len(messages):
        if messages[i]['role'] == 'user':
            question = messages[i]['content']
            i += 1

            if i < len(messages) and messages[i]['role'] == 'assistant':
                answer = messages[i]['content']
                i += 1
            else:
                answer = ''

            result.append({'question': question, 'answer': answer})

        elif messages[i]['role'] == 'assistant':
            result.append({'question': '', 'answer': messages[i]['content']})
            i += 1

        elif messages[i]['role'] == 'system':
            result.append({'question': messages[i]['content'], 'answer': ''})
            i += 1
            
    return result

def output(chunk):
    if b'"youChatToken"' in chunk:
        chunk_json = json.loads(chunk.decode().split('data: ')[1])

        print(chunk_json['youChatToken'], flush=True, end = '')

# Пример конфигурации (имитация sys.argv[1])
config_data = {
    "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help you?"},
        {"role": "user", "content": "What is the capital of France?"}
    ]
}

# Преобразование конфигурации в строку JSON
config_json = json.dumps(config_data)

# Имитация аргумента командной строки
sys.argv = ["script_name.py", config_json]

# Загрузка конфигурации из аргументов командной строки
config = json.loads(sys.argv[1])
messages = config['messages']
prompt = ''

# Подготовка запроса
if messages[-1]['role'] == 'user':
    prompt = messages[-1]['content']
    messages = messages[:-1]

# Кодирование параметров запроса
params = urllib.parse.urlencode({
    'q': prompt,
    'domain': 'youchat',
    'chat': transform(messages)
})

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Sec-Fetch-Mode': 'navigate',
    'Host': 'you.com',
    'Origin': 'https://you.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
    'Referer': 'https://you.com/api/streamingSearch?q=nice&safeSearch=Moderate&onShoppingPage=false&mkt=&responseFilter=WebPages,Translations,TimeZone,Computation,RelatedSearches&domain=youchat&queryTraceId=7a6671f8-5881-404d-8ea3-c3f8301f85ba&chat=%5B%7B%22question%22%3A%22hi%22%2C%22answer%22%3A%22Hello!%20How%20can%20I%20assist%20you%20today%3F%22%7D%5D&chatId=7a6671f8-5881-404d-8ea3-c3f8301f85ba&__cf_chl_tk=ex2bw6vn5vbLsUm8J5rDYUC0Bjzc1XZqka6vUl6765A-1684108495-0-gaNycGzNDtA',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Priority': 'u=0, i',
}

# Отправка запроса и обработка ответа
try:
    response = requests.get(f'https://you.com/api/streamingSearch?{params}',
                            headers=headers, content_callback=output, impersonate='safari15_5')
    exit(0)
except Exception as e:
    print('An error occurred:', e)