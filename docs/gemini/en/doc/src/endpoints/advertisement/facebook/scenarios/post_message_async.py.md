# Модуль src.endpoints.advertisement.facebook.scenarios.post_message_async

## Обзор

Модуль `src.endpoints.advertisement.facebook.scenarios.post_message_async`  предоставляет функции для публикации сообщений в Facebook, связанных с промо-кампаниями на AliExpress. В частности, модуль позволяет отправлять заголовок и описание кампании, а также загружать медиафайлы (изображения или видео) для публикации.

## Детали

Модуль `src.endpoints.advertisement.facebook.scenarios.post_message_async`  использует `Selenium` для взаимодействия с веб-страницей Facebook и `BeautifulSoup` для парсинга HTML-структуры.  Функции модуля, такие как  `post_title()`, `upload_media()`, `update_images_captions()`, `promote_post()`, позволяют автоматизировать процесс создания и публикации сообщений в Facebook, связанных с промо-кампаниями.

## Функции

### `post_title(d: Driver, category: SimpleNamespace) -> bool`

**Назначение**:  Отправляет заголовок и описание кампании в поле сообщения.

**Параметры**:
 - `d` (Driver): Экземпляр драйвера для взаимодействия с веб-страницей.
 - `category` (SimpleNamespace): Объект, содержащий заголовок и описание кампании.

**Возвращает**:
 - `bool`: `True`, если заголовок и описание отправлены успешно, иначе `None`.

**Исключения**:
 - `Exception`: Если возникают ошибки при прокрутке страницы или добавлении сообщения.

**Пример**:

```python
>>> driver = Driver(...)
>>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
>>> post_title(driver, category)
True
```

**Как работает**:
 - Функция выполняет прокрутку веб-страницы, чтобы добраться до поля добавления сообщения.
 - Затем она открывает поле добавления сообщения и вставляет в него заголовок и описание кампании, разделенные точкой с запятой.
 - В случае успеха, функция возвращает `True`.

### `upload_media(d: Driver, products: List[SimpleNamespace], no_video:bool = False) -> bool`

**Назначение**:  Загружает медиафайлы (изображения или видео) в раздел изображений и обновляет подписи к ним.

**Параметры**:
 - `d` (Driver): Экземпляр драйвера для взаимодействия с веб-страницей.
 - `products` (List[SimpleNamespace]): Список объектов, содержащих пути к медиафайлам.
 - `no_video` (bool, optional): Флаг, указывающий, что видео не должно загружаться. По умолчанию `False`.

**Возвращает**:
 - `bool`: `True`, если медиафайлы успешно загружены, иначе `None`.

**Исключения**:
 - `Exception`: Если возникают ошибки при загрузке медиафайлов или обновлении подписей.

**Пример**:

```python
>>> driver = Driver(...)
>>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
>>> await upload_media(driver, products)
True
```

**Как работает**:
 - Функция открывает форму добавления медиафайлов.
 - Затем она итерирует список `products` и загружает каждый медиафайл, используя путь к файлу из объекта `product`.
 - После загрузки медиафайлов функция обновляет подписи к изображениям.

### `update_images_captions(d: Driver, products: List[SimpleNamespace], textarea_list: List[WebElement]) -> None`

**Назначение**:  Асинхронно добавляет описания к загруженным медиафайлам.

**Параметры**:
 - `d` (Driver): Экземпляр драйвера для взаимодействия с веб-страницей.
 - `products` (List[SimpleNamespace]): Список объектов, содержащих подробную информацию о товарах, которая будет использована для обновления описаний.
 - `textarea_list` (List[WebElement]): Список текстовых полей, куда будут добавляться описания.

**Исключения**:
 - `Exception`: Если возникают ошибки при обновлении описаний медиафайлов.

**Как работает**:
 - Функция использует `asyncio.to_thread` для асинхронного выполнения функции `handle_product` для каждого товара из списка `products`.
 - Функция `handle_product` генерирует описание для каждого товара, используя информацию из объекта `product` и  заданные языковые настройки.
 - Затем она отправляет сгенерированное описание в соответствующее текстовое поле.

### `promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video:bool = False) -> bool`

**Назначение**:  Управляет процессом продвижения публикации с заголовком, описанием и медиафайлами.

**Параметры**:
 - `d` (Driver): Экземпляр драйвера для взаимодействия с веб-страницей.
 - `category` (SimpleNamespace): Объект, содержащий заголовок и описание кампании.
 - `products` (List[SimpleNamespace]): Список объектов, содержащих медиафайлы и подробную информацию, которая будет опубликована.
 - `no_video` (bool, optional): Флаг, указывающий, что видео не должно загружаться. По умолчанию `False`.

**Пример**:

```python
>>> driver = Driver(...)
>>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
>>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
>>> await promote_post(driver, category, products)
```

**Как работает**:
 - Функция последовательно вызывает функции `post_title()`, `upload_media()`, а затем выполняет действия, необходимые для публикации сообщения.
 - Она возвращает `True`, если все операции выполнены успешно, иначе `None`.

## Parameter Details

 - `d` (Driver): Экземпляр драйвера `Selenium`, используемый для взаимодействия с веб-страницей. 
 - `category` (SimpleNamespace): Объект, содержащий подробную информацию о кампании, включая заголовок, описание и, возможно, ссылку на страницу кампании.
 - `products` (List[SimpleNamespace]): Список объектов, содержащих информацию о товарах, которые будут использованы в публикации. Каждый объект `SimpleNamespace` может содержать такие атрибуты, как `product_title` (название товара), `original_price` (оригинальная цена), `sale_price` (цена со скидкой), `discount` (скидка), `evaluate_rate` (рейтинг товара), `promotion_link` (ссылка на промо-страницу товара), `tags` (теги товара) и `local_image_path` (путь к изображению товара) или `local_video_path` (путь к видео товара).
 - `no_video` (bool, optional): Флаг, указывающий, что видео не должно загружаться. По умолчанию `False`.

## Examples

**Пример 1:**

```python
from src.endpoints.advertisement.facebook.scenarios.post_message_async import post_title, upload_media, promote_post
from src.webdriver import Driver, Chrome
from src.utils.jjson import j_loads_ns
from src.logger.logger import logger
from types import SimpleNamespace
from pathlib import Path
from src import gs

# Загрузка локатора из файла JSON
locator: SimpleNamespace = j_loads_ns(
    Path(gs.path.src / 'endpoints' / 'advertisement' / 'facebook' / 'locators' / 'post_message.json')
)

# Создание экземпляра драйвера
driver = Driver(Chrome)

# Информация о категории
category = SimpleNamespace(title="Summer Sale", description="Get amazing deals on summer clothes!")

# Информация о товарах
products = [
    SimpleNamespace(
        product_title="Summer Dress",
        original_price="100$",
        sale_price="50$",
        discount="50%",
        local_image_path="path/to/image.jpg",
        language="en"  # или 'ru'
    ),
    SimpleNamespace(
        product_title="Sunglasses",
        original_price="80$",
        sale_price="40$",
        discount="50%",
        local_image_path="path/to/image2.jpg",
        language="en"  # или 'ru'
    )
]

# Опубликование сообщения
try:
    await promote_post(driver, category, products)
    logger.info("Сообщение успешно опубликовано.")
except Exception as ex:
    logger.error("Ошибка при публикации сообщения.", ex, exc_info=True)
```

**Пример 2:**

```python
from src.endpoints.advertisement.facebook.scenarios.post_message_async import post_title, upload_media, promote_post
from src.webdriver import Driver, Chrome
from src.utils.jjson import j_loads_ns
from src.logger.logger import logger
from types import SimpleNamespace
from pathlib import Path
from src import gs

# Загрузка локатора из файла JSON
locator: SimpleNamespace = j_loads_ns(
    Path(gs.path.src / 'endpoints' / 'advertisement' / 'facebook' / 'locators' / 'post_message.json')
)

# Создание экземпляра драйвера
driver = Driver(Chrome)

# Информация о категории
category = SimpleNamespace(title="New Arrivals", description="Check out our latest fashion trends!")

# Информация о товарах
products = [
    SimpleNamespace(
        product_title="Trendy Sneakers",
        original_price="150$",
        sale_price="75$",
        discount="50%",
        local_image_path="path/to/image.jpg",
        language="en"  # или 'ru'
    ),
    SimpleNamespace(
        product_title="Stylish Backpack",
        original_price="100$",
        sale_price="50$",
        discount="50%",
        local_image_path="path/to/image2.jpg",
        language="en"  # или 'ru'
    )
]

# Опубликование сообщения с отключением загрузки видео
try:
    await promote_post(driver, category, products, no_video=True)
    logger.info("Сообщение успешно опубликовано.")
except Exception as ex:
    logger.error("Ошибка при публикации сообщения.", ex, exc_info=True)
```

**Пример 3:**

```python
from src.endpoints.advertisement.facebook.scenarios.post_message_async import post_title, upload_media, promote_post
from src.webdriver import Driver, Chrome
from src.utils.jjson import j_loads_ns
from src.logger.logger import logger
from types import SimpleNamespace
from pathlib import Path
from src import gs

# Загрузка локатора из файла JSON
locator: SimpleNamespace = j_loads_ns(
    Path(gs.path.src / 'endpoints' / 'advertisement' / 'facebook' / 'locators' / 'post_message.json')
)

# Создание экземпляра драйвера
driver = Driver(Chrome)

# Информация о категории
category = SimpleNamespace(title="Hot Deals", description="Don't miss out on these amazing discounts!")

# Информация о товарах (только видео)
products = [
    SimpleNamespace(
        product_title="Summer Vacation Video",
        local_video_path="path/to/video.mp4",
        language="en"  # или 'ru'
    ),
]

# Опубликование сообщения с загрузкой только видео
try:
    await promote_post(driver, category, products, no_video=False)
    logger.info("Сообщение успешно опубликовано.")
except Exception as ex:
    logger.error("Ошибка при публикации сообщения.", ex, exc_info=True)
```