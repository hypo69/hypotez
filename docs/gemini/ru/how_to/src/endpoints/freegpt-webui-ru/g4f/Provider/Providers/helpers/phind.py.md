### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код отправляет запрос к API `www.phind.com` для получения ответа на вопрос, используя предоставленные параметры запроса. Он обрабатывает ответ потоково, удаляя метаданные и форматируя вывод для отображения пользователю. В случае ошибки, код автоматически повторяет запрос.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**: Импортируются библиотеки `sys`, `json`, `datetime` и `urllib.parse` для работы с данными, JSON, временем и URL. Также импортируется `requests` из `curl_cffi` для выполнения HTTP-запросов.
2. **Чтение конфигурации**: Из аргументов командной строки загружается JSON-конфигурация с использованием `sys.argv[1]` и `json.loads()`.
3. **Извлечение запроса**: Из конфигурации извлекается текст вопроса (prompt) из последнего сообщения в списке `messages`.
4. **Определение уровня экспертизы**: На основе значения `config['model']` определяется уровень экспертизы (`skill`) как `'expert'` для модели `'gpt-4'` или `'intermediate'` для других моделей.
5. **Формирование JSON-данных**: Создаются JSON-данные для запроса к API, включающие вопрос, параметры (уровень экспертизы, дату, язык и др.) и форматируются с использованием `json.dumps()` для минимизации размера.
6. **Формирование заголовков HTTP-запроса**: Создаются заголовки HTTP-запроса, включающие тип контента, параметры кэширования, User-Agent, Referer и другие необходимые параметры.
7. **Определение функции `output`**: Определяется функция `output(chunk)`, которая обрабатывает каждый чанк данных, полученный от API.
    - Функция проверяет наличие метаданных `PHIND_METADATA` и удаляет их.
    - Функция декодирует чанк данных из байтов в строку.
    - Функция выполняет замену специфических последовательностей символов для форматирования данных.
    - Функция выводит обработанный чанк данных в консоль с использованием `print(chunk, flush=True, end = '')`.
8. **Выполнение запроса в цикле**: В бесконечном цикле `while True` выполняется попытка отправки POST-запроса к API `https://www.phind.com/api/infer/answer`.
    - Используется функция `requests.post()` для отправки запроса с указанными заголовками и данными.
    - Функция `output` используется как `content_callback` для потоковой обработки данных ответа.
    - В случае успешного выполнения запроса, скрипт завершается с кодом `0`.
9. **Обработка ошибок**: Если во время выполнения запроса возникает исключение, оно перехватывается.
    - Выводится сообщение об ошибке в консоль с использованием `print('an error occured, retrying... |', e, flush=True)`.
    - Цикл повторяется, и происходит повторная попытка отправки запроса.

Пример использования
-------------------------

```python
import sys
import json
import datetime
import urllib.parse

from curl_cffi import requests

# Пример конфигурации, которая может быть передана как аргумент командной строки
config_data = {
    'messages': [{'content': 'Explain the concept of quantum entanglement.'}],
    'model': 'gpt-4'
}

# Преобразуем конфигурацию в строку JSON и передаем как аргумент командной строки
sys.argv = ['script_name.py', json.dumps(config_data)]

config = json.loads(sys.argv[1])
prompt = config['messages'][-1]['content']

skill = 'expert' if config['model'] == 'gpt-4' else 'intermediate'

json_data = json.dumps({
    'question': prompt,
    'options': {
        'skill': skill,
        'date': datetime.datetime.now().strftime('%d/%m/%Y'),
        'language': 'en',
        'detailed': True,
        'creative': True,
        'customLinks': []}}, separators=(',', ':'))

headers = {
    'Content-Type': 'application/json',
    'Pragma': 'no-cache',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Sec-Fetch-Mode': 'cors',
    'Content-Length': str(len(json_data)),
    'Origin': 'https://www.phind.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
    'Referer': f'https://www.phind.com/search?q={urllib.parse.quote(prompt)}&source=searchbox',
    'Connection': 'keep-alive',
    'Host': 'www.phind.com',
    'Sec-Fetch-Dest': 'empty'
}

def output(chunk):
    try:
        if b'PHIND_METADATA' in chunk:
            return
        
        if chunk == b'data:  \\r\\ndata: \\r\\ndata: \\r\\n\\r\\n':
            chunk = b'data:  \\n\\r\\n\\r\\n'

        chunk = chunk.decode()

        chunk = chunk.replace('data: \\r\\n\\r\\ndata: ', 'data: \\n')
        chunk = chunk.replace('\\r\\ndata: \\r\\ndata: \\r\\n\\r\\n', '\\n\\r\\n\\r\\n')
        chunk = chunk.replace('data: ', '').replace('\\r\\n\\r\\n', '')

        print(chunk, flush=True, end = '')
        
    except json.decoder.JSONDecodeError:
        pass

while True:
    try:
        response = requests.post('https://www.phind.com/api/infer/answer',
                         headers=headers, data=json_data, content_callback=output, timeout=999999, impersonate='safari15_5')
        
        exit(0)
    
    except Exception as e:
        print('an error occured, retrying... |', e, flush=True)
        continue