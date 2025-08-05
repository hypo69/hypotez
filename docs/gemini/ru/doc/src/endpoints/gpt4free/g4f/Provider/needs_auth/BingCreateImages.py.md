# Модуль BingCreateImages

## Обзор

Модуль `BingCreateImages` предоставляет класс `BingCreateImages`, который реализует асинхронный генератор для создания изображений с использованием сервиса Microsoft Designer в Bing. 

## Подробнее

Класс `BingCreateImages` наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он предоставляет методы для асинхронного генератора изображений, которые возвращают результат в виде объекта `ImageResponse`. Модуль также содержит необходимые настройки для работы с сервисом Bing, включая URL, метки, информацию о необходимости авторизации, поддерживаемые модели и т.д.

## Классы

### `class BingCreateImages`

**Описание**: Класс `BingCreateImages` реализует асинхронный генератор для создания изображений с использованием сервиса Microsoft Designer в Bing. 

**Наследует**:
- `AsyncGeneratorProvider`: Класс, предоставляющий общий механизм асинхронного генератора.
- `ProviderModelMixin`: Класс, который предоставляет информацию о модели.

**Атрибуты**:
- `label` (str): Метка для модели (Microsoft Designer in Bing).
- `url` (str): URL сервиса Bing для создания изображений.
- `working` (bool):  Флаг, указывающий, что модель доступна для использования.
- `needs_auth` (bool):  Флаг, указывающий, что для использования модели требуется авторизация.
- `image_models` (List[str]): Список поддерживаемых моделей для создания изображений.
- `models` (List[str]):  Список поддерживаемых моделей.
- `cookies` (Cookies): Cookies для аутентификации.
- `proxy` (str):  Прокси-сервер для запросов.

**Методы**:
- `__init__(self, cookies: Cookies = None, proxy: str = None, api_key: str = None) -> None`:  Инициализирует объект `BingCreateImages`.

    **Параметры**:
    - `cookies` (Cookies): Cookies для аутентификации (по умолчанию None).
    - `proxy` (str):  Прокси-сервер для запросов (по умолчанию None).
    - `api_key` (str):  Ключ API для аутентификации (по умолчанию None).

- `create_async_generator(cls, model: str, messages: Messages, prompt: str = None, api_key: str = None, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncResult`:  Создает асинхронный генератор для создания изображения.

    **Параметры**:
    - `model` (str): Модель для создания изображения (dall-e-3).
    - `messages` (Messages):  Список сообщений, содержащий информацию для генерации изображения.
    - `prompt` (str):  Текст подсказки для создания изображения (по умолчанию None).
    - `api_key` (str):  Ключ API для аутентификации (по умолчанию None).
    - `cookies` (Cookies):  Cookies для аутентификации (по умолчанию None).
    - `proxy` (str):  Прокси-сервер для запросов (по умолчанию None).
    - `**kwargs`:  Дополнительные аргументы (по умолчанию None).

    **Возвращает**:
    - `AsyncResult`: Асинхронный результат, содержащий информацию о созданном изображении.


- `generate(self, prompt: str) -> ImageResponse`:  Асинхронно генерирует изображение по подсказке.

    **Параметры**:
    - `prompt` (str): Текст подсказки для создания изображения.

    **Возвращает**:
    - `ImageResponse`: Объект, содержащий информацию о созданном изображении, включая URL, подсказку, метаданные и т.д.

    **Вызывает исключения**:
    - `MissingAuthError`: Если отсутствует cookie "_U" для аутентификации.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        prompt: str = None,
        api_key: str = None,
        cookies: Cookies = None,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        session = BingCreateImages(cookies, proxy, api_key)
        yield await session.generate(format_image_prompt(messages, prompt))
```

**Назначение**: Функция создает асинхронный генератор для создания изображения.

**Параметры**:
- `model` (str): Модель для создания изображения (dall-e-3).
- `messages` (Messages): Список сообщений, содержащий информацию для генерации изображения.
- `prompt` (str): Текст подсказки для создания изображения (по умолчанию None).
- `api_key` (str): Ключ API для аутентификации (по умолчанию None).
- `cookies` (Cookies): Cookies для аутентификации (по умолчанию None).
- `proxy` (str): Прокси-сервер для запросов (по умолчанию None).
- `**kwargs`: Дополнительные аргументы (по умолчанию None).

**Возвращает**:
- `AsyncResult`: Асинхронный результат, содержащий информацию о созданном изображении.

**Как работает функция**:
- Создает экземпляр класса `BingCreateImages` с предоставленными параметрами.
- Вызывает метод `generate` объекта `BingCreateImages` для создания изображения по подсказке.
- Возвращает асинхронный результат.

**Примеры**:
```python
>>> async def main():
...     result = await BingCreateImages.create_async_generator(model="dall-e-3", messages=[{"role": "user", "content": "Generate an image of a cat"}])
...     print(result)
>>> asyncio.run(main())
```

### `generate`

```python
    async def generate(self, prompt: str) -> ImageResponse:
        """
        Asynchronously creates a markdown formatted string with images based on the prompt.

        Args:
            prompt (str): Prompt to generate images.

        Returns:
            str: Markdown formatted string with images.
        """
        cookies = self.cookies or get_cookies(".bing.com", False)
        if cookies is None or "_U" not in cookies:
            raise MissingAuthError('Missing "_U" cookie')
        async with create_session(cookies, self.proxy) as session:
            images = await create_images(session, prompt)
            return ImageResponse(images, prompt, {"preview": "{image}?w=200&h=200"} if len(images) > 1 else {})
```

**Назначение**: Функция асинхронно генерирует изображение по подсказке.

**Параметры**:
- `prompt` (str): Текст подсказки для создания изображения.

**Возвращает**:
- `ImageResponse`: Объект, содержащий информацию о созданном изображении, включая URL, подсказку, метаданные и т.д.

**Вызывает исключения**:
- `MissingAuthError`: Если отсутствует cookie "_U" для аутентификации.

**Как работает функция**:
- Извлекает cookies для аутентификации.
- Если cookies не найдены или не содержат "_U", возникает ошибка `MissingAuthError`.
- Создает асинхронную сессию с использованием функции `create_session`.
- Вызывает функцию `create_images` для генерации изображения по подсказке.
- Создает объект `ImageResponse` и возвращает его.

**Примеры**:
```python
>>> async def main():
...     session = BingCreateImages(cookies={" _U": "your_api_key"})
...     result = await session.generate(prompt="Generate an image of a dog")
...     print(result)
>>> asyncio.run(main())