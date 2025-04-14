# Модуль WhiteRabbitNeo для g4f

## Обзор

Модуль `WhiteRabbitNeo` представляет собой асинхронный провайдер генерации текста, взаимодействующий с сервисом `whiterabbitneo.com`. Он предназначен для работы с сообщениями и поддерживает использование cookies для аутентификации. Этот модуль требует аутентификации и поддерживает историю сообщений.

## Подробней

Модуль является частью системы `g4f` и служит для интеграции с платформой `WhiteRabbitNeo` для генерации текста на основе предоставленных сообщений. Он использует асинхронные запросы для взаимодействия с API `WhiteRabbitNeo`.

## Классы

### `WhiteRabbitNeo`

**Описание**: Класс `WhiteRabbitNeo` является асинхронным провайдером, который взаимодействует с сервисом `WhiteRabbitNeo` для генерации текста.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL сервиса `WhiteRabbitNeo` ("https://www.whiterabbitneo.com").
- `working` (bool): Указывает, работает ли провайдер (в данном случае `True`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (`True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с провайдером (`True`).

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от сервиса `WhiteRabbitNeo`.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        cookies: Cookies = None,
        connector: BaseConnector = None,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для получения ответов от сервиса `WhiteRabbitNeo`.

        Args:
            model (str): Модель, используемая для генерации текста.
            messages (Messages): Список сообщений для отправки в сервис.
            cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
            connector (BaseConnector, optional): Объект коннектора для управления подключением. По умолчанию `None`.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий части ответа от сервиса.

        Raises:
            Exception: Если возникает ошибка при взаимодействии с сервисом.

        Как работает функция:
        - Проверяет наличие cookies, и если их нет, получает их с домена `www.whiterabbitneo.com`.
        - Формирует заголовки запроса, включая User-Agent, Accept, Referer и другие необходимые параметры.
        - Создает сессию `ClientSession` с заданными заголовками, cookies и коннектором.
        - Формирует данные запроса в формате JSON, включая сообщения, идентификатор и флаги.
        - Отправляет POST-запрос к API `WhiteRabbitNeo` (`/api/chat`) с данными и прокси (если указан).
        - Обрабатывает ответ от сервера, проверяя статус код.
        - Итерируется по частям содержимого ответа и декодирует их, выдавая в виде генератора.

        Внутренние функции:
        - Нет внутренних функций

        Примеры:
            # Пример использования асинхронного генератора
            async def main():
                messages = [{"role": "user", "content": "Hello, how are you?"}]
                async for chunk in WhiteRabbitNeo.create_async_generator(model="default", messages=messages):
                    print(chunk, end="")

            if __name__ == "__main__":
                import asyncio
                asyncio.run(main())
        """
        ...
```

## Параметры класса

- `url` (str): URL сервиса `WhiteRabbitNeo`.
- `working` (bool): Индикатор работоспособности провайдера.
- `supports_message_history` (bool): Поддержка истории сообщений.
- `needs_auth` (bool): Необходимость аутентификации.

## Примеры

Пример использования класса `WhiteRabbitNeo` для создания асинхронного генератора и получения ответов от сервиса:

```python
# Пример использования асинхронного генератора
async def main():
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for chunk in WhiteRabbitNeo.create_async_generator(model="default", messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())