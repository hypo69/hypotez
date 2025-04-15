# Модуль `Ylokh`

## Обзор

Модуль `Ylokh` предоставляет асинхронный генератор для взаимодействия с API `chat.ylokh.xyz`. Этот модуль предназначен для получения ответов от моделей, таких как `gpt-3.5-turbo`, в режиме стриминга или полной выдачи.

## Подробней

Модуль является частью проекта `hypotez` и предназначен для работы с API `chat.ylokh.xyz`. Он использует асинхронные запросы для получения ответов от моделей, таких как `gpt-3.5-turbo`. Модуль поддерживает стриминг ответов, а также полную выдачу ответа.
В модуле реализована поддержка прокси и таймаутов для запросов.

## Классы

### `Ylokh`

**Описание**:
Класс `Ylokh` является провайдером асинхронного генератора для работы с API `chat.ylokh.xyz`.

**Наследует**:
`AsyncGeneratorProvider` - базовый класс для асинхронных провайдеров генераторов.

**Атрибуты**:
- `url` (str): URL для взаимодействия с API (`https://chat.ylokh.xyz`).
- `working` (bool): Флаг, указывающий на работоспособность провайдера (по умолчанию `False`).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (по умолчанию `True`).
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo` (по умолчанию `True`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        proxy: str = None,
        timeout: int = 120,
        **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для получения ответов от API.

        Args:
            model (str): Название модели для запроса (например, "gpt-3.5-turbo").
            messages (Messages): Список сообщений для отправки в API.
            stream (bool, optional): Флаг для включения режима стриминга. По умолчанию `True`.
            proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
            timeout (int, optional): Время ожидания ответа от API в секундах. По умолчанию `120`.
            **kwargs: Дополнительные параметры для передачи в API.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий части ответа от API.

        Raises:
            Exception: Если возникает ошибка при запросе к API.

        Как работает функция:
        - Функция принимает параметры для запроса к API, такие как модель, сообщения, флаг стриминга, прокси и таймаут.
        - Формирует заголовки и данные для запроса.
        - Отправляет асинхронный POST-запрос к API `https://chatapi.ylokh.xyz/v1/chat/completions`.
        - Если включен режим стриминга, то функция итерируется по строкам ответа и извлекает содержимое из каждой строки.
        - Если режим стриминга выключен, то функция получает полный ответ в формате JSON и извлекает содержимое из него.
        """
```
#### **Параметры**:
- `model` (str): Название модели для запроса (например, "gpt-3.5-turbo").
- `messages` (Messages): Список сообщений для отправки в API.
- `stream` (bool, optional): Флаг для включения режима стриминга. По умолчанию `True`.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания ответа от API в секундах. По умолчанию `120`.
- `**kwargs`: Дополнительные параметры для передачи в API.

#### **Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий части ответа от API.

#### **Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for message in Ylokh.create_async_generator(model="gpt-3.5-turbo", messages=messages):
    print(message)
```
```python
# Пример использования create_async_generator с прокси
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for message in Ylokh.create_async_generator(model="gpt-3.5-turbo", messages=messages, proxy="http://your_proxy:8080"):
    print(message)
```
```python
# Пример использования create_async_generator с таймаутом
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for message in Ylokh.create_async_generator(model="gpt-3.5-turbo", messages=messages, timeout=60):
    print(message)
```