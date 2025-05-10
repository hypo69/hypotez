# Сценарий асинхронной публикации сообщения на Facebook

## Содержание

- [Обзор](#обзор)
- [Основные возможности](#основные-возможности)
- [Структура модуля](#структура-модуля)
- [Легенда](#легенда)
- [Функции](#функции)
  - [`post_title(d: Driver, category: SimpleNamespace) -> bool`](#post_titled-driver-category-simplenamespace-bool)
  - [`upload_media(d: Driver, products: List[SimpleNamespace], no_video: bool = False) -> bool`](#upload_mediad-driver-products-listsimplenamespace-no_video-bool-false-bool)
  - [`update_images_captions(d: Driver, products: List[SimpleNamespace], textarea_list: List[WebElement]) -> None`](#update_images_captionsd-driver-products-listsimplenamespace-textarea_list-listwebelement-none)
  - [`promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> bool`](#promote_postd-driver-category-simplenamespace-products-listsimplenamespace-no_video-bool-false-bool)
- [Использование](#использование)
  - [Пример](#пример)
- [Зависимости](#зависимости)
- [Обработка ошибок](#обработка-ошибок)
- [Вклад](#вклад)
- [Лицензия](#лицензия)

## Обзор

Этот скрипт является частью директории `hypotez/src/endpoints/advertisement/facebook/scenarios` и предназначен для автоматизации процесса публикации сообщений на Facebook. Скрипт взаимодействует со страницей Facebook, используя локаторы для выполнения различных действий, таких как отправка сообщений, загрузка медиафайлов и обновление подписей.

## Основные возможности

1. **Отправка заголовка и описания**: Отправляет заголовок и описание кампании в поле сообщения на Facebook.
2. **Загрузка медиафайлов**: Загружает медиафайлы (изображения и видео) на пост Facebook и обновляет их подписи.
3. **Продвижение поста**: Управляет всем процессом продвижения поста с заголовком, описанием и медиафайлами.

## Структура модуля

```mermaid
graph TD
    Start[Начало] --> InitDriver[Инициализация Driver]
    InitDriver --> LoadCategoryAndProducts[Загрузка категории и товаров]
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

## Легенда

1. **Start**: Начало выполнения скрипта.
2. **InitDriver**: Создание экземпляра класса `Driver`.
3. **LoadCategoryAndProducts**: Загрузка данных категории и товаров.
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

-----------------------

#### Функции

- **`post_title(d: Driver, category: SimpleNamespace) -> bool`**:
  - **Назначение**: Отправляет заголовок и описание кампании в поле сообщения на Facebook.
  - **Параметры**:
    - `d`: Экземпляр `Driver` для взаимодействия с веб-страницей.
    - `category`: Категория, содержащая заголовок и описание для отправки.
  - **Возвращает**: `True`, если заголовок и описание были успешно отправлены, иначе `None`.

- **`upload_media(d: Driver, products: List[SimpleNamespace], no_video: bool = False) -> bool`**:
  - **Назначение**: Загружает медиафайлы на пост Facebook и обновляет их подписи.
  - **Параметры**:
    - `d`: Экземпляр `Driver` для взаимодействия с веб-страницей.
    - `products`: Список товаров, содержащих пути к медиафайлам.
    - `no_video`: Флаг, указывающий, следует ли пропустить загрузку видео.
  - **Возвращает**: `True`, если медиафайлы были успешно загружены, иначе `None`.

- **`update_images_captions(d: Driver, products: List[SimpleNamespace], textarea_list: List[WebElement]) -> None`**:
  - **Назначение**: Асинхронно добавляет описания к загруженным медиафайлам.
  - **Параметры**:
    - `d`: Экземпляр `Driver` для взаимодействия с веб-страницей.
    - `products`: Список товаров с деталями для обновления.
    - `textarea_list`: Список текстовых полей, куда добавляются подписи.

- **`promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> bool`**:
  - **Назначение**: Управляет процессом продвижения поста с заголовком, описанием и медиафайлами.
  - **Параметры**:
    - `d`: Экземпляр `Driver` для взаимодействия с веб-страницей.
    - `category`: Детали категории, используемые для заголовка и описания поста.
    - `products`: Список товаров, содержащих медиа и детали для публикации.
    - `no_video`: Флаг, указывающий, следует ли пропустить загрузку видео.
  - **Возвращает**: `True`, если пост был успешно продвинут, иначе `None`.

## Использование

Для использования этого скрипта выполните следующие шаги:

1. **Инициализация Driver**: Создайте экземпляр класса `Driver`.
2. **Загрузка локаторов**: Загрузите локаторы из JSON-файла.
3. **Вызов функций**: Используйте предоставленные функции для отправки заголовка, загрузки медиа и продвижения поста.

#### Пример

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Инициализация Driver
driver = Driver(...)

# Загрузка категории и товаров
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg', ...)]

# Отправка заголовка
post_title(driver, category)

# Загрузка медиа и продвижение поста
await promote_post(driver, category, products)
```

## Зависимости

- `selenium`: Для веб-автоматизации.
- `asyncio`: Для асинхронных операций.
- `pathlib`: Для обработки путей к файлам.
- `types`: Для создания простых пространств имен.
- `typing`: Для аннотаций типов.

## Обработка ошибок

Скрипт включает надежную обработку ошибок, чтобы обеспечить продолжение выполнения даже в случае, если некоторые элементы не найдены или если возникли проблемы с веб-страницей. Это особенно полезно для обработки динамических или нестабильных веб-страниц.

## Вклад

Вклад в этот скрипт приветствуется. Пожалуйста, убедитесь, что любые изменения хорошо документированы и включают соответствующие тесты.

## Лицензия

Этот скрипт лицензирован под MIT License. Подробности смотрите в файле `LICENSE`.