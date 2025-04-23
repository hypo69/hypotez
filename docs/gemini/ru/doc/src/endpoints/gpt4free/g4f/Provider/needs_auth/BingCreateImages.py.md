# Модуль BingCreateImages

## Обзор

Модуль `BingCreateImages` предоставляет асинхронный интерфейс для генерации изображений с использованием Microsoft Designer в Bing. Он позволяет создавать изображения на основе текстового запроса, используя cookies для аутентификации. Модуль поддерживает прокси и может быть использован для интеграции в другие проекты, требующие генерацию изображений.

## Подробней

Модуль `BingCreateImages` является частью проекта `hypotez` и предназначен для работы с сервисом Microsoft Designer в Bing для генерации изображений. Он использует асинхронный подход для обеспечения неблокирующего выполнения операций. Для аутентификации используются cookies, что позволяет обходить ограничения, связанные с отсутствием API ключа.

## Классы

### `BingCreateImages`

**Описание**: Класс предоставляет методы для асинхронной генерации изображений с использованием Microsoft Designer в Bing.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдеров.

**Атрибуты**:
- `label` (str): Метка провайдера, отображаемая в интерфейсе.
- `url` (str): URL сервиса Bing Images Create.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с провайдером.
- `image_models` (List[str]): Список поддерживаемых моделей генерации изображений.
- `models` (List[str]): Псевдоним для `image_models`.
- `cookies` (Optional[Cookies]): Cookies для аутентификации.
- `proxy` (Optional[str]): Адрес прокси-сервера.
- `api_key` (Optional[str]): API ключ для аутентификации (альтернатива cookies).

**Принцип работы**:
Класс использует cookies для аутентификации в сервисе Bing Images Create и отправляет запросы на генерацию изображений на основе текстового запроса. Он обрабатывает ответы от сервиса и возвращает результат в виде markdown-форматированной строки с изображениями.

### `__init__`

```python
def __init__(self, cookies: Cookies = None, proxy: str = None, api_key: str = None) -> None:
    """
    Инициализирует экземпляр класса `BingCreateImages`.

    Args:
        cookies (Optional[Cookies]): Cookies для аутентификации. По умолчанию `None`.
        proxy (Optional[str]): Адрес прокси-сервера. По умолчанию `None`.
        api_key (Optional[str]): API ключ для аутентификации (альтернатива cookies). По умолчанию `None`.
    """
```

**Назначение**: Инициализация экземпляра класса `BingCreateImages` с параметрами аутентификации и прокси.

**Параметры**:
- `cookies` (Optional[Cookies]): Cookies для аутентификации.
- `proxy` (Optional[str]): Адрес прокси-сервера.
- `api_key` (Optional[str]): API ключ для аутентификации (альтернатива cookies).

**Как работает функция**:
- Функция `__init__` инициализирует экземпляр класса `BingCreateImages`.
- Если передан `api_key`, он добавляется в cookies под ключом `_U`.
- Сохраняет переданные cookies и прокси для использования в последующих запросах.

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
        """
        Создает асинхронный генератор для генерации изображений.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Список сообщений для формирования запроса.
            prompt (str, optional): Текстовый запрос для генерации изображений. По умолчанию `None`.
            api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
            cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий сгенерированные изображения.
        """
```

**Назначение**: Создание асинхронного генератора для генерации изображений.

**Параметры**:
- `model` (str): Модель для генерации изображений.
- `messages` (Messages): Список сообщений для формирования запроса.
- `prompt` (str, optional): Текстовый запрос для генерации изображений. По умолчанию `None`.
- `api_key` (str, optional): API ключ для аутентификации. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Как работает функция**:
- Функция `create_async_generator` создает экземпляр класса `BingCreateImages` и вызывает метод `generate` для генерации изображений.
- Возвращает асинхронный генератор, который возвращает сгенерированные изображения.

### `generate`

```python
    async def generate(self, prompt: str) -> ImageResponse:
        """
        Асинхронно создает markdown-форматированную строку с изображениями на основе запроса.

        Args:
            prompt (str): Текстовый запрос для генерации изображений.

        Returns:
            ImageResponse: Объект `ImageResponse`, содержащий список URL сгенерированных изображений и метаданные.

        Raises:
            MissingAuthError: Если отсутствует cookie "_U".
        """
```

**Назначение**: Асинхронная генерация изображений на основе текстового запроса.

**Параметры**:
- `prompt` (str): Текстовый запрос для генерации изображений.

**Возвращает**:
- `ImageResponse`: Объект `ImageResponse`, содержащий список URL сгенерированных изображений и метаданные.

**Вызывает исключения**:
- `MissingAuthError`: Если отсутствует cookie "_U".

**Как работает функция**:
- Функция `generate` получает cookies из экземпляра класса или из домена ".bing.com".
- Если cookie "_U" отсутствует, вызывается исключение `MissingAuthError`.
- Создается асинхронная сессия с использованием функции `create_session` из модуля `bing.create_images`.
- Вызывается функция `create_images` для генерации изображений на основе текстового запроса.
- Возвращается объект `ImageResponse`, содержащий список URL сгенерированных изображений и метаданные.

**Примеры**:
```python
# Пример использования класса BingCreateImages
from src.endpoints.gpt4free.g4f.Provider.needs_auth.BingCreateImages import BingCreateImages
import asyncio

async def main():
    # Замените на ваши реальные cookies
    cookies = {"_U": "your_bing_u_cookie"}
    prompt = "A futuristic cityscape"
    
    # Создание экземпляра класса BingCreateImages
    bing_create_images = BingCreateImages(cookies=cookies)
    
    # Генерация изображений
    image_response = await bing_create_images.generate(prompt)
    
    # Вывод результатов
    if image_response.images:
        print("Images generated:")
        for image_url in image_response.images:
            print(image_url)
    else:
        print("No images generated.")

if __name__ == "__main__":
    asyncio.run(main())
```