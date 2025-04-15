# Модуль для создания провайдера

## Обзор

Этот модуль предназначен для автоматического создания файлов провайдеров на основе cURL-команд, используемых в проекте `g4f` (Generative for free). Он автоматизирует процесс создания нового провайдера, генерируя код Python на основе предоставленной cURL-команды и сохраняя его в соответствующем файле. Также обновляет файл `__init__.py`, чтобы добавить новый провайдер в список доступных.

## Подробней

Модуль выполняет следующие шаги:
1.  Запрашивает у пользователя имя нового провайдера.
2.  Запрашивает cURL-команду для этого провайдера.
3.  Использует `g4f.ChatCompletion` для генерации кода провайдера на основе cURL-команды.
4.  Извлекает код из ответа.
5.  Сохраняет код в файл провайдера и добавляет его в `__init__.py`.

Этот процесс позволяет быстро добавлять новых провайдеров, минимизируя ручную работу и обеспечивая единообразие в структуре кода провайдеров.

## Функции

### `read_code`

```python
def read_code(text: str) -> str | None:
    """
    Извлекает код Python из текстовой строки, содержащей блоки кода, заключенные в тройные обратные кавычки.

    Args:
        text (str): Текст, содержащий код Python, заключенный в блоки ```python ... ``` или ```py ... ```.

    Returns:
        str | None: Извлеченный код Python или None, если код не найден.

    """
```

**Назначение**: Извлечение кода Python из текстового блока, который обычно представляет собой ответ от языковой модели.

**Параметры**:

*   `text` (str): Строка, содержащая текст, из которого нужно извлечь код.

**Возвращает**:

*   `str | None`: Код Python, извлеченный из текста, или `None`, если код не найден.

**Как работает функция**:
Функция использует регулярное выражение для поиска блоков кода, заключенных в тройные обратные кавычки (```) с указанием языка `python` или `py`. Если такой блок найден, функция извлекает код и возвращает его. Если блок кода не найден, функция возвращает `None`.

### `input_command`

```python
def input_command() -> str:
    """
    Позволяет пользователю ввести или вставить cURL команду через стандартный ввод.

    Returns:
        str: Объединенная строка, содержащая введенные команды cURL.
    """
```

**Назначение**: Функция предназначена для считывания многострочного ввода от пользователя, пока не будет достигнут конец файла (EOF). Это позволяет пользователю вставлять или вводить cURL команды, которые могут занимать несколько строк.

**Возвращает**:

*   `str`: Объединенная строка, содержащая введенные команды cURL.

**Как работает функция**:
Функция построчно считывает ввод пользователя, добавляя каждую строку в список `contents`. Процесс продолжается до тех пор, пока пользователь не сигнализирует о конце ввода (например, нажатием Ctrl+D в Unix-подобных системах или Ctrl+Z в Windows). Затем функция объединяет все строки в одну строку, разделяя их символами новой строки, и возвращает результат.

### Основной блок кода

Основной блок кода выполняет следующую последовательность действий:

1.  Запрашивает имя провайдера у пользователя.
2.  Формирует путь к файлу провайдера.
3.  Проверяет, существует ли файл провайдера.
4.  Если файл не существует, запрашивает cURL-команду у пользователя с помощью функции `input_command()`.
5.  Формирует промпт для `g4f.ChatCompletion`, включая cURL-команду и пример кода провайдера.
6.  Вызывает `g4f.ChatCompletion.create` для генерации кода провайдера.
7.  Извлекает код из ответа с помощью функции `read_code()`.
8.  Сохраняет код в файл провайдера.
9.  Добавляет импорт провайдера в файл `g4f/Provider/__init__.py`.
10. Если файл провайдера существует, читает код из файла.

```python
name = input("Name: ")
provider_path = f"g4f/Provider/{name}.py"

example = """
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
    command = input_command()

    prompt = f"""
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
    response = []
    for chunk in g4f.ChatCompletion.create(
        model=g4f.models.gpt_4o,
        messages=[{"role": "user", "content": prompt}],
        timeout=300,
        stream=True,
    ):
        print(chunk, end="", flush=True)
        response.append(chunk)
    print()
    response = "".join(response)

    if code := read_code(response):
        with open(provider_path, "w") as file:
            file.write(code)
        print("Saved at:", provider_path)
        with open("g4f/Provider/__init__.py", "a") as file:
            file.write(f"\nfrom .{name} import {name}")
else:
    with open(provider_path, "r") as file:
        code = file.read()
```

**Переменные**:

*   `name` (str): Имя провайдера, введенное пользователем.
*   `provider_path` (str): Путь к файлу провайдера.
*   `example` (str): Пример кода провайдера, используемый в промпте для `g4f.ChatCompletion`.
*   `command` (str): cURL-команда, введенная пользователем.
*   `prompt` (str): Промпт для `g4f.ChatCompletion`, включающий cURL-команду и пример кода провайдера.
*   `response` (list): Список чанков ответа от `g4f.ChatCompletion`.
*   `code` (str): Код провайдера, извлеченный из ответа.

**Принцип работы**:

1.  Запрашивает у пользователя имя провайдера и формирует путь к файлу провайдера.
2.  Если файл провайдера не существует, запрашивает cURL-команду у пользователя.
3.  Формирует промпт для `g4f.ChatCompletion`, который включает cURL-команду и пример кода провайдера.
4.  Вызывает `g4f.ChatCompletion.create` для генерации кода провайдера.
5.  Извлекает код из ответа.
6.  Сохраняет код в файл провайдера и добавляет импорт провайдера в файл `g4f/Provider/__init__.py`.
7.  Если файл провайдера существует, читает код из файла.

**Примеры**:

Чтобы создать нового провайдера:

1.  Запустите скрипт `create_provider.py`.
2.  Введите имя провайдера, например, "NewProvider".
3.  Вставьте cURL-команду для этого провайдера.
4.  Скрипт сгенерирует код провайдера и сохранит его в файле `g4f/Provider/NewProvider.py`.
5.  Скрипт также добавит импорт провайдера в файл `g4f/Provider/__init__.py`.