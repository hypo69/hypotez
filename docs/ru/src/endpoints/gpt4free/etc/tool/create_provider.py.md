# Модуль для создания провайдеров

## Обзор

Этот модуль предназначен для автоматического создания файлов провайдеров на основе команд cURL.
Он анализирует предоставленную команду cURL, генерирует код Python для нового провайдера и сохраняет его в указанном файле.

## Подробнее

Модуль `create_provider.py` автоматизирует процесс создания новых провайдеров для библиотеки `g4f` (GPT4Free) на основе команд `cURL`. Он принимает имя провайдера, запрашивает у пользователя команду `cURL`, генерирует код провайдера, используя модель `gpt-4o`, и сохраняет сгенерированный код в файл. Если файл провайдера уже существует, он просто считывает его содержимое.

## Функции

### `read_code`

```python
def read_code(text: str) -> str | None:
    """Функция извлекает код Python из текстовой строки, обрамленного символами ```.

    Args:
        text (str): Текст, содержащий код Python.

    Returns:
        str | None: Код Python, найденный в тексте, или None, если код не найден.

    Как работает функция:
    - Использует регулярное выражение для поиска блоков кода, заключенных в тройные обратные кавычки (```).
    - Извлекает код Python из найденного блока.
    - Возвращает извлеченный код или None, если соответствие не найдено.

    Примеры:
        >>> text = "Some text ```python\\nprint('Hello')\\n```"
        >>> read_code(text)
        "print('Hello')"

        >>> text = "No code here"
        >>> read_code(text) is None
        True
    """
```

### `input_command`

```python
def input_command() -> str:
    """Функция для ввода многострочной команды cURL через стандартный ввод.

    Args:
        None

    Returns:
        str: Объединенная строка, содержащая введенные команды.

    Как работает функция:
    - Предлагает пользователю ввести или вставить команду cURL.
    - Читает строки из стандартного ввода до тех пор, пока не встретится символ EOF (Ctrl-D или Ctrl-Z в Windows).
    - Объединяет введенные строки в одну строку, разделенную символами новой строки.
    - Возвращает полученную строку.
    """
```

## Основной код

Основная часть кода выполняет следующие действия:

1.  Запрашивает у пользователя имя провайдера.
2.  Формирует путь к файлу провайдера.
3.  Если файл провайдера не существует:

    *   Запрашивает у пользователя команду `cURL` с использованием функции `input_command()`.
    *   Формирует промпт для модели `gpt-4o`, чтобы создать код провайдера на основе команды `cURL` и примера.
    *   Отправляет промпт в модель `gpt-4o` для генерации кода.
    *   Извлекает сгенерированный код из ответа с использованием функции `read_code()`.
    *   Сохраняет код в файл провайдера.
    *   Добавляет строку импорта для нового провайдера в файл `g4f/Provider/__init__.py`.
4.  Если файл провайдера существует, считывает его содержимое.
```python
name: str = input("Name: ")
provider_path: str = f"g4f/Provider/{name}.py"

example: str = """
from __future__ import annotations

from aiohttp import ClientSession

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from .helper import format_prompt


class {name}(AsyncGeneratorProvider, ProviderModelMixin):
    label = ""
    url = "https://example.com"
    api_endpoint = "https://example.com/api/completion"
    working = True
    needs_auth = False
    supports_stream = True
    supports_system_message = True
    supports_message_history = True
    
    default_model = ''
    models = ['', '']
    
    model_aliases = {
        "alias1": "model1",
    }

   @classmethod
    def get_model(cls, model: str) -> str:
        if model in cls.models:
            return model
        elif model in cls.model_aliases:
            return cls.model_aliases[model]
        else:
            return cls.default_model

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        model = cls.get_model(model)
        
        headers = {{
            "authority": "example.com",
            "accept": "application/json",
            "origin": cls.url,
            "referer": f"{{cls.url}}/chat",
        }}
        async with ClientSession(headers=headers) as session:
            prompt = format_prompt(messages)
            data = {{
                "prompt": prompt,
                "model": model,
            }}
            async with session.post(f"{{cls.url}}/api/chat", json=data, proxy=proxy) as response:
                response.raise_for_status()
                async for chunk in response.content:
                    if chunk:
                        yield chunk.decode()
"""

if not path.isfile(provider_path):
    command: str = input_command()

    prompt: str = f"""
Create a provider from a cURL command. The command is:
```bash
{command}
```
A example for a provider:
```python
{example}
```
The name for the provider class:
{name}
Replace "hello" with `format_prompt(messages)`.
And replace "gpt-3.5-turbo" with `model`.
"""

    print("Create code...")
    response: list = []
    for chunk in g4f.ChatCompletion.create(
        model=g4f.models.gpt_4o,
        messages=[{"role": "user", "content": prompt}],
        timeout=300,
        stream=True,
    ):
        print(chunk, end="", flush=True)
        response.append(chunk)
    print()
    response: str = "".join(response)

    if code := read_code(response):
        with open(provider_path, "w") as file:
            file.write(code)
        print("Saved at:", provider_path)
        with open("g4f/Provider/__init__.py", "a") as file:
            file.write(f"\nfrom .{name} import {name}")
else:
    with open(provider_path, "r") as file:
        code: str = file.read()