# Модуль для публикации сообщений в Facebook

## Обзор

Модуль `post_message.py` предназначен для автоматизации процесса публикации сообщений в Facebook, включая ввод заголовка и описания, загрузку медиафайлов и отправку сообщения.

## Подробнее

Этот модуль содержит функции для выполнения следующих действий:

-   Ввод заголовка и описания сообщения.
-   Загрузка медиафайлов (изображений и видео).
-   Добавление подписей к изображениям.
-   Публикация сообщения.

Модуль использует библиотеку Selenium для взаимодействия с веб-интерфейсом Facebook.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `post_title`

```python
def post_title(d: Driver, message: SimpleNamespace | str) -> bool:
    """ Sends the title and description of a campaign to the post message box.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        message (SimpleNamespace | str): The category containing the title and description to be sent.

    Returns:
        bool: `True` if the title and description were sent successfully, otherwise `None`.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> post_title(driver, category)
        True
    """
```

**Назначение**: Отправляет заголовок и описание рекламной кампании в поле для ввода сообщения.

**Параметры**:

-   `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
-   `message` (SimpleNamespace | str): Объект SimpleNamespace или строка, содержащие заголовок и описание сообщения.

**Возвращает**:

-   `bool`: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

**Как работает функция**:

1.  Прокручивает страницу вверх.
2.  Открывает поле для добавления сообщения.
3.  Формирует текст сообщения, объединяя заголовок и описание из объекта `message`.
4.  Отправляет сообщение в поле для ввода.

```
    A: Прокрутка страницы вверх
    |
    B: Открытие поля для добавления сообщения
    |
    C: Формирование текста сообщения
    |
    D: Отправка сообщения в поле для ввода
```

**Примеры**:

```python
driver = Driver(Chrome)
message = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
result = post_title(driver, message)
print(result)  # Вывод: True или None
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
        >>> products = [SimpleNamespace(local_image_path=\'path/to/image.jpg\', ...)]
        >>> upload_media(driver, products)
        True
    """
```

**Назначение**: Загружает медиафайлы в секцию изображений и обновляет подписи.

**Параметры**:

-   `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
-   `media` (SimpleNamespace | List[SimpleNamespace] | str | list[str]): Список продуктов, содержащий пути к медиафайлам.
-   `no_video` (bool): Определяет, нужно ли загружать видео. По умолчанию `False`.
-   `without_captions` (bool): Определяет, нужно ли добавлять подписи к изображениям. По умолчанию `False`.

**Возвращает**:

-   `bool`: `True`, если медиафайлы были успешно загружены, иначе `None`.

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка при загрузке медиа или обновлении подписей.

**Как работает функция**:

1.  Открывает форму для добавления медиафайлов.
2.  Проверяет, является ли `media` списком. Если нет, преобразует в список.
3.  Итерируется по списку медиафайлов и загружает каждый файл.
4.  Если `without_captions` равен `False`, обновляет подписи для загруженных изображений.

```
    A: Открытие формы для добавления медиафайлов
    |
    B: Преобразование media в список (если необходимо)
    |
    C: Загрузка медиафайлов (в цикле)
    |
    D: Обновление подписей (если without_captions == False)
```

**Примеры**:

```python
driver = Driver(Chrome)
products = [SimpleNamespace(local_image_path='path/to/image.jpg')]
result = upload_media(driver, products)
print(result)  # Вывод: True или None
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
        Exception: If there\'s an error updating the media captions.
    """
```

**Назначение**: Добавляет описания к загруженным медиафайлам.

**Параметры**:

-   `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
-   `media` (List[SimpleNamespace]): Список продуктов с деталями для обновления.
-   `textarea_list` (List[WebElement]): Список текстовых полей, в которые добавляются подписи.

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка при обновлении подписей к медиафайлам.

**Как работает функция**:

1.  Загружает локализованные единицы текста из файла `translations.json`.
2.  Определяет внутреннюю функцию `handle_product` для обновления подписи для одного продукта.
3.  Итерируется по списку продуктов и вызывает `handle_product` для каждого продукта.

    A: Загрузка локализованных единиц текста
    |
    B: Определение внутренней функции handle_product
    |
    C: Итерация по списку продуктов (в цикле)
    |
    D: Вызов handle_product для каждого продукта

**Внутренние функции**:

#### `handle_product`

```python
def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> None:
    """ Handles the update of media captions for a single product.

    Args:
        product (SimpleNamespace): The product to update.
        textarea_list (List[WebElement]): List of textareas where captions are added.
        i (int): Index of the product in the list.
    """
```

**Назначение**: Обновляет подпись для одного продукта.

**Параметры**:

-   `product` (SimpleNamespace): Продукт для обновления.
-   `textarea_list` (List[WebElement]): Список текстовых полей, в которые добавляются подписи.
-   `i` (int): Индекс продукта в списке.

**Как работает функция**:

1.  Определяет язык продукта и направление текста (LTR или RTL).
2.  Формирует сообщение, добавляя детали продукта (заголовок, описание, цена и т.д.) в зависимости от направления текста.
3.  Отправляет сообщение в соответствующее текстовое поле.

```
        A: Определение языка продукта и направления текста
        |
        B: Формирование сообщения с деталями продукта
        |
        C: Отправка сообщения в текстовое поле
```

**Примеры**:

```python
driver = Driver(Chrome)
products = [SimpleNamespace(language='ru', product_title='Товар 1', description='Описание товара 1')]
textarea_list = [WebElement(...)]  # Замените на реальный список WebElement
update_images_captions(driver, products, textarea_list)
```

### `publish`

```python
def publish(d:Driver, attempts = 5) -> bool:
    """"""
    ...
```

**Назначение**: Публикует сообщение.

**Параметры**:

-   `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
-   `attempts` (int): Количество попыток публикации. По умолчанию 5.

**Возвращает**:

-   `bool`: `True`, если сообщение было успешно опубликовано, иначе `None`.

**Как работает функция**:

1.  Нажимает кнопку "Завершить редактирование".
2.  Нажимает кнопку "Опубликовать".
3.  Если публикация не удалась, пытается закрыть всплывающие окна и повторяет попытку.
4.  Ждет, пока поле ввода сообщения не освободится.

```
    A: Нажатие кнопки "Завершить редактирование"
    |
    B: Нажатие кнопки "Опубликовать"
    |
    C: Обработка ошибок и повторные попытки (если необходимо)
    |
    D: Ожидание освобождения поля ввода сообщения
```

**Примеры**:

```python
driver = Driver(Chrome)
result = publish(driver)
print(result)  # Вывод: True или None
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
        >>> products = [SimpleNamespace(local_image_path=\'path/to/image.jpg\', ...)]
        >>> promote_post(driver, category, products)
    """
```

**Назначение**: Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

**Параметры**:

-   `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
-   `category` (SimpleNamespace): Детали категории, используемые для заголовка и описания поста.
-   `products` (List[SimpleNamespace]): Список продуктов, содержащих медиа и детали для публикации.
-   `no_video` (bool): Определяет, нужно ли загружать видео. По умолчанию `False`.

**Как работает функция**:

1.  Отправляет заголовок и описание поста.
2.  Загружает медиафайлы.
3.  Нажимает кнопку "Завершить редактирование".
4.  Нажимает кнопку "Опубликовать".

```
    A: Отправка заголовка и описания поста
    |
    B: Загрузка медиафайлов
    |
    C: Нажатие кнопки "Завершить редактирование"
    |
    D: Нажатие кнопки "Опубликовать"
```

**Примеры**:

```python
driver = Driver(Chrome)
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
products = [SimpleNamespace(local_image_path='path/to/image.jpg')]
result = promote_post(driver, category, products)
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
        >>> products = [SimpleNamespace(local_image_path=\'path/to/image.jpg\', ...)]
        >>> promote_post(driver, category, products)
    """
```

**Назначение**: Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

**Параметры**:

-   `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
-   `message` (SimpleNamespace): Детали сообщения, используемые для заголовка и описания поста.
-   `no_video` (bool): Определяет, нужно ли загружать видео. По умолчанию `False`.
-   `images` (Optional[str | list[str]]): Список изображений для публикации.
-   `without_captions` (bool): Определяет, нужно ли добавлять подписи к изображениям. По умолчанию `False`.

**Как работает функция**:

1.  Отправляет заголовок и описание поста.
2.  Загружает медиафайлы.
3.  Если загружено одно изображение, нажимает кнопку "Отправить".
4.  Если загружено несколько изображений, нажимает кнопку "Завершить редактирование" и публикует сообщение.

```
    A: Отправка заголовка и описания поста
    |
    B: Загрузка медиафайлов
    |
    C: Нажатие кнопки "Отправить" (если одно изображение)
    |
    D: Нажатие кнопки "Завершить редактирование" и публикация (если несколько изображений)
```

**Примеры**:

```python
driver = Driver(Chrome)
message = SimpleNamespace(title="Заголовок кампании", description="Описание кампании", products=[SimpleNamespace(local_image_path='path/to/image.jpg')])
result = post_message(driver, message)