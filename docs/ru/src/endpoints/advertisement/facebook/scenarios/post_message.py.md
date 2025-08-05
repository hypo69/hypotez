# Модуль `post_message`

## Обзор

Модуль `post_message` предназначен для автоматизации процесса создания и публикации сообщений в Facebook, включая добавление текста, загрузку медиафайлов и обновление подписей к изображениям. Он предоставляет функции для управления процессом продвижения публикаций с использованием Selenium WebDriver.

## Подробней

Модуль содержит функции для выполнения следующих задач:

-   Ввод заголовка и описания публикации.
-   Загрузка медиафайлов (изображений и видео).
-   Обновление подписей к загруженным изображениям.
-   Публикация сообщения.

Этот модуль является частью системы автоматизации маркетинговых кампаний и предназначен для упрощения и ускорения процесса публикации контента в социальных сетях.

## Классы

В данном модуле классы отсутствуют.

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

**Назначение**: Отправляет заголовок и описание кампании в поле сообщения.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера WebDriver для взаимодействия с веб-страницей.
-   `message` (SimpleNamespace | str): Объект, содержащий заголовок и описание, или строка с сообщением.

**Возвращает**:

-   `bool`: `True`, если заголовок и описание успешно отправлены, иначе `None`.

**Как работает функция**:

1.  Выполняется прокрутка страницы вверх.
2.  Открывается поле для добавления сообщения.
3.  Формируется сообщение из заголовка и описания (если `message` является `SimpleNamespace`).
4.  Сообщение отправляется в поле ввода.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.driver import Driver, Chrome
from types import SimpleNamespace

# Пример использования с SimpleNamespace
driver = Driver(Chrome)
message_data = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
result = post_title(driver, message_data)
print(f"Результат отправки заголовка и описания: {result}")

# Пример использования со строкой
message_text = "Текст сообщения"
result = post_title(driver, message_text)
print(f"Результат отправки сообщения: {result}")
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

**Назначение**: Загружает медиафайлы (изображения или видео) и обновляет подписи к ним.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера WebDriver для взаимодействия с веб-страницей.
-   `media` (SimpleNamespace | List[SimpleNamespace] | str | list[str]): Путь к медиафайлу или список путей.
-   `no_video` (bool): Флаг, указывающий, следует ли избегать загрузки видео (по умолчанию `False`).
-   `without_captions` (bool): Флаг, указывающий, следует ли пропускать обновление подписей (по умолчанию `False`).

**Возвращает**:

-   `bool`: `True`, если медиафайлы успешно загружены, иначе `None`.

**Как работает функция**:

1.  Открывается форма добавления медиафайлов.
2.  Проверяется, является ли `media` списком, и преобразуется в список, если это не так.
3.  Итерируется по списку медиафайлов и загружает каждый файл.
4.  Если `without_captions` имеет значение `False`, обновляются подписи к загруженным изображениям.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.driver import Driver, Chrome
from types import SimpleNamespace

# Пример использования с SimpleNamespace
driver = Driver(Chrome)
media_data = SimpleNamespace(local_image_path="path/to/image.jpg")
result = upload_media(driver, media_data)
print(f"Результат загрузки медиафайла: {result}")

# Пример использования со списком SimpleNamespace
media_list = [
    SimpleNamespace(local_image_path="path/to/image1.jpg"),
    SimpleNamespace(local_image_path="path/to/image2.jpg")
]
result = upload_media(driver, media_list)
print(f"Результат загрузки списка медиафайлов: {result}")
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

-   `d` (Driver): Экземпляр драйвера WebDriver для взаимодействия с веб-страницей.
-   `media` (List[SimpleNamespace]): Список объектов, содержащих информацию о медиафайлах, включая описания.
-   `textarea_list` (List[WebElement]): Список элементов textarea, в которые добавляются подписи.

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

**Назначение**: Обновляет подпись для одного товара.

**Параметры**:

-   `product` (SimpleNamespace): Объект, содержащий информацию о товаре.
-   `textarea_list` (List[WebElement]): Список элементов textarea, в которые добавляются подписи.
-   `i` (int): Индекс товара в списке.

**Как работает функция**:

1.  Определяет направление текста (LTR или RTL) на основе языка товара.
2.  Формирует сообщение, содержащее заголовок, описание, цену и другие детали товара.
3.  Отправляет сообщение в соответствующий элемент textarea.

**Как работает функция `update_images_captions`**:

1.  Загружает локализованные единицы текста из файла `translations.json`.
2.  Итерируется по списку медиафайлов и вызывает `handle_product` для каждого файла.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.driver import Driver, Chrome
from types import SimpleNamespace
from selenium.webdriver.remote.webelement import WebElement

# Пример использования
driver = Driver(Chrome)
media_list = [SimpleNamespace(product_title="Товар 1", description="Описание 1", language="RU"),
              SimpleNamespace(product_title="Товар 2", description="Описание 2", language="EN")]
textarea_elements = [WebElement(None, None), WebElement(None, None)]  # Замените на реальные WebElement
update_images_captions(driver, media_list, textarea_elements)
```

### `publish`

```python
def publish(d:Driver, attempts = 5) -> bool:
    """"""
```

**Назначение**: Осуществляет публикацию сообщения после редактирования.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера WebDriver для взаимодействия с веб-страницей.
-   `attempts` (int): Количество попыток для публикации (по умолчанию 5).

**Возвращает**:

-   `bool`: `True`, если публикация успешна, иначе `None`.

**Как работает функция**:

1.  Выполняет несколько попыток публикации, на каждой итерации уменьшая счетчик `attempts`.
2.  Если попытки заканчиваются, функция возвращает `None`.
3.  На каждой итерации функция пытается нажать кнопку "finish_editing_button". Если это удается, ждет 1 секунду.
4.  Далее функция пытается нажать кнопку "publish". Если это не удается:
    -   Если появляется pop-up окно, пытается его закрыть и повторить попытку.
    -   Если появляется кнопка "not_now", пытается нажать на нее и повторить попытку.
    -   Если `attempts` еще больше нуля, ждет 5 секунд и повторяет попытку.
5.  После успешной попытки нажать кнопку "publish" функция проверяет, освободилось ли поле ввода. Если нет, повторяет попытки с теми же условиями, что и при неудачной публикации.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.driver import Driver, Chrome

# Пример использования
driver = Driver(Chrome)
result = publish(driver)
print(f"Результат публикации: {result}")
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

**Назначение**: Управляет процессом продвижения сообщения, включая добавление заголовка, описания и медиафайлов.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера WebDriver для взаимодействия с веб-страницей.
-   `category` (SimpleNamespace): Объект, содержащий заголовок и описание сообщения.
-   `products` (List[SimpleNamespace]): Список объектов, содержащих информацию о медиафайлах и деталях товара.
-   `no_video` (bool): Флаг, указывающий, следует ли избегать загрузки видео (по умолчанию `False`).

**Возвращает**:

-   `bool`: `True`, если продвижение прошло успешно, иначе `None`.

**Как работает функция**:

1.  Вызывает функцию `post_title` для добавления заголовка и описания.
2.  Вызывает функцию `upload_media` для загрузки медиафайлов.
3.  Нажимает кнопку завершения редактирования.
4.  Публикует сообщение.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.driver import Driver, Chrome
from types import SimpleNamespace

# Пример использования
driver = Driver(Chrome)
category_data = SimpleNamespace(title="Заголовок", description="Описание")
products_data = [SimpleNamespace(local_image_path="path/to/image.jpg")]
result = promote_post(driver, category_data, products_data)
print(f"Результат продвижения сообщения: {result}")
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

**Назначение**: Управляет процессом создания и публикации сообщения, включая добавление заголовка, описания и медиафайлов.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера WebDriver для взаимодействия с веб-страницей.
-   `message` (SimpleNamespace): Объект, содержащий заголовок и описание сообщения.
-   `no_video` (bool): Флаг, указывающий, следует ли избегать загрузки видео (по умолчанию `False`).
-   `images` (Optional[str | list[str]]): Путь к изображению или список путей к изображениям (по умолчанию `None`).
-   `without_captions` (bool): Флаг, указывающий, следует ли пропускать обновление подписей (по умолчанию `False`).

**Возвращает**:

-   `bool`: `True`, если публикация прошла успешно, иначе `None`.

**Как работает функция**:

1.  Вызывает функцию `post_title` для добавления заголовка и описания.
2.  Вызывает функцию `upload_media` для загрузки медиафайлов.
3.  Если было загружено только одно изображение, завершает процесс.
4.  Нажимает кнопку завершения редактирования.
5.  Публикует сообщение.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.driver import Driver, Chrome
from types import SimpleNamespace

# Пример использования
driver = Driver(Chrome)
message_data = SimpleNamespace(title="Заголовок", description="Описание", products=[SimpleNamespace(local_image_path="path/to/image.jpg")])
result = post_message(driver, message_data)
print(f"Результат публикации сообщения: {result}")