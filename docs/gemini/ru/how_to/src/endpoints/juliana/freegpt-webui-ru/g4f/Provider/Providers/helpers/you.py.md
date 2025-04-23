### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот код предназначен для взаимодействия с API `you.com` с целью получения ответов на запросы, используя историю сообщений. Он преобразует формат сообщений, отправляет запрос к API и выводит полученные токены чата.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**: Импортируются библиотеки `sys`, `json`, `urllib.parse` и `curl_cffi`.
2. **Чтение конфигурации**: Из аргументов командной строки считывается JSON-конфигурация.
3. **Извлечение сообщений**: Из конфигурации извлекается список сообщений.
4. **Преобразование сообщений**: Функция `transform` преобразует список сообщений в формат, ожидаемый API `you.com`.
   - Сообщения пользователя и ассистента объединяются в пары вопрос-ответ.
   - Сообщения с ролью "system" добавляются как отдельные вопросы без ответов.
5. **Формирование заголовков**: Определяются HTTP-заголовки для запроса к API, включая `Content-Type`, `Accept`, `User-Agent` и другие.
6. **Подготовка параметров запроса**:
   - Если последнее сообщение имеет роль "user", оно извлекается как `prompt`, а остальные сообщения используются для формирования истории чата.
   - Параметры запроса кодируются в URL-формат с использованием `urllib.parse.urlencode`.
7. **Функция вывода `output`**: Определяет функцию `output`, которая обрабатывает каждый чанк ответа от API.
   - Ищет в чанке токен `youChatToken`, извлекает его из JSON и выводит в консоль.
8. **Отправка запроса и обработка ответа**:
   - В цикле отправляется `GET`-запрос к API `you.com` с заданными параметрами и заголовками.
   - Используется функция `output` для обработки каждого чанка ответа.
   - В случае ошибки выполняется повторная попытка запроса.

Пример использования
-------------------------

```python
import sys
import json
import urllib.parse
from curl_cffi import requests

# Пример конфигурации (обычно передается через sys.argv[1])
config_json = """
{
    "messages": [
        {"role": "user", "content": "Привет!"},
        {"role": "assistant", "content": "Здравствуйте! Как я могу вам помочь?"},
        {"role": "user", "content": "Какая сегодня погода?"}
    ]
}
"""

# Эмулируем передачу аргумента командной строки
sys.argv = ["script_name.py", config_json]

config = json.loads(sys.argv[1])
messages = config['messages']
prompt = ''

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

if messages[-1]['role'] == 'user':
    prompt = messages[-1]['content']
    messages = messages[:-1]

params = urllib.parse.urlencode({
    'q': prompt,
    'domain': 'youchat',
    'chat': transform(messages)
})

def output(chunk):
    if b'"youChatToken"' in chunk:
        chunk_json = json.loads(chunk.decode().split('data: ')[1])
        print(chunk_json['youChatToken'], flush=True, end='')

# Этот код здесь не будет выполняться из-за отсутствия реального ответа от API
# while True:
#     try:
#         response = requests.get(f'https://you.com/api/streamingSearch?{params}',
#                         headers=headers, content_callback=output, impersonate='safari15_5')
        
#         exit(0)
    
#     except Exception as e:
#         print('an error occured, retrying... |', e, flush=True)
#         continue