# Модуль `Goabror`

## Обзор

Модуль предоставляет класс `Goabror`, который является асинхронным генератором для взаимодействия с API Goabror.uz. Он позволяет получать ответы от модели `gpt-4` на основе переданных сообщений. Модуль использует `aiohttp` для асинхронных HTTP-запросов и включает функциональность для обработки и форматирования запросов и ответов.

## Подробней

Этот модуль предназначен для интеграции с сервисом Goabror.uz, предоставляющим доступ к модели `gpt-4`. Он формирует запросы к API, отправляет их и обрабатывает ответы, возвращая результаты в виде асинхронного генератора. Это позволяет эффективно обрабатывать большие объемы данных и асинхронно взаимодействовать с API.

## Классы

### `Goabror`

**Описание**: Класс `Goabror` является провайдером, который взаимодействует с API Goabror.uz для получения ответов от модели `gpt-4`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Аттрибуты**:
- `url` (str): URL сайта Goabror.uz.
- `api_endpoint` (str): URL API для взаимодействия с моделью.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4`).
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Асинхронный генератор для получения ответов от API.

## Функции

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
        Создает асинхронный генератор для получения ответов от API Goabror.uz.

        Args:
            model (str): Название модели для использования.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API.

        Как работает функция:
        1.  Формирует заголовки HTTP-запроса, включая `accept`, `accept-language` и `user-agent`.
        2.  Создает асинхронную сессию `ClientSession` с заданными заголовками.
        3.  Формирует параметры запроса, включая `user` (отформатированные сообщения) и `system` (системное сообщение).
        4.  Отправляет GET-запрос к API с использованием `session.get`.
        5.  Обрабатывает ответ, проверяет статус и извлекает текстовое содержимое.
        6.  Пытается декодировать JSON-ответ, и если успешно, извлекает данные из поля `data`.
        7.  Если JSON-декодирование не удается, возвращает текст ответа как есть.
        8.  Генерирует результаты ответа с использованием `yield`.

        ASCII flowchart:

        Начало
        ↓
        Создание заголовков HTTP-запроса
        ↓
        Создание асинхронной сессии ClientSession
        ↓
        Формирование параметров запроса
        ↓
        Отправка GET-запроса к API
        ↓
        Обработка ответа и извлечение содержимого
        ↓
        Попытка декодирования JSON-ответа
        ├── Успешно → Извлечение данных из поля data
        │   ↓
        └── Не успешно → Возврат текста ответа
        ↓
        Генерация результатов ответа
        ↓
        Конец

        Примеры:
            Пример 1: Базовый вызов функции
            >>> async for response in Goabror.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Hello'}]):
            ...     print(response)

            Пример 2: Использование прокси
            >>> async for response in Goabror.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Hello'}], proxy='http://proxy.example.com'):
            ...     print(response)
        """
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }
        async with ClientSession(headers=headers) as session:
            params = {
                "user": format_prompt(messages, include_system=False),
                "system": get_system_prompt(messages),
            }
            async with session.get(f"{cls.api_endpoint}", params=params, proxy=proxy) as response:
                await raise_for_status(response)
                text_response = await response.text()
                try:
                    json_response = json.loads(text_response)
                    if "data" in json_response:
                        yield json_response["data"]
                    else:
                        yield text_response
                except json.JSONDecodeError:
                    yield text_response