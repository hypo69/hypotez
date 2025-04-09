# Модуль для создания изображений с использованием Bing

## Обзор

Модуль `create_images.py` предназначен для создания изображений на основе текстового запроса с использованием сервиса Bing Image Creator. Он включает в себя функции для установления сессии с Bing, отправки запроса на генерацию изображений, проверки статуса запроса и извлечения URL-адресов созданных изображений.

## Подробней

Этот модуль является частью проекта `hypotez` и обеспечивает функциональность создания изображений по текстовому описанию. Он использует библиотеки `aiohttp` для асинхронных HTTP-запросов и `Beautiful Soup` для парсинга HTML-ответов. Модуль обрабатывает ошибки, связанные с лимитами Bing Image Creator, блокировкой запросов и другими проблемами, которые могут возникнуть в процессе создания изображений.

## Функции

### `create_session`

```python
def create_session(cookies: Dict[str, str], proxy: str | None = None, connector: BaseConnector | None = None) -> ClientSession:
    """
    Создает новый клиентский сеанс с указанными cookie и заголовками.

    Args:
        cookies (Dict[str, str]): Cookie, которые будут использованы для сеанса.
        proxy (Optional[str], optional): Proxy-сервер для использования в сессии. По умолчанию `None`.
        connector (Optional[BaseConnector], optional): Aiohttp коннектор. По умолчанию `None`.

    Returns:
        ClientSession: Созданный клиентский сеанс.
    """
    ...
```

**Назначение**:
Функция `create_session` создает и настраивает асинхронную клиентскую сессию `aiohttp.ClientSession` для взаимодействия с сервисом Bing. Она устанавливает необходимые HTTP-заголовки, включая User-Agent, Referer и Cookie (если они предоставлены), а также использует прокси-сервер, если он указан.

**Параметры**:
- `cookies` (Dict[str, str]): Словарь, содержащий cookie для установки в сессии.
- `proxy` (Optional[str], optional): URL прокси-сервера для использования в сессии. По умолчанию `None`.
- `connector` (Optional[BaseConnector], optional): Кастомный коннектор для сессии `aiohttp`. По умолчанию `None`.

**Возвращает**:
- `ClientSession`: Объект `aiohttp.ClientSession`, настроенный с заданными параметрами.

**Как работает функция**:

1. **Определение заголовков**: Функция задает набор HTTP-заголовков, необходимых для взаимодействия с сервисом Bing.
2. **Добавление Cookie**: Если переданы cookie, они добавляются в заголовок "Cookie".
3. **Создание сессии**: Создается объект `aiohttp.ClientSession` с установленными заголовками и, при необходимости, с прокси-сервером.

```mermaid
graph LR
    A[Определение HTTP-заголовков] --> B{Переданы ли Cookie?}
    B -- Да --> C[Добавление Cookie в заголовок]
    B -- Нет --> D[Создание ClientSession с заголовками и прокси (если есть)]
    C --> D
    D --> E(Возврат ClientSession)
```

**Примеры**:

```python
import aiohttp

# Пример использования без прокси и cookie
session = create_session({})
assert isinstance(session, aiohttp.ClientSession)

# Пример использования с cookie
cookies = {"key": "value"}
session = create_session(cookies)
assert isinstance(session, aiohttp.ClientSession)
```

### `create_images`

```python
async def create_images(session: ClientSession, prompt: str, timeout: int = TIMEOUT_IMAGE_CREATION) -> List[str]:
    """
    Создает изображения на основе заданного запроса, используя сервис Bing.

    Args:
        session (ClientSession): Активная клиентская сессия.
        prompt (str): Запрос для генерации изображений.
        timeout (int): Тайм-аут для запроса.

    Returns:
        List[str]: Список URL-адресов созданных изображений.

    Raises:
        RuntimeError: Если создание изображения завершается неудачей или истекает время ожидания.
    """
    ...
```

**Назначение**:
Функция `create_images` асинхронно отправляет запрос в Bing Image Creator для создания изображений на основе заданного текстового запроса (prompt). Она обрабатывает ответы сервиса, проверяет наличие ошибок и извлекает URL-адреса созданных изображений.

**Параметры**:
- `session` (ClientSession): Активная клиентская сессия `aiohttp.ClientSession`.
- `prompt` (str): Текстовый запрос для генерации изображений.
- `timeout` (int, optional): Максимальное время ожидания ответа от сервиса в секундах. По умолчанию `TIMEOUT_IMAGE_CREATION`.

**Возвращает**:
- `List[str]`: Список URL-адресов созданных изображений.

**Вызывает исключения**:
- `MissingRequirementsError`: Если отсутствует библиотека `beautifulsoup4`.
- `RateLimitError`: Если превышен лимит запросов (нет доступных "монет").
- `RuntimeError`: Если создание изображений завершается неудачей или истекает время ожидания.

**Как работает функция**:

1. **Проверка зависимостей**: Проверяется, установлена ли библиотека `beautifulsoup4`. Если нет, вызывается исключение `MissingRequirementsError`.
2. **Кодирование запроса**: Текстовый запрос кодируется в формат URL.
3. **Отправка запроса**: Отправляется POST-запрос к Bing Image Creator с закодированным запросом.
4. **Обработка ответа**:
   - Проверяется наличие ошибок в ответе (например, превышение лимита запросов).
   - Если ошибок нет, извлекается URL для перенаправления.
5. **Опрос сервиса**: Выполняется опрос сервиса по URL перенаправления до тех пор, пока не будут получены URL-адреса изображений или не истечет время ожидания.
6. **Извлечение изображений**: Извлекаются URL-адреса изображений из полученного HTML-контента с помощью функции `read_images`.

```mermaid
graph LR
    A[Проверка зависимостей (beautifulsoup4)] --> B{Библиотека установлена?}
    B -- Нет --> C(Вызов MissingRequirementsError)
    B -- Да --> D[Кодирование запроса (prompt)]
    D --> E[Отправка POST-запроса в Bing Image Creator]
    E --> F[Обработка ответа]
    F --> G{Есть ошибки?}
    G -- Да --> H(Вызов RuntimeError или RateLimitError)
    G -- Нет --> I[Извлечение URL перенаправления]
    I --> J[Опрос сервиса по URL перенаправления]
    J --> K{Получены URL-адреса изображений или истекло время ожидания?}
    K -- Нет --> J
    K -- Да --> L[Извлечение URL-адресов изображений из HTML]
    L --> M(Возврат списка URL-адресов изображений)
```

**Примеры**:

```python
import aiohttp
import asyncio

# Пример использования (требуется активная сессия aiohttp)
async def main():
    async with aiohttp.ClientSession() as session:
        try:
            images = await create_images(session, "A futuristic cityscape")
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
    """
    ...
```

**Назначение**:
Функция `read_images` извлекает URL-адреса изображений из предоставленного HTML-контента, используя библиотеку `Beautiful Soup`. Она находит все теги `img` с определенными классами, извлекает атрибут `src` и возвращает список URL-адресов изображений.

**Параметры**:
- `html_content` (str): HTML-контент, содержащий URL-адреса изображений.

**Возвращает**:
- `List[str]`: Список URL-адресов изображений.

**Вызывает исключения**:
- `RuntimeError`: Если не найдены изображения или найдены "плохие" изображения.

**Как работает функция**:

1. **Парсинг HTML**: HTML-контент парсится с использованием `Beautiful Soup`.
2. **Поиск тегов img**: Выполняется поиск всех тегов `img` с классами `mimg` или `gir_mmimg`.
3. **Извлечение URL**: Извлекаются значения атрибута `src` из найденных тегов `img`.
4. **Проверка изображений**: Проверяется, не содержатся ли "плохие" изображения в списке.
5. **Возврат URL**: Возвращается список URL-адресов изображений.

```mermaid
graph LR
    A[Парсинг HTML с использованием Beautiful Soup] --> B[Поиск тегов img с классами mimg или gir_mmimg]
    B --> C{Теги img найдены?}
    C -- Нет --> D(Вызов RuntimeError - "No images found")
    C -- Да --> E[Извлечение атрибутов src из тегов img]
    E --> F[Проверка на "плохие" изображения]
    F --> G{Найдены "плохие" изображения?}
    G -- Да --> H(Вызов RuntimeError - "Bad images found")
    G -- Нет --> I(Возврат списка URL-адресов изображений)
```

**Примеры**:

```python
# Пример использования
html_content = """
<img class="mimg" src="https://example.com/image1.jpg?w=120">
<img class="gir_mmimg" src="https://example.com/image2.jpg?w=120">
"""
images = read_images(html_content)
print(images)  # Вывод: ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']