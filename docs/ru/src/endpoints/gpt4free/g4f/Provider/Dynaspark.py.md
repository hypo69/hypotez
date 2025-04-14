# Модуль Dynaspark

## Обзор

Модуль `Dynaspark` предоставляет асинхронный генератор для взаимодействия с сервисом Dynaspark, который позволяет генерировать ответы на основе предоставленных сообщений и медиафайлов с использованием различных моделей.
Модуль поддерживает как текстовые, так и визуальные модели, такие как `gemini-1.5-flash`.

## Подробней

Модуль `Dynaspark` является реализацией провайдера для g4f (GPT4Free), который позволяет использовать Dynaspark в качестве одного из источников для генерации ответов. Он включает в себя поддержку асинхронных запросов, работы с медиафайлами и выбора различных моделей. Класс `Dynaspark` наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, что обеспечивает поддержку асинхронной генерации и выбора моделей.

## Классы

### `Dynaspark`

**Описание**: Класс `Dynaspark` предоставляет интерфейс для взаимодействия с API Dynaspark.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронной генерации.
- `ProviderModelMixin`: Обеспечивает поддержку выбора моделей.

**Атрибуты**:
- `url` (str): URL сервиса Dynaspark.
- `login_url` (str | None): URL для логина (в данном случае `None`, так как аутентификация не требуется).
- `api_endpoint` (str): URL API для генерации ответов.
- `working` (bool): Флаг, указывающий, что провайдер работает.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (в данном случае `False`).
- `use_nodriver` (bool): Флаг, указывающий, используется ли бездрайверный режим.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-flash`).
- `default_vision_model` (str): Визуальная модель, используемая по умолчанию (`gemini-1.5-flash`).
- `vision_models` (List[str]): Список поддерживаемых визуальных моделей.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

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
    """Создает асинхронный генератор для получения ответов от Dynaspark.

    Args:
        model (str): Название модели для генерации ответа.
        messages (Messages): Список сообщений для передачи в модель.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        media (MediaListType, optional): Список медиафайлов для передачи в модель. По умолчанию `None`.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от Dynaspark.
    """
```

**Как работает функция**:

1. **Определение заголовков**:
   - Функция начинает с определения заголовков HTTP-запроса, которые будут отправлены на сервер Dynaspark.

2. **Создание асинхронной сессии**:
   - Используется `aiohttp.ClientSession` для создания асинхронной сессии, которая позволяет отправлять HTTP-запросы. Сессия создается с заданными заголовками.

3. **Подготовка данных формы**:
   - Создается объект `FormData` из библиотеки `aiohttp` для формирования данных, которые будут отправлены в теле POST-запроса.
   - Добавляются поля `user_input` (сформатированные сообщения) и `ai_model` (выбранная модель).

4. **Обработка медиафайлов**:
   - Если предоставлены медиафайлы, функция извлекает первый файл, преобразует его в байты и добавляет в форму с соответствующим именем, именем файла и типом содержимого.

5. **Отправка POST-запроса и обработка ответа**:
   - Отправляется POST-запрос на `api_endpoint` с данными формы и прокси (если указан).
   - Проверяется статус ответа с помощью `raise_for_status`.
   - Извлекается текст ответа и преобразуется в JSON.
   - Извлекается поле `response` из JSON и возвращается как результат работы генератора.

```
Определение заголовков --> Создание асинхронной сессии
      ↓
Подготовка данных формы
      ↓
Обработка медиафайлов --> Отправка POST-запроса и обработка ответа
      ↓
Извлечение и возврат ответа
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, Optional

async def main():
    model = "gemini-1.5-flash"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Привет!"}]
    proxy: Optional[str] = None
    media: Optional[List[tuple]] = None

    async for response in Dynaspark.create_async_generator(model=model, messages=messages, proxy=proxy, media=media):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
```
```python
# Пример с медиафайлом
import asyncio
from typing import List, Dict, Optional
from io import BytesIO
from PIL import Image

async def main():
    model = "gemini-1.5-flash"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Опиши изображение."}]
    proxy: Optional[str] = None
    
    # Создаем фейковое изображение для примера
    image = Image.new('RGB', (100, 100), color='red')
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()
    
    media: Optional[List[tuple]] = [("image.png", image_bytes)]  # Имя файла и байты

    async for response in Dynaspark.create_async_generator(model=model, messages=messages, proxy=proxy, media=media):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())