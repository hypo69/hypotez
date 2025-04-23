### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Данный блок кода отправляет запрос в API `phind.com` для получения ответа на заданный вопрос. Он формирует JSON-запрос с параметрами, включая текст вопроса, уровень экспертизы и текущую дату, а затем отправляет этот запрос с определенными заголовками.  Ответ от API обрабатывается потоково, извлекаются полезные данные и выводятся в консоль.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**:
   - Импортируются библиотеки `sys`, `json`, `datetime` и `urllib.parse`.
   - Из библиотеки `curl_cffi` импортируется модуль `requests`.

2. **Чтение конфигурации и извлечение данных**:
   - Считывается JSON-конфигурация из аргументов командной строки через `sys.argv[1]` и загружается в переменную `config`.
   - Извлекается текст вопроса (prompt) из `config['messages'][-1]['content']`.
   - Определяется уровень экспертизы (`skill`) на основе модели, указанной в `config['model']`.

3. **Формирование JSON-данных для запроса**:
   - Создается JSON-объект `json_data`, содержащий вопрос, параметры (`skill`, `date`, `language` и т.д.).
   - Этот объект сериализуется в строку с использованием `json.dumps()` и разделением параметров запятыми и двоеточиями.

4. **Формирование заголовков запроса**:
   - Создается словарь `headers`, содержащий заголовки HTTP-запроса, такие как `Content-Type`, `Origin`, `User-Agent` и `Referer`.
   - Заголовок `Referer` формируется с использованием URL-кодирования текста вопроса (`prompt`).
   - Заголовок `Content-Length` устанавливается равным длине JSON-данных.

5. **Определение функции `output` для обработки чанков ответа**:
   - Функция `output(chunk)` принимает чанк данных ответа от сервера.
   - Проверяется наличие маркера `b'PHIND_METADATA'` в чанке, и если он присутствует, чанк игнорируется.
   - Выполняется постобработка чанка для удаления или замены определенных последовательностей символов (`data: \\r\\n`, `\\r\\ndata: \\r\\ndata: \\r\\n\\r\\n`, `data: ` и `\\r\\n\\r\\n`).
   - Декодированный и обработанный чанк выводится в консоль с использованием `print(chunk, flush=True, end='')`.
   - Обрабатывается исключение `json.decoder.JSONDecodeError` в случае ошибки декодирования JSON.

6. **Отправка POST-запроса в цикле**:
   - В бесконечном цикле `while True` отправляется POST-запрос к API `https://www.phind.com/api/infer/answer`.
   - Используются сформированные ранее заголовки (`headers`) и JSON-данные (`json_data`).
   - Функция `output` используется в качестве `content_callback` для обработки потоковых данных ответа.
   - Устанавливается таймаут запроса равным 999999 секунд и используется `impersonate='safari15_5'` для имитации браузера Safari.
   - В случае успешного запроса, программа завершается с кодом 0.

7. **Обработка ошибок и повторные попытки**:
   - Если во время запроса возникает исключение, оно перехватывается.
   - В консоль выводится сообщение об ошибке, и цикл продолжается, предпринимая повторную попытку отправки запроса.

Пример использования
-------------------------

```python
import sys
import json
import datetime
import urllib.parse

from curl_cffi import requests

# Пример конфигурации (обычно передается как аргумент командной строки)
config = {
    'messages': [{'content': 'What is the capital of France?'}],
    'model': 'gpt-3.5'
}

# Преобразуем config в строку JSON и передаем её как аргумент
config_json = json.dumps(config)
sys.argv = ['script_name.py', config_json]

# Далее код, как в предоставленном фрагменте
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