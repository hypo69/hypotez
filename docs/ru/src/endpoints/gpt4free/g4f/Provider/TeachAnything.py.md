# Модуль `TeachAnything.py`

## Обзор

Модуль предоставляет асинхронный класс `TeachAnything`, который позволяет взаимодействовать с API сервиса teach-anything.com для генерации текста на основе предоставленных сообщений. Класс поддерживает модели `gemini-1.5-pro` и `gemini-1.5-flash`.

## Подробней

Модуль предназначен для интеграции с сервисом TeachAnything, предоставляющим API для генерации контента. Он использует асинхронные запросы для взаимодействия с API и предоставляет удобный интерфейс для отправки запросов и получения результатов.

## Классы

### `TeachAnything`

**Описание**: Класс для взаимодействия с API сервиса teach-anything.com. Позволяет генерировать текст на основе предоставленных сообщений, используя асинхронный подход.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `url` (str): URL сервиса teach-anything.com.
- `api_endpoint` (str): Endpoint API для генерации текста.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).
- `models` (List[str]): Список поддерживаемых моделей (`gemini-1.5-pro`, `gemini-1.5-flash`).

**Принцип работы**:
Класс `TeachAnything` использует асинхронные запросы для отправки данных на API сервиса teach-anything.com и получения сгенерированного текста. Он форматирует запросы, обрабатывает ответы и предоставляет результаты в виде асинхронного генератора.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения сгенерированного текста.
- `_get_headers`: Возвращает словарь с заголовками запроса.

## Методы класса

### `create_async_generator`

```python
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str | None = None,
        **kwargs: Any
    ) -> AsyncResult:
        """Создает асинхронный генератор для получения сгенерированного текста.

        Args:
            model (str): Имя модели для генерации текста.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str | None, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий сгенерированный текст.

        Raises:
            aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP-запроса.

        
        - Функция принимает модель, сообщения и прокси (опционально).
        - Форматирует сообщения в формат, требуемый API.
        - Отправляет POST-запрос к API с использованием `aiohttp.ClientSession`.
        - Получает ответ в виде чанков данных и декодирует их в UTF-8.
        - Возвращает асинхронный генератор, выдающий декодированный текст.
        - Обрабатывает ошибки декодирования и логирует их.

        Примеры:
            >>> async for chunk in TeachAnything.create_async_generator(model='gemini-1.5-pro', messages=[{'role': 'user', 'content': 'Hello'}]):
            ...     print(chunk)
        """
        ...
```

### `_get_headers`

```python
    @staticmethod
    def _get_headers() -> Dict[str, str]:
        """Возвращает словарь с заголовками запроса.

        Returns:
            Dict[str, str]: Словарь с заголовками запроса.

        
        - Функция возвращает словарь с необходимыми HTTP-заголовками для запроса к API.
        - Заголовки включают `accept`, `accept-language`, `content-type`, `user-agent` и другие.

        Примеры:
            >>> TeachAnything._get_headers()
            {'accept': '*/*', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'no-cache', 'content-type': 'application/json', 'dnt': '1', 'origin': 'https://www.teach-anything.com', 'pragma': 'no-cache', 'priority': 'u=1, i', 'referer': 'https://www.teach-anything.com/', 'sec-ch-us': '"Not?A_Brand";v="99", "Chromium";v="130"', 'sec-ch-us-mobile': '?0', 'sec-ch-us-platform': '"Linux"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}
        """
        ...
```