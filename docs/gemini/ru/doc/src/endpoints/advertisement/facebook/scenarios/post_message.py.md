# Модуль для публикации сообщений в Facebook
## Обзор

Модуль `post_message.py` предназначен для автоматизации процесса публикации сообщений, включая текст и медиафайлы, в Facebook с использованием Selenium WebDriver. Он предоставляет функции для ввода заголовка и описания сообщения, загрузки медиафайлов, добавления подписей к изображениям и публикации сообщения.

## Подробней

Этот модуль является частью проекта `hypotez` и автоматизирует процесс создания и публикации рекламных постов в Facebook. Он использует Selenium WebDriver для взаимодействия с веб-интерфейсом Facebook, загружает локаторы элементов интерфейса из JSON-файла и выполняет различные действия, такие как ввод текста, загрузка медиафайлов и нажатие кнопок. Модуль предназначен для упрощения и ускорения процесса публикации рекламных сообщений, а также для уменьшения вероятности ошибок, связанных с ручным вводом данных.

## Функции

### `post_title`

```python
def post_title(d: Driver, message: SimpleNamespace | str) -> bool:
    """
    Отправляет заголовок и описание кампании в поле сообщения.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        message (SimpleNamespace | str): Объект SimpleNamespace или строка, содержащая заголовок и описание для отправки.

    Returns:
        bool: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

    Пример:
        >>> driver = Driver(...)
        >>> message = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> post_title(driver, message)
        True
    """
```

**Назначение**:
Функция `post_title` отправляет заголовок и описание рекламной кампании в поле ввода сообщения в Facebook.

**Параметры**:
- `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
- `message` (SimpleNamespace | str): Объект `SimpleNamespace` или строка, содержащая заголовок и описание для отправки. Если передан `SimpleNamespace`, то используются атрибуты `title` и `description`. Если передана строка, то она используется как текст сообщения.

**Как работает функция**:
1. Прокручивает страницу вверх, чтобы убедиться, что поле ввода сообщения находится в видимой области.
2. Открывает поле ввода сообщения, нажимая на соответствующий локатор.
3. Формирует текст сообщения, объединяя заголовок и описание (если `message` является экземпляром `SimpleNamespace`) или используя переданную строку.
4. Отправляет сформированный текст в поле ввода сообщения.
5. В случае ошибки логирует информацию и возвращает `None`.

**Примеры**:
```python
driver = Driver(Chrome)
message = SimpleNamespace(title="Заголовок", description="Описание")
post_title(driver, message)

message = "Текст сообщения"
post_title(driver, message)
```

### `upload_media`

```python
def upload_media(d: Driver, media: SimpleNamespace | List[SimpleNamespace] | str | list[str],   no_video: bool = False, without_captions:bool = False) -> bool:
    """
    Загружает медиафайлы в секцию изображений и обновляет подписи.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        media (SimpleNamespace | List[SimpleNamespace] | str | list[str]): Список продуктов, содержащих пути к медиафайлам.
        no_video (bool): Если True, то видео не загружается. По умолчанию False.
        without_captions (bool): Если True, то подписи к изображениям не обновляются. По умолчанию False.

    Returns:
        bool: `True`, если медиафайлы были успешно загружены, иначе `None`.

    Raises:
        Exception: Если возникает ошибка во время загрузки медиа или обновления подписей.

    Пример:
        >>> driver = Driver(...)
        >>> products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]
        >>> upload_media(driver, products)
        True
    """
```

**Назначение**:
Функция `upload_media` загружает медиафайлы (изображения или видео) в секцию изображений в Facebook и обновляет подписи к ним.

**Параметры**:
- `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
- `media` (SimpleNamespace | List[SimpleNamespace] | str | list[str]): Список продуктов, содержащих пути к медиафайлам. Может быть как объектом `SimpleNamespace`, так и списком объектов `SimpleNamespace`, строкой или списком строк.
- `no_video` (bool): Если `True`, то видео не загружается. По умолчанию `False`.
- `without_captions` (bool): Если `True`, то подписи к изображениям не обновляются. По умолчанию `False`.

**Как работает функция**:
1. Открывает форму добавления медиафайлов.
2. Преобразует `media` в список, если это не список.
3. Итерируется по списку медиафайлов и загружает каждый файл.
4. Если `without_captions` равно `False`, то обновляет подписи к загруженным изображениям, вызывая функцию `update_images_captions`.
5. В случае ошибки логирует информацию и возвращает `None`.

**Примеры**:
```python
driver = Driver(Chrome)
products = [SimpleNamespace(local_image_path='путь/к/изображению1.jpg'), SimpleNamespace(local_image_path='путь/к/изображению2.jpg')]
upload_media(driver, products)

upload_media(driver, products, no_video=True)

upload_media(driver, products, without_captions=True)
```

### `update_images_captions`

```python
def update_images_captions(d: Driver, media: List[SimpleNamespace], textarea_list: List[WebElement]) -> None:
    """
    Добавляет описания к загруженным медиафайлам.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        media (List[SimpleNamespace]): Список продуктов с деталями для обновления.
        textarea_list (List[WebElement]): Список текстовых полей, в которые добавляются подписи.

    Raises:
        Exception: Если возникает ошибка при обновлении подписей медиафайлов.
    """
```

**Назначение**:
Функция `update_images_captions` добавляет описания к загруженным медиафайлам, используя информацию из переданных объектов `SimpleNamespace`.

**Параметры**:
- `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
- `media` (List[SimpleNamespace]): Список продуктов с деталями для обновления.
- `textarea_list` (List[WebElement]): Список текстовых полей, в которые добавляются подписи.

**Внутренние функции**:

#### `handle_product`

```python
def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> None:
    """
    Обрабатывает обновление подписей медиафайлов для одного продукта.

    Args:
        product (SimpleNamespace): Продукт для обновления.
        textarea_list (List[WebElement]): Список текстовых полей, в которые добавляются подписи.
        i (int): Индекс продукта в списке.
    """
```

**Назначение**:
Внутренняя функция `handle_product` обрабатывает обновление подписей медиафайлов для одного продукта.

**Параметры**:
- `product` (SimpleNamespace): Продукт для обновления.
- `textarea_list` (List[WebElement]): Список текстовых полей, в которые добавляются подписи.
- `i` (int): Индекс продукта в списке.

**Как работает функция**:
1. Определяет язык продукта и направление текста (LTR или RTL).
2. Формирует текст сообщения, добавляя детали продукта (название, описание, цена и т.д.) в зависимости от направления текста.
3. Отправляет сформированный текст в соответствующее текстовое поле.
4. В случае ошибки логирует информацию.

**Как работает функция `update_images_captions`**:
1. Загружает локализованные единицы из JSON-файла.
2. Итерируется по списку медиафайлов и вызывает функцию `handle_product` для каждого файла.
3. В случае ошибки логирует информацию.

**Примеры**:
```python
driver = Driver(Chrome)
products = [SimpleNamespace(product_title='Название продукта', description='Описание продукта', language='ru')]
textarea_list = driver.execute_locator(locator = locator.edit_image_properties_textarea, timeout = 10, timeout_for_event = 'presence_of_element_located' )
update_images_captions(driver, products, textarea_list)
```

### `publish`

```python
def publish(d:Driver, attempts = 5) -> bool:
    """
    Публикует сообщение.
    """
```

**Назначение**:
Функция `publish` публикует сообщение в Facebook.

**Параметры**:
- `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
- `attempts` (int): Количество попыток публикации. По умолчанию 5.

**Как работает функция**:
1. Нажимает кнопку завершения редактирования.
2. Нажимает кнопку публикации.
3. Если публикация не удалась, пытается закрыть всплывающие окна и повторяет попытку публикации.
4. В случае успеха возвращает `True`.
5. В случае ошибки логирует информацию и возвращает `None`.

**Примеры**:
```python
driver = Driver(Chrome)
publish(driver)
```

### `promote_post`

```python
def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> bool:
    """
    Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        category (SimpleNamespace): Детали категории, используемые для заголовка и описания поста.
        products (List[SimpleNamespace]): Список продуктов, содержащих медиа и детали для публикации.

    Пример:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]
        >>> promote_post(driver, category, products)
    """
```

**Назначение**:
Функция `promote_post` управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

**Параметры**:
- `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
- `category` (SimpleNamespace): Детали категории, используемые для заголовка и описания поста.
- `products` (List[SimpleNamespace]): Список продуктов, содержащих медиа и детали для публикации.
- `no_video` (bool): Если True, то видео не загружается. По умолчанию False.

**Как работает функция**:
1. Отправляет заголовок и описание, вызывая функцию `post_title`.
2. Загружает медиафайлы, вызывая функцию `upload_media`.
3. Нажимает кнопку завершения редактирования.
4. Нажимает кнопку публикации.
5. В случае ошибки логирует информацию и возвращает `None`.

**Примеры**:
```python
driver = Driver(Chrome)
category = SimpleNamespace(title="Заголовок", description="Описание")
products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg')]
promote_post(driver, category, products)
```

### `post_message`

```python
def post_message(d: Driver, message: SimpleNamespace,  no_video: bool = False,  images:Optional[str | list[str]] = None, without_captions:bool = False) -> bool:
    """
    Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        message (SimpleNamespace): Детали сообщения, используемые для заголовка и описания поста.
        products (List[SimpleNamespace]): Список продуктов, содержащих медиа и детали для публикации.

    Пример:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]
        >>> promote_post(driver, category, products)
    """
```

**Назначение**:
Функция `post_message` управляет процессом создания и публикации поста в Facebook с заголовком, описанием и медиафайлами.

**Параметры**:
- `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
- `message` (SimpleNamespace): Детали сообщения, используемые для заголовка и описания поста.
- `no_video` (bool): Если `True`, то видео не загружается. По умолчанию `False`.
- `images` (Optional[str | list[str]]): Список путей к изображениям. По умолчанию `None`.
- `without_captions` (bool): Если `True`, то подписи к изображениям не обновляются. По умолчанию `False`.

**Как работает функция**:
1. Отправляет заголовок и описание, вызывая функцию `post_title`.
2. Загружает медиафайлы, вызывая функцию `upload_media`.
3. Если было загружено только одно изображение, нажимает кнопку отправки.
4. В противном случае нажимает кнопку завершения редактирования и публикует сообщение, вызывая функцию `publish`.
5. В случае ошибки логирует информацию и возвращает `None`.

**Примеры**:
```python
driver = Driver(Chrome)
message = SimpleNamespace(title="Заголовок", description="Описание", products=[SimpleNamespace(local_image_path='путь/к/изображению.jpg')])
post_message(driver, message)

post_message(driver, message, no_video=True)

post_message(driver, message, without_captions=True)