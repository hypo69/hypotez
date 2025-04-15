### **Системные инструкции для обработки кода проекта `hypotez`**

=========================================================================================

Описание функциональности и правил для генерации, анализа и улучшения кода. Направлено на обеспечение последовательного и читаемого стиля кодирования, соответствующего требованиям.

---

### **Основные принципы**

#### **1. Общие указания**:
- Соблюдай четкий и понятный стиль кодирования.
- Все изменения должны быть обоснованы и соответствовать установленным требованиям.

#### **2. Комментарии**:
- Используй `#` для внутренних комментариев.
- Документация всех функций, методов и классов должна следовать такому формату: 
    ```python
        def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
            """ 
            Args:
                param (str): Описание параметра `param`.
                param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.
    
            Returns:
                dict | None: Описание возвращаемого значения. Возвращает словарь или `None`.
    
            Raises:
                SomeError: Описание ситуации, в которой возникает исключение `SomeError`.

            Ехаmple:
                >>> function('param', 'param1')
                {'param': 'param1'}
            """
    ```
- Комментарии и документация должны быть четкими, лаконичными и точными.

#### **3. Форматирование кода**:
- Используй одинарные кавычки. `a:str = 'value'`, `print('Hello World!')`;
- Добавляй пробелы вокруг операторов. Например, `x = 5`;
- Все параметры должны быть аннотированы типами. `def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:`;
- Не используй `Union`. Вместо этого используй `|`.

#### **4. Логирование**:
- Для логгирования Всегда Используй модуль `logger` из `src.logger.logger`.
- Ошибки должны логироваться с использованием `logger.error`.
Пример:
    ```python
        try:
            ...
        except Exception as ex:
            logger.error('Error while processing data', ех, exc_info=True)
    ```
#### **5 Не используй `Union[]` в коде. Вместо него используй `|`
Например:
```python
x: str | int ...
```




---

### **Основные требования**:

#### **1. Формат ответов в Markdown**:
- Все ответы должны быть выполнены в формате **Markdown**.

#### **2. Формат комментариев**:
- Используй указанный стиль для комментариев и документации в коде.
- Пример:

```python
from typing import Generator, Optional, List
from pathlib import Path


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

    Args:
        file_path (str | Path): Путь к файлу или каталогу.
        as_list (bool): Если `True`, возвращает генератор строк.
        extensions (Optional[List[str]]): Список расширений файлов для чтения из каталога.
        chunk_size (int): Размер чанков для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
    ...
```
- Всегда делай подробные объяснения в комментариях. Избегай расплывчатых терминов, 
- таких как *«получить»* или *«делать»*. Вместо этого используйте точные термины, такие как *«извлечь»*, *«проверить»*, *«выполнить»*.
- Вместо: *«получаем»*, *«возвращаем»*, *«преобразовываем»* используй имя объекта *«функция получае»*, *«переменная возвращает»*, *«код преобразовывает»* 
- Комментарии должны непосредственно предшествовать описываемому блоку кода и объяснять его назначение.

#### **3. Пробелы вокруг операторов присваивания**:
- Всегда добавляйте пробелы вокруг оператора `=`, чтобы повысить читаемость.
- Примеры:
  - **Неправильно**: `x=5`
  - **Правильно**: `x = 5`

#### **4. Использование `j_loads` или `j_loads_ns`**:
- Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
- Пример:

```python
# Неправильно:
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Правильно:
data = j_loads('config.json')
```

#### **5. Сохранение комментариев**:
- Все существующие комментарии, начинающиеся с `#`, должны быть сохранены без изменений в разделе «Улучшенный код».
- Если комментарий кажется устаревшим или неясным, не изменяйте его. Вместо этого отметьте его в разделе «Изменения».

#### **6. Обработка `...` в коде**:
- Оставляйте `...` как указатели в коде без изменений.
- Не документируйте строки с `...`.
```

#### **7. Аннотации**
Для всех переменных должны быть определены аннотации типа. 
Для всех функций все входные и выходные параметры аннотириваны
Для все параметров должны быть аннотации типа.


### **8. webdriver**
В коде используется webdriver. Он импртируется из модуля `webdriver` проекта `hypotez`
```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Firefox)

Пoсле чего может использоваться как

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

## Анализ кода `hypotez/src/endpoints/freegpt-webui-ru/g4f/Provider/Providers/H2o.py`

### 1. Блок-схема

```mermaid
graph TD
    A[Начало] --> B{Инициализация переменных: url, model, supports_stream, needs_auth, models}
    B --> C{Определение функции _create_completion(model, messages, stream, **kwargs)}
    C --> D{Формирование conversation из messages}
    D --> E{Создание сессии requests.Session()}
    E --> F{Установка headers для сессии}
    F --> G{Выполнение GET запроса к 'https://gpt-gm.h2o.ai/'}
    G --> H{Выполнение POST запроса к 'https://gpt-gm.h2o.ai/settings'}
    H --> I{Установка headers для запросов}
    I --> J{Формирование json_data с моделью}
    J --> K{Выполнение POST запроса к 'https://gpt-gm.h2o.ai/conversation'}
    K --> L{Извлечение conversationId из ответа}
    L --> M{Выполнение POST запроса к 'https://gpt-gm.h2o.ai/conversation/{conversationId}' с stream=True}
    M --> N{Итерация по строкам ответа}
    N --> O{Проверка наличия 'data' в строке}
    O -- Да --> P{Преобразование строки в JSON}
    P --> Q{Извлечение токена из JSON}
    Q --> R{Проверка токена на '<|endoftext|>'}
    R -- Да --> S[Завершение итерации]
    R -- Нет --> T{Генерация токена}
    T --> N
    O -- Нет --> N
    S --> U[Конец]
```

**Примеры для логических блоков:**

*   **A (Начало)**: Начало выполнения скрипта.
*   **B (Инициализация переменных)**:

    ```python
    url = 'https://gpt-gm.h2o.ai'
    model = ['falcon-40b', 'falcon-7b', 'llama-13b']
    supports_stream = True
    needs_auth = False
    models = {
        'falcon-7b': 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-7b-v3',
        'falcon-40b': 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1',
        'llama-13b': 'h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-13b'
    }
    ```
*   **C (Определение функции `_create_completion`)**:

    ```python
    def _create_completion(model: str, messages: list, stream: bool, **kwargs):
        ...
    ```
*   **D (Формирование conversation)**:

    ```python
    conversation = 'instruction: this is a conversation beween, a user and an AI assistant, respond to the latest message, referring to the conversation if needed\n'
    for message in messages:
        conversation += '%s: %s\n' % (message['role'], message['content'])
    conversation += 'assistant:'
    ```
*   **E (Создание сессии)**:

    ```python
    client = Session()
    ```
*   **F (Установка headers для сессии)**:

    ```python
    client.headers = {
        'authority': 'gpt-gm.h2o.ai',
        'origin': 'https://gpt-gm.h2o.ai',
        'referer': 'https://gpt-gm.h2o.ai/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    ```
*   **G (GET запрос)**:

    ```python
    client.get('https://gpt-gm.h2o.ai/')
    ```
*   **H (POST запрос к /settings)**:

    ```python
    response = client.post('https://gpt-gm.h2o.ai/settings', data={
        'ethicsModalAccepted': 'true',
        'shareConversationsWithModelAuthors': 'true',
        'ethicsModalAcceptedAt': '',
        'activeModel': 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1',
        'searchEnabled': 'true',
    })
    ```
*   **I (Установка headers для запросов)**:

    ```python
    headers = {
        'authority': 'gpt-gm.h2o.ai',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'origin': 'https://gpt-gm.h2o.ai',
        'referer': 'https://gpt-gm.h2o.ai/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    ```
*   **J (Формирование json_data)**:

    ```python
    json_data = {
        'model': models[model]
    }
    ```
*   **K (POST запрос к /conversation)**:

    ```python
    response = client.post('https://gpt-gm.h2o.ai/conversation',
                            headers=headers, json=json_data)
    ```
*   **L (Извлечение conversationId)**:

    ```python
    conversationId = response.json()['conversationId']
    ```
*   **M (POST запрос к /conversation/{conversationId})**:

    ```python
    completion = client.post(f'https://gpt-gm.h2o.ai/conversation/{conversationId}', stream=True, json = {
        'inputs': conversation,
        'parameters': {
            'temperature': kwargs.get('temperature', 0.4),
            'truncate': kwargs.get('truncate', 2048),
            'max_new_tokens': kwargs.get('max_new_tokens', 1024),
            'do_sample': kwargs.get('do_sample', True),
            'repetition_penalty': kwargs.get('repetition_penalty', 1.2),
            'return_full_text': kwargs.get('return_full_text', False)
        },
        'stream': True,
        'options': {
            'id': kwargs.get('id', str(uuid4())),
            'response_id': kwargs.get('response_id', str(uuid4())),
            'is_retry': False,
            'use_cache': False,
            'web_search_id': ''
        }
    })
    ```
*   **N (Итерация по строкам ответа)**:

    ```python
    for line in completion.iter_lines():
        ...
    ```
*   **O (Проверка наличия 'data' в строке)**:

    ```python
    if b'data' in line:
        ...
    ```
*   **P (Преобразование строки в JSON)**:

    ```python
    line = loads(line.decode('utf-8').replace('data:', ''))
    ```
*   **Q (Извлечение токена из JSON)**:

    ```python
    token = line['token']['text']
    ```
*   **R (Проверка токена на '<|endoftext|>')**:

    ```python
    if token == '<|endoftext|>':
        break
    else:
        yield (token)
    ```
*   **S (Завершение итерации)**: break
*   **T (Генерация токена)**: `yield (token)`
*   **U (Конец)**: Конец выполнения функции.

### 2. Диаграмма

```mermaid
graph TD
    A[Session] --> B{client.headers}
    B --> C{client.get('https://gpt-gm.h2o.ai/')}
    C --> D{client.post('https://gpt-gm.h2o.ai/settings', data)}
    D --> E{headers}
    E --> F{json_data = {'model': models[model]}}
    F --> G{client.post('https://gpt-gm.h2o.ai/conversation', headers, json_data)}
    G --> H{conversationId = response.json()['conversationId']}
    H --> I{completion = client.post(f'https://gpt-gm.h2o.ai/conversation/{conversationId}', stream=True, json)}
    I --> J{completion.iter_lines()}
    J --> K{loads(line.decode('utf-8').replace('data:', ''))}

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#ccf,stroke:#333,stroke-width:2px
    style K fill:#ccf,stroke:#333,stroke-width:2px
```

**Объяснение зависимостей:**

*   `requests.Session`: Используется для создания сессии HTTP-запросов. Это позволяет сохранять параметры между запросами (например, cookies).
*   `client.headers`: Заголовки HTTP-запроса, необходимые для взаимодействия с сервером.
*   `client.get('https://gpt-gm.h2o.ai/')`: Выполняется GET-запрос для получения главной страницы.
*   `client.post('https://gpt-gm.h2o.ai/settings', data)`: POST-запрос для установки настроек.
*   `headers`: Заголовки для POST-запроса к `/conversation`.
*   `json_data = {'model': models[model]}`: Данные в формате JSON, содержащие информацию о модели.
*   `client.post('https://gpt-gm.h2o.ai/conversation', headers, json_data)`: POST-запрос для начала разговора.
*   `conversationId = response.json()['conversationId']`: Извлечение идентификатора разговора из ответа сервера.
*   `completion = client.post(f'https://gpt-gm.h2o.ai/conversation/{conversationId}', stream=True, json)`: POST-запрос для получения ответа от модели в режиме стриминга.
*   `completion.iter_lines()`: Итерация по строкам ответа.
*   `loads(line.decode('utf-8').replace('data:', ''))`: Преобразование строки с данными в формат JSON.

### 3. Объяснение

**Импорты:**

*   `requests`: Используется для выполнения HTTP-запросов к API. В данном случае, для отправки запросов к серверам H2O.
*   `uuid`: Используется для генерации уникальных идентификаторов (`uuid4`).
*   `json`: Используется для работы с данными в формате JSON, в частности, для десериализации JSON-ответов от сервера.
*   `os`: Используется для работы с операционной системой, например, для получения имени файла.
*   `...typing`:  `sha256`, `Dict`, `get_type_hints` - элементы из абстрактного импорта. `sha256` - тип данных, `Dict` - словарь, `get_type_hints` - используется для получения аннотаций типов.

**Переменные:**

*   `url: str = 'https://gpt-gm.h2o.ai'`: Базовый URL для API H2O.
*   `model: list = ['falcon-40b', 'falcon-7b', 'llama-13b']`: Список поддерживаемых моделей.
*   `supports_stream: bool = True`: Указывает, что провайдер поддерживает потоковую передачу данных.
*   `needs_auth: bool = False`: Указывает, что для доступа к API не требуется аутентификация.
*   `models: dict`: Словарь, сопоставляющий короткие имена моделей с их полными идентификаторами на сервере H2O.

**Функции:**

*   `_create_completion(model: str, messages: list, stream: bool, **kwargs)`:
    *   `model (str)`: Идентификатор используемой модели.
    *   `messages (list)`: Список сообщений в формате `{'role': роль, 'content': содержимое}`.
    *   `stream (bool)`:  Флаг, указывающий на необходимость потоковой передачи данных.
    *   `**kwargs`: Дополнительные параметры, такие как `temperature`, `truncate`, `max_new_tokens` и т.д.
    *   Функция формирует запрос к API H2O, отправляет историю разговора и параметры генерации, а затем возвращает ответ в виде генератора токенов.

**Логика работы:**

1.  Инициализация сессии `requests.Session()` для выполнения HTTP-запросов.
2.  Установка заголовков (`headers`) для сессии, чтобы имитировать запросы из браузера.
3.  Выполнение GET-запроса к главной странице `https://gpt-gm.h2o.ai/`.
4.  Выполнение POST-запроса к `/settings` для установки параметров сессии, таких как принятие условий использования и выбор активной модели.
5.  Формирование тела запроса (`json_data`) с указанием используемой модели.
6.  Выполнение POST-запроса к `/conversation` для начала нового разговора и получения `conversationId`.
7.  Выполнение POST-запроса к `/conversation/{conversationId}` с параметром `stream=True` для получения ответа в режиме потоковой передачи.
8.  Итерация по строкам ответа, извлечение токенов и их генерация с использованием `yield`.

**Потенциальные ошибки и области для улучшения:**

*   Отсутствует обработка ошибок при выполнении HTTP-запросов. Необходимо добавить блоки `try...except` для обработки возможных исключений, таких как `requests.exceptions.RequestException`.
*   Жестко заданные URL-адреса и параметры запросов. Можно вынести их в конфигурационные файлы или переменные окружения для упрощения настройки и развертывания.
*   Отсутствует логирование. Было бы полезно добавить логирование для отслеживания запросов, ответов и ошибок.
*   Не все параметры из `kwargs` используются. Следует проверить, какие параметры действительно необходимы и используются.

**Взаимосвязи с другими частями проекта:**

*   Этот файл является провайдером для `g4f`, что позволяет использовать модели H2O в качестве одного из источников генерации текста.
*   Функция `_create_completion` используется для создания запроса к API и обработки ответа.
*   Переменные `model`, `supports_stream`, `needs_auth` используются для определения характеристик провайдера H2O.

Также присутствует строка:

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

Эта строка формирует строку `params`, которая, вероятно, используется для документирования или логирования информации о поддерживаемых параметрах функции `_create_completion`. Она использует `os.path.basename(__file__)[:-3]` для получения имени текущего файла без расширения `.py`, а также `get_type_hints` и `_create_completion.__code__.co_varnames` для получения информации о типах и именах параметров функции.

**Общее заключение:**

Этот код предоставляет функциональность для взаимодействия с API H2O для генерации текста. Он использует библиотеку `requests` для выполнения HTTP-запросов и обрабатывает ответы в режиме потоковой передачи. Код требует доработки в части обработки ошибок, конфигурации и логирования.