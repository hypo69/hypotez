# Модуль для создания изображений с помощью Bing Image Creator

## Обзор

Данный модуль предоставляет функцию `create_images`, которая позволяет создавать изображения на основе текстового запроса с помощью сервиса Bing Image Creator. 

## Подробней

Модуль `create_images.py` реализует функциональность для создания изображений с помощью сервиса Bing Image Creator. 

## Классы

### `None`

## Функции

### `create_session`

**Назначение**: Создает новый клиентский сеанс (ClientSession) с указанными cookie и заголовками.

**Параметры**:

- `cookies` (Dict[str, str]): Словарь с cookie, которые будут использоваться для сеанса.

**Возвращает**:

- `ClientSession`: Созданный клиентский сеанс.

**Как работает функция**:

- Функция `create_session` создает новый объект `ClientSession` с помощью библиотеки `aiohttp`.
- Она устанавливает заголовки запросов, включая `Accept`, `Accept-Encoding`, `Accept-Language`, `Content-Type`, `Referrer-Policy`, `Referrer`, `Origin`, `User-Agent`, `Sec-Ch-Ua`, `Sec-Ch-Ua-Mobile`, `Sec-Fetch-Dest`, `Sec-Fetch-Mode`, `Sec-Fetch-Site`, `Sec-Fetch-User`, `Upgrade-Insecure-Requests`.
- Если в параметре `cookies` переданы cookie, то функция добавляет их в заголовок `Cookie`.
- Функция возвращает созданный объект `ClientSession`.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.bing.create_images import create_session

# Пример использования функции:
cookies = {"cookie_name1": "cookie_value1", "cookie_name2": "cookie_value2"}
session = create_session(cookies)
```

### `create_images`

**Назначение**: Создает изображения на основе текстового запроса с помощью Bing Image Creator.

**Параметры**:

- `session` (ClientSession): Активный клиентский сеанс.
- `prompt` (str): Текстовый запрос для генерации изображений.
- `timeout` (int): Тайм-аут для запроса (по умолчанию 300 секунд).

**Возвращает**:

- `List[str]`: Список URL-адресов созданных изображений.

**Вызывает исключения**:

- `MissingRequirementsError`: Если отсутствует пакет `beautifulsoup4`.
- `RateLimitError`: Если не осталось монет (coins) для создания изображений.
- `RuntimeError`: Если создание изображения завершилось с ошибкой или тайм-аутом.

**Как работает функция**:

- Функция `create_images` выполняет запрос к сервису Bing Image Creator с текстовым запросом.
- Она проверяет наличие необходимых пакетов (`beautifulsoup4`).
- Если доступны монеты (coins), функция отправляет запрос POST на URL `https://www.bing.com/images/create?q={url_encoded_prompt}&rt=4&FORM=GENCRE` с текстовым запросом в кодировке URL.
- Она проверяет статус ответа и обрабатывает ошибки.
- Если статус ответа 302 (перенаправление), функция отправляет запрос POST на URL `https://www.bing.com/images/create?q={url_encoded_prompt}&rt=3&FORM=GENCRE`.
- Она извлекает ID запроса из URL перенаправления и периодически опрашивает статус генерации изображений, пока процесс не завершится.
- Она обрабатывает ошибки при генерации изображений и возвращает список URL-адресов созданных изображений.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.bing.create_images import create_images

# Пример использования функции:
session = create_session({"cookie_name": "cookie_value"})
images_urls = await create_images(session, "A cat sitting on a chair")
```

### `read_images`

**Назначение**: Извлекает URL-адреса изображений из HTML-содержимого.

**Параметры**:

- `html_content` (str): HTML-содержимое, содержащее URL-адреса изображений.

**Возвращает**:

- `List[str]`: Список URL-адресов изображений.

**Вызывает исключения**:

- `RuntimeError`: Если в HTML-содержимом не найдены изображения или обнаружены некорректные изображения.

**Как работает функция**:

- Функция `read_images` парсит HTML-содержимое с помощью библиотеки `BeautifulSoup`.
- Она ищет теги `img` с классами `mimg` или `gir_mmimg`.
- Она извлекает атрибут `src` из найденных тегов и возвращает список URL-адресов изображений.
- Функция проверяет, не содержатся ли в списке URL-адресов некорректные изображения, и возвращает только корректные адреса.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.bing.create_images import read_images

# Пример использования функции:
html_content = "<html><body><img src='https://example.com/image1.jpg' class='mimg'></body></html>"
images_urls = read_images(html_content)
```

## Параметры модуля

- `BING_URL` (str): Базовый URL сервиса Bing Image Creator.
- `TIMEOUT_LOGIN` (int): Тайм-аут для входа в аккаунт Bing (по умолчанию 1200 секунд).
- `TIMEOUT_IMAGE_CREATION` (int): Тайм-аут для создания изображений (по умолчанию 300 секунд).
- `ERRORS` (List[str]): Список сообщений об ошибках, которые могут возникнуть при создании изображений.
- `BAD_IMAGES` (List[str]): Список URL-адресов изображений, которые считаются некорректными.