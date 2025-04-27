# DfeHub.py

## Overview

Этот модуль предоставляет реализацию класса `DfeHub`, который представляет собой провайдера API для сервиса GPT4Free (DfeHub). Класс `DfeHub` наследует от базового класса `AbstractProvider` и предоставляет методы для создания завершений (completions) с использованием модели GPT-3.5-turbo. 

## Details

Класс `DfeHub` обеспечивает взаимодействие с API сервиса DfeHub. Он предназначен для отправки запросов на генерацию текста с использованием модели GPT-3.5-turbo.

## Classes

### `DfeHub`

**Description**: Класс `DfeHub` предоставляет реализацию провайдера API для сервиса GPT4Free (DfeHub),  взаимодействуя с API для отправки запросов на генерацию текста с использованием модели GPT-3.5-turbo.

**Inherits**: `AbstractProvider`

**Attributes**:
 - `url` (str): URL-адрес API сервиса DfeHub.
 - `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи (streaming) данных.
 - `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5-turbo.

**Methods**:
 - `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`

## Class Methods

### `create_completion`

```python
    @staticmethod
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool, **kwargs: Any) -> CreateResult:
        
        headers = {
            "authority"         : "chat.dfehub.com",
            "accept"            : "*/*",
            "accept-language"   : "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3",
            "content-type"      : "application/json",
            "origin"            : "https://chat.dfehub.com",
            "referer"           : "https://chat.dfehub.com/",
            "sec-ch-ua"         : '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "sec-ch-ua-mobile"  : "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest"    : "empty",
            "sec-fetch-mode"    : "cors",
            "sec-fetch-site"    : "same-origin",
            "user-agent"        : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "x-requested-with"  : "XMLHttpRequest",
        }

        json_data = {
            "messages"          : messages,
            "model"             : "gpt-3.5-turbo",
            "temperature"       : kwargs.get("temperature", 0.5),
            "presence_penalty"  : kwargs.get("presence_penalty", 0),
            "frequency_penalty" : kwargs.get("frequency_penalty", 0),
            "top_p"             : kwargs.get("top_p", 1),
            "stream"            : True
        }
        
        response = requests.post("https://chat.dfehub.com/api/openai/v1/chat/completions",
            headers=headers, json=json_data, timeout=3)

        for chunk in response.iter_lines():
            if b"detail" in chunk:
                delay = re.findall(r"\d+\.\d+", chunk.decode())
                delay = float(delay[-1])
                time.sleep(delay)
                yield from DfeHub.create_completion(model, messages, stream, **kwargs)
            if b"content" in chunk:
                data = json.loads(chunk.decode().split("data: ")[1])
                yield (data["choices"][0]["delta"]["content"])
```

**Purpose**: Функция `create_completion` реализует отправку запросов на API DfeHub для создания завершения (completions) текста с использованием модели GPT-3.5-turbo. 

**Parameters**:
 - `model` (str): Название модели. 
 - `messages` (list[dict[str, str]]): Список сообщений (messages) для контекста.
 - `stream` (bool): Флаг, указывающий на потоковую передачу (streaming) данных.
 - `kwargs` (Any): Дополнительные аргументы (keyword arguments) для настройки запроса. 

**Returns**:
 - `CreateResult`: Результат создания завершения (completions).

**Raises Exceptions**:
 - `Exception`: В случае возникновения ошибки при отправке запроса.

**How the Function Works**: 
 - Функция формирует заголовки запроса (`headers`) и данные запроса (`json_data`).
 - Запрос отправляется на URL `https://chat.dfehub.com/api/openai/v1/chat/completions` с использованием метода `requests.post`.
 - Полученный ответ (`response`) обрабатывается с помощью `response.iter_lines()`, который возвращает строки ответа построчно.
 - Каждая строка ответа анализируется на наличие специальных строк, таких как `"detail"` или `"content"`.
 - В случае наличия строки `"detail"` функция ожидает задержку (delay) и отправляет повторный запрос, чтобы получить завершение (completion) от модели.
 - В случае наличия строки `"content"` функция извлекает текстовый контент (`data["choices"][0]["delta"]["content"]`) и возвращает его в виде потока данных (streaming).

**Examples**:

```python
    messages = [
        {"role": "user", "content": "Привет, как дела?"},
        {"role": "assistant", "content": "Хорошо, а у тебя как?"},
    ]

    response = DfeHub.create_completion("gpt-3.5-turbo", messages, stream=True)

    for chunk in response:
        print(chunk, end="")
```

## Parameter Details

 - `model` (str): Название используемой модели.  В данном случае `gpt-3.5-turbo`. 
 - `messages` (list[dict[str, str]]): Список сообщений (messages), которые определяют контекст для генерации текста. 
 - `stream` (bool): Флаг, указывающий на потоковую передачу (streaming) данных.  
 - `kwargs` (Any): Дополнительные аргументы (keyword arguments) для настройки запроса:
     - `temperature`: Вещественное число, определяющее уровень креативности модели. 
     - `presence_penalty`: Вещественное число, определяющее штраф за повторение слов.
     - `frequency_penalty`: Вещественное число, определяющее штраф за повторение фраз.
     - `top_p`: Вещественное число, определяющее вероятность выбора следующего слова.