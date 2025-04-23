# Документация для модуля `ChatgptFree.py`

## Описание
Модуль предоставляет асинхронный генератор для взаимодействия с моделью `gpt-4o-mini-2024-07-18` через сервис `chatgptfree.ai`. Он содержит класс `ChatgptFree`, который реализует функциональность асинхронного генератора и предоставляет методы для создания и обработки запросов к указанному сервису.

## Подробности
Модуль предназначен для использования в асинхронных приложениях, требующих генерации текста на основе предоставленных сообщений. Он автоматически получает необходимые идентификаторы (post_id и nonce) с веб-сайта `chatgptfree.ai` и отправляет запросы на генерацию текста.

## Содержание

- [Классы](#Классы)
    - [ChatgptFree](#ChatgptFree)
- [Методы классов](#Методы-классов)
    - [create_async_generator](#create_async_generator)

## Классы

### `ChatgptFree`
**Описание**: Класс `ChatgptFree` предоставляет реализацию асинхронного генератора для взаимодействия с сервисом `chatgptfree.ai`.

**Наследует**:
- `AsyncGeneratorProvider`: базовый класс для асинхронных провайдеров генераторов.
- `ProviderModelMixin`: примесь, предоставляющая общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL-адрес сервиса `chatgptfree.ai`.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `_post_id` (str | None): Идентификатор поста, необходимый для запросов.
- `_nonce` (str | None): Одноразовый код, необходимый для запросов.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini-2024-07-18`).
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей для удобства использования.

**Принцип работы**:
1. При первом вызове `create_async_generator` класс выполняет GET-запрос к `cls.url` для получения `_post_id` и `_nonce`.
2. Формируется запрос к `f"{cls.url}/wp-admin/admin-ajax.php"` с использованием полученных `_post_id` и `_nonce`, а также предоставленных сообщений.
3. Ответ от сервера обрабатывается построчно, извлекая контент из JSON-ответов и генерируя его как асинхронный поток.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 120,
    cookies: dict = None,
    **kwargs
) -> AsyncGenerator[str, None]:
    """
    Создает асинхронный генератор для получения ответов от сервиса `chatgptfree.ai`.

    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Максимальное время ожидания запроса в секундах. По умолчанию `120`.
        cookies (dict, optional): Куки для отправки с запросом. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncGenerator[str, None]: Асинхронный генератор, выдающий текстовые ответы от модели.

    Raises:
        RuntimeError: Если не удается найти `post_id` или `nonce` на веб-странице.
        Exception: Если возникает ошибка при выполнении HTTP-запроса.

    Как работает функция:
    1. Функция извлекает параметры `model`, `messages`, `proxy`, `timeout` и `cookies` из входных данных.
    2. Формирует HTTP-заголовки, необходимые для запроса к сервису `chatgptfree.ai`.
    3. Создает асинхронную сессию с использованием `StreamSession` для выполнения потоковых запросов.
    4. Проверяет, были ли уже получены `_nonce` и `_post_id`. Если нет, выполняет GET-запрос к главной странице `chatgptfree.ai` для их извлечения с использованием регулярных выражений.
    5. Формирует данные для POST-запроса, включая `_wpnonce`, `post_id`, `url`, `action`, `message` и `bot_id`.
    6. Отправляет POST-запрос к `chatgptfree.ai/wp-admin/admin-ajax.php` с использованием асинхронной сессии.
    7. Обрабатывает ответ построчно, извлекая данные JSON из каждой строки, начиная с `data:`.
    8. Извлекает содержимое (`content`) из JSON-ответа и передает его через генератор.
    9. Если возникает ошибка декодирования JSON, пропускает строку.
    10. После завершения потока проверяет наличие остаточного буфера (`buffer`) и пытается декодировать его как JSON.
    11. Если декодирование удается и в JSON-ответе есть ключ `data`, передает его через генератор.
    12. В случае неудачи декодирования выводит сообщение об ошибке.

    Внутренние функции:
    - Отсутствуют.

    Примеры:
        Пример 1: Создание асинхронного генератора с минимальными параметрами.
        ```python
        messages = [{"role": "user", "content": "Hello, world!"}]
        generator = ChatgptFree.create_async_generator(model="gpt-4o-mini-2024-07-18", messages=messages)
        ```

        Пример 2: Создание асинхронного генератора с использованием прокси и куки.
        ```python
        messages = [{"role": "user", "content": "Translate to French: Hello, world!"}]
        cookies = {"example_cookie": "value"}
        generator = ChatgptFree.create_async_generator(
            model="gpt-4o-mini-2024-07-18", messages=messages, proxy="http://proxy.example.com", cookies=cookies
        )
        ```

        Пример 3: Обработка асинхронного генератора.
        ```python
        import asyncio
        async def main():
            messages = [{"role": "user", "content": "Tell me a joke."}]
            generator = ChatgptFree.create_async_generator(model="gpt-4o-mini-2024-07-18", messages=messages)
            async for message in generator:
                print(message, end="")
        asyncio.run(main())
        ```
    """