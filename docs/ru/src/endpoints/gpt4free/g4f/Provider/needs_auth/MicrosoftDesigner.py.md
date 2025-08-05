# Модуль `MicrosoftDesigner`

## Обзор

Модуль `MicrosoftDesigner` предоставляет асинхронный интерфейс для генерации изображений с использованием сервиса Microsoft Designer. Он включает в себя функциональность для получения токена доступа и user-agent, необходимые для аутентификации и выполнения запросов к API Microsoft Designer. Модуль поддерживает различные размеры изображений и позволяет использовать прокси для доступа к сервису.

## Подробнее

Модуль использует асинхронные запросы (`aiohttp`) для взаимодействия с API Microsoft Designer. Он обрабатывает аутентификацию, формирование запросов и извлечение сгенерированных изображений. В случае отсутствия валидного HAR-файла, модуль пытается получить токен доступа и user-agent с использованием playwright.

## Классы

### `MicrosoftDesigner`

**Описание**: Класс `MicrosoftDesigner` является основным классом, предоставляющим функциональность для генерации изображений с использованием Microsoft Designer.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Название провайдера ("Microsoft Designer").
- `url` (str): URL сервиса Microsoft Designer ("https://designer.microsoft.com").
- `working` (bool): Указывает, что провайдер в данный момент функционирует (True).
- `use_nodriver` (bool): Указывает, что используется headless-браузер (True).
- `needs_auth` (bool): Указывает, что требуется аутентификация (True).
- `default_image_model` (str): Модель изображения по умолчанию ("dall-e-3").
- `image_models` (List[str]): Список поддерживаемых моделей изображений, включая размеры ("dall-e-3", "1024x1024", "1024x1792", "1792x1024").
- `models` (List[str]): Псевдоним для `image_models`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для генерации изображений.
- `generate`: Генерирует изображение на основе заданного запроса.

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    prompt: str = None,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для генерации изображений.

    Args:
        cls (MicrosoftDesigner): Класс MicrosoftDesigner.
        model (str): Модель для генерации изображений.
        messages (Messages): Сообщения для формирования запроса.
        prompt (str, optional): Дополнительный запрос. По умолчанию None.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию None.
        **kwargs: Дополнительные аргументы.

    Yields:
        ImageResponse: Объект ImageResponse, содержащий сгенерированные изображения.

    
    - Определяет размер изображения на основе выбранной модели.
    - Вызывает метод `generate` для фактической генерации изображения и передает результат в генератор.
    """
    ...
```

#### `generate`

```python
@classmethod
async def generate(cls, prompt: str, image_size: str, proxy: str = None) -> ImageResponse:
    """Генерирует изображение на основе заданного запроса.

    Args:
        cls (MicrosoftDesigner): Класс MicrosoftDesigner.
        prompt (str): Запрос для генерации изображения.
        image_size (str): Размер изображения.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию None.

    Returns:
        ImageResponse: Объект ImageResponse, содержащий сгенерированные изображения.

    Raises:
        NoValidHarFileError: Если не найден валидный HAR-файл.

    
    - Пытается прочитать токен доступа и user-agent из HAR-файла.
    - В случае неудачи, пытается получить токен доступа и user-agent с использованием `get_access_token_and_user_agent`.
    - Вызывает функцию `create_images` для создания изображений на основе полученных данных.
    - Возвращает объект `ImageResponse` с сгенерированными изображениями.
    """
    ...
```

## Функции

### `create_images`

```python
async def create_images(prompt: str, access_token: str, user_agent: str, image_size: str, proxy: str = None, seed: int = None):
    """Создает изображения с использованием API Microsoft Designer.

    Args:
        prompt (str): Запрос для генерации изображения.
        access_token (str): Токен доступа для аутентификации.
        user_agent (str): User-agent для запросов.
        image_size (str): Размер изображения.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию None.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию None.

    Returns:
        list[str]: Список URL сгенерированных изображений.

    
    - Формирует URL запроса к API Microsoft Designer.
    - Создает заголовки запроса, включая токен доступа и user-agent.
    - Формирует данные формы для отправки запроса, включая запрос, размер изображения и другие параметры.
    - Отправляет POST-запрос к API и обрабатывает ответ.
    - Осуществляет опрос API до тех пор, пока не будут получены сгенерированные изображения.
    - Извлекает URL изображений из ответа и возвращает их в виде списка.

    Внутренние функции:
        Отсутствуют.
    """
    ...
```

### `readHAR`

```python
def readHAR(url: str) -> tuple[str, str]:
    """Читает HAR-файл для получения токена доступа и user-agent.

    Args:
        url (str): URL, для которого требуется найти токен доступа.

    Returns:
        tuple[str, str]: Кортеж, содержащий токен доступа и user-agent.

    Raises:
        NoValidHarFileError: Если не найден валидный HAR-файл с токеном доступа.

    
    - Перебирает HAR-файлы, полученные с помощью `get_har_files()`.
    - Читает содержимое каждого файла и пытается извлечь токен доступа и user-agent для заданного URL.
    - Возвращает извлеченные токен доступа и user-agent.

    Внутренние функции:
        Отсутствуют.
    """
    ...
```

### `get_access_token_and_user_agent`

```python
async def get_access_token_and_user_agent(url: str, proxy: str = None):
    """Получает токен доступа и user-agent с использованием playwright.

    Args:
        url (str): URL, для которого требуется получить токен доступа.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию None.

    Returns:
        tuple[str, str]: Кортеж, содержащий токен доступа и user-agent.

    Raises:
        MissingRequirementsError: Если не установлены необходимые зависимости для playwright.

    
    - Запускает headless-браузер с использованием `get_nodriver`.
    - Переходит на заданный URL.
    - Извлекает user-agent из браузера.
    - Извлекает токен доступа из localStorage браузера.
    - Закрывает страницу и браузер.
    - Возвращает извлеченные токен доступа и user-agent.

    Внутренние функции:
        Отсутствуют.
    """
    ...
```

## Примеры

Пример использования `MicrosoftDesigner` для генерации изображения:

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.MicrosoftDesigner import MicrosoftDesigner
from src.logger import logger
import asyncio

async def main():
    try:
        prompt = "A futuristic cityscape"
        image_size = "1024x1024"
        image_response = await MicrosoftDesigner.generate(prompt, image_size)

        if image_response and image_response.images:
            for image_url in image_response.images:
                print(f"Image URL: {image_url}")
        else:
            print("No images generated.")
    except Exception as ex:
        logger.error('Error while generating image', ex, exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())