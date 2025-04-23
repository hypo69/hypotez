# Модуль `post_ad`

## Обзор

Модуль `post_ad` предназначен для автоматической публикации рекламных сообщений в группах Facebook с использованием Selenium WebDriver. Он содержит функции для отправки заголовка сообщения, загрузки медиа-контента и публикации сообщения.

## Подробней

Этот модуль является частью системы для автоматизации рекламных публикаций. Он использует драйвер веб-браузера для взаимодействия с Facebook и выполняет шаги, необходимые для создания и публикации рекламного объявления. Основная цель модуля - упростить и автоматизировать процесс размещения рекламы в Facebook.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `post_ad`

```python
def post_ad(d: Driver, message: SimpleNamespace) -> bool:
    """
    Функция отправляет рекламное сообщение, состоящее из заголовка и медиафайлов, в Facebook.

    Args:
        d (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
        message (SimpleNamespace): Объект, содержащий данные для публикации сообщения, включая описание и путь к изображению.

    Returns:
        bool: `True`, если сообщение успешно опубликовано, иначе `False`.

    Raises:
        Exception: Если происходит ошибка во время отправки заголовка, загрузки медиа или публикации сообщения.

    Example:
        >>> driver = Driver(...)
        >>> message = SimpleNamespace(description="Описание рекламного сообщения", image_path="/path/to/image.jpg")
        >>> post_ad(driver, message)
        True
    """

    global fails

    def post_message_title(d: Driver, message: str) -> bool:
        """
        Функция отправляет заголовок сообщения.

        Args:
            d (Driver): Инстанс драйвера.
            message (str): Текст заголовка сообщения.

        Returns:
            bool: `True`, если заголовок успешно отправлен, иначе `False`.

        Raises:
            Exception: Если происходит ошибка при отправке заголовка сообщения.

        Example:
            >>> driver = Driver(...)
            >>> post_message_title(driver, "Заголовок сообщения")
            True
        """
        ...
    
    def upload_post_media(d: Driver, media: str, without_captions: bool = True) -> bool:
        """
        Функция загружает медиа-контент для сообщения.

        Args:
            d (Driver): Инстанс драйвера.
            media (str): Путь к медиафайлу.
            without_captions (bool): Флаг, указывающий, нужно ли использовать подписи.

        Returns:
            bool: `True`, если медиафайл успешно загружен, иначе `False`.

        Raises:
            Exception: Если происходит ошибка при загрузке медиафайла.

        Example:
            >>> driver = Driver(...)
            >>> upload_post_media(driver, "/path/to/image.jpg")
            True
        """
        ...

    def message_publish(d: Driver) -> bool:
        """
        Функция публикует сообщение.

        Args:
            d (Driver): Инстанс драйвера.

        Returns:
            bool: `True`, если сообщение успешно опубликовано, иначе `False`.

        Raises:
            Exception: Если происходит ошибка при публикации сообщения.

        Example:
            >>> driver = Driver(...)
            >>> message_publish(driver)
            True
        """
        ...
    if not post_message_title(d, f"{ message.description}" ):
        logger.error("Failed to send event title", exc_info=False)
        fails += 1
        if fails < 15:
            print(f"{fails=}")
            return
        else:
            ...

    time.sleep(1)
    if hasattr(message, 'image_path') and message.image_path:
        if not upload_post_media(d, media = message.image_path, without_captions = True):
            return

    if not message_publish(d):
        return
    fails = 0
    return True
```

**Назначение**:
Функция `post_ad` отправляет рекламное сообщение, включающее заголовок и медиафайлы, в Facebook.

**Параметры**:
- `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей Facebook.
- `message` (SimpleNamespace): Объект, содержащий данные для публикации сообщения, включая описание и путь к изображению.

**Возвращает**:
- `bool`: `True`, если сообщение успешно опубликовано, иначе `False`.

**Вызывает исключения**:
- Отсутствуют явные исключения, но могут возникать исключения внутри вызываемых функций `post_message_title`, `upload_post_media` и `message_publish`.

**Внутренние функции**:
- `post_message_title`: Отправляет заголовок сообщения.
- `upload_post_media`: Загружает медиа-контент для сообщения.
- `message_publish`: Публикует сообщение.

**Как работает функция**:
1. Отправляет заголовок сообщения, используя функцию `post_message_title`.
2. Если отправка заголовка не удалась, регистрирует ошибку и увеличивает счетчик неудачных попыток (`fails`).
3. Если количество неудачных попыток превышает 15, возвращает `None`.
4. Делает паузу на 1 секунду.
5. Если в объекте `message` присутствует атрибут `image_path` и он не пустой, загружает медиафайл с помощью функции `upload_post_media`.
6. Публикует сообщение с помощью функции `message_publish`.
7. Сбрасывает счетчик неудачных попыток (`fails`) в 0.
8. Возвращает `True`, если все операции выполнены успешно.

**Примеры**:
```python
driver = Driver(Chrome)
message = SimpleNamespace(description="Рекламное сообщение", image_path="/path/to/image.jpg")
result = post_ad(driver, message)
if result:
    print("Сообщение успешно опубликовано")
else:
    print("Не удалось опубликовать сообщение")
```

## Параметры модуля

- `locator` (SimpleNamespace): Объект, содержащий локаторы элементов веб-страницы Facebook, загруженные из JSON-файла.
- `fails` (int): Глобальная переменная, используемая для подсчета количества неудачных попыток публикации сообщения.