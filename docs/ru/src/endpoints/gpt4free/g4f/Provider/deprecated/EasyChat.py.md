## \file hypotez/src/endpoints/gpt4free/g4f/Provider/deprecated/EasyChat.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с провайдером EasyChat.
==================================================

Модуль содержит класс :class:`EasyChat`, который является устаревшим провайдером для получения ответов от языковой модели.
Он использует API EasyChat для создания и обработки запросов.

 .. module:: src.endpoints.gpt4free.g4f.Provider.deprecated.EasyChat
"""

## Обзор

Модуль предоставляет класс `EasyChat`, который позволяет взаимодействовать с сервисом EasyChat для генерации ответов на основе языковой модели. Этот провайдер поддерживает стриминг ответов и работу с моделью `gpt-3.5-turbo`.

## Подробнее

Класс `EasyChat` реализует логику для отправки запросов к API EasyChat и получения ответов. Он поддерживает как потоковую передачу ответов, так и получение полных ответов за один запрос.

## Классы

### `EasyChat(AbstractProvider)`

**Описание**: Класс для взаимодействия с провайдером EasyChat.

**Наследует**:
- `AbstractProvider`: Абстрактный класс, определяющий интерфейс для всех провайдеров.

**Атрибуты**:
- `url` (str): URL-адрес сервиса EasyChat (`"https://free.easychat.work"`).
- `supports_stream` (bool): Поддержка потоковой передачи (`True`).
- `supports_gpt_35_turbo` (bool): Поддержка модели `gpt-3.5-turbo` (`True`).
- `working` (bool): Указывает, работает ли провайдер (`False`).

**Методы**:
- `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`: Создает запрос на завершение текста.

## Методы класса

### `create_completion`

```python
@staticmethod
def create_completion(
    model: str,
    messages: list[dict[str, str]],
    stream: bool, **kwargs: Any) -> CreateResult:
    """
    Создает запрос на завершение текста к API EasyChat.

    Args:
        model (str): Идентификатор используемой модели.
        messages (list[dict[str, str]]): Список сообщений для отправки в запросе.
                                         Каждое сообщение представлено в виде словаря с ключами "role" и "content".
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу.
        **kwargs (Any): Дополнительные параметры запроса.

    Returns:
        CreateResult: Результат создания завершения. Тип `CreateResult` - это `Generator[str, None, None]` при `stream=True` или `str` при `stream=False`.

    Raises:
        Exception: Если получен код ответа, отличный от 200.
        Exception: Если в ответе от сервера отсутствует поле "choices".

    Как работает функция:
    - Определяет список активных серверов EasyChat.
    - Выбирает случайный сервер из списка активных серверов или использует сервер, указанный в kwargs.
    - Формирует заголовки запроса, включая информацию о браузере и типе контента.
    - Формирует JSON-данные для отправки в запросе, включая сообщения, модель, параметры temperature, presence_penalty, frequency_penalty и top_p.
    - Создает сессию requests для управления куками.
    - Отправляет POST-запрос к API EasyChat.
    - Обрабатывает ответ в зависимости от того, используется ли потоковая передача:
        - Если потоковая передача не используется, извлекает контент из ответа JSON и возвращает его.
        - Если потоковая передача используется, итерируется по чанкам ответа и извлекает контент из каждого чанка.
    - В случае ошибки выбрасывает исключение.

    Внутренние функции:
        - Отсутствуют.

    Примеры:
        >>> model = "gpt-3.5-turbo"
        >>> messages = [{"role": "user", "content": "Hello, how are you?"}]
        >>> stream = False
        >>> result = EasyChat.create_completion(model, messages, stream)
        >>> print(next(result))
        'I am doing well, thank you for asking. How can I assist you today?'

        >>> model = "gpt-3.5-turbo"
        >>> messages = [{"role": "user", "content": "Tell me a joke."}]
        >>> stream = True
        >>> result = EasyChat.create_completion(model, messages, stream)
        >>> for chunk in result:
        ...     print(chunk, end="")
        Why don't scientists trust atoms?Because they make up everything!
    """
    active_servers = [
        "https://chat10.fastgpt.me",
        "https://chat9.fastgpt.me",
        "https://chat1.fastgpt.me",
        "https://chat2.fastgpt.me",
        "https://chat3.fastgpt.me",
        "https://chat4.fastgpt.me",
        "https://gxos1h1ddt.fastgpt.me"
    ]

    server  = active_servers[kwargs.get("active_server", random.randint(0, 5))]
    headers = {
        "authority"         : f"{server}".replace("https://", ""),
        "accept"            : "text/event-stream",
        "accept-language"   : "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3,fa=0.2",
        "content-type"      : "application/json",
        "origin"            : f"{server}",
        "referer"           : f"{server}/",
        "x-requested-with"  : "XMLHttpRequest",
        'plugins'           : '0',
        'sec-ch-ua'         : '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile'  : '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest'    : 'empty',
        'sec-fetch-mode'    : 'cors',
        'sec-fetch-site'    : 'same-origin',
        'user-agent'        : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'usesearch'         : 'false',
        'x-requested-with'  : 'XMLHttpRequest'
    }

    json_data = {
        "messages"          : messages,
        "stream"            : stream,
        "model"             : model,
        "temperature"       : kwargs.get("temperature", 0.5),
        "presence_penalty"  : kwargs.get("presence_penalty", 0),
        "frequency_penalty" : kwargs.get("frequency_penalty", 0),
        "top_p"             : kwargs.get("top_p", 1)
    }

    session = requests.Session()
    # init cookies from server
    session.get(f"{server}/")

    response = session.post(f"{server}/api/openai/v1/chat/completions",
        headers=headers, json=json_data, stream=stream)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code} from server : {response.reason}")
    if not stream:
        json_data = response.json()

        if "choices" in json_data:
            yield json_data["choices"][0]["message"]["content"]
        else:
            raise Exception("No response from server")

    else:
            
        for chunk in response.iter_lines():
                
            if b"content" in chunk:
                splitData = chunk.decode().split("data:")

                if len(splitData) > 1:
                    yield json.loads(splitData[1])["choices"][0]["delta"]["content"]