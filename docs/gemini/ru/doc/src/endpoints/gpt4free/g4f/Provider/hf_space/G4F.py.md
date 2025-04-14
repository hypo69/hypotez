# Модуль `G4F`

## Обзор

Модуль предоставляет класс `G4F`, который является частью фреймворка G4F и предназначен для взаимодействия с моделями, размещенными на платформе Hugging Face Spaces. В частности, класс поддерживает модели `flux` и `DeepseekAI_JanusPro7b` для генерации изображений. Он обеспечивает асинхронный способ создания изображений с использованием API Hugging Face Spaces, включая получение токенов GPU и обработку запросов к API.

## Подробней

Модуль `G4F` расширяет функциональность класса `DeepseekAI_JanusPro7b` и включает поддержку моделей `flux` и `flux-dev`, перенаправляя запросы к классу `FluxDev` для этих моделей. Он также обеспечивает получение токенов GPU для доступа к API и форматирование запросов изображений.

## Классы

### `FluxDev`

**Описание**:
Класс `FluxDev` предоставляет конфигурацию для доступа к модели `FLUX.1-dev` на Hugging Face Spaces.

**Наследует**:
- `BlackForestLabs_Flux1Dev`: Наследует функциональность для взаимодействия с моделями BlackForestLabs.

**Атрибуты**:
- `url` (str): URL Space на Hugging Face, где размещена модель `FLUX.1-dev`.
- `space` (str): Имя Space на Hugging Face.
- `referer` (str): Referer URL для HTTP-запросов.

### `G4F`

**Описание**:
Класс `G4F` предназначен для взаимодействия с моделями G4F framework, размещенными на Hugging Face Spaces.

**Наследует**:
- `DeepseekAI_JanusPro7b`: Наследует функциональность для взаимодействия с моделями DeepseekAI.

**Атрибуты**:
- `label` (str): Метка, идентифицирующая провайдера.
- `space` (str): Имя Space на Hugging Face.
- `url` (str): URL Space на Hugging Face.
- `api_url` (str): URL API для взаимодействия с моделью.
- `url_flux` (str): URL для запросов к модели flux.
- `referer` (str): Referer URL для HTTP-запросов.
- `default_model` (str): Модель по умолчанию (`flux`).
- `model_aliases` (dict): Псевдонимы моделей (например, `flux-schnell` -> `flux`).
- `image_models` (list): Список моделей, поддерживающих генерацию изображений.
- `models` (list): Список всех поддерживаемых моделей.

**Методы**:

- `create_async_generator`: Метод для создания асинхронного генератора для генерации изображений.

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
        """Создает асинхронный генератор для генерации изображений на основе указанной модели.

        Args:
            model (str): Имя модели для генерации изображения.
            messages (Messages): Список сообщений, используемых для формирования запроса.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            prompt (str, optional): Текст запроса для генерации изображения. По умолчанию `None`.
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию `"1:1"`.
            width (int, optional): Ширина изображения в пикселях. По умолчанию `None`.
            height (int, optional): Высота изображения в пикселях. По умолчанию `None`.
            seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
            cookies (dict, optional): Cookie для HTTP-запросов. По умолчанию `None`.
            api_key (str, optional): API-ключ для доступа к сервису. По умолчанию `None`.
            zerogpu_uuid (str, optional): UUID для ZeroGPU. По умолчанию `"[object Object]"`.
            **kwargs: Дополнительные параметры.

        Yields:
            AsyncResult: Частичные результаты генерации изображения, включая статусы и URL изображения.

        Raises:
            Exception: Если происходит ошибка при получении токена GPU или при генерации изображения.

        Как работает функция:
        - Проверяет, является ли модель `flux` или `flux-dev`, и перенаправляет запрос к `FluxDev`, если это так.
        - Если модель не является `flux`, вызывает метод `create_async_generator` родительского класса `DeepseekAI_JanusPro7b`.
        - Форматирует размеры изображения, чтобы они были кратны 8.
        - Формирует `prompt` для генерации изображения на основе предоставленных сообщений, если `prompt` не был предоставлен.
        - Генерирует случайное зерно, если зерно не было предоставлено.
        - Создает полезную нагрузку `payload` для запроса к API.
        - Получает токен GPU, если `api_key` не предоставлен.
        - Отправляет запрос к API и возвращает URL изображения.
        - Асинхронно ожидает завершения задачи генерации изображения и возвращает результаты.

        Внутренние функции:
        - `generate`: Асинхронная функция, которая отправляет запрос к API и возвращает URL изображения.
            ```python
             async def generate():
                """Асинхронная функция, отправляющая запрос к API и возвращающая URL сгенерированного изображения.

                Returns:
                    ImageResponse: Объект `ImageResponse` с URL изображения и альтернативным текстом.

                Raises:
                    Exception: Если возникает ошибка при отправке или обработке HTTP-запроса.

                Как работает внутренняя функция:
                - Отправляет POST-запрос к API с использованием `aiohttp.ClientSession`.
                - Проверяет статус ответа с помощью `raise_for_status`.
                - Извлекает URL изображения из JSON-ответа.
                - Возвращает объект `ImageResponse` с URL изображения и альтернативным текстом.
                """
            ```

        Примеры:
            Пример вызова для модели 'flux':
            ```python
            async for chunk in G4F.create_async_generator(
                model='flux',
                messages=[{'role': 'user', 'content': 'Generate a cat image'}]
            ):
                print(chunk)
            ```

            Пример вызова для модели 'deepseekai':
            ```python
            async for chunk in G4F.create_async_generator(
                model='deepseekai',
                messages=[{'role': 'user', 'content': 'Generate a dog image'}],
                width=512,
                height=512
            ):
                print(chunk)
            ```
        """
```

## Параметры класса

- `label` (str): Метка, идентифицирующая провайдера.
- `space` (str): Имя Space на Hugging Face.
- `url` (str): URL Space на Hugging Face.
- `api_url` (str): URL API для взаимодействия с моделью.
- `url_flux` (str): URL для запросов к модели flux.
- `referer` (str): Referer URL для HTTP-запросов.
- `default_model` (str): Модель по умолчанию (`flux`).
- `model_aliases` (dict): Псевдонимы моделей (например, `flux-schnell` -> `flux`).
- `image_models` (list): Список моделей, поддерживающих генерацию изображений.
- `models` (list): Список всех поддерживаемых моделей.

**Примеры**:

Пример создания экземпляра класса `G4F`:

```python
flux_dev = FluxDev()
g4f = G4F()
```

Пример использования `create_async_generator` для генерации изображения:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.G4F import G4F

async def main():
    async for chunk in G4F.create_async_generator(
        model='flux',
        messages=[{'role': 'user', 'content': 'Generate a cat image'}]
    ):
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())