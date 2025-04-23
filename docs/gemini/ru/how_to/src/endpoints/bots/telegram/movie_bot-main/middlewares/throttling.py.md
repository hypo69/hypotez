### Как использовать ThrottlingMiddleware
=========================================================================================

Описание
-------------------------
`ThrottlingMiddleware` - это middleware для aiogram, который реализует механизм ограничения скорости обработки сообщений от пользователей. Он предотвращает злоупотребление ботом, ограничивая количество запросов от одного и того же пользователя в течение определенного времени.

Шаги выполнения
-------------------------
1. **Инициализация**: При создании экземпляра `ThrottlingMiddleware` указывается `time_limit` (в секундах), который определяет, как часто пользователь может отправлять сообщения. По умолчанию установлено значение 2 секунды.
2. **Проверка**: При получении нового сообщения middleware проверяет, есть ли `chat.id` пользователя в кэше `self.limit`.
3. **Ограничение**: Если `chat.id` пользователя уже есть в кэше, это означает, что пользователь недавно отправлял сообщение, и middleware не передает сообщение дальше для обработки.
4. **Добавление в кэш**: Если `chat.id` пользователя отсутствует в кэше, это означает, что пользователь еще не отправлял сообщений в течение установленного времени, и `chat.id` добавляется в кэш.
5. **Обработка**: После добавления `chat.id` в кэш сообщение передается следующему обработчику.

Пример использования
-------------------------

```python
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int = 2) -> None:
        """
        Инициализирует middleware для ограничения скорости обработки сообщений.

        Args:
            time_limit (int, optional): Время в секундах, в течение которого сообщения от одного пользователя ограничиваются. По умолчанию 2 секунды.
        """
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Выполняет проверку и ограничение скорости обработки сообщений.

        Args:
            handler (Callable[[Message, Dict[str, Any]], Awaitable[Any]]): Следующий обработчик сообщения.
            event (Message): Объект сообщения от пользователя.
            data (Dict[str, Any]): Дополнительные данные.

        Returns:
            Any: Результат обработки сообщения следующим обработчиком.
        """
        if event.chat.id in self.limit:
            return  # Игнорируем сообщение, если пользователь отправил его слишком быстро
        else:
            self.limit[event.chat.id] = None  # Добавляем пользователя в кэш
        return await handler(event, data)  # Передаем сообщение следующему обработчику


# Пример использования в aiogram:
async def main():
    # from aiogram import Bot, Dispatcher
    # Вместо этого используйте:
    from aiogram import Bot

    TOKEN = "YOUR_BOT_TOKEN"
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрация middleware
    dp.message.middleware(ThrottlingMiddleware(time_limit=2))

    # Другие обработчики и запуск бота
    # ...

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())