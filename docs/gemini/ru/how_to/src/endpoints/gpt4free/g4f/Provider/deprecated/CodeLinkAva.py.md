### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот блок кода определяет асинхронного провайдера `CodeLinkAva` для взаимодействия с API по генерации текста. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и обрабатывает потоковую передачу данных от API. Провайдер предназначен для использования с моделями, совместимыми с `gpt-3.5-turbo`.

Шаги выполнения
-------------------------
1. **Определение класса `CodeLinkAva`**:
   - Создается класс `CodeLinkAva`, наследуемый от `AsyncGeneratorProvider`.
   - Определяются атрибуты класса: `url` (URL API), `supports_gpt_35_turbo` (поддержка моделей `gpt-3.5-turbo`) и `working` (статус работоспособности провайдера).

2. **Создание асинхронного генератора**:
   - Метод `create_async_generator` создает асинхронный генератор для получения ответов от API.
   - Формируются заголовки запроса, включающие `User-Agent`, `Accept`, `Origin`, `Referer` и другие необходимые параметры.

3. **Выполнение POST-запроса к API**:
   - Используется `aiohttp.ClientSession` для выполнения асинхронного POST-запроса к API (`https://ava-alpha-api.codelink.io/api/chat`).
   - В тело запроса передаются сообщения, температура и флаг потоковой передачи (`stream`).

4. **Обработка потокового ответа**:
   - Асинхронно перебираются строки ответа, полученные от API.
   - Каждая строка декодируется и проверяется на наличие префикса `data: `.
   - Если строка начинается с `data: [DONE]`, обработка завершается.
   - Извлекается содержимое сообщения из JSON-формата (`line["choices"][0]["delta"].get("content")`).
   - Если содержимое присутствует, оно передается через `yield`, делая функцию генератором.

Пример использования
-------------------------

```python
from aiohttp import ClientSession
import json

from ...typing import AsyncGenerator
from ..base_provider import AsyncGeneratorProvider


class CodeLinkAva(AsyncGeneratorProvider):
    url = "https://ava-ai-ef611.web.app"
    supports_gpt_35_turbo = True
    working = False

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: list[dict[str, str]],
        **kwargs
    ) -> AsyncGenerator:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-language": "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3",
            "Origin": cls.url,
            "Referer": f"{cls.url}/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        async with ClientSession(
                headers=headers
            ) as session:
            data = {
                "messages": messages,
                "temperature": 0.6,
                "stream": True,
                **kwargs
            }
            async with session.post("https://ava-alpha-api.codelink.io/api/chat", json=data) as response:
                response.raise_for_status()
                async for line in response.content:
                    line = line.decode()
                    if line.startswith("data: "):\n                        if line.startswith("data: [DONE]"):\n                            break\n                        line = json.loads(line[6:-1])\n
                        content = line["choices"][0]["delta"].get("content")
                        if content:
                            yield content