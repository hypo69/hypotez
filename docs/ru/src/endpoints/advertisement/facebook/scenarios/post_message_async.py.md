# Модуль: `src.endpoints.advertisement.facebook.scenarios.post_message_async`

## Обзор

Модуль `post_message_async.py` предназначен для автоматизации процесса публикации рекламных сообщений в Facebook, включая добавление заголовка, описания и медиафайлов (изображений или видео). Он использует библиотеку `selenium` для взаимодействия с веб-интерфейсом Facebook. Модуль содержит функции для загрузки медиафайлов, добавления подписей к изображениям и публикации сообщения.

## Подробней

Модуль предоставляет асинхронные функции для выполнения операций, таких как загрузка медиа и обновление подписей, чтобы повысить производительность и отзывчивость. Он использует локаторы, хранящиеся в JSON файле, для поиска элементов на странице Facebook.

## Функции

### `post_title`

```python
def post_title(d: Driver, category: SimpleNamespace) -> bool:
    """ Sends the title and description of a campaign to the post message box.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        category (SimpleNamespace): The category containing the title and description to be sent.

    Returns:
        bool: `True` if the title and description were sent successfully, otherwise `None`.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> post_title(driver, category)
        True
    """
```

**Назначение**: Отправляет заголовок и описание рекламной кампании в поле для создания сообщения в Facebook.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `category` (SimpleNamespace): Объект, содержащий заголовок (`title`) и описание (`description`) для публикации.

**Возвращает**:

-   `bool`: `True`, если заголовок и описание успешно отправлены, иначе `None`.

**Как работает функция**:

1.  Выполняется прокрутка страницы назад с помощью `d.scroll`, чтобы убедиться, что элемент для ввода сообщения виден.
2.  Открывается окно добавления сообщения с помощью `d.execute_locator(locator.open_add_post_box)`.
3.  Формируется сообщение путем объединения заголовка и описания из объекта `category`.
4.  Сообщение добавляется в поле ввода с помощью `d.execute_locator(locator.add_message, message)`.
5.  В случае успеха возвращается `True`, иначе логируется ошибка и возвращается `None`.

**ASCII flowchart**:

```
A - Прокрутка страницы назад
|
B - Открытие окна добавления сообщения
|
C - Формирование сообщения
|
D - Добавление сообщения в поле ввода
```

Где:

-   `A`: Прокрутка страницы назад.
-   `B`: Открытие окна добавления сообщения.
-   `C`: Формирование сообщения из заголовка и описания.
-   `D`: Добавление сообщения в поле ввода.

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Пример использования функции post_title
driver = Driver(...)  # Инициализация драйвера
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
result = post_title(driver, category)
print(result)  # Вывод: True или None в случае ошибки
```

### `upload_media`

```python
async def upload_media(d: Driver, products: List[SimpleNamespace], no_video:bool = False) -> bool:
    """ Uploads media files to the images section and updates captions.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        products (List[SimpleNamespace]): List of products containing media file paths.

    Returns:
        bool: `True` if media files were uploaded successfully, otherwise `None`.

    Raises:
        Exception: If there is an error during media upload or caption update.

    Examples:
        >>> driver = Driver(...)
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> await upload_media(driver, products)
        True
    """
```

**Назначение**: Загружает медиафайлы (изображения или видео) в секцию изображений и обновляет подписи к ним.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `products` (List[SimpleNamespace]): Список объектов, содержащих пути к медиафайлам. Каждый объект должен иметь атрибут `local_image_path` (путь к изображению) и может иметь `local_video_path` (путь к видео).
-   `no_video` (bool): Если `True`, загрузка видео будет пропущена, даже если `local_video_path` существует. По умолчанию `False`.

**Возвращает**:

-   `bool`: `True`, если медиафайлы успешно загружены, иначе `None`.

**Вызывает исключения**:

-   `Exception`: Если происходит ошибка во время загрузки медиа или обновления подписей.

**Как работает функция**:

1.  Открывается форма добавления медиафайлов с помощью `d.execute_locator(locator.open_add_foto_video_form)`.
2.  Если `products` не является списком, он преобразуется в список.
3.  Перебираются все продукты в списке `products`.
4.  Для каждого продукта определяется путь к медиафайлу: если существует `local_video_path` и `no_video` равно `False`, используется путь к видео, иначе используется путь к изображению.
5.  Медиафайл загружается с использованием `d.execute_locator(locator.foto_video_input, media_path)`.
6.  После загрузки медиа, нажимается кнопка редактирования загруженного медиа с помощью `d.execute_locator(locator.edit_uloaded_media_button)`.
7.  Получается элемент `uploaded_media_frame`, который обрамляет загруженные медиа.
8.  Извлекается список текстовых полей (textarea) для ввода подписей к изображениям.
9.  Асинхронно обновляются подписи к изображениям с использованием функции `update_images_captions`.
10. В случае успеха возвращается `True`, иначе логируется ошибка и возвращается `None`.

**ASCII flowchart**:

```
A - Открытие формы добавления медиа
|
B - Проверка типа products (list)
|
C - Перебор продуктов
|
D - Определение пути к медиафайлу (изображение или видео)
|
E - Загрузка медиафайла
|
F - Нажатие на кнопку редактирования загруженного медиа
|
G - Получение элемента `uploaded_media_frame`
|
H - Извлечение списка текстовых полей (textarea) для ввода подписей к изображениям
|
I - Асинхронное обновление подписей к изображениям
```

Где:

-   `A`: Открытие формы добавления медиа.
-   `B`: Проверка типа `products` (преобразование в список, если необходимо).
-   `C`: Перебор продуктов в списке.
-   `D`: Определение пути к медиафайлу (изображение или видео).
-   `E`: Загрузка медиафайла.
-   `F`: Нажатие на кнопку редактирования загруженного медиа
-   `G`: Получение элемента `uploaded_media_frame`
-   `H`: Извлечение списка текстовых полей (textarea) для ввода подписей к изображениям.
-   `I`: Асинхронное обновление подписей к изображениям.

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace
import asyncio

# Пример использования функции upload_media
driver = Driver(...)  # Инициализация драйвера
products = [SimpleNamespace(local_image_path='путь/к/изображению1.jpg', local_video_path = 'путь/к/видео1.mp4'), SimpleNamespace(local_image_path='путь/к/изображению2.jpg')]
async def main():
    result = await upload_media(driver, products)
    print(result)  # Вывод: True или None в случае ошибки
asyncio.run(main())
```

### `update_images_captions`

```python
async def update_images_captions(d: Driver, products: List[SimpleNamespace], textarea_list: List[WebElement]) -> None:
    """ Adds descriptions to uploaded media files asynchronously.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        products (List[SimpleNamespace]): List of products with details to update.
        textarea_list (List[WebElement]): List of textareas where captions are added.

    Raises:
        Exception: If there\'s an error updating the media captions.
    """
```

**Назначение**: Добавляет описания к загруженным медиафайлам асинхронно.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `products` (List[SimpleNamespace]): Список объектов, содержащих детали продуктов для обновления.
-   `textarea_list` (List[WebElement]): Список текстовых полей, в которые добавляются подписи.

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка при обновлении подписей медиа.

**Внутренние функции**:

#### `handle_product`

```python
def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> None:
    """ Handles the update of media captions for a single product synchronously.

    Args:
        product (SimpleNamespace): The product to update.
        textarea_list (List[WebElement]): List of textareas where captions are added.
        i (int): Index of the product in the list.
    """
```

**Назначение**: Обновляет подпись для одного продукта синхронно.

**Параметры**:

-   `product` (SimpleNamespace): Продукт для обновления.
-   `textarea_list` (List[WebElement]): Список текстовых полей, в которые добавляются подписи.
-   `i` (int): Индекс продукта в списке.

**Как работает функция**:

1.  Определяется направление текста (слева направо или справа налево) на основе языка продукта.
2.  Формируется сообщение, включающее заголовок продукта, оригинальную цену, цену со скидкой, размер скидки, рейтинг и ссылку на акцию.
3.  В зависимости от направления текста, детали продукта добавляются в сообщение в разном порядке.
4.  Сообщение отправляется в соответствующее текстовое поле.

**Как работает функция `update_images_captions`**:

1.  Загружаются локализованные единицы текста из файла `translations.json`.
2.  Перебираются продукты в списке `products`.
3.  Для каждого продукта вызывается функция `handle_product` в отдельном потоке с использованием `asyncio.to_thread`.

**ASCII flowchart**:

```
A - Загрузка локализованных единиц текста
|
B - Перебор продуктов
|
C - Вызов handle_product для каждого продукта в отдельном потоке
```

Где:

-   `A`: Загрузка локализованных единиц текста.
-   `B`: Перебор продуктов в списке.
-   `C`: Вызов `handle_product` для каждого продукта в отдельном потоке.

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace
from selenium.webdriver.remote.webelement import WebElement
import asyncio

# Пример использования функции update_images_captions
driver = Driver(...)  # Инициализация драйвера
products = [SimpleNamespace(product_title='Продукт 1', original_price='100', sale_price='50', discount='50%', evaluate_rate='4.5', promotion_link='link1', tags='tag1', language='ru')]
textarea_list = [WebElement(...), WebElement(...)]  # Список WebElement, представляющих textarea
async def main():
    await update_images_captions(driver, products, textarea_list)
asyncio.run(main())
```

### `promote_post`

```python
async def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video:bool = False) -> bool:
    """ Manages the process of promoting a post with a title, description, and media files.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        category (SimpleNamespace): The category details used for the post title and description.
        products (List[SimpleNamespace]): List of products containing media and details to be posted.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> await promote_post(driver, category, products)
    """
```

**Назначение**: Управляет процессом продвижения поста, включая добавление заголовка, описания и медиафайлов.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `category` (SimpleNamespace): Объект, содержащий заголовок (`title`) и описание (`description`) для публикации.
-   `products` (List[SimpleNamespace]): Список объектов, содержащих пути к медиафайлам и детали продуктов.
-   `no_video` (bool): Если `True`, загрузка видео будет пропущена, даже если `local_video_path` существует. По умолчанию `False`.

**Как работает функция**:

1.  Добавляется заголовок и описание с использованием функции `post_title`.
2.  Загружаются медиафайлы с использованием функции `upload_media`.
3.  Нажимается кнопка завершения редактирования.
4.  Нажимается кнопка публикации.

**ASCII flowchart**:

```
A - Добавление заголовка и описания
|
B - Загрузка медиафайлов
|
C - Нажатие кнопки завершения редактирования
|
D - Нажатие кнопки публикации
```

Где:

-   `A`: Добавление заголовка и описания с использованием `post_title`.
-   `B`: Загрузка медиафайлов с использованием `upload_media`.
-   `C`: Нажатие кнопки завершения редактирования.
-   `D`: Нажатие кнопки публикации.

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace
import asyncio

# Пример использования функции promote_post
driver = Driver(...)  # Инициализация драйвера
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
products = [SimpleNamespace(local_image_path='путь/к/изображению1.jpg')]
async def main():
    await promote_post(driver, category, products)
asyncio.run(main())