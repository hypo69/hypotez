### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код отправляет запрос к API `chatbot.theb.ai` для получения ответа на заданный вопрос. Он использует библиотеку `curl_cffi` для выполнения HTTP-запросов и форматирует полученные чанки ответа для вывода в консоль.

Шаги выполнения
-------------------------
1. **Импорт библиотек**: Импортируются необходимые библиотеки, такие как `json`, `sys`, `re`, и `curl_cffi`.
2. **Чтение конфигурации**: Загружается JSON-конфигурация из аргументов командной строки, содержащая промпт для запроса.
3. **Формирование заголовков**: Определяются HTTP-заголовки для запроса, включающие `authority`, `accept`, `content-type` и другие.
4. **Подготовка данных для запроса**: Формируется JSON-данные, включающие промпт и опции.
5. **Определение функции форматирования**: Определяется функция `format(chunk)`, которая извлекает контент из чанков ответа и выводит его в консоль.
6. **Отправка запроса в цикле**: В бесконечном цикле отправляется POST-запрос к API `chatbot.theb.ai` с использованием `curl_cffi.requests.post`.
7. **Обработка ответа**: Функция `format` вызывается для каждого чанка ответа, который извлекается и выводится в консоль.
8. **Обработка ошибок**: В случае возникновения ошибки при отправке запроса или обработке ответа, выводится сообщение об ошибке и происходит повторная попытка.
9. **Завершение работы**: После успешного получения и обработки ответа, программа завершается с кодом 0.

Пример использования
-------------------------

```python
import json
import sys
from re import findall
from curl_cffi import requests

# Пример конфигурации (обычно передается как аргумент командной строки)
config_data = {
    "messages": [
        {"content": "Напиши короткое стихотворение о весне."}
    ]
}

# Преобразуем словарь в JSON-строку для передачи как аргумент командной строки
config_json = json.dumps(config_data)

# Эмулируем аргумент командной строки
sys.argv = ["script_name.py", config_json]

# Загрузка конфигурации из аргументов командной строки
config = json.loads(sys.argv[1])
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