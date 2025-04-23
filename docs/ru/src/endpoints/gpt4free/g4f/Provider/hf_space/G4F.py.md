# Модуль G4F

## Обзор

Модуль `G4F` предоставляет класс для взаимодействия с фреймворком G4F (Generative Framework) через Hugging Face Spaces. Он поддерживает как текстовую генерацию, так и генерацию изображений, используя различные модели, включая `flux` и `DeepseekAI_JanusPro7b`. Модуль предназначен для интеграции с API G4F и предоставляет удобный интерфейс для создания асинхронных генераторов контента.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для использования в качестве провайдера моделей машинного обучения через интерфейс Hugging Face Spaces. Он включает в себя поддержку как текстовых, так и графических моделей, а также обеспечивает обработку ошибок и управление токенами доступа.

## Классы

### `FluxDev`

**Описание**: Класс `FluxDev` наследует функциональность от `BlackForestLabs_Flux1Dev` и предоставляет специфические параметры для работы с моделью Flux.1-dev.

**Наследует**: `BlackForestLabs_Flux1Dev`

**Атрибуты**:
- `url` (str): URL пространства Hugging Face для Flux.1-dev.
- `space` (str): Имя пространства Hugging Face для Flux.1-dev.
- `referer` (str): Referer URL для запросов к Flux.1-dev.

**Методы**:
- Отсутствуют, использует методы родительского класса.

### `G4F`

**Описание**: Класс `G4F` наследует функциональность от `DeepseekAI_JanusPro7b` и предоставляет методы для взаимодействия с G4F framework, включая генерацию изображений.

**Наследует**: `DeepseekAI_JanusPro7b`

**Атрибуты**:
- `label` (str): Метка для идентификации провайдера "G4F framework".
- `space` (str): Имя пространства Hugging Face для Janus-Pro-7B.
- `url` (str): URL пространства Hugging Face для G4F.
- `api_url` (str): URL API для G4F.
- `url_flux` (str): URL для запуска предсказаний Flux.
- `referer` (str): Referer URL для запросов к API.
- `default_model` (str): Модель по умолчанию ("flux").
- `model_aliases` (dict): Алиасы для моделей (например, "flux-schnell").
- `image_models` (list): Список моделей, поддерживающих генерацию изображений.
- `models` (list): Полный список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для генерации контента.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    prompt: str = None,
    aspect_ratio: str = "1:1",
    width: int = None,
    height: int = None,
    seed: int = None,
    cookies: dict = None,
    api_key: str = None,
    zerogpu_uuid: str = "[object Object]",
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для генерации контента, используя различные модели.

    Args:
        cls (type[G4F]): Ссылка на класс `G4F`.
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для генерации контента.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        prompt (str, optional): Текст запроса для генерации изображения. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
        cookies (dict, optional): Cookies для отправки с запросом. По умолчанию `None`.
        api_key (str, optional): API ключ для доступа к сервису. По умолчанию `None`.
        zerogpu_uuid (str, optional): UUID для zerogpu. По умолчанию "[object Object]".
        **kwargs: Дополнительные параметры.

    Yields:
        AsyncResult: Части контента, генерируемые асинхронно.

    Raises:
        Exception: Если возникает ошибка при генерации контента.
    """
    async def generate():
        """
        Внутренняя функция для выполнения запроса к API и получения изображения.

        Args:
            Отсутствуют.

        Returns:
            ImageResponse: Объект с URL сгенерированного изображения и альтернативным текстом.

        Raises:
            Exception: Если возникает ошибка при выполнении запроса.
        """
    
    # Проверка, используется ли модель "flux" или "flux-dev"
    if model in ("flux", "flux-dev"):
        # Если да, делегируем создание генератора классу FluxDev
        async for chunk in FluxDev.create_async_generator(
            model, messages,
            proxy=proxy,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            width=width,
            height=height,
            seed=seed,
            cookies=cookies,
            api_key=api_key,
            zerogpu_uuid=zerogpu_uuid,
            **kwargs
        ):
            yield chunk # Возвращаем полученные части контента
        return # Завершаем выполнение функции

    # Проверка, не содержит ли имя модели подстроку, указанную в классе
    if cls.default_model not in model:
        # Если нет, вызываем метод create_async_generator родительского класса
        async for chunk in super().create_async_generator(
            model, messages,
            proxy=proxy,
            prompt=prompt,
            seed=seed,
            cookies=cookies,
            api_key=api_key,
            zerogpu_uuid=zerogpu_uuid,
            **kwargs
        ):
            yield chunk # Возвращаем полученные части контента
        return # Завершаем выполнение функции

    # Извлечение имени модели
    model = cls.get_model(model)
    # Убедимся, что ширина и высота кратны 8 и больше 32
    width = max(32, width - (width % 8))
    height = max(32, height - (height % 8))
    # Если prompt не задан, форматируем его из messages
    if prompt is None:
        prompt = format_image_prompt(messages)
    # Если seed не задан, генерируем случайное значение
    if seed is None:
        seed = random.randint(9999, 2**32 - 1)

    # Формируем payload для запроса к API
    payload = {
        "data": [
            prompt,
            seed,
            width,
            height,
            True,
            1
        ],
        "event_data": None,
        "fn_index": 3,
        "session_hash": get_random_string(),
        "trigger_id": 10
    }

    # Асинхронный контекстный менеджер для работы с сессией
    async with ClientSession() as session:
        # Если api_key не задан, получаем zerogpu_uuid и api_key
        if api_key is None:
            yield Reasoning(status="Acquiring GPU Token") # Возвращаем статус
            zerogpu_uuid, api_key = await get_zerogpu_token(cls.space, session, JsonConversation(), cookies) # Получаем токен

        # Формируем заголовки для запроса
        headers = {
            "x-zerogpu-token": api_key,
            "x-zerogpu-uuid": zerogpu_uuid,
        }
        headers = {k: v for k, v in headers.items() if v is not None}

        # Определение внутренней асинхронной функции generate
        async def generate():
            """
            Внутренняя функция для выполнения запроса к API и получения изображения.

            Args:
                Отсутствуют.

            Returns:
                ImageResponse: Объект с URL сгенерированного изображения и альтернативным текстом.

            Raises:
                Exception: Если возникает ошибка при выполнении запроса.
            """
            # Выполняем POST запрос к API
            async with session.post(cls.url_flux, json=payload, proxy=proxy, headers=headers) as response:
                await raise_for_status(response) # Проверяем статус ответа
                response_data = await response.json() # Преобразуем ответ в JSON
                image_url = response_data["data"][0]['url'] # Извлекаем URL изображения
                return ImageResponse(image_url, alt=prompt) # Возвращаем объект ImageResponse

        # Создаем задачу для асинхронного выполнения
        background_tasks = set()
        started = time.time() # Запоминаем время начала генерации
        task = asyncio.create_task(generate()) # Создаем задачу
        background_tasks.add(task) # Добавляем задачу в набор
        task.add_done_callback(background_tasks.discard) # Добавляем callback для удаления задачи из набора после завершения

        # Ожидаем завершения задачи
        while background_tasks:
            yield Reasoning(status=f"Generating {time.time() - started:.2f}s") # Возвращаем статус
            await asyncio.sleep(0.2) # Засыпаем на 0.2 секунды
        
        yield await task # Возвращаем результат задачи
        yield Reasoning(status=f"Finished {time.time() - started:.2f}s") # Возвращаем статус завершения

## Параметры класса

- `label` (str): Метка для идентификации провайдера "G4F framework".
- `space` (str): Имя пространства Hugging Face для Janus-Pro-7B.
- `url` (str): URL пространства Hugging Face для G4F.
- `api_url` (str): URL API для G4F.
- `url_flux` (str): URL для запуска предсказаний Flux.
- `referer` (str): Referer URL для запросов к API.
- `default_model` (str): Модель по умолчанию ("flux").
- `model_aliases` (dict): Алиасы для моделей (например, "flux-schnell").
- `image_models` (list): Список моделей, поддерживающих генерацию изображений.
- `models` (list): Полный список поддерживаемых моделей.

## Примеры

Пример использования класса `G4F` для создания асинхронного генератора:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.G4F import G4F
from src.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Generate a cat image"}]
    async for chunk in G4F.create_async_generator(
        model="flux",
        messages=messages,
        width=512,
        height=512
    ):
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())
```
```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.G4F import G4F
from src.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Нарисуй кошку"}]
    async for chunk in G4F.create_async_generator(
        model="flux",
        messages=messages,
        width=512,
        height=512
    ):
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())
```
```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.G4F import G4F
from src.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Нарисуй кошку"}]
    async for chunk in G4F.create_async_generator(
        model="DeepseekAI_JanusPro7b",
        messages=messages,
        width=512,
        height=512
    ):
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())