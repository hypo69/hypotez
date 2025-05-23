# Модуль `MagickPen.py`

## Обзор

Модуль предоставляет класс `MagickPen`, который является асинхронным генератором для взаимодействия с API MagickPen.com.
Он предназначен для получения ответов от языковой модели GPT-4o-mini. Модуль поддерживает потоковую передачу ответов, системные сообщения и историю сообщений.

## Подробней

Модуль извлекает необходимые API credentials из JavaScript файла на сайте MagickPen.com.
Далее, модуль отправляет запрос к API и возвращает ответ в виде асинхронного генератора.

## Классы

### `MagickPen`

**Описание**: Класс для взаимодействия с API MagickPen.com.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сайта MagickPen.com.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Поддерживает ли потоковую передачу ответов.
- `supports_system_message` (bool): Поддерживает ли системные сообщения.
- `supports_message_history` (bool): Поддерживает ли историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini`).
- `models` (list): Список поддерживаемых моделей (`gpt-4o-mini`).

**Методы**:
- `fetch_api_credentials()`: Асинхронно извлекает API credentials.
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от API.

## Методы класса

### `fetch_api_credentials`

```python
    @classmethod
    async def fetch_api_credentials(cls) -> tuple:
        """
        Асинхронно извлекает API credentials из JavaScript файла.

        Returns:
            tuple: Кортеж, содержащий `X_API_SECRET`, `signature`, `timestamp`, `nonce` и `secret`.

        Raises:
            Exception: Если не удается извлечь все необходимые данные из JavaScript файла.
        """
        ...
```

**Назначение**: Извлечение учетных данных API, необходимых для аутентификации запросов к MagickPen.

**Как работает функция**:
1. **Определение URL**: Указывается URL JavaScript файла, содержащего необходимые секреты и параметры.
2. **Выполнение GET-запроса**: Отправляет асинхронный GET-запрос к указанному URL для получения содержимого JavaScript файла.
3. **Поиск `X-API-Secret`**: Использует регулярное выражение для поиска значения переменной `X-API-Secret` в полученном тексте.
4. **Генерация параметров**: Генерирует параметры `timestamp` (текущее время в миллисекундах) и `nonce` (случайное число).
5. **Создание подписи**: Создает строку для подписи, объединяя фиксированную строку, `timestamp` и `nonce`, сортирует ее, а затем вычисляет MD5-хеш этой строки.
6. **Поиск `secret`**: Использует регулярное выражение для поиска значения переменной `secret` в полученном тексте.
7. **Возврат учетных данных**: Возвращает кортеж, содержащий `X_API_SECRET`, `signature`, `timestamp`, `nonce` и `secret`.
8. **Обработка ошибок**: Если какой-либо из параметров не найден, вызывается исключение `Exception` с сообщением об ошибке.

**Примеры**:

```python
# Пример вызова метода
X_API_SECRET, signature, timestamp, nonce, secret = await MagickPen.fetch_api_credentials()
print(f"X_API_SECRET: {X_API_SECRET}")
print(f"signature: {signature}")
print(f"timestamp: {timestamp}")
print(f"nonce: {nonce}")
print(f"secret: {secret}")
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от API.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API.
        """
        ...
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API MagickPen и получения ответов на основе предоставленных сообщений.

**Как работает функция**:
1. **Выбор модели**: Получает название модели с помощью `cls.get_model(model)`.
2. **Получение учетных данных**: Вызывает метод `cls.fetch_api_credentials()` для получения необходимых API credentials.
3. **Формирование заголовков**: Создает словарь `headers` с необходимыми заголовками для запроса, включая учетные данные и параметры.
4. **Создание сессии**: Создает асинхронную сессию с использованием `aiohttp.ClientSession` и переданных заголовков.
5. **Форматирование промпта**: Форматирует сообщения с помощью функции `format_prompt(messages)` для подготовки запроса к API.
6. **Формирование payload**: Создает словарь `payload` с данными для отправки, включая отформатированный промпт и другие параметры.
7. **Отправка запроса**: Отправляет асинхронный POST-запрос к API endpoint (`cls.api_endpoint`) с использованием созданной сессии, `payload` и прокси (если указан).
8. **Обработка ответа**: Проходит по чанкам ответа от сервера и декодирует каждый чанк, передавая его в генератор.
9. **Обработка ошибок**: В случае ошибки при отправке запроса или обработке ответа, логирует ошибку.

**Примеры**:

```python
# Пример вызова метода
async for chunk in MagickPen.create_async_generator(model="gpt-4o-mini", messages=[{"role": "user", "content": "Hello"}], proxy=None):
    print(chunk)