# Модуль для создания изображений через Bing

## Обзор

Этот модуль содержит функции для создания изображений на основе текстового запроса с использованием сервиса Bing Image Creator. Он включает в себя функции для создания сессии, отправки запроса на генерацию изображений, опроса состояния задачи и извлечения URL-адресов готовых изображений.

## Подробнее

Модуль взаимодействует с Bing Image Creator для генерации изображений на основе текстовых запросов. Он использует `aiohttp` для асинхронных HTTP-запросов и `BeautifulSoup` для извлечения данных из HTML-ответов. Модуль обрабатывает ошибки, такие как ограничение скорости, блокировка запросов и другие проблемы, возникающие в процессе создания изображений.

## Функции

### `create_session`

```python
def create_session(cookies: Dict[str, str], proxy: str = None, connector: BaseConnector = None) -> ClientSession:
    """
    Создает новый клиентский сеанс с указанными файлами cookie и заголовками.

    Args:
        cookies (Dict[str, str]): Файлы cookie, которые будут использоваться для сеанса.
        proxy (str, optional): Прокси-сервер для использования в сеансе. По умолчанию `None`.
        connector (BaseConnector, optional): Пользовательский коннектор для сеанса. По умолчанию `None`.

    Returns:
        ClientSession: Созданный клиентский сеанс.
    """
```

**Как работает функция**:
 1. Функция `create_session` создает клиентскую сессию `aiohttp.ClientSession` с заданными заголовками и опциональными cookies, прокси и коннектором.
 2. Заголовки включают информацию о браузере, типе контента и политике referrer.
 3. Если предоставлены cookies, они добавляются в заголовок `Cookie`.
 4. Функция использует `get_connector` для создания или получения коннектора с поддержкой прокси, если это необходимо.

```
Создание заголовков --> Добавление Cookies --> Создание сессии
```

**Примеры**:

```python
import aiohttp

# Пример создания сессии без cookies и прокси
session = create_session(cookies={})

# Пример создания сессии с cookies и прокси
session = create_session(cookies={'cookie1': 'value1', 'cookie2': 'value2'}, proxy='http://proxy.example.com')
```

### `create_images`

```python
async def create_images(session: ClientSession, prompt: str, timeout: int = TIMEOUT_IMAGE_CREATION) -> List[str]:
    """
    Создает изображения на основе заданного запроса с использованием сервиса Bing.

    Args:
        session (ClientSession): Активная клиентская сессия.
        prompt (str): Запрос для генерации изображений.
        timeout (int): Время ожидания для запроса.

    Returns:
        List[str]: Список URL-адресов созданных изображений.

    Raises:
        MissingRequirementsError: Если отсутствует пакет `beautifulsoup4`.
        RateLimitError: Если закончились монеты для создания изображений.
        RuntimeError: Если не удалось создать изображения или истекло время ожидания.
    """
```

**Как работает функция**:

 1. Функция `create_images` генерирует изображения на основе заданного текстового запроса, используя сервис Bing Image Creator.
 2. Проверяет наличие необходимых пакетов (`beautifulsoup4`).
 3. Кодирует запрос в URL-формат.
 4. Отправляет POST-запрос к Bing для создания изображений.
 5. Проверяет наличие ошибок, таких как ограничение скорости или блокировка запроса.
 6. Отправляет GET-запросы для опроса состояния задачи генерации изображений.
 7. Извлекает URL-адреса изображений из HTML-ответа.
 8. Обрабатывает возможные ошибки и возвращает список URL-адресов изображений.

```
Проверка требований --> Кодирование запроса --> POST запрос --> Проверка ошибок --> Опрос состояния --> Извлечение URL
```

**Примеры**:

```python
import asyncio
from aiohttp import ClientSession

async def main():
    async with ClientSession() as session:
        prompt = "A futuristic cityscape"
        try:
            image_urls = await create_images(session, prompt)
            print("Image URLs:", image_urls)
        except Exception as ex:
            print("Error:", ex)

if __name__ == "__main__":
    asyncio.run(main())
```

### `read_images`

```python
def read_images(html_content: str) -> List[str]:
    """
    Извлекает URL-адреса изображений из HTML-контента.

    Args:
        html_content (str): HTML-контент, содержащий URL-адреса изображений.

    Returns:
        List[str]: Список URL-адресов изображений.

    Raises:
        RuntimeError: Если не удалось найти изображения.
    """
```

**Как работает функция**:

 1. Функция `read_images` извлекает URL-адреса изображений из предоставленного HTML-контента.
 2. Использует `BeautifulSoup` для парсинга HTML.
 3. Находит все теги `img` с классами `mimg` или `gir_mmimg`.
 4. Извлекает атрибут `src` из каждого тега `img` и удаляет параметры ширины (`?w=`).
 5. Проверяет, не содержатся ли URL-адреса в списке плохих изображений.
 6. Возвращает список URL-адресов изображений.

```
Парсинг HTML --> Поиск тегов IMG --> Извлечение SRC --> Проверка плохих URL --> Возврат URL
```

**Примеры**:

```python
html_content = """
<img class="mimg" src="https://example.com/image1.jpg?w=300">
<img class="gir_mmimg" src="https://example.com/image2.jpg?w=300">
"""
image_urls = read_images(html_content)
print("Image URLs:", image_urls)  # Вывод: ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']