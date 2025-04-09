# Модуль для взаимодействия с провайдером You.com через API

## Обзор

Этот модуль предоставляет функциональность для взаимодействия с API You.com с целью получения ответов на запросы, используя предоставленные сообщения и параметры. Он включает в себя преобразование формата сообщений, отправку запросов к API и обработку полученных данных.

## Подробней

Этот модуль используется для интеграции с сервисом You.com, предоставляя возможность отправлять запросы и получать ответы в формате, необходимом для дальнейшей обработки. Модуль состоит из нескольких частей: преобразование сообщений в нужный формат, формирование параметров запроса и отправка запроса к API с последующей обработкой ответа.

## Функции

### `transform`

```python
def transform(messages: list) -> list:
    """
    Преобразует список сообщений в формат, требуемый API You.com.

    Args:
        messages (list): Список сообщений, где каждое сообщение представляет собой словарь с ключами 'role' и 'content'.

    Returns:
        list: Преобразованный список сообщений, где каждое сообщение содержит ключи 'question' и 'answer'.

    Как работает функция:
    1. Функция принимает список сообщений в формате, где каждое сообщение имеет роль ('user', 'assistant' или 'system') и содержимое.
    2. Итерируется по списку сообщений, обрабатывая сообщения пользователя и ассистента.
    3. Если встречается сообщение пользователя, его содержимое сохраняется как вопрос, а следующее сообщение ассистента (если есть) сохраняется как ответ.
    4. Если встречается сообщение только от ассистента, оно добавляется как ответ с пустым вопросом.
    5. Сообщения с ролью "system" добавляются как вопрос с пустым ответом.
    6. Возвращается преобразованный список сообщений.

    ASCII flowchart:

    Начало --> A [Вход: список сообщений]
    A --> B [Инициализация: i = 0, result = []]
    B --> C [Цикл: пока i < len(messages)]
    C -- Да --> D [Проверка: messages[i]['role'] == 'user']
    C -- Нет --> E [Проверка: messages[i]['role'] == 'assistant']
    D --> F [question = messages[i]['content'], i += 1]
    F --> G [Проверка: i < len(messages) and messages[i]['role'] == 'assistant']
    G -- Да --> H [answer = messages[i]['content'], i += 1]
    G -- Нет --> I [answer = '']
    H --> J [result.append({'question': question, 'answer': answer})]
    I --> J
    E --> K [result.append({'question': '', 'answer': messages[i]['content']}), i += 1]
    K --> J
    C -- Нет --> L [Проверка: messages[i]['role'] == 'system']
    L --> M [result.append({'question': messages[i]['content'], 'answer': ''}), i += 1]
    M --> J
    J --> C [i += 1]
    C -- Нет --> N [Возврат: result]
    N --> Конец

    Примеры:
    1.  Преобразование списка сообщений с вопросом и ответом:
        >>> messages = [{'role': 'user', 'content': 'Привет'}, {'role': 'assistant', 'content': 'Здравствуйте'}]
        >>> transform(messages)
        [{'question': 'Привет', 'answer': 'Здравствуйте'}]

    2.  Преобразование списка сообщений только с вопросом:
        >>> messages = [{'role': 'user', 'content': 'Как дела?'}]
        >>> transform(messages)
        [{'question': 'Как дела?', 'answer': ''}]

    3.  Преобразование списка сообщений с системным сообщением:
        >>> messages = [{'role': 'system', 'content': 'Начнем разговор'}]
        >>> transform(messages)
        [{'question': 'Начнем разговор', 'answer': ''}]
    """
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
```

### `output`

```python
def output(chunk):
    """
    Обрабатывает полученные чанки данных от API You.com и извлекает токен ответа.

    Args:
        chunk: Чанк данных, полученный от API.

    Как работает функция:

    1. Проверяет, содержит ли чанк данных строку `b'"youChatToken"'`.
    2. Если содержит, декодирует чанк, разделяет его по строке `'data: '`, загружает JSON из второй части разделенной строки.
    3. Извлекает значение из ключа `youChatToken` и выводит его в stdout без добавления новой строки, с немедленным сбросом буфера вывода.

    ASCII flowchart:

    A --> B [Проверка: b'"youChatToken"' in chunk]
    B -- Да --> C [Декодирование чанка: chunk.decode()]
    B -- Нет --> Конец
    C --> D [Разделение по 'data: ']
    D --> E [Загрузка JSON из второй части]
    E --> F [Вывод chunk_json['youChatToken'] в stdout без новой строки и с сбросом буфера]
    F --> Конец

    Примеры:

    1. Обработка чанка с данными, содержащими токен:
       Предположим, что chunk содержит: b'data: {"youChatToken": "example_token"}'
       Функция выведет: example_token

    2. Обработка чанка с данными, не содержащими токен:
       Предположим, что chunk содержит: b'data: {"other_data": "some_value"}'
       Функция ничего не выведет.
    """
    if b'"youChatToken"' in chunk:
        chunk_json = json.loads(chunk.decode().split('data: ')[1])

        print(chunk_json['youChatToken'], flush=True, end = '')