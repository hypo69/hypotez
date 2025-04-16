# Модуль `utils.py`

## Обзор

Модуль содержит утилиты для обработки сообщений в Telegram боте, в частности, функцию `process_dell_text_msg`, предназначенную для удаления текстовых сообщений. Модуль использует библиотеку `aiogram` для работы с Telegram API, `loguru` для логирования и конфигурацию бота из модуля `bot.config`.

## Подробней

Модуль предназначен для организации процессов удаления сообщений в Telegram боте. Он содержит асинхронную функцию `process_dell_text_msg`, которая удаляет последнее сообщение пользователя, если оно существует, а также удаляет текущее сообщение пользователя. В случае возникновения ошибок, функция логирует их с помощью `logger`.

## Функции

### `process_dell_text_msg`

```python
async def process_dell_text_msg(message: Message, state: FSMContext):
    """Обрабатывает текстовое сообщение для удаления последнего сообщения пользователя и текущего сообщения.
    
    Args:
        message (Message): Объект сообщения Telegram.
        state (FSMContext): Объект контекста конечного автомата aiogram.
    
    Raises:
        Exception: Если происходит ошибка при удалении сообщения.

    Example:
        >>> from aiogram import types
        >>> from aiogram.fsm.context import FSMContext
        >>> async def test():
        ...     message = types.Message(message_id=123, from_user=types.User(id=456))
        ...     state = FSMContext(bot=None, chat_id=456, user_id=456)
        ...     await process_dell_text_msg(message, state)
    """
```

**Назначение**: Обработка текстового сообщения для удаления последнего сообщения пользователя и текущего сообщения.

**Параметры**:
- `message` (Message): Объект сообщения Telegram.
- `state` (FSMContext): Объект контекста конечного автомата aiogram.

**Возвращает**:
- Ничего. Функция ничего не возвращает.

**Вызывает исключения**:
- `Exception`: Если происходит ошибка при удалении сообщения.

**Как работает функция**:

1. Функция получает данные из состояния `state` с помощью `await state.get_data()`.
2. Извлечение идентификатора последнего сообщения (`last_msg_id`) из полученных данных.
3. Проверяет, существует ли `last_msg_id`.
4. Если `last_msg_id` существует, пытается удалить сообщение с использованием `bot.delete_message`, передавая `chat_id` и `message_id`.
5. В случае неудачи удаления сообщения, логирует предупреждение с помощью `logger.warning`.
6. Пытается удалить текущее сообщение пользователя с помощью `message.delete()`.
7. Если при удалении сообщения возникает исключение, логирует ошибку с использованием `logger.error`.

**Примеры**:

```python
from aiogram import types
from aiogram.fsm.context import FSMContext

async def test():
    message = types.Message(message_id=123, from_user=types.User(id=456))
    state = FSMContext(bot=None, chat_id=456, user_id=456)
    await process_dell_text_msg(message, state)