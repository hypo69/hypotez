# Модуль `post_message_async`

## Обзор

Модуль `post_message_async` предназначен для автоматизации процесса публикации рекламных сообщений в социальной сети Facebook. Он включает в себя функции для заполнения заголовка и описания поста, загрузки медиафайлов (изображений и видео), добавления подписей к изображениям и публикации поста. Модуль использует Selenium WebDriver для взаимодействия с веб-интерфейсом Facebook и асинхронные функции для оптимизации производительности.

## Подробней

Этот модуль является частью системы автоматизации рекламных кампаний проекта `hypotez`. Он позволяет автоматизировать рутинные операции по созданию и публикации рекламных постов в Facebook, такие как загрузка медиаконтента, добавление текста и настройка параметров публикации. Код модуля разбит на отдельные функции, каждая из которых выполняет определенную задачу в процессе публикации поста.

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
    ...
```

**Назначение**: Отправляет заголовок и описание рекламной кампании в поле сообщения для публикации.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `category` (SimpleNamespace): Объект, содержащий заголовок (`title`) и описание (`description`) кампании.

**Возвращает**:

-   `bool`: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

**Как работает функция**:

1.  Выполняет скролл страницы назад, чтобы убедиться, что все элементы интерфейса доступны.
2.  Открывает окно добавления поста, используя локатор `locator.open_add_post_box`.
3.  Формирует текст сообщения, объединяя заголовок и описание из объекта `category`.
4.  Добавляет сообщение в поле для ввода текста, используя локатор `locator.add_message`.
5.  Возвращает `True` в случае успеха или `None` в случае ошибки на любом из этапов.

**ASCII flowchart**:

```
A - Прокрутка страницы назад
|
B - Открытие окна добавления поста
|
C - Формирование текста сообщения
|
D - Добавление сообщения в поле ввода
|
E
```

Где:

-   `A`: Прокрутка страницы назад для обеспечения видимости элементов.
-   `B`: Открытие окна добавления поста.
-   `C`: Формирование текста сообщения из заголовка и описания.
-   `D`: Добавление сформированного сообщения в поле ввода текста.
-   `E`: Функция завершена.

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Пример использования функции post_title
driver = Driver(browser_name='chrome')  # Инициализация драйвера (пример)
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
result = post_title(driver, category)
print(result)
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
    ...
```

**Назначение**: Загружает медиафайлы (изображения или видео) и обновляет подписи к ним.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `products` (List[SimpleNamespace]): Список продуктов, содержащих пути к медиафайлам. Каждый продукт должен иметь атрибут `local_image_path` (путь к изображению) и опционально `local_video_path` (путь к видео).
-   `no_video` (bool, optional): Определяет, нужно ли загружать видео. По умолчанию `False`.

**Возвращает**:

-   `bool`: `True`, если все медиафайлы были успешно загружены и подписи обновлены, иначе `None`.

**Вызывает исключения**:

-   `Exception`: Если произошла ошибка во время загрузки медиафайла или обновления подписи.

**Как работает функция**:

1.  Открывает форму добавления медиафайлов, используя локатор `locator.open_add_foto_video_form`.
2.  Проверяет, является ли `products` списком. Если нет, преобразует его в список.
3.  Перебирает продукты в списке `products`.
4.  Определяет путь к медиафайлу (видео, если `no_video` равно `False` и видеофайл существует, иначе изображение).
5.  Загружает медиафайл, используя локатор `locator.foto_video_input`.
6.  После загрузки медиафайлов нажимает кнопку редактирования загруженных медиафайлов, используя локатор `locator.edit_uloaded_media_button`.
7.  Получает список текстовых полей для ввода подписей к изображениям, используя локатор `locator.edit_image_properties_textarea`.
8.  Асинхронно обновляет подписи к изображениям, вызывая функцию `update_images_captions`.
9.  Возвращает `True` в случае успеха или `None` в случае ошибки на любом из этапов.

**ASCII flowchart**:

```
A - Открытие формы добавления медиафайлов
|
B - Проверка типа данных products
|
C - Цикл по списку products
|
D - Определение пути к медиафайлу (видео или изображение)
|
E - Загрузка медиафайла
|
F - Нажатие кнопки редактирования загруженных медиафайлов
|
G - Получение списка текстовых полей для подписей
|
H - Асинхронное обновление подписей к изображениям
|
I
```

Где:

-   `A`: Открытие формы добавления медиафайлов.
-   `B`: Проверка, является ли `products` списком.
-   `C`: Цикл по списку продуктов для загрузки медиафайлов.
-   `D`: Определение пути к медиафайлу (видео или изображение).
-   `E`: Загрузка медиафайла с использованием драйвера.
-   `F`: Нажатие кнопки редактирования загруженных медиафайлов.
-   `G`: Получение списка текстовых полей для ввода подписей к изображениям.
-   `H`: Асинхронное обновление подписей к изображениям.
-   `I`: Функция завершена.

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace
import asyncio

# Пример использования функции upload_media
async def main():
    driver = Driver(browser_name='chrome')  # Инициализация драйвера (пример)
    products = [SimpleNamespace(local_image_path="путь/к/изображению1.jpg"), SimpleNamespace(local_image_path="путь/к/изображению2.jpg")]
    result = await upload_media(driver, products)
    print(result)

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
        Exception: If there's an error updating the media captions.
    """
    ...
```

**Назначение**: Асинхронно добавляет описания к загруженным медиафайлам.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `products` (List[SimpleNamespace]): Список продуктов с деталями для обновления подписей.
-   `textarea_list` (List[WebElement]): Список текстовых полей, в которые добавляются подписи.

**Вызывает исключения**:

-   `Exception`: Если произошла ошибка во время обновления подписей к медиафайлам.

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
    ...
```

**Назначение**: Синхронно обрабатывает обновление подписи для одного продукта.

**Параметры**:

-   `product` (SimpleNamespace): Продукт, для которого нужно обновить подпись.
-   `textarea_list` (List[WebElement]): Список текстовых полей, в которые добавляются подписи.
-   `i` (int): Индекс продукта в списке.

**Как работает функция**:

1.  Загружает локализованные единицы текста из файла `translations.json`.
2.  Определяет направление текста (`LTR` или `RTL`) на основе языка продукта.
3.  Формирует сообщение, добавляя детали продукта (название, цены, скидки и т.д.) в зависимости от направления текста.
4.  Отправляет сообщение в соответствующее текстовое поле.

**Как работает функция `update_images_captions`**:

1.  Загружает локализованные единицы текста из файла `translations.json`.
2.  Определяет функцию `handle_product` для обработки каждого продукта.
3.  Перебирает продукты в списке `products`.
4.  Для каждого продукта вызывает функцию `handle_product` в отдельном потоке, используя `asyncio.to_thread`.

**ASCII flowchart**:

```
A - Загрузка локализованных единиц текста
|
B - Цикл по списку products
|
C - Вызов функции handle_product для каждого продукта в отдельном потоке
|
D
```

Где:

-   `A`: Загрузка локализованных единиц текста из файла `translations.json`.
-   `B`: Цикл по списку продуктов для обновления подписей.
-   `C`: Вызов функции `handle_product` для каждого продукта в отдельном потоке.
-   `D`: Функция завершена.

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace
from selenium.webdriver.remote.webelement import WebElement
import asyncio

# Пример использования функции update_images_captions
async def main():
    driver = Driver(browser_name='chrome')  # Инициализация драйвера (пример)
    products = [SimpleNamespace(language="ru", product_title="Название продукта", original_price="100", sale_price="50", discount="50%", evaluate_rate="5 звезд", promotion_link="ссылка", tags="теги")]
    textarea_list = [WebElement(None, None)]  # Заглушка для textarea_list
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
    ...
```

**Назначение**: Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `category` (SimpleNamespace): Объект, содержащий детали категории, используемые для заголовка и описания поста.
-   `products` (List[SimpleNamespace]): Список продуктов, содержащих медиафайлы и детали для публикации.
-   `no_video` (bool, optional): Определяет, нужно ли загружать видео. По умолчанию `False`.

**Как работает функция**:

1.  Вызывает функцию `post_title` для добавления заголовка и описания поста.
2.  Вызывает функцию `upload_media` для загрузки медиафайлов.
3.  Нажимает кнопку завершения редактирования, используя локатор `locator.finish_editing_button`.
4.  Нажимает кнопку публикации, используя локатор `locator.publish`.
5.  Возвращает `True` в случае успеха или `None` в случае ошибки на любом из этапов.

**ASCII flowchart**:

```
A - Вызов функции post_title
|
B - Вызов функции upload_media
|
C - Нажатие кнопки завершения редактирования
|
D - Нажатие кнопки публикации
|
E
```

Где:

-   `A`: Вызов функции `post_title` для добавления заголовка и описания поста.
-   `B`: Вызов функции `upload_media` для загрузки медиафайлов.
-   `C`: Нажатие кнопки завершения редактирования.
-   `D`: Нажатие кнопки публикации.
-   `E`: Функция завершена.

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace
import asyncio

# Пример использования функции promote_post
async def main():
    driver = Driver(browser_name='chrome')  # Инициализация драйвера (пример)
    category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
    products = [SimpleNamespace(local_image_path="путь/к/изображению1.jpg")]
    result = await promote_post(driver, category, products)
    print(result)

asyncio.run(main())