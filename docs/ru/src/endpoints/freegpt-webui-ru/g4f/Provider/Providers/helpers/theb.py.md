# Модуль для взаимодействия с chatbot.theb.ai

## Обзор

Модуль предназначен для отправки запросов к API `chatbot.theb.ai` с использованием библиотеки `curl-cffi` и обработки ответов, возвращаемых сервером. Он включает в себя функции для форматирования полученных данных и обработки возможных ошибок соединения или формата данных. Модуль использует параметры конфигурации, переданные через аргументы командной строки, и отправляет запросы до тех пор, пока не получит корректный ответ или не произойдет критическая ошибка.

## Подробней

Этот модуль является частью проекта `hypotez` и используется для взаимодействия с AI-моделью `chatbot.theb.ai`. Он отправляет текстовый запрос и обрабатывает ответ, выводя его в режиме реального времени. В случае возникновения ошибок, модуль автоматически повторяет попытки отправки запроса. Расположение модуля в структуре проекта указывает на его роль как вспомогательного инструмента для взаимодействия с внешним API.

## Функции

### `format`

```python
def format(chunk):
    """Форматирует и выводит фрагмент ответа, извлекая полезное содержимое.

    Args:
        chunk (bytes): Фрагмент ответа от сервера в виде байтовой строки.

    Returns:
        None

    Raises:
        Exception: Выводит сообщение об ошибке при неудачном извлечении содержимого и повторяет попытку.

    Example:
        Пример вызова функции с различными параметрами
        format(b'{"content":"Hello", "fin":true}')
    """
```

**Назначение**:
Функция `format` предназначена для извлечения и вывода содержимого из фрагментов ответов, полученных от сервера `chatbot.theb.ai`. Она использует регулярные выражения для поиска и извлечения текста, заключенного в поле `content` JSON-подобной структуры.

**Как работает функция**:

1.  **Извлечение содержимого**: Функция пытается извлечь содержимое из фрагмента ответа, используя регулярное выражение `r'content":"(.*)"},"fin'`.
2.  **Вывод содержимого**: В случае успешного извлечения, функция выводит извлеченное содержимое в стандартный поток вывода, не добавляя символ новой строки после каждого фрагмента.
3.  **Обработка ошибок**: Если извлечение содержимого не удается (например, из-за неожиданного формата фрагмента), функция перехватывает исключение и выводит сообщение об ошибке, указывая на необходимость повторной попытки.

```
A - Получение фрагмента ответа (chunk)
|
-- B - Попытка извлечения содержимого с использованием регулярного выражения
|
C - Успешное извлечение?
| Да
D - Вывод извлеченного содержимого
| Нет
E - Вывод сообщения об ошибке и повторная попытка
```

**Примеры**:

```python
format(b'{"content":"Привет", "fin":true}')
format(b'{"content":"Мир", "fin":false}')
```

## Код

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

def format(chunk):
    """Форматирует и выводит фрагмент ответа, извлекая полезное содержимое.

    Args:
        chunk (bytes): Фрагмент ответа от сервера в виде байтовой строки.

    Returns:
        None

    Raises:
        Exception: Выводит сообщение об ошибке при неудачном извлечении содержимого и повторяет попытку.

    Example:
        Пример вызова функции с различными параметрами
        format(b'{"content":"Hello", "fin":true}')
    """
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