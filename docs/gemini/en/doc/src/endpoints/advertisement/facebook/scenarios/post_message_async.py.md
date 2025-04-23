# Модуль: src.endpoints.advertisement.facebook.scenarios.post_message_async

## Обзор

Модуль `post_message_async` предназначен для автоматизации процесса публикации рекламных сообщений в Facebook, включая загрузку медиафайлов и добавление подписей к ним. Он использует Selenium WebDriver для взаимодействия с веб-интерфейсом Facebook.

## Подробнее

Этот модуль содержит функции для отправки заголовка и описания кампании, загрузки медиафайлов и обновления подписей к изображениям. Он асинхронно выполняет операции, такие как загрузка медиа и обновление подписей, чтобы повысить производительность.

## Функции

### `post_title`

```python
def post_title(d: Driver, category: SimpleNamespace) -> bool:
    """
    Отправляет заголовок и описание кампании в поле сообщения.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        category (SimpleNamespace): Объект, содержащий заголовок и описание для отправки.

    Returns:
        bool: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

    Примеры:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> post_title(driver, category)
        True
    """
```

**Описание**:

Функция `post_title` отправляет заголовок и описание рекламной кампании в поле для ввода сообщения в Facebook. Она выполняет следующие действия:

1.  Прокручивает страницу вверх.
2.  Открывает поле добавления поста.
3.  Формирует сообщение, объединяя заголовок и описание из объекта `category`.
4.  Отправляет сообщение в поле для ввода поста.

Если какая-либо из операций завершается неудачей, функция регистрирует ошибку и возвращает `None`.

**Параметры**:

*   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
*   `category` (SimpleNamespace): Объект, содержащий атрибуты `title` (заголовок) и `description` (описание) для публикации.

**Возвращает**:

*   `bool`: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

**Пример использования**:

```python
driver = Driver(Chrome)
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
result = post_title(driver, category)
```

### `upload_media`

```python
async def upload_media(d: Driver, products: List[SimpleNamespace], no_video:bool = False) -> bool:
    """
    Загружает медиафайлы в секцию изображений и обновляет подписи.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        products (List[SimpleNamespace]): Список товаров, содержащих пути к медиафайлам.
        no_video (bool): Флаг, указывающий, следует ли загружать видео. По умолчанию `False`.

    Returns:
        bool: `True`, если медиафайлы были успешно загружены, иначе `None`.

    Raises:
        Exception: Если возникает ошибка во время загрузки медиа или обновления подписей.

    Примеры:
        >>> driver = Driver(...)
        >>> products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]
        >>> await upload_media(driver, products)
        True
    """
```

**Описание**:

Функция `upload_media` загружает медиафайлы (изображения или видео) в Facebook и обновляет подписи к ним. Она выполняет следующие шаги:

1.  Открывает форму добавления медиа.
2.  Определяет, какой тип медиа следует загружать (изображение или видео) на основе атрибутов продукта и флага `no_video`.
3.  Загружает медиафайл для каждого продукта из списка `products`.
4.  Открывает форму редактирования загруженных медиафайлов.
5.  Асинхронно обновляет подписи к изображениям, вызывая функцию `update_images_captions`.

Если во время выполнения возникает ошибка, функция регистрирует её и возвращает `None`.

**Параметры**:

*   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
*   `products` (List[SimpleNamespace]): Список объектов `SimpleNamespace`, каждый из которых содержит информацию о продукте, включая пути к медиафайлам (`local_image_path` и `local_video_path`).
*   `no_video` (bool): Флаг, указывающий, следует ли загружать видео. По умолчанию `False`.

**Возвращает**:

*   `bool`: `True`, если медиафайлы были успешно загружены, иначе `None`.

**Пример использования**:

```python
driver = Driver(Chrome)
products = [SimpleNamespace(local_image_path='путь/к/изображению1.jpg', local_video_path='путь/к/видео1.mp4'),
            SimpleNamespace(local_image_path='путь/к/изображению2.jpg', local_video_path='путь/к/видео2.mp4')]
await upload_media(driver, products, no_video=True)
```

### `update_images_captions`

```python
async def update_images_captions(d: Driver, products: List[SimpleNamespace], textarea_list: List[WebElement]) -> None:
    """
    Добавляет описания к загруженным медиафайлам асинхронно.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        products (List[SimpleNamespace]): Список товаров с деталями для обновления.
        textarea_list (List[WebElement]): Список текстовых полей, куда добавляются подписи.

    Raises:
        Exception: Если возникает ошибка при обновлении подписей к медиафайлам.
    """
```

**Описание**:

Функция `update_images_captions` асинхронно добавляет описания к загруженным медиафайлам в Facebook. Она загружает локальные единицы перевода из файла `translations.json` и для каждого продукта формирует сообщение на основе его атрибутов (таких как `product_title`, `original_price`, `sale_price` и т.д.) и локали. Затем она отправляет это сообщение в соответствующее текстовое поле.

Для каждого продукта создается отдельная асинхронная задача, которая выполняется в отдельном потоке.

**Параметры**:

*   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
*   `products` (List[SimpleNamespace]): Список объектов `SimpleNamespace`, каждый из которых содержит информацию о продукте, включая заголовок, цену, скидку и ссылку.
*   `textarea_list` (List[WebElement]): Список веб-элементов (текстовых полей), в которые нужно добавить подписи.

**Внутренняя функция `handle_product`**:

```python
def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> None:
    """
    Обрабатывает обновление подписей к медиафайлам для одного продукта синхронно.

    Args:
        product (SimpleNamespace): Товар для обновления.
        textarea_list (List[WebElement]): Список текстовых полей, куда добавляются подписи.
        i (int): Индекс продукта в списке.
    """
```

Внутренняя функция `handle_product` отвечает за формирование сообщения для одного продукта и отправку его в соответствующее текстовое поле. Она определяет направление текста (LTR или RTL) на основе языка продукта и формирует сообщение, объединяя различные атрибуты продукта с соответствующими локализованными строками.

**Пример использования**:

```python
driver = Driver(Chrome)
products = [SimpleNamespace(product_title='Товар 1', original_price='100$', sale_price='50$', language='ru'),
            SimpleNamespace(product_title='Product 2', original_price='200$', sale_price='100$', language='en')]
textarea_list = driver.execute_locator(locator.edit_image_properties_textarea)
await update_images_captions(driver, products, textarea_list)
```

### `promote_post`

```python
async def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video:bool = False) -> bool:
    """
    Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        category (SimpleNamespace): Детали категории, используемые для заголовка и описания поста.
        products (List[SimpleNamespace]): Список товаров, содержащих медиа и детали для публикации.
        no_video (bool): Флаг, указывающий, следует ли загружать видео. По умолчанию `False`.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]
        >>> await promote_post(driver, category, products)
    """
```

**Описание**:

Функция `promote_post` управляет процессом продвижения поста в Facebook, включая отправку заголовка и описания, загрузку медиафайлов и публикацию поста. Она вызывает функции `post_title` и `upload_media` для выполнения соответствующих задач.

**Параметры**:

*   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
*   `category` (SimpleNamespace): Объект, содержащий заголовок и описание для публикации.
*   `products` (List[SimpleNamespace]): Список объектов `SimpleNamespace`, каждый из которых содержит информацию о продукте, включая пути к медиафайлам.
*   `no_video` (bool): Флаг, указывающий, следует ли загружать видео. По умолчанию `False`.

**Пример использования**:

```python
driver = Driver(Chrome)
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
products = [SimpleNamespace(local_image_path='путь/к/изображению1.jpg', local_video_path='путь/к/видео1.mp4'),
            SimpleNamespace(local_image_path='путь/к/изображению2.jpg', local_video_path='путь/к/видео2.mp4')]
await promote_post(driver, category, products, no_video=True)
```