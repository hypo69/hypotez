# Модуль `post_message_async`

## Обзор

Модуль `post_message_async` предназначен для автоматизации процесса публикации рекламных сообщений в Facebook, включая добавление заголовка, описания и медиафайлов (изображений или видео). Он использует асинхронный подход для выполнения операций, что позволяет повысить производительность и отзывчивость системы.

## Подробней

Этот модуль является частью проекта `hypotez` и отвечает за взаимодействие с Facebook для публикации рекламных постов. Он использует Selenium WebDriver для управления браузером и выполнения действий на веб-странице. Модуль загружает локаторы элементов интерфейса из JSON-файла и использует их для поиска и взаимодействия с элементами на странице Facebook.
Модуль состоит из нескольких асинхронных функций, которые выполняют следующие задачи:
- Публикация заголовка и описания рекламной кампании.
- Загрузка медиафайлов (изображений или видео).
- Добавление описаний к загруженным медиафайлам.
- Завершение процесса публикации.

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

**Назначение**: Функция отправляет заголовок и описание рекламной кампании в поле для создания сообщения на Facebook.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `category` (SimpleNamespace): Объект, содержащий атрибуты `title` (заголовок) и `description` (описание) для публикации.

**Возвращает**:

-   `bool`: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

**Как работает функция**:

1.  Выполняет прокрутку страницы вверх.
2.  Кликает на элемент, открывающий форму добавления сообщения.
3.  Формирует сообщение, объединяя заголовок и описание из объекта `category`.
4.  Вставляет сформированное сообщение в поле для ввода текста.
5.  Возвращает `True` в случае успеха.

**Примеры**:

```python
driver = Driver(Chrome)
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
result = post_title(driver, category)
print(result)  # Вывод: True или None в случае ошибки
```

### `upload_media`

```python
async def upload_media(d: Driver, products: List[SimpleNamespace], no_video:bool = False) -> bool:
    """
    Загружает медиафайлы в раздел изображений и обновляет подписи.

    Args:
        d (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
        products (List[SimpleNamespace]): Список товаров, содержащих пути к медиафайлам.
        no_video(bool): Параметр указывающий, что видео загружать не надо

    Returns:
        bool: `True`, если медиафайлы были успешно загружены, иначе `None`.

    Raises:
        Exception: Если произошла ошибка во время загрузки медиафайлов или обновления подписей.

    Примеры:
        >>> driver = Driver(...)
        >>> products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]
        >>> await upload_media(driver, products)
        True
    """
```

**Назначение**: Функция загружает медиафайлы (изображения или видео) на Facebook и обновляет подписи к ним.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `products` (List[SimpleNamespace]): Список товаров, содержащих информацию о медиафайлах, включая пути к изображениям и видео.
-   `no_video`: (bool) Если True - загружает только картинки

**Возвращает**:

-   `bool`: `True`, если медиафайлы были успешно загружены, иначе `None`.

**Как работает функция**:

1.  Открывает форму добавления медиафайлов.
2.  Итерируется по списку товаров.
3.  Определяет путь к медиафайлу (видео или изображение) на основе атрибутов товара.
4.  Загружает медиафайл, используя элемент ввода файла на странице.
5.  Кликает на кнопку редактирования загруженного медиафайла.
6.  Извлекает текстовые поля для ввода подписей к изображениям.
7.  Вызывает асинхронную функцию `update_images_captions` для добавления описаний к загруженным медиафайлам.

**Примеры**:

```python
driver = Driver(Chrome)
products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', local_video_path='путь/к/видео.mp4', language='ru')]
result = await upload_media(driver, products)
print(result)  # Вывод: True или None в случае ошибки
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
        Exception: Если произошла ошибка при обновлении подписей к медиафайлам.
    """
```

**Назначение**: Функция добавляет описания к загруженным медиафайлам на Facebook.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `products` (List[SimpleNamespace]): Список товаров, содержащих информацию для формирования описаний.
-   `textarea_list` (List[WebElement]): Список веб-элементов (текстовых полей), в которые будут добавлены описания.

**Как работает функция**:

1.  Загружает локализованные текстовые ресурсы из JSON-файла.
2.  Определяет направление текста (слева направо или справа налево) на основе языка товара.
3.  Формирует сообщение, содержащее информацию о товаре (название, цена, скидка и т.д.) на основе локализованных ресурсов.
4.  Отправляет сформированное сообщение в соответствующее текстовое поле.

**Внутренние функции**:

*   `handle_product`
    ```python
        def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> None:
            """
            Обрабатывает обновление подписей к медиафайлам для одного товара синхронно.

            Args:
                product (SimpleNamespace): Товар для обновления.
                textarea_list (List[WebElement]): Список текстовых полей, куда добавляются подписи.
                i (int): Индекс товара в списке.
            """
    ```
    **Назначение**: Функция обрабатывает обновление подписей к медиафайлам для одного товара синхронно.

    **Параметры**:

    *   `product` (SimpleNamespace): Товар для обновления.
    *   `textarea_list` (List[WebElement]): Список текстовых полей, куда добавляются подписи.
    *   `i` (int): Индекс товара в списке.

    **Как работает функция**:
    1.  Извлекает направление текста для текущего языка товара (LTR или RTL).
    2.  Строит текст сообщения, включая заголовок товара, оригинальную цену, цену со скидкой, размер скидки, рейтинг и ссылку на продвижение.
    3.  Вставляет сформированный текст в соответствующее поле textarea на странице.
    4.  Выводит сообщение об ошибке в случае неудачи при отправке текста в textarea.

**Примеры**:

```python
driver = Driver(Chrome)
products = [SimpleNamespace(product_title='Товар 1', original_price='100$', sale_price='50$', discount='50%', evaluate_rate='4.5', promotion_link='http://example.com', language='ru')]
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
        no_video(bool): Если True - то не публикует видео

    Примеры:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
        >>> products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]
        >>> await promote_post(driver, category, products)
    """
```

**Назначение**: Функция управляет процессом продвижения поста в Facebook, включая добавление заголовка, описания и медиафайлов.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера, используемый для взаимодействия с веб-страницей.
-   `category` (SimpleNamespace): Объект, содержащий заголовок и описание для публикации.
-   `products` (List[SimpleNamespace]): Список товаров, содержащих информацию о медиафайлах.
-   `no_video`: (bool) Если True - загружает только картинки

**Как работает функция**:

1.  Вызывает функцию `post_title` для отправки заголовка и описания.
2.  Вызывает асинхронную функцию `upload_media` для загрузки медиафайлов.
3.  Кликает на кнопку завершения редактирования.
4.  Кликает на кнопку публикации.

**Примеры**:

```python
driver = Driver(Chrome)
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', local_video_path='путь/к/видео.mp4', language='ru')]
result = await promote_post(driver, category, products)
print(result)  # Вывод: True или None в случае ошибки