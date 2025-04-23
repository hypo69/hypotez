# Модуль Reka

## Обзор

Модуль `Reka` предоставляет интерфейс для взаимодействия с провайдером `Reka` (space.reka.ai) для создания завершений текста и обработки изображений. Этот модуль является частью проекта `hypotez` и предназначен для интеграции с различными AI-моделями.

## Более подробно

Модуль `Reka` предназначен для работы с платформой `space.reka.ai`. Он поддерживает создание текстовых завершений и загрузку изображений для использования в запросах. Модуль требует аутентификации и использует cookies для поддержания сессии.

## Классы

### `Reka`

**Описание**: Класс `Reka` является подклассом `AbstractProvider` и предоставляет методы для взаимодействия с API `Reka`.

**Наследует**:
- `AbstractProvider`: Абстрактный класс, определяющий интерфейс для всех провайдеров.

**Атрибуты**:
- `domain` (str): Доменное имя `space.reka.ai`.
- `url` (str): URL для взаимодействия с `Reka`.
- `working` (bool): Указывает, работает ли провайдер.
- `needs_auth` (bool): Указывает, требуется ли аутентификация.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `default_vision_model` (str): Модель, используемая по умолчанию для обработки изображений.
- `cookies` (dict): Cookies для аутентификации.
- `proxy` (str): Прокси-сервер для выполнения запросов.

**Методы**:
- `create_completion()`: Создает завершение текста на основе предоставленных сообщений.
- `upload_image()`: Загружает изображение на сервер `Reka`.
- `get_access_token()`: Получает токен доступа для аутентификации.

## Методы класса

### `create_completion`

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    api_key: str = None,
    image: ImageType = None,
    **kwargs
) -> CreateResult:
    """Создает завершение текста на основе предоставленных сообщений, используя API Reka.

    Args:
        cls (Reka): Класс Reka.
        model (str): Модель для генерации текста.
        messages (Messages): Список сообщений для отправки.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
        proxy (str, optional): Прокси-сервер для выполнения запросов. По умолчанию `None`.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        image (ImageType, optional): Изображение для отправки. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        CreateResult: Результат создания завершения текста.

    Raises:
        ValueError: Если не найдены cookies или отсутствует `appSession` в cookies.

    Как работает функция:
    - Функция `create_completion` сначала проверяет наличие API-ключа. Если он отсутствует, она пытается получить cookies для домена `Reka`.
    - Если cookies не найдены или в них отсутствует `appSession`, выбрасывается исключение `ValueError`.
    - Если API-ключ не предоставлен, функция пытается получить его с помощью метода `get_access_token`.
    - Затем формируется список сообщений для отправки в формате, ожидаемом API `Reka`.
    - Если предоставлено изображение, оно загружается на сервер с помощью метода `upload_image`, и URL изображения добавляется в последнее сообщение.
    - Формируются заголовки запроса, включая токен авторизации.
    - Отправляется POST-запрос к API `Reka` с использованием `requests.post`.
    - Функция итерирует по ответам сервера и извлекает текст из каждого ответа, возвращая его как часть потока.
    """
    ...
```

**Примеры**:

```python
# Пример вызова функции create_completion
messages = [{"role": "user", "content": "Привет, как дела?"}]
result = Reka.create_completion(model="reka-core", messages=messages, stream=True)
for token in result:
    print(token)
```

### `upload_image`

```python
def upload_image(cls, access_token, image: ImageType) -> str:
    """Загружает изображение на сервер Reka и возвращает URL изображения.

    Args:
        cls (Reka): Класс Reka.
        access_token (str): Токен доступа для аутентификации.
        image (ImageType): Изображение для загрузки.

    Returns:
        str: URL загруженного изображения.

    Как работает функция:
    - Функция `upload_image` генерирует случайный токен `boundary_token` для разделения данных в multipart/form-data запросе.
    - Формируются заголовки запроса, включая токен авторизации и content-type.
    - Изображение преобразуется в байты с помощью функции `to_bytes`.
    - Формируется тело запроса в формате multipart/form-data, включающее данные изображения.
    - Отправляется POST-запрос к API `Reka` для загрузки изображения.
    - Функция возвращает URL загруженного изображения из JSON-ответа.
    """
    ...
```

**Примеры**:

```python
# Пример вызова функции upload_image
access_token = "test_token"
image_path = "path/to/image.png"  # <Замените image_path на реальный путь к изображению>
with open(image_path, "rb") as file:
    image_data = file.read()
image_url = Reka.upload_image(access_token, image_data)
print(image_url)
```

### `get_access_token`

```python
def get_access_token(cls):
    """Получает токен доступа для аутентификации.

    Args:
        cls (Reka): Класс Reka.

    Returns:
        str: Токен доступа.

    Raises:
        ValueError: Если не удалось получить токен доступа.

    Как работает функция:
    - Функция `get_access_token` формирует заголовки запроса.
    - Отправляется GET-запрос к API `Reka` для получения токена доступа.
    - Функция возвращает токен доступа из JSON-ответа.
    - Если запрос не удался, выбрасывается исключение `ValueError`.
    """
    ...
```

**Примеры**:

```python
# Пример вызова функции get_access_token
try:
    access_token = Reka.get_access_token()
    print(access_token)
except ValueError as ex:
    print(f"Ошибка получения токена доступа: {ex}")
```

## Параметры класса

- `domain` (str): Доменное имя `space.reka.ai`.
- `url` (str): URL для взаимодействия с `Reka`.
- `working` (bool): Указывает, работает ли провайдер.
- `needs_auth` (bool): Указывает, требуется ли аутентификация.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `default_vision_model` (str): Модель, используемая по умолчанию для обработки изображений.
- `cookies` (dict): Cookies для аутентификации.