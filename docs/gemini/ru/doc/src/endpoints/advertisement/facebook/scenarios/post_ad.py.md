# Модуль `post_ad`

## Обзор

Модуль `post_ad.py` предназначен для автоматизации процесса публикации рекламных сообщений в группах Facebook. Он содержит функцию `post_ad`, которая выполняет основные шаги по отправке сообщения, загрузке медиа (если есть) и публикации объявления.

## Подробней

Этот модуль является частью системы автоматизации рекламы в Facebook проекта `hypotez`. Он использует `selenium` для взаимодействия с веб-интерфейсом Facebook, выполняя действия, необходимые для создания и публикации рекламных постов.

## Функции

### `post_ad`

```python
def post_ad(d: Driver, message:SimpleNamespace) -> bool:
    """ Sends the title of event.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        event (SimpleNamespace): The event containing the title, data of event and description to be sent.

    Returns:
        bool: `True` if the title and description were sent successfully, otherwise `None`.

    Examples:
        >>> driver = Driver(...)
        >>> event = SimpleNamespace(title="Campaign Title", description="Event Description")
        >>> post_title(driver, event)
        True
    """
```

**Назначение**: Отправляет рекламное сообщение в Facebook.

**Параметры**:

-   `d` (Driver): Инстанс драйвера, используемый для взаимодействия с веб-страницей.
-   `message` (SimpleNamespace): Объект, содержащий данные сообщения, такие как описание и путь к изображению.

**Возвращает**:

-   `bool`: `True`, если сообщение успешно отправлено и опубликовано, иначе `None`.

**Как работает функция**:

1.  **Отправка заголовка сообщения**: Функция вызывает `post_message_title` для отправки заголовка сообщения. В случае неудачи увеличивает счетчик `fails` и, если количество неудач превышает 15, завершает работу.
2.  **Загрузка медиа**: Если у сообщения есть путь к изображению (`image_path`), функция вызывает `upload_post_media` для загрузки медиафайла.
3.  **Публикация сообщения**: Функция вызывает `message_publish` для фактической публикации сообщения.
4.  **Сброс счетчика ошибок**: При успешной публикации счетчик `fails` сбрасывается.

**Внутренние функции**: Нет

**Примеры**:

```python
from src.webdriver.driver import Driver
from types import SimpleNamespace

# Создание инстанса драйвера (пример с Firefox)
driver = Driver(Firefox)

# Создание объекта сообщения
message = SimpleNamespace(description="Пример рекламного сообщения", image_path="/path/to/image.jpg")

# Вызов функции post_ad
result = post_ad(driver, message)
print(result)  # Выведет True, если публикация прошла успешно
```

```ascii
Отправка заголовка сообщения
│
├── Успешно: Загрузка медиа (если есть)
│   │
│   └── Успешно: Публикация сообщения
│       │
│       └── Сброс счетчика ошибок
│
└── Неудача: Увеличение счетчика ошибок
    │
    └── Превышено количество попыток: Завершение