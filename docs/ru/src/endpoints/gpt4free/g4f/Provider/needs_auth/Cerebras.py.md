# Модуль для взаимодействия с Cerebras Inference API

## Обзор

Модуль `Cerebras.py` предоставляет класс `Cerebras`, который является подклассом `OpenaiAPI` и предназначен для взаимодействия с Cerebras Inference API. Он позволяет генерировать текст на основе предоставленных сообщений, используя различные модели, предоставляемые Cerebras.

## Подробней

Этот модуль предназначен для использования в проекте `hypotez` для интеграции с Cerebras Inference API. Он обеспечивает асинхронную генерацию текста с использованием моделей Cerebras, таких как `llama3.1-70b`, `llama3.1-8b` и другие. Модуль также обеспечивает получение ключа API из cookies, если он не был предоставлен напрямую. Расположение файла в проекте указывает на то, что он является одним из провайдеров для gpt4free, требующих аутентификации.

## Классы

### `Cerebras`

**Описание**: Класс для взаимодействия с Cerebras Inference API.

**Наследует**:
- `OpenaiAPI`: Класс `Cerebras` наследует функциональность от класса `OpenaiAPI`, предоставляя базовые методы для взаимодействия с API OpenAI.

**Атрибуты**:
- `label` (str): Метка провайдера, в данном случае `"Cerebras Inference"`.
- `url` (str): URL главной страницы Cerebras Inference, `"https://inference.cerebras.ai/"`.
- `login_url` (str): URL страницы входа в Cerebras Cloud, `"https://cloud.cerebras.ai"`.
- `api_base` (str): Базовый URL для Cerebras API, `"https://api.cerebras.ai/v1"`.
- `working` (bool): Указывает, работает ли провайдер, в данном случае `True`.
- `default_model` (str): Модель, используемая по умолчанию, `"llama3.1-70b"`.
- `models` (List[str]): Список поддерживаемых моделей, включая `default_model`, `"llama3.1-8b"`, `"llama-3.3-70b"` и `"deepseek-r1-distill-llama-70b"`.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей, позволяющий использовать более короткие имена для моделей.

**Методы**:
- `create_async_generator()`: Асинхронный генератор для создания запросов к API.

## Функции

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        api_key: str = None,
        cookies: Cookies = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для запросов к Cerebras Inference API.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            api_key (str, optional): API ключ. По умолчанию `None`.
            cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор чанков текста.

        Как работает функция:
        1. **Проверяет наличие API-ключа**:
           - Если `api_key` не предоставлен, пытается получить его из cookies.
        2. **Получение API-ключа из cookies**:
           - Если `cookies` не предоставлены, пытается получить их для домена `.cerebras.ai`.
           - Открывает асинхронную сессию с использованием полученных cookies.
           - Запрашивает API-ключ из `https://inference.cerebras.ai/api/auth/session`.
           - Извлекает `demoApiKey` из JSON ответа, если он существует.
        3. **Создание асинхронного генератора**:
           - Вызывает метод `create_async_generator` родительского класса `OpenaiAPI` с переданными параметрами и дополнительными заголовками.
        4. **Генерация чанков текста**:
           - Итерируется по чанкам текста, полученным от родительского класса, и передает их вызывающей стороне.

        """
        if api_key is None:
            if cookies is None:
                cookies = get_cookies(".cerebras.ai")
            async with ClientSession(cookies=cookies) as session:
                async with session.get("https://inference.cerebras.ai/api/auth/session") as response:
                    await raise_for_status(response)
                    data = await response.json()
                    if data:
                        api_key = data.get("user", {}).get("demoApiKey")
        async for chunk in super().create_async_generator(
            model, messages,
            impersonate="chrome",
            api_key=api_key,
            headers={
                "User-Agent": "ex/JS 1.5.0",
            },
            **kwargs
        ):
            yield chunk
```

**Параметры**:
- `cls` (Type[Cerebras]): Ссылка на класс `Cerebras`.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `api_key` (str, optional): API ключ. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор чанков текста.

```
Проверка наличия API-ключа или получение из cookies
│
├─── Получение API-ключа из cookies (если api_key отсутствует)
│   │
│   ├─── Получение cookies для домена .cerebras.ai (если cookies отсутствуют)
│   │   │
│   ├─── Создание асинхронной сессии с cookies
│   │   │
│   ├─── Запрос API-ключа из https://inference.cerebras.ai/api/auth/session
│   │   │
│   └─── Извлечение demoApiKey из JSON ответа
│
└─── Создание асинхронного генератора через super().create_async_generator
    │
    └─── Генерация чанков текста и передача их вызывающей стороне
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

# Допустим, у вас есть функция для получения сообщений
async def get_messages() -> List[Dict[str, str]]:
    return [{"role": "user", "content": "Hello, Cerebras!"}]

async def main():
    model_name = "llama3.1-70b"
    messages = await get_messages()
    api_key = "your_api_key"  # Замените на ваш API-ключ
    cookies = {}  # Замените на ваши cookies, если необходимо

    async def consume_generator(generator: AsyncGenerator[str, None]) -> None:
        async for chunk in generator:
            print(chunk, end="")

    generator = Cerebras.create_async_generator(model=model_name, messages=messages, api_key=api_key, cookies=cookies)
    
    # Для работы с асинхронным генератором, нужно обернуть его в asyncio.create_task
    task = asyncio.create_task(consume_generator(await generator))
    
    # Ждем завершения задачи
    await task

if __name__ == "__main__":
    asyncio.run(main())