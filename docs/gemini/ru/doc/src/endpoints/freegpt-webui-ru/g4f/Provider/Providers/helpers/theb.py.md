# Модуль для взаимодействия с TheB.ai

## Обзор

Этот модуль предназначен для взаимодействия с моделью TheB.ai с использованием библиотеки `curl_cffi` для отправки HTTP-запросов. 

## Подробней

Модуль использует конфигурационные данные, полученные из аргументов командной строки, для формирования запроса к TheB.ai. 

## Функции

### `format`

**Назначение**: Форматирует ответ TheB.ai для вывода в консоль.

**Параметры**:

- `chunk` (bytes): Часть ответа TheB.ai, полученная в виде байтового потока.

**Возвращает**:

- None: Функция выводит форматированный ответ в консоль.

**Вызывает исключения**:

- Exception: Если возникают проблемы с обработкой ответа.

**Как работает функция**:

- Извлекает содержимое ответа `content` с помощью регулярных выражений.
- Выводит `content` в консоль с помощью `print`.

**Примеры**:

```python
>>> chunk = b'"content":"Пример ответа модели TheB.ai", "fin"'
>>> format(chunk)
Пример ответа модели TheB.ai
```

## Примеры использования

```python
import json
import sys
from re import findall
from curl_cffi import requests

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

while True:
    try:
        response = requests.post('https://chatbot.theb.ai/api/chat-process',
                                headers=headers, json=json_data, content_callback=format, impersonate='chrome110')

        exit(0)

    except Exception as e:
        print('[ERROR] an error occured, retrying... |', e, flush=True)
        continue
```

**Описание**:

- Модуль считывает конфигурационные данные из аргументов командной строки.
- Формирует запрос к TheB.ai с помощью `requests.post`.
- Использует `format` для обработки и вывода ответа TheB.ai.
- Продолжает попытки отправки запроса, если возникают ошибки.