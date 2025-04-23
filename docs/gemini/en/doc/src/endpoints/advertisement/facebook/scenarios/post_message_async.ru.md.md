# Модуль src.endpoints.advertisement.facebook.post_message_async

## Обзор

Этот модуль предназначен для асинхронной публикации сообщений на Facebook. Он автоматизирует процесс взаимодействия со страницей Facebook, включая отправку текста, загрузку медиафайлов и обновление подписей.

## Более подробно

Этот скрипт автоматизирует процесс публикации рекламных постов на Facebook. Он состоит из нескольких функций, каждая из которых отвечает за определенный этап публикации.

## Структура модуля

```mermaid
graph TD
    Start[Начало] --> InitDriver[Инициализация Driver]
    InitDriver --> LoadCategoryAndProducts[Загрузка категории и продуктов]
    LoadCategoryAndProducts --> SendTitle[Отправка заголовка]
    SendTitle --> CheckTitleSuccess{Успешно?}
    CheckTitleSuccess -->|Да| UploadMediaAndPromotePost[Загрузка медиа и продвижение поста]
    CheckTitleSuccess -->|Нет| TitleError[Ошибка: Не удалось отправить заголовок]
    UploadMediaAndPromotePost --> UploadMedia[Загрузка медиа]
    UploadMedia --> CheckMediaSuccess{Успешно?}
    CheckMediaSuccess -->|Да| UpdateCaptions[Обновление подписей к изображениям]
    CheckMediaSuccess -->|Нет| MediaError[Ошибка: Не удалось загрузить медиа]
    UpdateCaptions --> PromotePost[Продвижение поста]
    PromotePost --> CheckPromoteSuccess{Успешно?}
    CheckPromoteSuccess -->|Да| End[Конец]
    CheckPromoteSuccess -->|Нет| PromoteError[Ошибка: Не удалось продвинуть пост]
```

### Легенда

1. **Start**: Начало выполнения скрипта.
2. **InitDriver**: Создание экземпляра класса `Driver`.
3. **LoadCategoryAndProducts**: Загрузка данных категории и продуктов.
4. **SendTitle**: Вызов функции `post_title` для отправки заголовка.
5. **CheckTitleSuccess**: Проверка успешности отправки заголовка.
   - **Да**: Переход к загрузке медиа и продвижению поста.
   - **Нет**: Вывод ошибки "Не удалось отправить заголовок".
6. **UploadMediaAndPromotePost**: Вызов функции `promote_post`.
7. **UploadMedia**: Вызов функции `upload_media` для загрузки медиафайлов.
8. **CheckMediaSuccess**: Проверка успешности загрузки медиа.
   - **Да**: Переход к обновлению подписей к изображениям.
   - **Нет**: Вывод ошибки "Не удалось загрузить медиа".
9. **UpdateCaptions**: Вызов функции `update_images_captions` для обновления подписей.
10. **PromotePost**: Завершение процесса продвижения поста.
11. **CheckPromoteSuccess**: Проверка успешности продвижения поста.
    - **Да**: Конец выполнения скрипта.
    - **Нет**: Вывод ошибки "Не удалось продвинуть пост".

## Функции

### `post_title`

```python
def post_title(d: Driver, category: SimpleNamespace) -> bool:
    """
    Отправляет заголовок и описание кампании в поле сообщения на Facebook.
    Args:
        d (Driver): Экземпляр `Driver` для взаимодействия с веб-страницей.
        category (SimpleNamespace): Категория, содержащая заголовок и описание для отправки.

    Returns:
        bool: `True`, если заголовок и описание были успешно отправлены, иначе `None`.
    """
    ...
```

**Назначение**: Отправляет заголовок и описание кампании в поле сообщения на Facebook.

**Параметры**:

- `d` (Driver): Экземпляр `Driver` для взаимодействия с веб-страницей.
- `category` (SimpleNamespace): Категория, содержащая заголовок и описание для отправки.

**Возвращает**:

- `bool`: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

**Пример**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Инициализация Driver
driver = Driver(...)

# Загрузка категории
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")

# Отправка заголовка
post_title(driver, category)
```

### `upload_media`

```python
def upload_media(d: Driver, products: List[SimpleNamespace], no_video: bool = False) -> bool:
    """
    Загружает медиафайлы на пост Facebook и обновляет их подписи.
    Args:
        d (Driver): Экземпляр `Driver` для взаимодействия с веб-страницей.
        products (List[SimpleNamespace]): Список продуктов, содержащих пути к медиафайлам.
        no_video (bool, optional): Флаг, указывающий, следует ли пропустить загрузку видео. По умолчанию `False`.

    Returns:
        bool: `True`, если медиафайлы были успешно загружены, иначе `None`.
    """
    ...
```

**Назначение**: Загружает медиафайлы на пост Facebook и обновляет их подписи.

**Параметры**:

- `d` (Driver): Экземпляр `Driver` для взаимодействия с веб-страницей.
- `products` (List[SimpleNamespace]): Список продуктов, содержащих пути к медиафайлам.
- `no_video` (bool, optional): Флаг, указывающий, следует ли пропустить загрузку видео. По умолчанию `False`.

**Возвращает**:

- `bool`: `True`, если медиафайлы были успешно загружены, иначе `None`.

**Пример**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Инициализация Driver
driver = Driver(...)

# Загрузка продуктов
products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]

# Загрузка медиа
upload_media(driver, products)
```

### `update_images_captions`

```python
def update_images_captions(d: Driver, products: List[SimpleNamespace], textarea_list: List[WebElement]) -> None:
    """
    Асинхронно добавляет описания к загруженным медиафайлам.
    Args:
        d (Driver): Экземпляр `Driver` для взаимодействия с веб-страницей.
        products (List[SimpleNamespace]): Список продуктов с деталями для обновления.
        textarea_list (List[WebElement]): Список текстовых полей, куда добавляются подписи.
    """
    ...
```

**Назначение**: Асинхронно добавляет описания к загруженным медиафайлам.

**Параметры**:

- `d` (Driver): Экземпляр `Driver` для взаимодействия с веб-страницей.
- `products` (List[SimpleNamespace]): Список продуктов с деталями для обновления.
- `textarea_list` (List[WebElement]): Список текстовых полей, куда добавляются подписи.

**Пример**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace
from selenium.webdriver.remote.webelement import WebElement

# Инициализация Driver
driver = Driver(...)

# Загрузка продуктов
products = [SimpleNamespace(description='Описание изображения', ...)]

# Получение списка текстовых полей (пример)
textarea_list = [WebElement(...)]

# Обновление подписей к изображениям
update_images_captions(driver, products, textarea_list)
```

### `promote_post`

```python
def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> bool:
    """
    Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.
    Args:
        d (Driver): Экземпляр `Driver` для взаимодействия с веб-страницей.
        category (SimpleNamespace): Детали категории, используемые для заголовка и описания поста.
        products (List[SimpleNamespace]): Список продуктов, содержащих медиа и детали для публикации.
        no_video (bool, optional): Флаг, указывающий, следует ли пропустить загрузку видео. По умолчанию `False`.

    Returns:
        bool: `True`, если пост был успешно продвинут, иначе `None`.
    """
    ...
```

**Назначение**: Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.

**Параметры**:

- `d` (Driver): Экземпляр `Driver` для взаимодействия с веб-страницей.
- `category` (SimpleNamespace): Детали категории, используемые для заголовка и описания поста.
- `products` (List[SimpleNamespace]): Список продуктов, содержащих медиа и детали для публикации.
- `no_video` (bool, optional): Флаг, указывающий, следует ли пропустить загрузку видео. По умолчанию `False`.

**Возвращает**:

- `bool`: `True`, если пост был успешно продвинут, иначе `None`.

**Пример**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Инициализация Driver
driver = Driver(...)

# Загрузка категории и продуктов
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]

# Продвижение поста
promote_post(driver, category, products)