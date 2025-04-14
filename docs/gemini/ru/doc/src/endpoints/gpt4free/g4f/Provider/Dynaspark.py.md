# Модуль Dynaspark

## Обзор

Модуль `Dynaspark` предназначен для взаимодействия с сервисом Dynaspark для генерации текстовых ответов и обработки изображений. Он предоставляет асинхронный генератор, который позволяет получать ответы от модели Dynaspark в асинхронном режиме.

## Подробнее

Модуль поддерживает работу с различными моделями, включая `gemini-1.5-flash` и `gemini-2.0-flash`, а также позволяет передавать изображения для обработки. Он использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов и формирует данные запроса в формате `FormData`.

## Классы

### `Dynaspark`

**Описание**: Класс `Dynaspark` является провайдером для работы с сервисом Dynaspark.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `url` (str): URL сервиса Dynaspark.
- `login_url` (Optional[str]): URL для логина (в данном случае `None`).
- `api_endpoint` (str): URL для отправки запросов на генерацию ответов.
- `working` (bool): Флаг, указывающий, что провайдер работает (в данном случае `True`).
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (в данном случае `False`).
- `use_nodriver` (bool): Флаг, указывающий, используется ли драйвер (в данном случае `True`).
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных (в данном случае `True`).
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения (в данном случае `False`).
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений (в данном случае `False`).
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-flash`).
- `default_vision_model` (str): Модель для обработки изображений, используемая по умолчанию (совпадает с `default_model`).
- `vision_models` (List[str]): Список поддерживаемых моделей для обработки изображений.
- `models` (List[str]): Список всех поддерживаемых моделей (в данном случае совпадает с `vision_models`).
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от модели.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        media: MediaListType = None,
        **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для получения ответов от модели Dynaspark.

        Args:
            model (str): Имя модели для генерации ответа.
            messages (Messages): Список сообщений для передачи в модель.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            media (MediaListType, optional): Список медиа-файлов (изображений) для передачи в модель. По умолчанию `None`.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

        Raises:
            Exception: Если возникает ошибка при выполнении запроса к сервису Dynaspark.
        """
```

#### Как работает функция:

1. **Формирование заголовков запроса**:
   - Создаются заголовки HTTP-запроса, включающие `accept`, `accept-language`, `origin`, `referer` и `user-agent`.

2. **Создание асинхронной сессии**:
   - Используется `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов. Сессия создается с заданными заголовками.

3. **Формирование данных формы (FormData)**:
   - Создается объект `FormData` для передачи данных в запросе.
   - Добавляются поля `user_input` (сформатированный промпт из сообщений) и `ai_model` (выбранная модель).
   - Если предоставлены медиа-файлы (изображения), они добавляются в поле `file` формы.

4. **Выполнение POST-запроса**:
   - Выполняется POST-запрос к `cls.api_endpoint` с данными формы и прокси (если указан).
   - Используется `raise_for_status` для проверки статуса ответа.

5. **Обработка ответа**:
   - Получается текстовое содержимое ответа и преобразуется в JSON.
   - Извлекается поле `response` из JSON и возвращается как результат работы генератора.

#### Примеры:

```python
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

from hypotez.src.endpoints.gpt4free.g4f.Provider.Dynaspark import Dynaspark
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages, MediaListType

async def main():
    model = "gemini-1.5-flash"
    messages: Messages = [{"role": "user", "content": "Напиши короткий стих о весне."}]
    proxy = None  # Замените на ваш прокси, если необходимо
    media: MediaListType = None  # Замените на список медиа-файлов, если необходимо

    generator: AsyncGenerator = Dynaspark.create_async_generator(model=model, messages=messages, proxy=proxy, media=media)

    async for response in generator:
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

```python
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

from hypotez.src.endpoints.gpt4free.g4f.Provider.Dynaspark import Dynaspark
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages, MediaListType

async def main():
    model = "gemini-2.0-flash-lite"
    messages: Messages = [{"role": "user", "content": "Опиши осенний лес в нескольких предложениях."}]
    proxy = "http://your_proxy:8080"  # Пример использования прокси
    media: MediaListType = None

    generator: AsyncGenerator = Dynaspark.create_async_generator(model=model, messages=messages, proxy=proxy, media=media)

    async for response in generator:
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
```
```python
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

from hypotez.src.endpoints.gpt4free.g4f.Provider.Dynaspark import Dynaspark
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages, MediaListType
from PIL import Image
import io

async def main():
    model = "gemini-1.5-flash"
    messages: Messages = [{"role": "user", "content": "Что изображено на картинке?"}]
    proxy = None
    
    # Пример изображения (замените на реальный путь к изображению или байты)
    image_path = "path/to/your/image.jpg"
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    media: MediaListType = [(image, "image.jpg")]

    generator: AsyncGenerator = Dynaspark.create_async_generator(model=model, messages=messages, proxy=proxy, media=media)

    async for response in generator:
        print(response)

if __name__ == "__main__":
    asyncio.run(main())