### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код отправляет запрос к API `chatbot.theb.ai` для получения ответа от чат-бота на основе предоставленного запроса. Он использует библиотеку `curl-cffi` для выполнения HTTP-запроса с указанными заголовками и данными. Полученный ответ обрабатывается по частям и выводится в консоль.

Шаги выполнения
-------------------------
1. **Импорт библиотек**: Импортируются необходимые библиотеки, такие как `json`, `sys`, `re` (из `findall`) и `curl_cffi` (из `requests`).
2. **Чтение конфигурации**: Из аргументов командной строки считывается JSON-конфигурация и извлекается текст запроса (`prompt`) из последнего сообщения в списке сообщений.
3. **Определение заголовков**: Определяются заголовки HTTP-запроса, включая `authority`, `accept`, `content-type`, `origin`, `referer` и другие.
4. **Формирование данных запроса**: Формируются данные запроса в формате JSON, включающие текст запроса (`prompt`) и пустой словарь опций (`options`).
5. **Определение функции `format`**: Определяется функция `format`, которая извлекает содержимое ответа чат-бота из каждой части (`chunk`) полученных данных и выводит его в консоль. В случае ошибки выводится сообщение об ошибке и попытке повтора.
6. **Отправка запроса и обработка ответа**: В бесконечном цикле отправляется POST-запрос к API `chatbot.theb.ai/api/chat-process` с указанными заголовками и данными. Функция `format` используется для обработки каждой части ответа.
7. **Обработка ошибок**: Если при отправке запроса или обработке ответа возникает ошибка, выводится сообщение об ошибке и цикл повторяется.
8. **Завершение работы**: После успешного получения и обработки ответа программа завершает свою работу с кодом выхода 0.

Пример использования
-------------------------

```python
import json
import sys
from re import findall
from curl_cffi import requests

# Пример JSON-конфигурации, передаваемой как аргумент командной строки
config_json = """
{
    "messages": [
        {"role": "user", "content": "Привет!"},
        {"role": "assistant", "content": "Здравствуйте!"},
        {"role": "user", "content": "Как дела?"}
    ]
}
"""

# Заменяем sys.argv[1] на config_json для локального тестирования
config = json.loads(config_json)
prompt = config['messages'][-1]['content']

headers = {
    'authority': 'chatbot.theb.ai',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
    'content-type': 'application/json',
    'origin': 'https://chatbot.theb.ai',
    'referer': 'https://chatbot.theb.ai/',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

json_data = {
    'prompt': prompt,
    'options': {}
}

def format(chunk):
    try:
        completion_chunk = findall(r'content":"(.*)"},"fin', chunk.decode())[0]
        print(completion_chunk, flush=True, end='')

    except Exception as e:
        print(f'[ERROR] an error occured, retrying... | [[{chunk.decode()}]]', flush=True)
        return

while True:
    try:
        response = requests.post('https://chatbot.theb.ai/api/chat-process',
                            headers=headers, json=json_data, content_callback=format, impersonate='chrome110')
        exit(0)
    except Exception as e:
        print('[ERROR] an error occured, retrying... |', e, flush=True)
        continue