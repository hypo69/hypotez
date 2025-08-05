# Модуль `utils.py` для Telegram-бота Digital Market

## Обзор

Этот модуль содержит вспомогательные функции для обработки текстовых сообщений в Telegram-боте Digital Market. 
Он предоставляет функции для удаления предыдущих сообщений и обработки ошибок при удалении. 

## Функции

### `process_dell_text_msg(message: Message, state: FSMContext)`

**Назначение**: 
Функция удаляет предыдущее сообщение и текущее сообщение в Telegram-чате.

**Параметры**:

- `message` (Message): Текущее сообщение от пользователя.
- `state` (FSMContext): Контекст состояния бота.

**Возвращает**: 
- `None`

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при удалении сообщений.

**Как работает**:
- Функция извлекает идентификатор последнего сообщения (`last_msg_id`) из контекста состояния (`state`).
- Если `last_msg_id` существует, функция пытается удалить предыдущее сообщение с помощью метода `bot.delete_message()`. 
- Если `last_msg_id` не найден, выводится предупреждающее сообщение в лог.
- Затем функция удаляет текущее сообщение (`message`) с помощью метода `message.delete()`. 
- При возникновении ошибок во время удаления сообщений, функция записывает сообщение об ошибке в лог с использованием `logger.error()`.

**Пример**:

```python
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import bot

async def process_dell_text_msg(message: Message, state: FSMContext):
    # Извлечение данных из контекста состояния
    data = await state.get_data()
    last_msg_id = data.get('last_msg_id')

    try:
        # Удаление предыдущего сообщения, если его ID известен
        if last_msg_id:
            await bot.delete_message(chat_id=message.from_user.id, message_id=last_msg_id)
        else:
            logger.warning("Ошибка: Не удалось найти идентификатор последнего сообщения для удаления.")
        # Удаление текущего сообщения
        await message.delete()

    except Exception as ex:
        # Запись сообщения об ошибке в лог
        logger.error(f"Произошла ошибка при удалении сообщения: {str(ex)}")