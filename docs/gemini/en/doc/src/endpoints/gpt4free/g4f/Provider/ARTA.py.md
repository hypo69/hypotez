# src/endpoints/gpt4free/g4f/Provider/ARTA.py

## Обзор

Файл содержит класс `ARTA`, который является асинхронным генератором изображений. Класс предоставляет возможность генерации изображений на основе текстовых запросов, используя API сервиса ARTA. Поддерживается выбор различных стилей для генерации изображений.

## Более детально

Этот код используется для интеграции с сервисом ARTA, позволяющим генерировать изображения на основе текстовых запросов. Он включает в себя механизмы аутентификации, запроса на генерацию изображений и проверки статуса генерации. Код поддерживает выбор различных моделей (стилей) для генерации изображений.

## Классы

### `ARTA`

**Описание**: Класс `ARTA` является асинхронным провайдером и предоставляет методы для генерации изображений на основе текстовых запросов с использованием API сервиса ARTA.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL сервиса ARTA.
- `auth_url` (str): URL для аутентификации.
- `token_refresh_url` (str): URL для обновления токена.
- `image_generation_url` (str): URL для генерации изображений.
- `status_check_url` (str): URL для проверки статуса генерации изображений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Модель для генерации изображений, используемая по умолчанию.
- `model_aliases` (dict): Словарь, содержащий псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.

**Принцип работы**:
1. **Аутентификация**: Класс использует механизм аутентификации через Google API для получения токена доступа. Токен сохраняется локально и обновляется при необходимости.
2. **Генерация изображений**: На основе текстового запроса и выбранной модели формируется запрос к API ARTA.
3. **Проверка статуса**: После запроса на генерацию, класс периодически проверяет статус генерации изображения.
4. **Возврат результата**: Когда изображение сгенерировано, класс возвращает URL изображения.

### Методы:
- `get_auth_file()`: Возвращает путь к файлу, в котором хранится информация об аутентификации.
- `create_token()`: Создает новый токен аутентификации.
- `refresh_token()`: Обновляет токен аутентификации.
- `read_and_refresh_token()`: Считывает токен из файла и, при необходимости, обновляет его.
- `create_async_generator()`: Создает асинхронный генератор для генерации изображений.

## Методы класса

### `get_auth_file`

```python
    @classmethod
    def get_auth_file(cls):
        """
        Возвращает путь к файлу, в котором хранится информация об аутентификации.
        
        Returns:
            Path: Путь к файлу аутентификации.
        """
```

### `create_token`

```python
    @classmethod
    async def create_token(cls, path: Path, proxy: str | None = None):
        """
        Создает новый токен аутентификации.

        Args:
            path (Path): Путь для сохранения данных аутентификации.
            proxy (str | None, optional): Адрес прокси-сервера. По умолчанию `None`.

        Returns:
            dict: Данные аутентификации.

        Raises:
            ResponseError: Если не удалось получить токен аутентификации.
        """
```

### `refresh_token`

```python
    @classmethod
    async def refresh_token(cls, refresh_token: str, proxy: str = None) -> tuple[str, str]:
        """
        Обновляет токен аутентификации.

        Args:
            refresh_token (str): Токен обновления.
            proxy (str | None, optional): Адрес прокси-сервера. По умолчанию `None`.

        Returns:
            tuple[str, str]: Новый токен и токен обновления.
        """
```

### `read_and_refresh_token`

```python
    @classmethod
    async def read_and_refresh_token(cls, proxy: str | None = None) -> str:
        """
        Считывает токен из файла и, при необходимости, обновляет его.

        Args:
            proxy (str | None, optional): Адрес прокси-сервера. По умолчанию `None`.

        Returns:
            str: Данные аутентификации.
        """
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        prompt: str = None,
        negative_prompt: str = "blurry, deformed hands, ugly",
        n: int = 1,
        guidance_scale: int = 7,
        num_inference_steps: int = 30,
        aspect_ratio: str = "1:1",
        seed: int = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для генерации изображений.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Список сообщений.
            proxy (str | None, optional): Адрес прокси-сервера. По умолчанию `None`.
            prompt (str | None, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
            negative_prompt (str, optional): Негативный запрос, описывающий, что не должно быть на изображении. По умолчанию "blurry, deformed hands, ugly".
            n (int, optional): Количество генерируемых изображений. По умолчанию 1.
            guidance_scale (int, optional): Масштаб соответствия запросу. По умолчанию 7.
            num_inference_steps (int, optional): Количество шагов для генерации изображения. По умолчанию 30.
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
            seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Yields:
            AsyncResult: Результат генерации изображения.

        Raises:
            ResponseError: Если не удалось инициировать генерацию изображения или произошла ошибка в процессе генерации.

        Как работает функция:
        1. Функция получает параметры для генерации изображения, такие как модель, текстовый запрос, негативный запрос, количество изображений, масштаб соответствия запросу, количество шагов для генерации изображения, соотношение сторон и зерно для генерации случайных чисел.
        2. Функция получает токен аутентификации, используя метод `read_and_refresh_token`.
        3. Функция формирует запрос к API ARTA для генерации изображения, передавая в запросе токен аутентификации и параметры генерации изображения.
        4. Функция проверяет статус генерации изображения, периодически опрашивая API ARTA.
        5. Если статус генерации изображения равен "DONE", функция извлекает URL изображения из ответа API ARTA и возвращает URL изображения.
        6. Если статус генерации изображения равен "IN_QUEUE" или "IN_PROGRESS", функция ожидает некоторое время и повторяет проверку статуса.
        7. Если статус генерации изображения не равен "DONE", "IN_QUEUE" или "IN_PROGRESS", функция вызывает исключение `ResponseError`.

        Внутренние функции:
        - Отсутствуют.
        """
```
## Параметры класса

- `url` (str): URL сервиса ARTA.
- `auth_url` (str): URL для аутентификации.
- `token_refresh_url` (str): URL для обновления токена.
- `image_generation_url` (str): URL для генерации изображений.
- `status_check_url` (str): URL для проверки статуса генерации изображений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Модель для генерации изображений, используемая по умолчанию.
- `model_aliases` (dict): Словарь, содержащий псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.

## Примеры

### Использование `get_auth_file`
```python
path = ARTA.get_auth_file()
print(path)
```

### Использование `create_token`
```python
import asyncio
from pathlib import Path

async def main():
    path = Path("auth_arta.json")
    auth_data = await ARTA.create_token(path)
    print(auth_data)

if __name__ == "__main__":
    asyncio.run(main())
```

### Использование `refresh_token`
```python
import asyncio

async def main():
    refresh_token = "<refresh_token>" #  токен обновления
    new_token, new_refresh_token = await ARTA.refresh_token(refresh_token)
    print(f"New token: {new_token}, New refresh token: {new_refresh_token}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Использование `read_and_refresh_token`
```python
import asyncio

async def main():
    auth_data = await ARTA.read_and_refresh_token()
    print(auth_data)

if __name__ == "__main__":
    asyncio.run(main())
```

### Использование `create_async_generator`
```python
import asyncio

async def main():
    async for result in ARTA.create_async_generator(
        model="Flux",
        messages=[{"role": "user", "content": "Generate a futuristic city"}]
    ):
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```