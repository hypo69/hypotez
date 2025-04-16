# Модуль `post_message_async.py`

## Обзор

Модуль `post_message_async.py` предназначен для автоматизации процесса публикации рекламных сообщений в Facebook, включая добавление заголовка, описания и медиафайлов (изображений или видео). Он использует Selenium WebDriver для взаимодействия с веб-интерфейсом Facebook и выполняет операции асинхронно для повышения эффективности.

## Подробнее

Этот модуль является частью системы автоматизации рекламных кампаний и предоставляет функции для загрузки медиаконтента, добавления подписей к изображениям и публикации сообщений на Facebook. Он предназначен для работы в асинхронном режиме, что позволяет одновременно обрабатывать несколько задач и повышает общую производительность системы.

## Классы

В данном модуле классы отсутствуют.

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

**Назначение**: Отправляет заголовок и описание рекламной кампании в поле сообщения.

**Параметры**:
- `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
- `category` (SimpleNamespace): Объект, содержащий заголовок и описание кампании.

**Возвращает**:
- `bool`: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

**Как работает функция**:
1. Выполняется скролл страницы назад.
2. Открывается окно "добавить пост".
3. Формируется сообщение из заголовка и описания категории.
4. Сообщение добавляется в поле для ввода сообщения.

**Примеры**:

```python
driver = Driver(Firefox)  # или другой драйвер
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
result = post_title(driver, category)
print(result)  # Выведет: True или None в случае ошибки
```

### `upload_media`

```python
async def upload_media(d: Driver, products: List[SimpleNamespace], no_video:bool = False) -> bool:
    """ Uploads media files to the images section and updates captions.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        products (List[SimpleNamespace]): List of products containing media file paths.
        no_video (bool): Флаг, указывающий на необходимость исключения видео из загрузки. По умолчанию `False`.

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

**Назначение**: Загружает медиафайлы (изображения или видео) и обновляет подписи к ним.

**Параметры**:
- `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
- `products` (List[SimpleNamespace]): Список объектов, содержащих пути к медиафайлам.
- `no_video` (bool): Флаг, указывающий на необходимость исключения видео из загрузки. По умолчанию `False`.

**Возвращает**:
- `bool`: `True`, если медиафайлы были успешно загружены, иначе `None`.

**Как работает функция**:
1. Открывается форма "добавить медиа".
2. Проверяется, является ли `products` списком.
3. Итерируется по списку продуктов и загружает медиафайлы.
4. Обновляются подписи для загруженных медиафайлов.

**Примеры**:

```python
driver = Driver(Firefox)  # или другой драйвер
products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', local_video_path='путь/к/видео.mp4')]
result = await upload_media(driver, products)
print(result)  # Выведет: True или None в случае ошибки
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
```

**Назначение**: Асинхронно добавляет описания к загруженным медиафайлам.

**Параметры**:
- `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
- `products` (List[SimpleNamespace]): Список объектов, содержащих детали для обновления.
- `textarea_list` (List[WebElement]): Список элементов `<textarea>`, в которые добавляются подписи.

**Как работает функция**:
1. Загружается файл `translations.json` с локализованными единицами.
2. Определяется внутренняя функция `handle_product`, которая обновляет подписи для каждого продукта.
3. Асинхронно обрабатывается каждый продукт, и вызывается `handle_product` для обновления подписей.

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

**Назначение**: Синхронно обрабатывает обновление подписей для одного продукта.

**Параметры**:
- `product` (SimpleNamespace): Объект продукта для обновления.
- `textarea_list` (List[WebElement]): Список элементов `<textarea>`, в которые добавляются подписи.
- `i` (int): Индекс продукта в списке.

**Как работает функция**:
1. Определяется направление текста (LTR или RTL) на основе языка продукта.
2. Формируется сообщение, содержащее детали продукта (название, цены, скидки и т.д.) на основе направления текста.
3. Отправляется сообщение в соответствующий элемент `<textarea>`.

**Примеры**:

```python
driver = Driver(Firefox)  # или другой драйвер
products = [SimpleNamespace(language='ru', product_title='Товар 1', original_price='100$', sale_price='50$')]
textarea_list = driver.execute_locator(locator.edit_image_properties_textarea) # Получение списка textarea
await update_images_captions(driver, products, textarea_list)
```

### `promote_post`

```python
async def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video:bool = False) -> bool:
    """ Manages the process of promoting a post with a title, description, and media files.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        category (SimpleNamespace): The category details used for the post title and description.
        products (List[SimpleNamespace]): List of products containing media and details to be posted.
        no_video (bool): Флаг, указывающий на необходимость исключения видео из загрузки. По умолчанию `False`.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> await promote_post(driver, category, products)
    """
```

**Назначение**: Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

**Параметры**:
- `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
- `category` (SimpleNamespace): Объект, содержащий детали категории для заголовка и описания поста.
- `products` (List[SimpleNamespace]): Список объектов, содержащих медиафайлы и детали для поста.
- `no_video` (bool): Флаг, указывающий на необходимость исключения видео из загрузки. По умолчанию `False`.

**Как работает функция**:
1. Добавляется заголовок и описание поста.
2. Загружаются медиафайлы.
3. Нажимается кнопка "завершить редактирование".
4. Нажимается кнопка "опубликовать".

**Примеры**:

```python
driver = Driver(Firefox)  # или другой драйвер
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg')]
result = await promote_post(driver, category, products)
print(result)  # Выведет: True или None в случае ошибки
```