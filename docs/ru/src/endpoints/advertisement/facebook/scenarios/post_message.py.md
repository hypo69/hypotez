# Модуль для публикации сообщений в Facebook

## Обзор

Модуль `post_message.py` предназначен для автоматизации процесса публикации сообщений в Facebook, включая ввод заголовка и описания, загрузку медиафайлов и отправку сообщения. Он использует Selenium WebDriver для взаимодействия с веб-интерфейсом Facebook.

## Подробнее

Модуль содержит функции для выполнения следующих задач:

-   Ввод заголовка и описания сообщения.
-   Загрузка медиафайлов (изображений и видео).
-   Добавление подписей к загруженным изображениям.
-   Публикация сообщения.

Эти функции используются для автоматизации процесса создания рекламных постов в Facebook.

## Классы

В данном модуле классы не определены.

## Функции

### `post_title`

```python
def post_title(d: Driver, message: SimpleNamespace | str) -> bool:
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

*   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
*   `message` (SimpleNamespace | str): Объект SimpleNamespace или строка, содержащая заголовок и описание для отправки.

**Возвращает**:

*   `bool`: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

**Как работает функция**:

1.  Выполняется скролл страницы вверх.
2.  Открывается поле добавления поста.
3.  Формируется сообщение, объединяющее заголовок и описание.
4.  Отправляется сообщение в поле для ввода.

```
A: Скролл страницы
|
B: Открытие поля добавления поста
|
C: Формирование сообщения
|
D: Отправка сообщения в поле ввода
```

**Примеры**:

```python
driver = Driver(Firefox)
message = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
post_title(driver, message)
```

### `upload_media`

```python
def upload_media(d: Driver, media: SimpleNamespace | List[SimpleNamespace] | str | list[str],   no_video: bool = False, without_captions:bool = False) -> bool:
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
        >>> upload_media(driver, products)
        True
    """
```

**Назначение**: Загружает медиафайлы в секцию изображений и обновляет подписи.

**Параметры**:

*   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
*   `media` (SimpleNamespace | List[SimpleNamespace] | str | list[str]): Список продуктов, содержащий пути к медиафайлам.
*   `no_video` (bool, optional):  Указывает, нужно ли загружать видео. По умолчанию `False`.
*   `without_captions` (bool, optional):  Указывает, нужно ли добавлять подписи. По умолчанию `False`.

**Возвращает**:

*   `bool`: `True`, если медиафайлы были успешно загружены, иначе `None`.

**Вызывает исключения**:

*   `Exception`: Если происходит ошибка во время загрузки медиафайла или обновления подписи.

**Как работает функция**:

1.  Открывается форма добавления медиа.
2.  Проверяется, является ли `media` списком, и если нет, преобразуется в список.
3.  Перебираются элементы списка `media_list` и загружаются медиафайлы.
4.  Обновляются подписи для загруженных медиафайлов, если `without_captions` имеет значение `False`.

```
A: Открытие формы добавления медиа
|
B: Преобразование media в список
|
C: Загрузка медиафайлов
|
D: Обновление подписей (если необходимо)
```

**Примеры**:

```python
driver = Driver(Firefox)
products = [SimpleNamespace(local_image_path='path/to/image.jpg', description='Описание изображения')]
upload_media(driver, products)
```

### `update_images_captions`

```python
def update_images_captions(d: Driver, media: List[SimpleNamespace], textarea_list: List[WebElement]) -> None:
    """ Adds descriptions to uploaded media files.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        products (List[SimpleNamespace]): List of products with details to update.
        textarea_list (List[WebElement]): List of textareas where captions are added.

    Raises:
        Exception: If there's an error updating the media captions.
    """
```

**Назначение**: Добавляет описания к загруженным медиафайлам.

**Параметры**:

*   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
*   `media` (List[SimpleNamespace]): Список продуктов с деталями для обновления.
*   `textarea_list` (List[WebElement]): Список текстовых полей, в которые добавляются подписи.

**Вызывает исключения**:

*   `Exception`: Если происходит ошибка при обновлении подписей к медиафайлам.

**Как работает функция**:

1.  Загружаются локализованные единицы из файла `translations.json`.
2.  Определяется внутренняя функция `handle_product`, которая обрабатывает обновление подписей для одного продукта.
3.  Перебираются продукты и вызывается `handle_product` для каждого из них.

**Внутренние функции**:

*   `handle_product`:

    ```python
    def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> None:
        """ Handles the update of media captions for a single product.

        Args:
            product (SimpleNamespace): The product to update.
            textarea_list (List[WebElement]): List of textareas where captions are added.
            i (int): Index of the product in the list.
        """
    ```

    **Назначение**: Обрабатывает обновление подписей к медиафайлу для одного продукта.

    **Параметры**:

    *   `product` (SimpleNamespace): Продукт для обновления.
    *   `textarea_list` (List[WebElement]): Список текстовых полей, в которые добавляются подписи.
    *   `i` (int): Индекс продукта в списке.

    **Как работает функция**:

    1.  Определяется язык продукта.
    2.  Формируется сообщение, включающее заголовок, описание, цену и другие детали продукта.
    3.  Отправляется сообщение в текстовое поле.

```
A: Загрузка локализованных единиц
|
B: Определение handle_product
|
C: Перебор продуктов
|
D: Вызов handle_product для каждого продукта
```

**Примеры**:

```python
driver = Driver(Firefox)
products = [SimpleNamespace(language='en', product_title='Название', description='Описание')]
textarea_list = driver.execute_locator(locator.edit_image_properties_textarea)
update_images_captions(driver, products, textarea_list)
```

### `publish`

```python
def publish(d:Driver, attempts = 5) -> bool:
    """"""
```

**Назначение**: Осуществляет попытку публикации поста.

**Параметры**:

*   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
*   `attempts` (int, optional): Количество попыток публикации. По умолчанию 5.

**Возвращает**:

*   `bool`: `True`, если публикация прошла успешно.

**Как работает функция**:

1.  Пытается нажать кнопку завершения редактирования.
2.  Пытается опубликовать пост. Если публикация не удалась, закрывает всплывающее окно и повторяет попытку.

```
A: Нажатие кнопки завершения редактирования
|
B: Попытка публикации
|
C: Если публикация не удалась, закрытие всплывающего окна и повтор попытки
```

**Примеры**:

```python
driver = Driver(Firefox)
publish(driver)
```

### `promote_post`

```python
def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> bool:
    """ Manages the process of promoting a post with a title, description, and media files.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        category (SimpleNamespace): The category details used for the post title and description.
        products (List[SimpleNamespace]): List of products containing media and details to be posted.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> promote_post(driver, category, products)
    """
```

**Назначение**: Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

**Параметры**:

*   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
*   `category` (SimpleNamespace): Детали категории, используемые для заголовка и описания поста.
*   `products` (List[SimpleNamespace]): Список продуктов, содержащих медиа и детали для публикации.
*   `no_video` (bool, optional):  Указывает, нужно ли загружать видео. По умолчанию `False`.

**Как работает функция**:

1.  Отправляется заголовок и описание поста.
2.  Загружаются медиафайлы.
3.  Выполняется завершение редактирования.
4.  Публикуется пост.

```
A: Отправка заголовка и описания
|
B: Загрузка медиафайлов
|
C: Завершение редактирования
|
D: Публикация поста
```

**Примеры**:

```python
driver = Driver(Firefox)
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
products = [SimpleNamespace(local_image_path='path/to/image.jpg')]
promote_post(driver, category, products)
```

### `post_message`

```python
def post_message(d: Driver, message: SimpleNamespace,  no_video: bool = False,  images:Optional[str | list[str]] = None, without_captions:bool = False) -> bool:
    """ Manages the process of promoting a post with a title, description, and media files.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        message (SimpleNamespace): The message details used for the post title and description.
        products (List[SimpleNamespace]): List of products containing media and details to be posted.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> promote_post(driver, category, products)
    """
```

**Назначение**: Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

**Параметры**:

*   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
*   `message` (SimpleNamespace): Детали сообщения, используемые для заголовка и описания поста.
*   `no_video` (bool, optional): Указывает, нужно ли загружать видео. По умолчанию `False`.
*   `images` (Optional[str | list[str]], optional): Список путей к изображениям. По умолчанию `None`.
*   `without_captions` (bool, optional): Указывает, нужно ли использовать подписи. По умолчанию `False`.

**Как работает функция**:

1.  Отправляется заголовок и описание поста.
2.  Загружаются медиафайлы.
3.  Если есть одно изображение, отправляется сообщение.
4.  Выполняется завершение редактирования.
5.  Публикуется пост.

```
A: Отправка заголовка и описания
|
B: Загрузка медиафайлов
|
C: Если одно изображение, отправка сообщения
|
D: Завершение редактирования
|
E: Публикация поста
```

**Примеры**:

```python
driver = Driver(Firefox)
message = SimpleNamespace(title="Заголовок сообщения", description="Описание сообщения", products=[SimpleNamespace(local_image_path='path/to/image.jpg')])
post_message(driver, message)