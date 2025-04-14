# Модуль Aivvm
## Обзор

Модуль `Aivvm` представляет собой провайдер для взаимодействия с сервисом `chat.aivvm.com` для получения ответов от языковых моделей, таких как `GPT-3.5` и `GPT-4`. Этот модуль является частью проекта `hypotez` и предназначен для использования в качестве одного из провайдеров в системе. Он предоставляет функциональность для отправки запросов к API `Aivvm` и получения ответов в потоковом режиме.

## Подробнее

Модуль содержит класс `Aivvm`, который наследуется от абстрактного класса `AbstractProvider`. Он определяет URL, поддерживает потоковую передачу данных, а также модели `gpt-3.5-turbo` и `gpt-4`.
В коде определен словарь `models`, который содержит информацию о поддерживаемых моделях, таких как `gpt-3.5-turbo`, `gpt-4` и другие.

## Классы

### `Aivvm(AbstractProvider)`

**Описание**:
Класс `Aivvm` предоставляет реализацию для взаимодействия с API `chat.aivvm.com`.

**Наследует**:

- `AbstractProvider`: Абстрактный класс, определяющий интерфейс для провайдеров.

**Атрибуты**:

- `url` (str): URL для отправки запросов.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.
- `supports_gpt_4` (bool): Указывает, поддерживает ли провайдер модель `gpt-4`.

**Методы**:

- `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`: Отправляет запрос на создание завершения и возвращает результат.

### `create_completion`

```python
    @classmethod
    def create_completion(cls,
        model: str,
        messages: Messages,
        stream: bool,
        **kwargs
    ) -> CreateResult:
        """
        Создает запрос на завершение текста, используя указанную модель и сообщения.

        Args:
            model (str): Идентификатор модели для использования.
            messages (Messages): Список сообщений для отправки в запросе.
            stream (bool): Указывает, следует ли использовать потоковый режим.
            **kwargs: Дополнительные аргументы.

        Returns:
            CreateResult: Результат создания завершения.

        Raises:
            ValueError: Если указанная модель не поддерживается.

         **Как работает функция**:
         - Функция `create_completion` принимает параметры `model`, `messages`, `stream` и `kwargs`.
         - Если `model` не указана, она устанавливается в значение `gpt-3.5-turbo`.
         - Если `model` не найдена в словаре `models`, вызывается исключение `ValueError`.
         - Создается словарь `json_data`, который содержит информацию о модели, сообщениях, ключе, промте и температуре.
         - Данные преобразуются в формат JSON.
         - Формируются заголовки HTTP-запроса.
         - Отправляется POST-запрос к API `chat.aivvm.com` с использованием библиотеки `requests`.
         - Функция итерируется по содержимому ответа в чанках размером 4096 байт.
         - Каждый чанк декодируется в UTF-8 и возвращается.
         - Если возникает ошибка `UnicodeDecodeError`, чанк декодируется с использованием `unicode-escape`.

        """
        if not model:
            model = "gpt-3.5-turbo"
        elif model not in models:
            raise ValueError(f"Model is not supported: {model}")

        json_data = {
            "model"       : models[model],
            "messages"    : messages,
            "key"         : "",
            "prompt"      : kwargs.get("system_message", "You are ChatGPT, a large language model trained by OpenAI. Follow the user\'s instructions carefully. Respond using markdown."),
            "temperature" : kwargs.get("temperature", 0.7)
        }

        data = json.dumps(json_data)

        headers = {
            "accept"            : "text/event-stream",
            "accept-language"   : "en-US,en;q=0.9",
            "content-type"      : "application/json",
            "content-length"    : str(len(data)),
            "sec-ch-ua"         : "\\"Chrome\\";v=\\"117\\", \\"Not;A=Brand\\";v=\\"8\\", \\"Chromium\\";v=\\"117\\"",
            "sec-ch-ua-mobile"  : "?0",
            "sec-ch-ua-platform": "\\"Windows\\"",
            "sec-fetch-dest"    : "empty",
            "sec-fetch-mode"    : "cors",
            "sec-fetch-site"    : "same-origin",
            "sec-gpc"           : "1",
            "referrer"          : "https://chat.aivvm.com/",
            "user-agent"        : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

        response = requests.post("https://chat.aivvm.com/api/chat", headers=headers, data=data, stream=True)
        response.raise_for_status()

        for chunk in response.iter_content(chunk_size=4096):\
            try:
                yield chunk.decode("utf-8")
            except UnicodeDecodeError:
                yield chunk.decode("unicode-escape")
```

**Примеры**:

```python
# Пример вызова функции create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, how are you?"}]
stream = True
result = Aivvm.create_completion(model=model, messages=messages, stream=stream)
for chunk in result:
    print(chunk)
```
```python
# Пример вызова функции create_completion с указанием system_message и temperature
model = "gpt-4"
messages = [{"role": "user", "content": "Translate 'hello' to French."}]
stream = False
kwargs = {"system_message": "You are a translator.", "temperature": 0.5}
result = Aivvm.create_completion(model=model, messages=messages, stream=stream, **kwargs)
if result:
    print(result)
```
```python
# Пример обработки исключения ValueError, если модель не поддерживается
try:
    model = "unsupported-model"
    messages = [{"role": "user", "content": "Test message"}]
    stream = True
    Aivvm.create_completion(model=model, messages=messages, stream=stream)
except ValueError as ex:
    print(f"Error: {ex}")
```
```python
# Пример отправки сообщений с разными ролями
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
stream = True
result = Aivvm.create_completion(model=model, messages=messages, stream=stream)
for chunk in result:
    print(chunk)
```
```python
# Пример использования температуры, чтобы сделать ответы более детерминированными
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Tell me a joke."}]
stream = True
kwargs = {"temperature": 0.2}
result = Aivvm.create_completion(model=model, messages=messages, stream=stream, **kwargs)
for chunk in result:
    print(chunk)
```
```python
# Пример использования stream=False и проверки, что возвращается не пустой результат
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "What is 2 + 2?"}]
stream = False
result = Aivvm.create_completion(model=model, messages=messages, stream=stream)
if result:
    print(result)
else:
    print("No result received.")