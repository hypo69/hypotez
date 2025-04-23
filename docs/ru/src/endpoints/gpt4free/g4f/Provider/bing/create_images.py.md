# Модуль для создания изображений с использованием Bing Image Creator

## Обзор

Модуль `create_images.py` предназначен для генерации изображений на основе текстового запроса с использованием сервиса Bing Image Creator. Он включает функции для создания сессии с заданными параметрами, запроса на создание изображений и извлечения URL-адресов сгенерированных изображений из HTML-контента.

## Подробнее

Этот модуль предоставляет возможность программно создавать изображения, используя Bing Image Creator. Он обрабатывает создание сессии, отправку запроса на генерацию изображений и извлечение результатов. Модуль также включает обработку ошибок и исключений, таких как ограничения по использованию сервиса и блокировка запросов.

## Функции

### `create_session`

```python
def create_session(cookies: Dict[str, str], proxy: str = None, connector: BaseConnector = None) -> ClientSession:
    """
    Создает новую клиентскую сессию с указанными cookies и заголовками.

    Args:
        cookies (Dict[str, str]): Cookies, используемые для сессии.
        proxy (str, optional): Proxy для подключения. По умолчанию `None`.
        connector (BaseConnector, optional): Connector aiohttp. По умолчанию `None`.

    Returns:
        ClientSession: Созданная клиентская сессия.
    """
```

**Назначение**:
Функция создает и настраивает клиентскую сессию `aiohttp.ClientSession` с заданными заголовками и cookies. Это необходимо для выполнения HTTP-запросов к сервису Bing Image Creator.

**Параметры**:
- `cookies` (Dict[str, str]): Словарь, содержащий cookies для установки в сессии.
- `proxy` (str, optional): Адрес прокси-сервера для использования в сессии. По умолчанию `None`.
- `connector` (BaseConnector, optional): Кастомный коннектор для сессии. По умолчанию `None`.

**Возвращает**:
- `ClientSession`: Объект клиентской сессии `aiohttp.ClientSession` с настроенными заголовками и коннектором.

**Как работает функция**:
1. Определяются HTTP-заголовки, включая User-Agent, Referer и другие необходимые параметры.
2. Если переданы cookies, они добавляются в заголовки.
3. Создается объект `ClientSession` с заданными заголовками и коннектором (если указан).

**Примеры**:

```python
cookies = {'_U': 'value1', '_UR': 'value2'}
session = create_session(cookies=cookies, proxy='http://proxy:8080')
```

### `create_images`

```python
async def create_images(session: ClientSession, prompt: str, timeout: int = TIMEOUT_IMAGE_CREATION) -> List[str]:
    """
    Создает изображения на основе заданного запроса, используя сервис Bing.

    Args:
        session (ClientSession): Активная клиентская сессия.
        prompt (str): Запрос для генерации изображений.
        timeout (int): Время ожидания для запроса. По умолчанию `TIMEOUT_IMAGE_CREATION`.

    Returns:
        List[str]: Список URL-адресов созданных изображений.

    Raises:
        RuntimeError: Если создание изображений завершается неудачей или истекает время ожидания.
        MissingRequirementsError: Если отсутствует библиотека `beautifulsoup4`.
        RateLimitError: Если закончились доступные "coins" для создания изображений.
    """
```

**Назначение**:
Функция отправляет запрос в Bing Image Creator для генерации изображений на основе заданного текстового запроса. Она обрабатывает ответы сервиса, проверяет наличие ошибок и возвращает список URL-адресов сгенерированных изображений.

**Параметры**:
- `session` (ClientSession): Активная клиентская сессия `aiohttp.ClientSession`.
- `prompt` (str): Текстовый запрос для генерации изображений.
- `timeout` (int, optional): Максимальное время ожидания ответа от сервиса в секундах. По умолчанию `TIMEOUT_IMAGE_CREATION`.

**Возвращает**:
- `List[str]`: Список URL-адресов сгенерированных изображений.

**Вызывает исключения**:
- `RuntimeError`: Если происходит ошибка при создании изображений, например, таймаут или ошибка от сервиса.
- `MissingRequirementsError`: Если не установлена библиотека `beautifulsoup4`.
- `RateLimitError`: Если исчерпан лимит запросов (нет доступных "coins").

**Как работает функция**:
1. Проверяет наличие необходимых библиотек (`beautifulsoup4`).
2. Кодирует запрос `prompt` в URL-совместимый формат.
3. Отправляет POST-запрос к Bing Image Creator с закодированным запросом.
4. Проверяет статус ответа и обрабатывает возможные ошибки, такие как отсутствие "coins" или блокировка запроса.
5. Если запрос успешен, извлекает URL перенаправления и отправляет GET-запрос к этому URL.
6. Опрашивает конечную точку API до тех пор, пока не получит список изображений или не истечет время ожидания.
7. Извлекает и возвращает список URL-адресов изображений с помощью функции `read_images`.

**Примеры**:

```python
async def main():
    cookies = {'_U': 'value1', '_UR': 'value2'}
    async with create_session(cookies=cookies) as session:
        try:
            images = await create_images(session, "a cat in space")
            print(images)
        except Exception as ex:
            print(f"Error: {ex}")

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
        RuntimeError: Если не удалось найти изображения или обнаружены "плохие" изображения.
    """
```

**Назначение**:
Функция извлекает URL-адреса изображений из предоставленного HTML-контента, используя библиотеку `BeautifulSoup`.

**Параметры**:
- `html_content` (str): HTML-контент, содержащий URL-адреса изображений.

**Возвращает**:
- `List[str]`: Список URL-адресов изображений, извлеченных из HTML-контента.

**Вызывает исключения**:
- `RuntimeError`: Если не удалось найти изображения или обнаружены "плохие" изображения (содержащиеся в списке `BAD_IMAGES`).

**Как работает функция**:
1. Использует `BeautifulSoup` для парсинга HTML-контента.
2. Ищет все теги `<img>` с классами `mimg` или `gir_mmimg`.
3. Извлекает атрибут `src` из каждого найденного тега `<img>`.
4. Удаляет параметры ширины из URL-адресов изображений.
5. Проверяет, не содержатся ли URL-адреса в списке "плохих" изображений (`BAD_IMAGES`).
6. Возвращает список URL-адресов изображений.

**Примеры**:

```python
html_content = """
<img class="mimg" src="https://example.com/image1.jpg?w=300">
<img class="gir_mmimg" src="https://example.com/image2.jpg?w=300">
"""
images = read_images(html_content)
print(images)  # Вывод: ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']