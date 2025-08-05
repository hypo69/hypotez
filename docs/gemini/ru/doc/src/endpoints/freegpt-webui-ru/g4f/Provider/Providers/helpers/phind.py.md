# Модуль для взаимодействия с API Phind

## Обзор

Данный модуль обеспечивает взаимодействие с API Phind, предоставляя средства для отправки запросов и обработки ответов. Модуль использует библиотеку `curl_cffi` для выполнения HTTP-запросов. 

## Подробности

В модуле определена функция `output`, которая обрабатывает фрагменты ответа от API Phind, преобразуя их в удобочитаемый формат и выводя на консоль. 

Функция `output` использует следующие шаги:

1. **Проверка наличия метаданных:** проверяет, содержится ли в фрагменте метаданная `PHIND_METADATA`. Если да, то фрагмент игнорируется.
2. **Обработка пустых данных:** если фрагмент представляет собой пустые данные, то он заменяется на `data:  \n\r\n\r\n`.
3. **Декодирование фрагмента:** фрагмент декодируется из байтового формата в строковый.
4. **Очистка фрагмента:** фрагмент очищается от лишних символов (`data: ` и `\r\n\r\n`).
5. **Вывод фрагмента:** фрагмент выводится на консоль.

## Функции

### `output(chunk)`

**Назначение**: Функция обрабатывает фрагменты ответа от API Phind, преобразуя их в удобочитаемый формат и выводя на консоль. 

**Параметры**:

- `chunk` (bytes): Фрагмент ответа от API Phind.

**Возвращает**: `None`

**Вызывает исключения**:

- `json.decoder.JSONDecodeError`: если фрагмент ответа не является корректным JSON.

**Как работает функция**:

Функция проверяет наличие метаданных в фрагменте ответа, обрабатывает пустые данные, декодирует и очищает фрагмент, а затем выводит его на консоль.

**Примеры**:

```python
>>> output(b'data:  \r\ndata: \\r\\ndata: \\r\\n\\r\\n')
data:  \n\r\n\r\n
>>> output(b'data: {"answer": "Ответ от API Phind"}\r\n\r\n')
{"answer": "Ответ от API Phind"}
```

## Параметры

- `config`: Словарь, содержащий конфигурационные параметры, включая `messages` (список сообщений) и `model` (имя модели).
- `prompt`: Последнее сообщение, отправленное в API Phind.
- `skill`: Уровень навыка (``expert`` или ``intermediate``), заданный на основе модели.
- `json_data`: Данные в формате JSON, которые отправляются в API Phind.
- `headers`: Словарь с заголовками HTTP-запроса.

## Примеры

```python
>>> config = json.loads(sys.argv[1])
>>> prompt = config['messages'][-1]['content']
>>> skill = 'expert' if config['model'] == 'gpt-4' else 'intermediate'
>>> json_data = json.dumps({'question': prompt, 'options': {'skill': skill, 'date': datetime.datetime.now().strftime('%d/%m/%Y'), 'language': 'en', 'detailed': True, 'creative': True, 'customLinks': []}}, separators=(',', ':'))
>>> headers = {'Content-Type': 'application/json', 'Pragma': 'no-cache', 'Accept': '*/*', 'Sec-Fetch-Site': 'same-origin', 'Accept-Language': 'en-GB,en;q=0.9', 'Cache-Control': 'no-cache', 'Sec-Fetch-Mode': 'cors', 'Content-Length': str(len(json_data)), 'Origin': 'https://www.phind.com', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15', 'Referer': f'https://www.phind.com/search?q={urllib.parse.quote(prompt)}&source=searchbox', 'Connection': 'keep-alive', 'Host': 'www.phind.com', 'Sec-Fetch-Dest': 'empty'}
>>> response = requests.post('https://www.phind.com/api/infer/answer', headers=headers, data=json_data, content_callback=output, timeout=999999, impersonate='safari15_5')