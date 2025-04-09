# Модуль `MyShell`

## Обзор

Модуль `MyShell` предоставляет класс `MyShell`, который является провайдером для взаимодействия с API MyShell AI. Он поддерживает модели GPT-3.5 Turbo и потоковую передачу данных. Этот модуль предназначен для отправки запросов к MyShell AI и получения ответов, используя веб-драйвер для обхода Cloudflare защиты.

## Подробнее

Модуль `MyShell` интегрируется в систему `hypotez` как один из провайдеров для доступа к различным AI-моделям. Он использует веб-драйвер для обхода защиты Cloudflare и отправки запросов к API MyShell AI.

## Классы

### `MyShell`

**Описание**: Класс `MyShell` является реализацией абстрактного провайдера `AbstractProvider` и предоставляет функциональность для взаимодействия с API MyShell AI.

**Наследует**:
- `AbstractProvider`: Абстрактный класс, определяющий интерфейс для всех провайдеров в системе `hypotez`.

**Атрибуты**:
- `url` (str): URL-адрес для взаимодействия с MyShell AI.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.

**Методы**:
- `create_completion`: Отправляет запрос к MyShell AI и возвращает результат.

## Функции

### `create_completion`

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    timeout: int = 120,
    webdriver = None,
    **kwargs
) -> CreateResult:
    """
    Отправляет запрос к MyShell AI и возвращает результат.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        stream (bool): Указывает, использовать ли потоковую передачу данных.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
        webdriver:  Инстанс веб-драйвера для выполнения JavaScript кода в браузере.
        **kwargs: Дополнительные аргументы.

    Returns:
        CreateResult: Результат выполнения запроса.

    Как работает функция:
    1. Инициализация сессии веб-драйвера с использованием `WebDriverSession`.
    2. Обход защиты Cloudflare с использованием функции `bypass_cloudflare`.
    3. Формирование данных для отправки в API MyShell AI.
    4. Выполнение JavaScript-кода для отправки запроса и получения ответа.
    5. Извлечение данных из потока ответов и возвращение результата.

    ASII flowchart:

    A [Инициализация сессии веб-драйвера]
    ↓
    B [Обход защиты Cloudflare]
    ↓
    C [Формирование данных для запроса]
    ↓
    D [Отправка запроса через JavaScript]
    ↓
    E [Получение потока ответов]
    ↓
    F [Извлечение данных из потока]
    ↓
    G [Возврат результата]

    Примеры:
        model = "gpt-3.5-turbo"
        messages = [{"role": "user", "content": "Hello, MyShell!"}]
        stream = True
        proxy = None
        timeout = 120

        result = MyShell.create_completion(
            model=model,
            messages=messages,
            stream=stream,
            proxy=proxy,
            timeout=timeout,
            webdriver=webdriver
        )
    """
    ...