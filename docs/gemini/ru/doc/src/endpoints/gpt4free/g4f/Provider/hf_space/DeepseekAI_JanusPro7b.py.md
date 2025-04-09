# Модуль DeepseekAI_JanusPro7b

## Обзор

Модуль `DeepseekAI_JanusPro7b` предоставляет асинхронный интерфейс для взаимодействия с моделью DeepseekAI Janus-Pro-7B, размещенной на Hugging Face Spaces. Он позволяет генерировать текст и изображения, используя API Hugging Face Spaces, а также поддерживает потоковую передачу данных.

## Подробнее

Модуль предназначен для использования в проектах, требующих взаимодействия с большими языковыми моделями и моделями генерации изображений. Он включает в себя функции для форматирования запросов, обработки ответов и управления сессиями с использованием асинхронного HTTP-клиента.

## Классы

### `DeepseekAI_JanusPro7b`

**Описание**: Класс `DeepseekAI_JanusPro7b` является основным классом, предоставляющим функциональность для взаимодействия с моделью DeepseekAI Janus-Pro-7B. Он наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, что позволяет ему использовать асинхронные генераторы для обработки данных и предоставляет методы для управления моделями.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронных генераторов для потоковой обработки данных.
- `ProviderModelMixin`: Предоставляет методы для управления моделями и их параметрами.

**Атрибуты**:
- `label` (str): Метка провайдера, используемая для идентификации.
- `space` (str): Название пространства на Hugging Face, где размещена модель.
- `url` (str): URL пространства на Hugging Face.
- `api_url` (str): URL API для взаимодействия с моделью.
- `referer` (str): Referer, используемый в HTTP-запросах.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию для генерации текста.
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений.
- `default_vision_model` (str): Модель, используемая по умолчанию для обработки изображений.
- `image_models` (List[str]): Список моделей, поддерживающих генерацию изображений.
- `vision_models` (List[str]): Список моделей, поддерживающих обработку изображений.
- `models` (List[str]): Объединенный список моделей для текста и изображений.

**Методы**:
- `run()`: Выполняет HTTP-запрос к API Hugging Face Spaces.
- `create_async_generator()`: Создает асинхронный генератор для взаимодействия с моделью.

## Функции

### `run`

```python
    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, image: dict = None, seed: int = 0):
        """Выполняет HTTP-запрос к API Hugging Face Spaces.

        Args:
            method (str): HTTP-метод ("post" или "get").
            session (StreamSession): Асинхронная HTTP-сессия.
            prompt (str): Текст запроса.
            conversation (JsonConversation): Объект, содержащий информацию о текущем диалоге.
            image (dict, optional): Информация об изображении. Defaults to None.
            seed (int): Случайное число для воспроизводимости результатов.

        Returns:
            StreamResponse: Ответ от API.
        """
```

**Назначение**: Функция `run` выполняет HTTP-запрос к API Hugging Face Spaces для взаимодействия с моделью DeepseekAI Janus-Pro-7B. Она поддерживает методы POST и GET для отправки текстовых и графических запросов.

**Параметры**:
- `cls`: Ссылка на класс `DeepseekAI_JanusPro7b`.
- `method` (str): HTTP-метод, который будет использоваться для запроса. Может быть "post" для текстовых запросов или "image" для запросов генерации изображений.
- `session` (StreamSession): Асинхронная HTTP-сессия, используемая для отправки запроса.
- `prompt` (str): Текст запроса, который будет отправлен модели.
- `conversation` (JsonConversation): Объект, содержащий информацию о текущем диалоге, такую как идентификаторы сессии и токены.
- `image` (dict, optional): Информация об изображении, которое будет отправлено модели. Используется только для запросов генерации изображений. По умолчанию `None`.
- `seed` (int): Случайное число, используемое для инициализации генератора случайных чисел. Это позволяет воспроизводить результаты запроса. По умолчанию `0`.

**Возвращает**:
- `StreamResponse`: Асинхронный объект ответа, который содержит результат запроса.

**Как работает функция**:

1. **Определение заголовков**: Функция начинает с определения заголовков HTTP-запроса, включая тип контента, токен и UUID.
2. **Выбор метода**: В зависимости от значения параметра `method`, функция выполняет POST-запрос для текстовых или графических запросов или GET-запрос для получения данных.
3. **Формирование данных**: Для POST-запросов формируются данные в формате JSON, содержащие запрос, seed и другие параметры.
4. **Выполнение запроса**: Используется асинхронная HTTP-сессия (`session`) для отправки запроса к API Hugging Face Spaces.
5. **Возврат ответа**: Функция возвращает объект ответа (`StreamResponse`), который может быть использован для дальнейшей обработки.

**ASCII flowchart**:

```
Начало
  ↓
Определение заголовков (headers)
  ↓
Проверка method == "post"
  ├──> True: Формирование JSON данных для POST запроса
  │    ↓
  │    Выполнение POST запроса к API
  │    ↓
  └──> False: Проверка method == "image"
       ├──> True: Формирование JSON данных для запроса image
       │    ↓
       │    Выполнение POST запроса к API image
       │    ↓
       └──> False: Выполнение GET запроса к API
            ↓
            Возврат StreamResponse
            ↓
Конец
```

**Примеры**:

```python
# Пример вызова функции для текстового запроса
import asyncio
from aiohttp import ClientSession
from your_module import StreamSession, JsonConversation  # Замените your_module на фактическое имя модуля

async def main():
    # Создание экземпляра StreamSession (пример)
    async with StreamSession() as session:
        # Пример использования
        conversation = JsonConversation(session_hash="test_session", zerogpu_token="test_token", zerogpu_uuid="test_uuid")
        response = await DeepseekAI_JanusPro7b.run(
            method="post",
            session=session,
            prompt="Hello, how are you?",
            conversation=conversation,
            seed=42
        )
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

```python
# Пример вызова функции для запроса генерации изображений
import asyncio
from aiohttp import ClientSession
from your_module import StreamSession, JsonConversation  # Замените your_module на фактическое имя модуля

async def main():
    async with StreamSession() as session:
        conversation = JsonConversation(session_hash="test_session", zerogpu_token="test_token", zerogpu_uuid="test_uuid")
        response = await DeepseekAI_JanusPro7b.run(
            method="image",
            session=session,
            prompt="A cat sitting on a mat",
            conversation=conversation,
            seed=42
        )
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        media: MediaListType = None,
        prompt: str = None,
        proxy: str = None,
        cookies: Cookies = None,
        api_key: str = None,
        zerogpu_uuid: str = "[object Object]",
        return_conversation: bool = False,
        conversation: JsonConversation = None,
        seed: int = None,
        **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для взаимодействия с моделью.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            media (MediaListType, optional): Список медиафайлов для отправки. Defaults to None.
            prompt (str, optional): Текст запроса. Defaults to None.
            proxy (str, optional): URL прокси-сервера. Defaults to None.
            cookies (Cookies, optional): HTTP куки. Defaults to None.
            api_key (str, optional): API ключ. Defaults to None.
            zerogpu_uuid (str, optional): UUID для zerogpu. Defaults to "[object Object]".
            return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать объект conversation. Defaults to False.
            conversation (JsonConversation, optional): Объект, содержащий информацию о текущем диалоге. Defaults to None.
            seed (int, optional): Случайное число для воспроизводимости результатов. Defaults to None.
            **kwargs: Дополнительные параметры.

        Yields:
            AsyncResult: Результат от API.
        """
```

**Назначение**: Функция `create_async_generator` создает асинхронный генератор для взаимодействия с моделью DeepseekAI Janus-Pro-7B. Она позволяет отправлять текстовые и графические запросы, а также обрабатывать ответы в потоковом режиме.

**Параметры**:
- `cls`: Ссылка на класс `DeepseekAI_JanusPro7b`.
- `model` (str): Название модели, которую необходимо использовать.
- `messages` (Messages): Список сообщений, которые будут отправлены модели.
- `media` (MediaListType, optional): Список медиафайлов (изображений), которые будут отправлены модели. По умолчанию `None`.
- `prompt` (str, optional): Текст запроса, который будет отправлен модели. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера, который будет использоваться для отправки запроса. По умолчанию `None`.
- `cookies` (Cookies, optional): HTTP куки, которые будут отправлены с запросом. По умолчанию `None`.
- `api_key` (str, optional): API ключ, необходимый для аутентификации запроса. По умолчанию `None`.
- `zerogpu_uuid` (str, optional): UUID для zerogpu. По умолчанию `"[object Object]"`.
- `return_conversation` (bool, optional): Флаг, указывающий, нужно ли возвращать объект conversation. По умолчанию `False`.
- `conversation` (JsonConversation, optional): Объект, содержащий информацию о текущем диалоге, такую как идентификаторы сессии и токены. По умолчанию `None`.
- `seed` (int, optional): Случайное число, используемое для инициализации генератора случайных чисел. Это позволяет воспроизводить результаты запроса. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который возвращает результаты от API.

**Как работает функция**:

1. **Определение метода**: Функция начинает с определения метода запроса ("post" или "image") в зависимости от типа запроса (текстовый или графический).
2. **Форматирование запроса**: Если `prompt` не задан, функция форматирует сообщения (`messages`) в текст запроса.
3. **Инициализация seed**: Если `seed` не задан, функция генерирует случайное число.
4. **Создание сессии**: Функция создает асинхронную HTTP-сессию (`StreamSession`) для отправки запроса.
5. **Получение токена**: Если `api_key` не задан, функция получает токен zerogpu.
6. **Создание conversation**: Если `conversation` не задан, функция создает объект `JsonConversation`, содержащий информацию о текущем диалоге.
7. **Загрузка медиафайлов**: Если `media` задан, функция загружает медиафайлы на сервер.
8. **Выполнение запроса**: Функция выполняет HTTP-запрос к API Hugging Face Spaces с использованием метода `run`.
9. **Обработка ответа**: Функция обрабатывает ответ от API в потоковом режиме и возвращает результаты.

**ASCII flowchart**:

```
Начало
  ↓
Определение метода (method)
  ↓
Форматирование запроса (prompt)
  ↓
Инициализация seed
  ↓
Создание StreamSession
  ↓
Получение zerogpu_token (если api_key не задан)
  ↓
Создание JsonConversation (если conversation не задан)
  ↓
Загрузка медиафайлов (если media задан)
  ↓
Выполнение запроса через cls.run()
  ↓
Обработка ответа в потоковом режиме
  ↓
Возврат AsyncResult
  ↓
Конец
```

**Примеры**:

```python
# Пример вызова функции для текстового запроса
import asyncio
from your_module import Messages  # Замените your_module на фактическое имя модуля

async def main():
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for result in DeepseekAI_JanusPro7b.create_async_generator(
        model="janus-pro-7b",
        messages=messages
    ):
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

```python
# Пример вызова функции для запроса генерации изображений
import asyncio
from your_module import Messages  # Замените your_module на фактическое имя модуля

async def main():
    messages = [{"role": "user", "content": "A cat sitting on a mat"}]
    async for result in DeepseekAI_JanusPro7b.create_async_generator(
        model="janus-pro-7b-image",
        messages=messages
    ):
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### `get_zerogpu_token`

```python
async def get_zerogpu_token(space: str, session: StreamSession, conversation: JsonConversation, cookies: Cookies = None):
    """Получает токен zerogpu для доступа к API.

    Args:
        space (str): Название пространства на Hugging Face.
        session (StreamSession): Асинхронная HTTP-сессия.
        conversation (JsonConversation): Объект, содержащий информацию о текущем диалоге.
        cookies (Cookies, optional): HTTP куки. Defaults to None.

    Returns:
        Tuple[str, str]: UUID и токен zerogpu.
    """
```

**Назначение**: Функция `get_zerogpu_token` получает токен zerogpu для доступа к API Hugging Face Spaces.

**Параметры**:
- `space` (str): Название пространства на Hugging Face.
- `session` (StreamSession): Асинхронная HTTP-сессия.
- `conversation` (JsonConversation): Объект, содержащий информацию о текущем диалоге.
- `cookies` (Cookies, optional): HTTP куки. По умолчанию `None`.

**Возвращает**:
- `Tuple[str, str]`: Кортеж, содержащий UUID и токен zerogpu.

**Как работает функция**:

1. **Получение UUID и токена из conversation**: Функция пытается получить UUID и токен zerogpu из объекта `conversation`.
2. **Получение куки**: Если куки не переданы, функция получает их для домена "huggingface.co".
3. **Получение UUID и токена со страницы пространства**: Если UUID не найден в `conversation`, функция отправляет GET-запрос к странице пространства и извлекает UUID и токен из HTML-кода.
4. **Получение токена через API**: Функция отправляет GET-запрос к API Hugging Face Spaces для получения токена.
5. **Возврат UUID и токена**: Функция возвращает UUID и токен zerogpu.

**ASCII flowchart**:

```
Начало
  ↓
Попытка получения UUID и токена из conversation
  ↓
Получение куки (если не переданы)
  ↓
Если UUID не найден в conversation:
  ├──> GET запрос к странице пространства
  │   ↓
  │   Извлечение UUID и токена из HTML-кода
  │   ↓
  └──> Нет действия
  ↓
GET запрос к API для получения токена
  ↓
Возврат UUID и токена
  ↓
Конец
```

**Примеры**:

```python
# Пример вызова функции
import asyncio
from aiohttp import ClientSession
from your_module import StreamSession, JsonConversation  # Замените your_module на фактическое имя модуля

async def main():
    async with StreamSession() as session:
        conversation = JsonConversation(session_hash="test_session", zerogpu_token="test_token", zerogpu_uuid="test_uuid")
        uuid, token = await get_zerogpu_token(
            space="deepseek-ai/Janus-Pro-7B",
            session=session,
            conversation=conversation
        )
        print(f"UUID: {uuid}, Token: {token}")

if __name__ == "__main__":
    asyncio.run(main())