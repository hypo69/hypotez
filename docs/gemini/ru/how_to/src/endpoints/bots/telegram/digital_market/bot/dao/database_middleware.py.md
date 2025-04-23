### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует middleware для интеграции базы данных в боты Telegram, использующие библиотеку aiogram. Он создает и управляет сессиями базы данных, обеспечивая их доступность в обработчиках (handlers) и автоматическое выполнение операций commit или rollback в зависимости от типа middleware.

Шаги выполнения
-------------------------
1. **Определение базового класса `BaseDatabaseMiddleware`**:
   - Этот класс является базовым для всех middleware, работающих с базой данных.
   - Метод `__call__` создает асинхронную сессию базы данных с использованием `async_session_maker`.
   - Сессия устанавливается в словарь `data`, который передается между middleware и обработчиками.
   - Вызывается обработчик `handler` с передачей ему события `event` и данных `data`.
   - После выполнения обработчика вызывается метод `after_handler` для выполнения дополнительных действий (например, commit).
   - В случае возникновения исключения выполняется откат транзакции (`session.rollback()`).
   - В блоке `finally` сессия закрывается (`session.close()`).
   - Методы `set_session` и `after_handler` предназначены для переопределения в подклассах.

2. **Реализация `DatabaseMiddlewareWithoutCommit`**:
   - Этот класс устанавливает сессию базы данных в словарь `data` под ключом `'session_without_commit'`.
   - Не выполняет commit транзакции после выполнения обработчика.

3. **Реализация `DatabaseMiddlewareWithCommit`**:
   - Этот класс устанавливает сессию базы данных в словарь `data` под ключом `'session_with_commit'`.
   - После выполнения обработчика выполняет commit транзакции, вызывая `await session.commit()`.

Пример использования
-------------------------

```python
from aiogram import Dispatcher, types
from aiogram import F
from aiogram.filters import CommandStart

# Предположим, что async_session_maker уже определен и настроен

# Подключение middleware к Dispatcher
async def setup_database_middleware(dp: Dispatcher):
    # dp.message.middleware(DatabaseMiddlewareWithoutCommit()) # можно использовать так
    dp.message.outer_middleware(DatabaseMiddlewareWithCommit()) # а лучше вот так - это как пример
    dp.callback_query.outer_middleware(DatabaseMiddlewareWithCommit())

# Пример обработчика, использующего сессию базы данных
async def start_command(message: types.Message, session_with_commit):
    """
    Обработчик команды /start.
    """
    # Используем сессию для выполнения операций с базой данных
    # Например, добавление нового пользователя
    async with session_with_commit as session:
        pass
        # new_user = User(user_id=message.from_user.id, username=message.from_user.username)
        # session.add(new_user)
        # await session.commit()
    await message.answer("Привет! Я бот.")


async def test_query(query: types.CallbackQuery, session_with_commit):
    """
    Обработчик callback query.
    """
    await query.answer(
        text="Успешно!",
        show_alert=True
    )

async def main():
    # dp = Dispatcher(bot)
    # await setup_database_middleware(dp)
    # dp.message.register_message_handler(start_command, CommandStart())
    # try:
    #     await dp.start_polling()
    # finally:
    #     await bot.session.close()
    pass

# Запуск бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())