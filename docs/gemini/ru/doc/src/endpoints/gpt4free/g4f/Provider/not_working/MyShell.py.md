# Модуль `MyShell`

## Обзор

Модуль `MyShell` предоставляет класс `MyShell`, который реализует интерфейс `AbstractProvider` для работы с GPT4Free. 

## Подробнее

Данный модуль обеспечивает доступ к API  `myshell.ai` для получения ответов от модели GPT-3.5 Turbo.  Он использует `WebDriverSession` для взаимодействия с API, прокси-сервер для обхода ограничений и обрабатывает поток ответов с помощью JavaScript-кода.

## Классы

### `MyShell`

**Описание**: Класс `MyShell` реализует интерфейс `AbstractProvider` для работы с GPT4Free через API `myshell.ai`.

**Наследует**: `AbstractProvider`

**Атрибуты**:

- `url (str)`: URL-адрес API сервиса.
- `working (bool)`:  Флаг, указывающий, работает ли провайдер.
- `supports_gpt_35_turbo (bool)`: Флаг, указывающий, поддерживает ли провайдер модель GPT-3.5 Turbo.
- `supports_stream (bool)`: Флаг, указывающий, поддерживает ли провайдер потоковую передачу ответов.

**Методы**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, timeout: int = 120, webdriver = None, **kwargs) -> CreateResult`:  Метод отправляет запрос к API `myshell.ai`, получает ответ и возвращает результат в виде потока.

**Как работает класс**:

- Класс `MyShell` наследует интерфейс `AbstractProvider`, реализуя метод `create_completion` для работы с GPT4Free. 
- При вызове метода `create_completion` создается сессия WebDriver, обходит ограничение Cloudflare (если необходимо), формируется запрос с данными (включая ID бота, номер сценария, текст запроса и тип сообщения) и отправляется к API `myshell.ai`. 
- Ответ от API обрабатывается с помощью JavaScript-кода, который парсит поток JSON-данных и извлекает текст ответа.
- Результат возвращается в виде потока.

**Примеры**:

```python
# Создание экземпляра класса MyShell
provider = MyShell()

# Отправка запроса с помощью метода create_completion
messages = [
    {'role': 'user', 'content': 'Привет! Расскажи мне анекдот.'}
]
response = provider.create_completion(
    model='gpt-3.5-turbo',
    messages=messages,
    stream=True
)

# Печать ответа
for chunk in response:
    print(chunk)
```


## Методы класса

### `create_completion`

```python
    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str = None,
        timeout: int = 120,
        webdriver = None,
        **kwargs
    ) -> CreateResult:
        """
        Отправляет запрос к API `myshell.ai` и получает ответ в виде потока.
        
        Args:
            model (str):  Модель GPT для запроса.
            messages (Messages): Список сообщений для запроса.
            stream (bool): Флаг, указывающий, нужно ли использовать потоковый режим передачи.
            proxy (str, optional): Прокси-сервер для обхода ограничений. По умолчанию `None`.
            timeout (int, optional):  Таймаут запроса в секундах. По умолчанию 120.
            webdriver (Driver, optional): Экземпляр WebDriver для работы с API. 
            **kwargs: Дополнительные аргументы для запроса. 

        Returns:
            CreateResult: Результат выполнения запроса в виде потока.

        Raises:
            Exception: Если возникает ошибка во время выполнения запроса.
        
        Example:
            >>> from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.MyShell import MyShell
            >>> provider = MyShell()
            >>> messages = [
            ...    {'role': 'user', 'content': 'Привет! Расскажи мне анекдот.'}
            ... ]
            >>> response = provider.create_completion(
            ...    model='gpt-3.5-turbo',
            ...    messages=messages,
            ...    stream=True
            ... )
            >>> for chunk in response:
            ...     print(chunk)
            ...
        """
        with WebDriverSession(webdriver, "", proxy=proxy) as driver:
            bypass_cloudflare(driver, cls.url, timeout)
            
            # Send request with message
            data = {
                "botId": "4738",
                "conversation_scenario": 3,
                "message": format_prompt(messages),
                "messageType": 1
            }
            script = """
response = await fetch("https://api.myshell.ai/v1/bot/chat/send_message", {
    "headers": {
        "accept": "application/json",
        "content-type": "application/json",
        "myshell-service-name": "organics-api",
        "visitor-id": localStorage.getItem("mix_visitorId")
    },
    "body": '{body}',
    "method": "POST"
})
window._reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
"""
            driver.execute_script(script.replace("{body}", json.dumps(data)))
            script = """
chunk = await window._reader.read();
if (chunk.done) {
    return null;
}
content = '';
chunk.value.split('\\n').forEach((line, index) => {
    if (line.startsWith('data: ')) {
        try {
            const data = JSON.parse(line.substring('data: '.length));
            if ('content' in data) {
                content += data['content'];
            }
        } catch(e) {}
    }
});
return content;
"""
            while True:
                chunk = driver.execute_script(script)
                if chunk:
                    yield chunk
                elif chunk != "":
                    break
                else:
                    time.sleep(0.1)
```

## Параметры класса

- `model (str)`: Модель GPT для запроса. 
- `messages (Messages)`: Список сообщений для запроса.
- `stream (bool)`: Флаг, указывающий, нужно ли использовать потоковый режим передачи.
- `proxy (str, optional)`: Прокси-сервер для обхода ограничений. По умолчанию `None`.
- `timeout (int, optional)`: Таймаут запроса в секундах. По умолчанию 120.
- `webdriver (Driver, optional)`: Экземпляр WebDriver для работы с API. 
- `**kwargs`: Дополнительные аргументы для запроса. 

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.MyShell import MyShell

# Создание экземпляра класса MyShell
provider = MyShell()

# Отправка запроса с помощью метода create_completion
messages = [
    {'role': 'user', 'content': 'Привет! Расскажи мне анекдот.'}
]
response = provider.create_completion(
    model='gpt-3.5-turbo',
    messages=messages,
    stream=True
)

# Печать ответа
for chunk in response:
    print(chunk)