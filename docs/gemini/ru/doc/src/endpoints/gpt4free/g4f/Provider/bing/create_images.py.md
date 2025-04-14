# Модуль для создания изображений с использованием Bing Image Creator

## Обзор

Этот модуль предоставляет функциональность для создания изображений на основе текстового запроса (prompt) с использованием сервиса Bing Image Creator. Он включает функции для установления сессии с Bing, отправки запроса на создание изображений, опроса статуса создания и извлечения URL-адресов созданных изображений из HTML-контента.

## Подробнее

Модуль предназначен для автоматизации процесса создания изображений через Bing Image Creator. Он обрабатывает установление сессии, кодирование запроса, отправку запросов к API Bing, обработку ответов и извлечение ссылок на изображения.

## Функции

### `create_session`

```python
def create_session(cookies: Dict[str, str], proxy: str = None, connector: BaseConnector = None) -> ClientSession:
    """
    Создает новую клиентскую сессию с указанными cookies и заголовками.

    Args:
        cookies (Dict[str, str]): Cookies для использования в сессии.
        proxy (str, optional): Прокси-сервер для использования в сессии. По умолчанию `None`.
        connector (BaseConnector, optional): Connector для использования в сессии. По умолчанию `None`.

    Returns:
        ClientSession: Созданная клиентская сессия.
    """
    ...
```

**Назначение**: Создает и настраивает сессию `ClientSession` с заданными заголовками и cookies для последующего взаимодействия с Bing.

**Параметры**:
- `cookies` (Dict[str, str]): Словарь с cookies, которые будут добавлены в заголовки сессии.
- `proxy` (str, optional): Строка, представляющая адрес прокси-сервера. По умолчанию `None`.
- `connector` (BaseConnector, optional): Объект `BaseConnector` для управления подключением. По умолчанию `None`.

**Возвращает**:
- `ClientSession`: Объект сессии `ClientSession`, настроенный с заданными заголовками и cookies.

**Как работает функция**:
Функция создает словарь `headers` с необходимыми HTTP-заголовками, включая `User-Agent`, `Accept-Language` и другие. Если предоставлены cookies, они добавляются в заголовок `Cookie`. Затем создается объект `ClientSession` с этими заголовками и, если указано, с прокси-сервером.

**Примеры**:
```python
cookies = {'cookie1': 'value1', 'cookie2': 'value2'}
session = create_session(cookies=cookies)
# Сессия будет создана с указанными cookies.

session = create_session(cookies=cookies, proxy='http://proxy.example.com')
# Сессия будет создана с указанными cookies и прокси-сервером.
```

### `create_images`

```python
async def create_images(session: ClientSession, prompt: str, timeout: int = TIMEOUT_IMAGE_CREATION) -> List[str]:
    """
    Создает изображения на основе заданного запроса, используя сервис Bing.

    Args:
        session (ClientSession): Активная клиентская сессия.
        prompt (str): Запрос для генерации изображений.
        timeout (int): Тайм-аут для запроса. По умолчанию `TIMEOUT_IMAGE_CREATION`.

    Returns:
        List[str]: Список URL-адресов созданных изображений.

    Raises:
        MissingRequirementsError: Если отсутствует пакет `beautifulsoup4`.
        RuntimeError: Если не удалось создать изображения или истекло время ожидания.
        RateLimitError: Если закончились "coins" для создания изображений.
    """
    ...
```

**Назначение**: Отправляет запрос к Bing Image Creator для создания изображений на основе заданного текстового запроса.

**Параметры**:
- `session` (ClientSession): Активная сессия `ClientSession`, используемая для отправки запросов.
- `prompt` (str): Текстовый запрос (prompt), на основе которого будут созданы изображения.
- `timeout` (int, optional): Максимальное время ожидания ответа от сервера в секундах. По умолчанию `TIMEOUT_IMAGE_CREATION`.

**Возвращает**:
- `List[str]`: Список URL-адресов созданных изображений.

**Вызывает исключения**:
- `MissingRequirementsError`: Если библиотека `beautifulsoup4` не установлена.
- `RuntimeError`: Если произошла ошибка при создании изображений или истекло время ожидания.
- `RateLimitError`: Если у аккаунта закончились "coins" для создания изображений.

**Как работает функция**:
1. Проверяет наличие необходимых зависимостей (`beautifulsoup4`).
2. Кодирует prompt в URL-совместимый формат.
3. Отправляет POST-запрос к Bing Image Creator с закодированным prompt.
4. Проверяет ответ на наличие ошибок, таких как блокировка prompt или отсутствие доступных "coins".
5. Если запрос успешен, извлекает URL перенаправления и ID запроса.
6. Опрашивает API Bing до тех пор, пока не получит список URL-адресов изображений или не истечет время ожидания.
7. Извлекает и возвращает список URL-адресов изображений.

**Примеры**:
```python
async def main():
    async with ClientSession() as session:
        try:
            image_urls = await create_images(session, "a futuristic cityscape")
            print(image_urls)
        except Exception as ex:
            print(f"Error creating images: {ex}")

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
        RuntimeError: Если не найдены изображения или обнаружены плохие изображения.
    """
    ...
```

**Назначение**: Извлекает URL-адреса изображений из предоставленного HTML-контента, используя BeautifulSoup для парсинга HTML.

**Параметры**:
- `html_content` (str): Строка, содержащая HTML-контент, который необходимо проанализировать.

**Возвращает**:
- `List[str]`: Список URL-адресов изображений, найденных в HTML-контенте.

**Вызывает исключения**:
- `RuntimeError`: Если не найдены изображения или обнаружены "плохие" изображения.

**Как работает функция**:
1. Использует BeautifulSoup для парсинга HTML-контента.
2. Ищет все теги `img` с классами `mimg` или `gir_mmimg`.
3. Извлекает атрибут `src` из каждого найденного тега `img` и удаляет параметры ширины (`?w=`).
4. Проверяет, содержит ли список изображений "плохие" изображения (определенные в `BAD_IMAGES`).
5. Возвращает список URL-адресов изображений.

**Примеры**:
```python
html_content = """
<img class="mimg" src="https://example.com/image1.jpg?w=300">
<img class="gir_mmimg" src="https://example.com/image2.jpg?w=300">
"""
image_urls = read_images(html_content)
print(image_urls)  # Вывод: ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']