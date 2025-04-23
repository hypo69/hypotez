# Модуль для работы с провайдером Phind

## Обзор

Модуль предназначен для взаимодействия с API Phind для получения ответов на запросы. Он отправляет запросы к API и обрабатывает ответы, возвращая результаты пользователю.
Модуль использует библиотеку `curl_cffi` для выполнения HTTP-запросов.

## Подробней

Модуль `phind.py` является частью проекта `hypotez` и отвечает за интеграцию с сервисом Phind, который предоставляет ответы на вопросы, основываясь на указанных параметрах, таких как уровень экспертизы и дата.
Он формирует JSON-запрос с необходимыми данными, отправляет его на API Phind и обрабатывает полученные ответы.
Этот модуль важен для обеспечения функциональности, связанной с получением информации и ответов через Phind.

## Функции

### `output`

```python
def output(chunk):
    """Обрабатывает и выводит чанки данных, полученные от API Phind.

    Args:
        chunk (bytes): Часть данных, полученная от API Phind.

    Raises:
        json.decoder.JSONDecodeError: Если происходит ошибка при декодировании JSON.

    
        Функция `output` принимает чанк данных в байтовом формате, выполняет ряд преобразований для очистки и форматирования данных, и выводит результат в консоль.
        В первую очередь, функция проверяет наличие маркера `PHIND_METADATA` в чанке и прерывает выполнение, если маркер обнаружен.
        Затем, функция выполняет замену определенных последовательностей символов для корректного отображения данных.
        После преобразований, функция декодирует чанк из байтового формата в строку и заменяет специфические последовательности символов, такие как 'data: ' и '\\r\\n\\r\\n', чтобы привести данные к нужному виду.
        В конце, функция выводит обработанный чанк в консоль с помощью `print` и завершает свою работу.

    Примеры:
        Пример вызова функции:

        >>> chunk = b'data: {"answer": "example answer"}\\r\\n\\r\\n'
        >>> output(chunk)
        {"answer": "example answer"}
    """
```

## Код

```python
import sys
import json
import datetime
import urllib.parse

from curl_cffi import requests

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
```

## Параметры

- `config` (dict): Конфигурация, загруженная из `sys.argv[1]`.
- `prompt` (str): Текст запроса, извлеченный из `config['messages'][-1]['content']`.
- `skill` (str): Уровень экспертизы, определяемый моделью (`'expert'` для `gpt-4`, `'intermediate'` в противном случае).
- `json_data` (str): JSON-представление данных запроса, включающее вопрос и параметры.
- `headers` (dict): HTTP-заголовки для запроса.

## Как работает модуль

1.  **Чтение конфигурации**:
    *   Модуль начинает с чтения конфигурации из аргументов командной строки (`sys.argv[1]`) и загружает её как JSON.
    *   Из конфигурации извлекается текст запроса (`prompt`).
2.  **Определение уровня экспертизы**:
    *   На основе модели, указанной в конфигурации, определяется уровень экспертизы (`skill`). Если модель `gpt-4`, то уровень `expert`, иначе `intermediate`.
3.  **Формирование JSON-данных**:
    *   Формируются JSON-данные для запроса, включающие текст запроса, уровень экспертизы, дату и другие параметры.
4.  **Определение HTTP-заголовков**:
    *   Определяются HTTP-заголовки, необходимые для запроса, такие как `Content-Type`, `User-Agent` и другие.
5.  **Отправка запроса и обработка ответа**:
    *   В цикле `while True` отправляется POST-запрос к API Phind с использованием библиотеки `curl_cffi`.
    *   Функция `output` используется в качестве `content_callback` для обработки чанков данных, возвращаемых API.
    *   В случае успеха, цикл завершается вызовом `exit(0)`.
6.  **Обработка ошибок**:
    *   Если при отправке запроса или обработке ответа возникает исключение, выводится сообщение об ошибке и цикл повторяется.

## Примеры

### Пример JSON конфигурации:

```json
{
    "messages": [
        {
            "content": "Explain the concept of blockchain."
        }
    ],
    "model": "gpt-4"
}
```

### Пример запуска модуля из командной строки:

```bash
python phind.py '{"messages": [{"content": "Explain the concept of blockchain."}], "model": "gpt-4"}'