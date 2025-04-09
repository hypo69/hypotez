# Модуль для работы с Google Bard

## Обзор

Модуль предоставляет функциональность для взаимодействия с Google Bard через API. Он позволяет отправлять запросы и получать ответы от модели Palm2. Модуль требует аутентификации и может использовать прокси для обхода географических ограничений.

## Подробнее

Этот модуль предназначен для интеграции с Google Bard, используя неофициальный API. Он использует cookies для аутентификации и отправляет запросы через HTTP POST. Важно отметить, что использование неофициальных API может быть нестабильным и подвержено изменениям со стороны Google.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """Создает запрос к Google Bard и возвращает ответ.

    Args:
        model (str): Название модели для использования (в данном случае 'Palm2').
        messages (list): Список сообщений для отправки в Bard. Каждое сообщение должно содержать ключи 'role' и 'content'.
        stream (bool): Определяет, должен ли ответ возвращаться потоком.
        **kwargs: Дополнительные аргументы, такие как 'proxy'.

    Returns:
        Generator[str, None, None]: Генератор строк, содержащих ответ от Bard.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    Как работает функция:
    1.  **Извлечение PSID**: Извлекает значение cookie '__Secure-1PSID' из cookies браузера Chrome.
    2.  **Форматирование сообщений**: Форматирует список сообщений в строку, где каждое сообщение представлено в формате "роль: содержание".
    3.  **Формирование запроса**: Создает строку запроса, объединяя отформатированные сообщения с префиксом "Assistant:".
    4.  **Прокси**: Проверяет, передан ли прокси-сервер. Если нет, выводит предупреждение.
    5.  **Инициализация параметров**: Инициализирует переменные snlm0e, conversation_id, response_id и choice_id.
    6.  **Создание HTTP-клиента**: Создает сессию requests и настраивает прокси, если он предоставлен.
    7.  **Настройка заголовков**: Устанавливает необходимые заголовки для HTTP-запроса, включая cookie с PSID.
    8.  **Получение SNlM0e**: Извлекает значение SNlM0e из HTML-кода главной страницы Bard.
    9.  **Подготовка параметров запроса**: Формирует параметры запроса, включая случайный идентификатор запроса.
    10. **Подготовка данных запроса**: Формирует данные запроса, включая отформатированный запрос и идентификаторы.
    11. **Отправка запроса**: Отправляет POST-запрос к API Bard.
    12. **Обработка ответа**: Извлекает данные чата из ответа и возвращает их через генератор.
    13. **Обработка ошибок**: В случае ошибки возвращает строку "error".
    """

    # Извлечение PSID из cookies браузера Chrome
    psid = {cookie.name: cookie.value for cookie in browser_cookie3.chrome(domain_name='.google.com')}['__Secure-1PSID']
    
    # Форматирование сообщений для отправки в Bard
    formatted = '\n'.join([
        '%s: %s' % (message['role'], message['content']) for message in messages
    ])
    prompt = f'{formatted}\nAssistant:'

    # Проверка наличия прокси и вывод предупреждения, если он не указан
    proxy = kwargs.get('proxy', False)
    if proxy == False:
        print('warning!, you did not give a proxy, a lot of countries are banned from Google Bard, so it may not work')
    
    # Инициализация переменных для хранения данных о контексте диалога
    snlm0e = None
    conversation_id = None
    response_id = None
    choice_id = None

    # Создание HTTP-клиента с настройкой прокси и заголовков
    client = requests.Session()
    client.proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'} if proxy else None

    client.headers = {
        'authority': 'bard.google.com',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'origin': 'https://bard.google.com',
        'referer': 'https://bard.google.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-same-domain': '1',
        'cookie': f'__Secure-1PSID={psid}'
    }

    # Получение токена SNlM0e, если он еще не известен
    snlm0e = re.search(r'SNlM0e\\":\\"(.*?)\\"',
                    client.get('https://bard.google.com/').text).group(1) if not snlm0e else snlm0e

    # Подготовка параметров запроса
    params = {
        'bl': 'boq_assistant-bard-web-server_20230326.21_p0',
        '_reqid': random.randint(1111, 9999),
        'rt': 'c'
    }

    # Подготовка данных запроса
    data = {
        'at': snlm0e,
        'f.req': json.dumps([None, json.dumps([[prompt], None, [conversation_id, response_id, choice_id]])])}

    # Определение типа запроса
    intents = '.'.join([
        'assistant',
        'lamda',
        'BardFrontendService'
    ])

    # Отправка POST-запроса к API Bard
    response = client.post(f'https://bard.google.com/_/BardChatUi/data/{intents}/StreamGenerate',
                        data=data, params=params)

    # Обработка ответа от Bard
    chat_data = json.loads(response.content.splitlines()[3])[0][2]
    if chat_data:
        json_chat_data = json.loads(chat_data)

        # Возврат ответа в виде генератора
        yield json_chat_data[0][0]
        
    else:
        # Возврат ошибки, если не удалось получить ответ
        yield 'error'

    """
    A [Извлечение PSID]
    ↓
    B [Форматирование сообщений]
    ↓
    C [Проверка прокси]
    ↓
    D [Создание HTTP-клиента и настройка заголовков]
    ↓
    E [Получение SNlM0e]
    ↓
    F [Подготовка параметров и данных запроса]
    ↓
    G [Отправка POST-запроса]
    ↓
    H [Обработка ответа]
    """

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '({0})'.format(', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]]))
```

**Примеры**:

Пример вызова функции:

```python
messages = [{'role': 'user', 'content': 'Hello, Bard!'}]
for response in _create_completion(model='Palm2', messages=messages, stream=False):
    print(response)