# Документация для модуля `theb.py`

## Обзор

Модуль `theb.py` предназначен для взаимодействия с чат-ботом `chatbot.theb.ai` с использованием `curl_cffi` для выполнения HTTP-запросов. Он получает конфигурацию и промпт через аргументы командной строки, формирует заголовки и JSON-данные для запроса, и обрабатывает ответы, выводя их в консоль.

## Подробней

Модуль предназначен для отправки запросов к API чат-бота `chatbot.theb.ai` и обработки потоковых ответов. Он использует библиотеку `curl_cffi` для выполнения HTTP-запросов, что позволяет имитировать запросы из браузера. Конфигурация, включая промпт, передается через аргументы командной строки в формате JSON.

## Функции

### `format`

```python
def format(chunk):
    """Функция обрабатывает полученный чанк данных из ответа сервера, извлекая содержимое и выводя его в консоль.

    Args:
        chunk (bytes): Часть данных, полученных от сервера.

    Returns:
        None

    Raises:
        Exception: Если не удается извлечь содержимое из чанка.
    """
    try:
        completion_chunk = findall(r'content":"(.*)"},"fin', chunk.decode())[0]
        print(completion_chunk, flush=True, end='')

    except Exception as ex:
        print(f'[ERROR] an error occured, retrying... | [[{chunk.decode()}]]', flush=True)
        return

```

**Назначение**: Обрабатывает полученный чанк данных из ответа сервера, извлекая полезное содержимое и выводя его в консоль.

**Параметры**:
- `chunk` (bytes): Часть данных, полученных от сервера.

**Возвращает**:
- `None`: Функция ничего не возвращает явно.

**Вызывает исключения**:
- `Exception`: Возникает, если не удается извлечь содержимое из чанка.

**Как работает функция**:

1.  Функция `format` принимает на вход чанк данных (`chunk`) в виде байтовой строки.
2.  Использует регулярное выражение `r'content":"(.*)"},"fin'` для поиска и извлечения содержимого, заключенного в `"content":"..."},"fin"`.
3.  Если находит, извлекает первую группу, соответствующую содержимому.
4.  Выводит извлеченное содержимое в консоль с помощью `print`, отключая добавление новой строки (`end=''`) и включает немедленный вывод (`flush=True`).
5.  Если происходит исключение (например, не найдено соответствие регулярному выражению), перехватывает его и выводит сообщение об ошибке вместе с содержимым чанка.

**Примеры**:

```python
# Пример вызова функции format
chunk = b'{"content":"Hello, world!"},"fin"'
format(chunk)  # Выведет в консоль: Hello, world!

chunk = b'Some other data'
format(chunk)  # Выведет в консоль: [ERROR] an error occured, retrying... | [[Some other data]]
```

## Переменные

-   `config` (dict): Конфигурация, загруженная из аргументов командной строки в формате JSON.
-   `prompt` (str): Текст запроса, извлеченный из конфигурации.
-   `headers` (dict): Заголовки HTTP-запроса для имитации запроса из браузера.
-   `json_data` (dict): JSON-данные, отправляемые в теле запроса, содержащие промпт и опции.

## Цикл обработки запросов

Основной цикл `while True:` выполняет следующие действия:

1.  Отправляет POST-запрос к `https://chatbot.theb.ai/api/chat-process` с заданными заголовками и JSON-данными.
2.  Использует `content_callback=format` для обработки каждого чанка данных, возвращаемого сервером.
3.  В случае успешного выполнения запроса завершает программу с кодом 0.
4.  Если происходит ошибка (например, сетевая), перехватывает исключение, выводит сообщение об ошибке и повторяет попытку.