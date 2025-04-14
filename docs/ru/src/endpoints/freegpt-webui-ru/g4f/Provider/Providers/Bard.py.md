# Модуль для взаимодействия с Google Bard

## Обзор

Модуль предоставляет функциональность для взаимодействия с моделью Google Bard. Он позволяет отправлять запросы к Bard и получать ответы. Модуль использует cookies для аутентификации и поддерживает настройку прокси-сервера.

## Подробнее

Этот модуль предназначен для интеграции с Google Bard, используя предоставленные cookies для аутентификации. Он отправляет сообщения в Bard и возвращает сгенерированный ответ. Важно отметить, что модуль требует наличия активного аккаунта Google и корректных cookies для успешной работы.
Расположение файла в проекте: `hypotez/src/endpoints/freegpt-webui-ru/g4f/Provider/Providers/Bard.py`

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает запрос к Google Bard и возвращает ответ.

    Args:
        model (str): Имя модели, используемой для генерации ответа (в данном случае всегда 'Palm2').
        messages (list): Список сообщений для Bard, где каждое сообщение содержит роль и контент.
        stream (bool): Флаг, указывающий, нужно ли возвращать ответ в режиме потока (в данном случае всегда `False`).
        **kwargs: Дополнительные параметры, такие как `proxy`.

    Returns:
        Generator[str, None, None]: Генератор, выдающий ответ от Bard.

    Raises:
        Exception: Если возникает ошибка при взаимодействии с Bard.

    Как работает функция:
    1.  Извлекает значение cookie `__Secure-1PSID` из cookies браузера Chrome для аутентификации.
    2.  Форматирует список сообщений в строку, пригодную для отправки в Bard.
    3.  Определяет, использовать ли прокси-сервер.
    4.  Инициализирует параметры `snlm0e`, `conversation_id`, `response_id` и `choice_id`.
    5.  Создает сессию `requests` и устанавливает заголовки, включая cookie и User-Agent.
    6.  Получает значение `SNlM0e` из главной страницы Bard, если оно еще не определено.
    7.  Формирует параметры запроса, включая случайный `_reqid`.
    8.  Создает данные запроса, содержащие отформатированный запрос.
    9.  Определяет endpoint для отправки запроса.
    10. Отправляет POST-запрос к Bard и получает ответ.
    11. Извлекает данные чата из ответа и возвращает их через генератор.
    12. В случае ошибки возвращает строку "error".

    Схема работы функции:
    ```
    A [Получение cookie __Secure-1PSID]
    |
    B [Форматирование сообщений]
    |
    C [Определение прокси]
    |
    D [Инициализация параметров]
    |
    E [Создание сессии requests]
    |
    F [Получение SNlM0e]
    |
    G [Формирование параметров запроса]
    |
    H [Создание данных запроса]
    |
    I [Отправка POST-запроса]
    |
    J [Извлечение данных чата]
    |
    K [Возврат ответа]
    ```
    Примеры:
    1.  Успешный запрос к Bard:

        ```python
        messages = [{"role": "user", "content": "Привет, Bard!"}]
        for response in _create_completion(model="Palm2", messages=messages, stream=False):
            print(response)
        ```
    2.  Запрос к Bard с использованием прокси:

        ```python
        messages = [{"role": "user", "content": "Привет, Bard!"}]
        for response in _create_completion(model="Palm2", messages=messages, stream=False, proxy="http://proxy.example.com:8080"):
            print(response)
        ```
    """
    psid = {cookie.name: cookie.value for cookie in browser_cookie3.chrome(
        domain_name=\'.google.com\')}[\'__Secure-1PSID\']
    
    formatted = \'\\n\'.join([\
        \'%s: %s\' % (message[\'role\'], message[\'content\']) for message in messages\
    ])
    prompt = f\'{formatted}\\nAssistant:\'\

    proxy = kwargs.get(\'proxy\', False)
    if proxy == False:
        print(\'warning!, you did not give a proxy, a lot of countries are banned from Google Bard, so it may not work\')
    
    snlm0e = None
    conversation_id = None
    response_id = None
    choice_id = None

    client = requests.Session()
    client.proxies = {\
        \'http\': f\'http://{proxy}\',\
        \'https\': f\'http://{proxy}\'} if proxy else None

    client.headers = {\
        \'authority\': \'bard.google.com\',\
        \'content-type\': \'application/x-www-form-urlencoded;charset=UTF-8\',\
        \'origin\': \'https://bard.google.com\',\
        \'referer\': \'https://bard.google.com/\',\
        \'user-agent\': \'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36\',\
        \'x-same-domain\': \'1\',\
        \'cookie\': f\'__Secure-1PSID={psid}\'\
    }

    snlm0e = re.search(r\'SNlM0e\\":\\"(.*?)\\"\',\
                    client.get(\'https://bard.google.com/\').text).group(1) if not snlm0e else snlm0e

    params = {\
        \'bl\': \'boq_assistant-bard-web-server_20230326.21_p0\',\
        \'_reqid\': random.randint(1111, 9999),\
        \'rt\': \'c\'\
    }

    data = {\
        \'at\': snlm0e,\
        \'f.req\': json.dumps([None, json.dumps([[prompt], None, [conversation_id, response_id, choice_id]])])}

    intents = \'.\'.join([\
        \'assistant\',\
        \'lamda\',\
        \'BardFrontendService\'\
    ])

    response = client.post(f\'https://bard.google.com/_/BardChatUi/data/{intents}/StreamGenerate\',\
                        data=data, params=params)

    chat_data = json.loads(response.content.splitlines()[3])[0][2]
    if chat_data:
        json_chat_data = json.loads(chat_data)

        yield json_chat_data[0][0]
        
    else:
        yield \'error\'

```

### `params`

```python
params = f\'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: \' + \
    \'(%s)\' % \', \'.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```
- **Назначение**: Формирует строку с информацией о поддержке параметров функцией `_create_completion`.
- **Как работает**:
    1.  Формирует базовую строку, включающую имя текущего файла (без расширения `.py`).
    2.  Использует `get_type_hints` для получения аннотаций типов параметров функции `_create_completion`.
    3.  Создает подстроку для каждого параметра, содержащую имя параметра и его тип.
    4.  Объединяет все подстроки в одну строку, разделенную запятыми.
    5.  Форматирует итоговую строку, добавляя информацию о поддерживаемых параметрах.
- **Пример**:
    - Предположим, функция `_create_completion` имеет параметры `model: str`, `messages: list` и `stream: bool`. Тогда строка `params` будет выглядеть примерно так:
    ```
    'g4f.Providers.Bard supports: (model: str, messages: list, stream: bool)'
    ```
```